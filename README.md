# Prisma_API_scripts
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

## prisma_cloud_repo_scanner.py 
### This script gets the list of all repositories connected on a Prisma Cloud tenant and returns a list of repositories which were last scanned more than x days ago (x is a variable) 
- Run the following using Python:\
    `python prisma_cloud_repo_scanner.py --days 10`

In the above example, the script will return a list of all the repositories that haven't been scanned for the last 10 days or more. \
You can modify the number of days you'd like the script to scan for 

## prisma_cloud_pipeline_tools.py 
### This script gets the list of all pipeline-tools on a Prisma Cloud tenant and stores it in a status file. 
### It then compares that with the last scan and returns a list of changes (additions/deletions/modifications) that occurred.  
- Run the following using Python:\
      `python prisma_cloud_pipeline_tools.py`

In the above example, the script will return the list of changes (additions/deletions/modifications) that it detected between the current state of pipeline-tools and between the last state which is saved in the `prisma_pipeline_state.json` file.

## set_prisma_repo_branches.py
### This script manages the scanned branches of repositories in Prisma Cloud. It can set a new branch for scanning for all repositories or a specific repository.

Usage options:
1. Scan only mode:
   `python set_prisma_repo_branches.py --scan-only`

2. Set branch for all repositories:
   `python set_prisma_repo_branches.py --branch main`

3. Set branch in interactive mode:
   `python set_prisma_repo_branches.py --branch main --interactive`

4. Set branch for a specific repository:
   `python set_prisma_repo_branches.py --repository <repository_name> --branch <branch_name>`

The script will create a timestamped JSON file with the current branch information for all repositories before making any changes. It requires the PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY environment variables to be set for authentication.

## Additional Resources

For more detailed information on specific actions, please refer to the following resources:

- **Creating an Access Key and Secret Key**: Learn how to generate and manage your credentials by following the official Prisma Cloud documentation: [Create Access Keys](https://docs.prismacloud.io/en/enterprise-edition/content-collections/administration/create-access-keys)

- **Setting up a Python Environment**: To create and manage a Python virtual environment, refer to the official Python documentation: [Creating Virtual Environments](https://docs.python.org/3/library/venv.html)

These resources will provide you with step-by-step instructions to help you get started quickly and efficiently.
