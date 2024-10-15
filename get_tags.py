import requests
import os
import argparse
import json
from get_prisma_token import get_auth_token

def get_tags(api_url, auth_token, tag_type=None, repo_id=None, file_path=None):
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }
    
    params = {}
    if tag_type:
        params['type'] = tag_type
    if repo_id:
        params['repoId'] = repo_id
    if file_path:
        params['filePath'] = file_path

    response = requests.get(f"{api_url}/code/api/v1/tag-rules", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def print_tag_rule(rule):
    print(f"\nTag Rule ID: {rule['id']}")
    print(f"Name: {rule['name']}")
    print(f"Description: {rule['description']}")
    print(f"Created By: {rule['createdBy']}")
    print(f"Creation Date: {rule['creationDate']}")
    print(f"Is Enabled: {rule['isEnabled']}")
    print(f"Tag Rule OOTB ID: {rule['tagRuleOOTBId']}")
    print("Repositories:")
    for repo in rule['repositories']:
        print(f"  - {repo['name']} (Source: {repo['source']}, Owner: {repo['owner']}, Default Branch: {repo['defaultBranch']})")
    print(f"Can Do Actions: {rule['canDoActions']}")
    
    if rule['definition']:
        print("Definition:")
        print(json.dumps(rule['definition'], indent=2))

def main():
    parser = argparse.ArgumentParser(description="Get tag rules from Prisma Cloud")
    parser.add_argument("--type", help="Filter by tag type")
    parser.add_argument("--repo-id", help="Filter by repository ID")
    parser.add_argument("--file-path", help="Filter by file path")
    args = parser.parse_args()

    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    tag_rules = get_tags(api_url, auth_token, args.type, args.repo_id, args.file_path)
    
    if tag_rules:
        print("Tag Rules:")
        for rule in tag_rules:
            print_tag_rule(rule)
    else:
        print("No tag rules found or an error occurred.")

if __name__ == "__main__":
    main()