import requests
import os
from get_prisma_token import get_auth_token

def delete_suppression_rule(api_url, auth_token, policy_id, suppression_id):
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }
    
    url = f"{api_url}/bridgecrew/api/v1/suppressions/{policy_id}/justifications/{suppression_id}"
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code

def main():
    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    policy_id = input("Enter the Policy ID: ")
    suppression_id = input("Enter the Suppression ID: ")
    
    try:
        status_code = delete_suppression_rule(api_url, auth_token, policy_id, suppression_id)
        print(f"\nSuppression rule deleted successfully. Status code: {status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while deleting the suppression rule: {e}")

if __name__ == "__main__":
    main()
