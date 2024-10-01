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
    return response.json().get('token')
