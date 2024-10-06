# Prisma_API_scripts
A collection of python scripts that uses Prisma Cloud API to perform useful actions

## Prerequisites 
Before starting to use the collection, make sure you have a valid Prisma Cloud tenant and make sure to create an Access key and Secret key 

Set the following as your environment variables 
1. PRISMA_API_URL
2. PRISMA_ACCESS_KEY
3. PRISMA_SECRET_KEY
   


### how to use 
- clone the repo locally \
&nbsp;&nbsp;&nbsp;&nbsp;`git clone https://github.com/schnitz-air/repositories_last_scanned.git`
- cd into the created directory \
&nbsp;&nbsp;&nbsp;&nbsp;`cd repositories_last_scanned\`
- choose the script you want to execute from the list below and follow specific instructions

## prisma_cloud_repo_scanner.py 
### This script gets the list of all repositories connected on a Prisma Cloud tenant and returns a list of repositories which were last scanned more than x days ago (x is a variable) 
- run the following using python (was tested using python version 3.12.3)\
&nbsp;&nbsp;&nbsp;&nbsp;`python prisma_cloud_repo_scanner.py --days 10`

In the above example, the script will return a list of all the repositories that haven't been scanned for the last 10 days or more. \
You can modify the number of days you'd like the script to scan for 

## prisma_cloud_pipeline_tools.py 
### This script gets the list of all pipeline-tools on a Prisma Cloud tenant and stores it in a status file. 
### it then compares that with the last scan and returns a list of changes (additions/deletions/modifications) that occured.  
- run the following using python (was tested using python version 3.12.3)\
  &nbsp;&nbsp;&nbsp;&nbsp;`python prisma_cloud_pipeline_tools.py`

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

