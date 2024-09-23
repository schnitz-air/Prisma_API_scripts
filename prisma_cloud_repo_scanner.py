import requests
import json
import datetime
import argparse
import logging
import os 
from dateutil.parser import parse
from get_prisma_token import get_auth_token

def get_repositories(api_url, auth_token, last_scanned_before):
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }

    payload = {
        "data":{}
    }

    try:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(f"Request URL: {api_url}/code/api/v1/repositories")
        logging.debug(f"Request Headers: {headers}")
        logging.debug(f"Request Payload: {payload}")
        response = requests.get(f"{api_url}/code/api/v1/repositories", headers=headers)
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

def main():
    parser = argparse.ArgumentParser(description="List repositories in Prisma Cloud tenant last scanned before a given date.")
    parser.add_argument("--days", type=int, required=True, help="Number of days to look back for last scan date")
    
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
        filtered_repos = [repo for repo in repositories if repo['lastScanDate'] and parse(repo['lastScanDate']).date() < last_scanned_before.date() and repo['source'] != 'cli']
        for repo in filtered_repos:
            last_scanned_date = parse(repo['lastScanDate'])
            print(f"- {repo['repository']} (Last scanned: {last_scanned_date.date()} source: {repo['source']})")
        print(f"\nTotal repositories found: {len(filtered_repos)}")
    else:
        print("No repositories found or an error occurred.")

if __name__ == "__main__":
    main()
