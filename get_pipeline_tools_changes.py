import json
import datetime
import argparse
import os 
from dateutil.parser import parse
from get_prisma_token import get_auth_token
from get_pipeline_tools import get_pipeline_tools
from get_repo import get_repo_scanned
import sqlite3
import time

DATABASE_FILE = 'prisma_pipeline_states.db'

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS states
                 (timestamp INTEGER PRIMARY KEY, state TEXT)''')
    conn.commit()
    conn.close()

def save_state(state):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO states VALUES (?, ?)", (int(time.time()), json.dumps(state)))
    conn.commit()
    conn.close()

def load_states(days=7):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    timestamp = int(time.time()) - (days * 86400)
    c.execute("SELECT * FROM states WHERE timestamp >= ? ORDER BY timestamp DESC", (timestamp,))
    states = {row[0]: json.loads(row[1]) for row in c.fetchall()}
    conn.close()
    return states

def cleanup_old_states(days=30):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    timestamp = int(time.time()) - (days * 86400)
    c.execute("DELETE FROM states WHERE timestamp < ?", (timestamp,))
    conn.commit()
    conn.close()

def compare_states(previous_state, current_state):
    added = [item for item in current_state if item not in previous_state]
    removed = [item for item in previous_state if item not in current_state]
    modified = [item for item in current_state if item in previous_state and current_state[item] != previous_state[item]]
    return added, removed, modified

def match_repos_with_apps(repositories, pipelines):
    repo_app_map = {repo['id']: {'name': repo['name'], 'apps': []} for repo in repositories}
    for pipeline in pipelines:
        cas_id = pipeline.get('casId')
        if cas_id in repo_app_map:
            repo_app_map[cas_id]['apps'].append(pipeline['appName'])
    return repo_app_map

def main():
    init_db()
    print(f"Database initialized at: {os.path.abspath(DATABASE_FILE)}")
    parser = argparse.ArgumentParser(description="List pipeline_tools in Prisma Cloud tenant last scanned before a given date.")
    parser.add_argument("--show", action="store_true", help="Show all repositories and their associated appNames")
    args = parser.parse_args()

    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    pipelines = get_pipeline_tools(api_url, auth_token)

    if args.show:
        repositories = get_repo_scanned(api_url, auth_token)
        repo_app_map = match_repos_with_apps(repositories, pipelines)
        
        print("Repositories and their associated appNames:")
        for repo_id, repo_data in repo_app_map.items():
            print(f"\nRepository: {repo_data['name']} (ID: {repo_id})")
            if repo_data['apps']:
                for app in repo_data['apps']:
                    print(f"  - {app}")
            else:
                print("  No associated appNames found")
    else:
        if pipelines:
            for pipeline in pipelines:
                print(pipeline)
        else:
            print("No pipeline CI files were found or an error occurred.")
        
        current_state = {pipeline['appName']: pipeline for pipeline in pipelines}
        save_state(current_state)

        previous_states = load_states()

        for timestamp, state in previous_states.items():
            print(f"\nChanges since {datetime.datetime.fromtimestamp(timestamp)}:")
            added, removed, modified = compare_states(state, current_state)

            print("Added pipelines:")
            for pipeline in added:
                print(f"  - {pipeline}")

            print("\nRemoved pipelines:")
            for pipeline in removed:
                print(f"  - {pipeline}")

            print("\nModified pipelines:")
            for pipeline in modified:
                print(f"  - {pipeline}")

        cleanup_old_states()

if __name__ == "__main__":
    main()