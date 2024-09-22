import requests
import json
import datetime
import argparse
from dateutil.parser import parse

def get_auth_token(api_url, username, password):
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

def get_repositories(api_url, auth_token, last_scanned_before):
    headers = {
        "accept": "application/json; charset=UTF-8",
        "content-type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }

    payload = {
        "query": "config from source where source.lastScannedDate < '{}'".format(last_scanned_before.isoformat()),
        "limit": 1000  # Adjust this value based on your needs
    }

    try:
        response = requests.post(f"{api_url}/code/api/v1/repositories/search", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print("Error 403: Forbidden. Please check your API key and permissions.")
        else:
            print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    return None

import os

def main():
    parser = argparse.ArgumentParser(description="List repositories in Prisma Cloud tenant last scanned before a given date.")
    parser.add_argument("--days", type=int, default=30, help="Number of days to look back for last scan date (default: 30)")
    
    args = parser.parse_args()

    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    last_scanned_before = datetime.datetime.now() - datetime.timedelta(days=args.days)
    repositories = get_repositories(api_url, auth_token, last_scanned_before)
    
    if repositories:
        print(f"Repositories last scanned before {last_scanned_before.date()}:")
        for repo in repositories:
            last_scanned_date = parse(repo['lastScannedDate'])
            print(f"- {repo['repository']} (Last scanned: {last_scanned_date.date()})")
        print(f"\nTotal repositories found: {len(repositories)}")
    else:
        print("No repositories found or an error occurred.")

if __name__ == "__main__":
    main()
