import requests
import os
from utils.get_prisma_token import get_auth_token

def get_suppression_rules(api_url, auth_token):
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }
    
    response = requests.get(f"{api_url}/code/api/v1/suppressions", headers=headers)
    response.raise_for_status()
    return response.json()

def print_suppression_rule(rule):
    print(f"\nSuppression Type: {rule['suppressionType']}")
    print(f"ID: {rule['id']}")
    print(f"Policy ID: {rule['policyId']}")
    print(f"Creation Date: {rule['creationDate']}")
    print(f"Comment: {rule['comment']}")
    
    if 'expirationDate' in rule:
        print(f"Expiration Date: {rule['expirationDate']}")
    
    if rule['suppressionType'] == 'Cves' and 'cves' in rule:
        print("CVEs:")
        for cve in rule['cves']:
            print(f"  - UUID: {cve['uuid']}")
            print(f"    ID: {cve['id']}")
            print(f"    CVE: {cve['cve']}")
    
    if rule['suppressionType'] == 'Resources' and 'resources' in rule:
        print("Resources:")
        for resource in rule['resources']:
            print(f"  - Account ID: {resource['accountId']}")
            print(f"    Resource ID: {resource['resourceId']}")

def main():
    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    suppression_rules = get_suppression_rules(api_url, auth_token)
    
    if suppression_rules:
        print("Suppression Rules:")
        for rule in suppression_rules:
            print_suppression_rule(rule)
    else:
        print("No suppression rules found or an error occurred.")

if __name__ == "__main__":
    main()
