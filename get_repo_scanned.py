import requests

def get_repo_scanned(api_url, auth_token):
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(f"{api_url}/code/api/v1/repositories", headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    from get_prisma_token import get_auth_token
    import os
    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')
    auth_token = get_auth_token(api_url, username, password)
    repositories = get_repo_scanned(api_url, auth_token)
    print(repositories)
