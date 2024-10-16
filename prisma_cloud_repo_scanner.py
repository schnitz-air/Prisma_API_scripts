import datetime
import argparse
import os 
from dateutil.parser import parse
from get_prisma_token import get_auth_token
from get_repo_scanned import get_repo_scanned

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
    repositories = get_repo_scanned(api_url, auth_token)
    
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