# get_tags.py

This script retrieves and displays tag rules from a Prisma Cloud tenant.

## Features

- Fetches tag rules using the Prisma Cloud API
- Supports filtering by tag type, repository ID, and file path
- Displays detailed information about each tag rule, including:
  - Tag Rule ID
  - Name
  - Description
  - Created By
  - Creation Date
  - Enabled status
  - Tag Rule OOTB ID
  - Associated repositories
  - Can Do Actions status
  - Rule definition (if available)

## Usage

Ensure you have set the required environment variables:
- PRISMA_API_URL
- PRISMA_ACCESS_KEY
- PRISMA_SECRET_KEY

Then run the script using Python with optional arguments:


python get_tags.py [--type TAG_TYPE] [--repo-id REPO_ID] [--file-path FILE_PATH]


## Command-line Arguments

- `--type TAG_TYPE`: Filter tag rules by type (e.g., "custom", "builtin")
- `--repo-id REPO_ID`: Filter tag rules by repository ID
- `--file-path FILE_PATH`: Filter tag rules by file path

## Expected Output

The script will display detailed information about each tag rule that matches the specified filters. If no filters are provided, all tag rules will be displayed.

## Dependencies

- Python 3.x
- `requests` library (install using `pip install requests`)
- `dotenv` library (install using `pip install python-dotenv`)

Make sure to install the required dependencies before running the script.
