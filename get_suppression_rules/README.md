# get_suppression_rules.py

This script retrieves and displays suppression rules from a Prisma Cloud tenant.

## Features

- Fetches suppression rules using the Prisma Cloud API
- Displays detailed information about each suppression rule, including:
  - Suppression Type
  - ID
  - Policy ID
  - Creation Date
  - Comment
  - Expiration Date (if applicable)
  - CVEs (for Cves suppression type)
  - Resources (for Resources suppression type)

## Usage

Ensure you have set the required environment variables:
- PRISMA_API_URL
- PRISMA_ACCESS_KEY
- PRISMA_SECRET_KEY

Then run the script using Python:

```bash
python get_suppression_rules.py
