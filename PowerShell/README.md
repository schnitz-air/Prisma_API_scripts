# Prisma Cloud Repository Onboarding Script

## Overview
This PowerShell script automates the process of onboarding repositories to Prisma Cloud. It supports both Azure Repos and GitHub repositories, allowing users to easily add multiple repositories for monitoring and security scanning.

## Prerequisites
- PowerShell 5.1 or later
- Prisma Cloud API access (Access Key and Secret Key)
- Azure Repos or GitHub integration set up in Prisma Cloud
- A text file containing the list of repositories to onboard (see "repolist.txt" as a template)

## Environment Variables
Set the following environment variables before running the script:
- PRISMA_ACCESS_KEY: Your Prisma Cloud Access Key
- PRISMA_SECRET_KEY: Your Prisma Cloud Secret Key
- PRISMA_API_URL: The Prisma Cloud API URL (e.g., https://api4.prismacloud.io)

## Setup
1. Ensure PowerShell 5.1 or later is installed on your system.
2. Set the required environment variables as mentioned above.
3. Edit the file `repolist.txt` in the same directory as the script, containing the repositories to onboard (one per line).

## Usage
1. Open a PowerShell terminal.
2. Navigate to the directory containing the script.
3. Run the script
4. Follow the on-screen prompts to:
- Enter the target role name (The desired role to onboard the repositories to)
- Select the repository type (Azure Repos or GitHub)
- Confirm the list of repositories to onboard

## Script Workflow
1. The script prompts for the target role name.
2. User selects the repository type (Azure Repos or GitHub).
3. The script reads the repository list to be onboarded from `repolist.txt`.
4. It validates the repository format based on the selected type.
5. The script retrieves the appropriate integration ID from Prisma Cloud.
6. Repositories are added to Prisma Cloud for monitoring.

## Repository Format
- For Azure Repos: `Organization/Project/Repository`
- For GitHub: `Owner/Repository`

## Logging
The script logs its actions to `PrismaCloudScript.log` in the same directory.

## Troubleshooting
- Ensure all prerequisites are met and environment variables are set before running the script.
- Check the log file for detailed error messages if the script fails.
- Verify that the repository list file is correctly formatted and accessible.

