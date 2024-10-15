import requests
import json

def get_auth_token(api_url, username, password):
    """
    Retrieves an authentication token from the Prisma Cloud API.

    Args:
    api_url (str): The base URL of the Prisma Cloud API.
    username (str): The username for authentication.
    password (str): The password for authentication.

    Returns:
    str: The authentication token if successful.

    Raises:
    requests.exceptions.HTTPError: If the API request fails.
    """
    login_url = f"{api_url}/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(login_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    token = response.json().get('token')
    print(f"Received JWT Token: {token}")
    return token

if __name__ == "__main__":
    import os
    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')
    if all([api_url, username, password]):
        get_auth_token(api_url, username, password)
    else:
        print("Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY environment variables.")
