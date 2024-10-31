"""
Prisma Cloud Repository Branch Manager

This script interacts with the Prisma Cloud API to manage and monitor the scanned branches
of repositories. It can perform the following operations:

1. Scan and save the current branch information for all repositories.
2. Set a new branch for scanning for all or selected repositories.
3. Operate in interactive mode, prompting for confirmation before changing each repository's branch.

The script requires environment variables for authentication:
- PRISMA_API_URL: The base URL for the Prisma Cloud API
- PRISMA_ACCESS_KEY: The access key for API authentication
- PRISMA_SECRET_KEY: The secret key for API authentication

Usage:
1. Scan only mode:
   python set_prisma_repo_branches.py --scan-only

2. Set branch for all repositories:
   python set_prisma_repo_branches.py --branch main

3. Set branch in interactive mode:
   python set_prisma_repo_branches.py --branch main --interactive

The script will create a timestamped JSON file with the current branch information
for all repositories before making any changes.
"""

import requests
import argparse
import os
import json
from datetime import datetime
from utils.get_prisma_token import get_auth_token
from utils.get_repo import get_repo_scanned

def set_repository_branch(api_url, auth_token, repo_id, branch):
    """
    Set the scanning branch for a specific repository.

    Args:
    api_url (str): The base URL for the Prisma Cloud API.
    auth_token (str): The authentication token for API requests.
    repo_id (str): The ID of the repository to update.
    branch (str): The name of the branch to set 

    Returns:
    bool: True if the branch was successfully set, False otherwise.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }

    try:
        response = requests.post(f"{api_url}/bridgecrew/api/v1/branches/{repo_id}/scannedBranch/{branch}", headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error setting branch for repository {repo_id}: {e}")
        return False

def save_repository_branches(repositories):
    """
    Save the repository information in the order: source, owner, defaultBranch.
    Include the total number of repositories listed.

    Args:
    repositories (list): A list of dictionaries containing repository information.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"repository_branches_{timestamp}.json"
    
    repo_info = {
        repo['repository']: {
            'source': repo.get('source', 'Unknown'),
            'owner': repo.get('owner', 'Unknown'),
            'defaultBranch': repo.get('defaultBranch', 'N/A')
        } for repo in repositories
    }
    
    output_data = {
        "total_repositories": len(repositories),
        "repositories": repo_info
    }
    
    with open(filename, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Repository information saved to {filename}")

def main():
    """
    Main function to parse arguments and execute the script's functionality.
    """
    parser = argparse.ArgumentParser(description="Set the scanned branch for repositories in Prisma Cloud.")
    parser.add_argument("--branch", type=str, help="Branch name to set for Prisma scanning")
    parser.add_argument("--interactive", action="store_true", help="Prompt for confirmation before changing each repository's branch")
    parser.add_argument("--scan-only", action="store_true", help="Only scan and save existing branches without making changes")
    parser.add_argument("--repository", type=str, help="Specific repository to update")
    
    args = parser.parse_args()

    if not args.scan_only and not args.branch:
        parser.error("--branch is required when not using --scan-only")

    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    repositories = get_repo_scanned(api_url, auth_token)
    
    if repositories:
        if args.repository:
            repositories = [repo for repo in repositories if repo['repository'] == args.repository]
            if not repositories:
                print(f"Repository '{args.repository}' not found.")
                return
        
        save_repository_branches(repositories)
        
        if args.scan_only:
            print("Scan completed. Repository branches have been saved.")
            return

        print(f"Setting branch '{args.branch}' for repositories:")
        for repo in repositories:
            repo_id = repo['id']
            repo_name = repo['repository']
            repo_source = repo.get('source', 'Unknown')
            repo_owner = repo.get('owner', 'Unknown')
            
            print(f"\nRepository: {repo_name}")
            print(f"ID: {repo_id}")
            print(f"Source: {repo_source}")
            print(f"Owner: {repo_owner}")
            
            if args.interactive:
                confirm = input(f"Change branch for this repository? (y/n): ").lower()
                if confirm != 'y':
                    print(f"Skipped")
                    continue
            
            if set_repository_branch(api_url, auth_token, repo_id, args.branch):
                print(f"Branch set successfully to '{args.branch}'")
            else:
                print(f"Failed to set branch")
        print(f"\nTotal repositories processed: {len(repositories)}")
    else:
        print("No repositories found or an error occurred.")

if __name__ == "__main__":
    main()