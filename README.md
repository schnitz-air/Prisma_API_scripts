# Prisma API scripts
A collection of Python scripts that uses Prisma Cloud API to perform useful actions

# Community Supported
The templates/scripts in this repo are released under an as-is, best effort, support policy. These scripts should be seen as community supported and not as an official Palo Alto Networks solution. 
All code in this repo is provided without support or warranty from Palo Alto Networks. Please review code used from this repo prior to use in your environment.

## Prerequisites 
Before starting to use this collection, make sure you have:
- A valid Prisma Cloud tenant
- Created an Access key and Secret key
- Python installed (tested with version 3.12.3)

Set the following as your environment variables:
1. PRISMA_API_URL
2. PRISMA_ACCESS_KEY
3. PRISMA_SECRET_KEY
   
Bash example \
`export PRISMA_API_URL="https://api.prismacloud.io"` \
`export PRISMA_ACCESS_KEY="your_access_key_here"` \
`export PRISMA_SECRET_KEY="your_secret_key_here"` 

Note: Additional details on creating access keys and setting up a Python environment can be found in the "Additional Resources" section below.

### How to use 
- Clone the repo locally \
    `git clone https://github.com/schnitz-air/repositories_last_scanned.git`
- cd into the created directory \
    `cd repositories_last_scanned\`
- Choose the script you want to execute from the list below and follow specific instructions

## Available Scripts

### 1. Set Scanned Branch (set_scanned_branch.py)
Sets the scanned branches of repositories in Prisma Cloud.
[Read more about set_scanned_branch.py](docs/set_scanned_branch.md)

### 2. Prisma Cloud Pipeline Tools (get_pipeline_tools_changes.py)
Monitors changes in pipeline tools on a Prisma Cloud tenant.
[Read more about get_pipeline_tools.py](docs/get_pipeline_tools.md)

### 3. Prisma Cloud Repository Scanner (set_scanned_branch.py)
Lists repositories that haven't been scanned in the past x days.
[Read more about get_repo_last_scanner.py](docs/get_repo_last_scanned.md)

### 4. Get Suppression Rules (/utils/get_suppression_rules.py)
Retrieves and displays suppression rules from Prisma Cloud.
[Read more about get_suppression_rules.py](docs/get_supression_rules.md)

### 5. Get Tags (utils/get_tags.py)
Retrieves and displays tag rules from Prisma Cloud.
[Read more about get_tags.py](docs/get_tags.md)
## Additional Resources

For more detailed information on specific actions, please refer to the following resources:

- **Creating an Access Key and Secret Key**: Learn how to generate and manage your credentials by following the official Prisma Cloud documentation: [Create Access Keys](https://docs.prismacloud.io/en/enterprise-edition/content-collections/administration/create-access-keys)

- **Setting up a Python Environment**: To create and manage a Python virtual environment, refer to the official Python documentation: [Creating Virtual Environments](https://docs.python.org/3/library/venv.html)

These resources will provide you with step-by-step instructions to help you get started quickly and efficiently.
