import requests
import os
from .get_prisma_token import get_auth_token

def get_enforcement_rules(api_url, auth_token):
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }
    
    response = requests.get(f"{api_url}/code/api/v1/policies/enforcement-rules", headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    enforcement_rules = get_enforcement_rules(api_url, auth_token)
    
    if enforcement_rules:
        print("Enforcement Rules:")
        for rule in enforcement_rules:
            print(f"\nRule ID: {rule['id']}")
            print(f"Name: {rule['name']}")
            print(f"Description: {rule['description']}")
            print(f"Enabled: {rule['enabled']}")
            print(f"Severity: {rule['severity']}")
            print(f"Type: {rule['type']}")
            if 'policies' in rule:
                print("Policies:")
                for policy in rule['policies']:
                    print(f"  - {policy}")
    else:
        print("No enforcement rules found or an error occurred.")

if __name__ == "__main__":
    main()
