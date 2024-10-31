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

### 1. Set Scanned Branch
Manages the scanned branches of repositories in Prisma Cloud.
[Read more about set_scanned_branch.py](docs/set_scanned_branch/README.md)
### 2. Get Pipeline Tools
Monitors changes in pipeline tools on a Prisma Cloud tenant.
[Read more about prisma_cloud_pipeline_tools.py](docs/get_pipeline_tools/README.md)

### 3. Prisma Cloud Repository Scanner
Lists repositories that haven't been scanned recently.
[Read more about prisma_cloud_repo_scanner.py](docs/get_repo_last_scanned/README.md)

### 4. Get Suppression Rules
Retrieves and displays suppression rules from Prisma Cloud.
[Read more about get_suppression_rules.py](docs/get_suppression_rules/README.md)

## Additional Resources

For more detailed information on specific actions, please refer to the following resources:

- **Creating an Access Key and Secret Key**: Learn how to generate and manage your credentials by following the official Prisma Cloud documentation: [Create Access Keys](https://docs.prismacloud.io/en/enterprise-edition/content-collections/administration/create-access-keys)

- **Setting up a Python Environment**: To create and manage a Python virtual environment, refer to the official Python documentation: [Creating Virtual Environments](https://docs.python.org/3/library/venv.html)

These resources will provide you with step-by-step instructions to help you get started quickly and efficiently.
