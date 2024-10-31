import requests
import logging
import os

def get_pipeline_tools(api_url, auth_token):
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }

    payload = {
        "data":{}
    }

    try:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(f"Request URL: {api_url}/code/api/v1/ci-inventory")
        logging.debug(f"Request Headers: {headers}")
        logging.debug(f"Request Payload: {payload}")
        response = requests.get(f"{api_url}/code/api/v1/ci-inventory", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"Error 403: Forbidden. Please check your API key and permissions.")
            print(f"Response headers: {e.response.headers}")
            print(f"Response body: {e.response.text}")
        else:
            print(f"HTTP Error {e.response.status_code}: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    return None

if __name__ == "__main__":
    from utils.get_prisma_token import get_auth_token
    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')
    auth_token = get_auth_token(api_url, username, password)
    pipelines = get_pipeline_tools(api_url, auth_token)
    print(pipelines)
