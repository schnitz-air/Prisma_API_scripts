import requests
import os
import uuid
from datetime import datetime
from get_prisma_token import get_auth_token

import uuid

import time

import json

def create_suppression_rule(api_url, auth_token, account_id, resource_id, comment):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }
    
    payload = {
        "suppressionType": "Resources",
        "comment": comment,
        "origin": "AutomationScript",
        "expirationTime": "0",
        "resources": [
            {
                "accountId": account_id,
                "id": resource_id
            }
        ],
    }
    
    # Debug output
    print("\nDebug: POST Request Details")
    print(f"URL: {api_url}/bridgecrew/api/v1/suppressions/BC_GIT_2")
    print("Headers:")
    print(json.dumps(headers, indent=2))
    print("Payload:")
    print(json.dumps(payload, indent=2))
    
    policy_id = "BC_GIT_2"
    response = requests.post(f"{api_url}/bridgecrew/api/v1/suppressions/{policy_id}", headers=headers, json=payload)
    response.raise_for_status()
    return response.json(), policy_id
def main():
    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    account_id = input("Enter the Organization/Repo (Account ID): ")
    resource_id = input("Enter the file:resource name/id (Resource ID): ")
    comment = input("Enter a comment for the suppression: ")   
    
    try:
        new_suppression, policy_id = create_suppression_rule(api_url, auth_token, account_id, resource_id, comment)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while creating the suppression rule: {e}")

if __name__ == "__main__":
    main()