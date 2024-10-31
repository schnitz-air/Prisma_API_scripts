This file is part of a set of individual README files for each script. Here's the content for README_set_prisma_repo_branches.md:

# set_prisma_repo_branches.py

This script manages the scanned branches of repositories in Prisma Cloud. It can set a new branch for scanning for all repositories or a specific repository.

## Usage

1. Scan only mode:
   
   python set_prisma_repo_branches.py --scan-only
   

2. Set a new branch for all repositories:
   
   python set_prisma_repo_branches.py --new-branch <branch_name>
   

3. Set a new branch for a specific repository:
   
   python set_prisma_repo_branches.py --new-branch <branch_name> --repo <repo_name>
   

## Options

- `--scan-only`: Scan and display current branch information without making changes.
- `--new-branch <branch_name>`: Specify the new branch to set for scanning.
- `--repo <repo_name>`: Specify a particular repository to update (optional).

## Requirements

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - python-dotenv

## Configuration

Ensure you have a `.env` file in the same directory as the script with the following variables:


PRISMA_ACCESS_KEY=<your_access_key>
PRISMA_SECRET_KEY=<your_secret_key>
PRISMA_API_URL=<prisma_api_url>


Replace the placeholders with your actual Prisma Cloud credentials and API URL.

## Notes

- This script requires appropriate permissions in Prisma Cloud to view and modify repository settings.
- Always verify the changes after running the script to ensure the desired outcome.
