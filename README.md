# repositories_last_scanned
A python script that retrieves all repositories that their last scanned date is greater than x days 

As stated above, this script gets the list of all repositories connected on a Prisma Cloud tenant and returns a list of repositories which were last scanned more than x days ago (x is a variable) 

## Prerequisites 
Before starting, make sure you have a valid Prisma Cloud tenant and make sure to create an Access key and Secret key 

Set the following as your environment variables 
1. PRISMA_API_URL
2. PRISMA_ACCESS_KEY
3. PRISMA_SECRET_KEY

## how to use 
- clone the repo locally \
&nbsp;&nbsp;&nbsp;&nbsp;`git clone https://github.com/schnitz-air/repositories_last_scanned.git`
- cd into the created directory \
&nbsp;&nbsp;&nbsp;&nbsp;`cd repositories_last_scanned\`
- run the following using python (was tested using python version 3.12.3)\
&nbsp;&nbsp;&nbsp;&nbsp;`python prisma_cloud_repo_scanner.py --days 10`

In the above example, the script will return a list of all the repositories that haven't been scanned for the last 10 days or more. \
You can modify the number of days you'd like the script to scan for 
