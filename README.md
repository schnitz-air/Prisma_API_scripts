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
### This script allows you to set specific branches for scanning in Prisma Cloud for a given repository
This script interacts with the Prisma Cloud API to manage and monitor the scanned branches
of repositories. It can perform the following operations:

1. Scan and save the current branch information for all repositories.
2. Set a new branch for scanning for all or selected repositories.
3. Operate in interactive mode, prompting for confirmation before changing each repository's branch.
4. Operate in scan-only mode, which will only scan and display the current branch information without making any changes.

Usage:
1. Scan only mode:
   python set_prisma_repo_branches.py --scan-only

2. Set branch 'main' for all repositories:
   python set_prisma_repo_branches.py --branch main

3. Set branch 'main' in interactive mode:
   python set_prisma_repo_branches.py --branch main --interactive

The script will create a timestamped JSON file with the current branch information
for all repositories before making any changes.


