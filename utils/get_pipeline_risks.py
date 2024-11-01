import requests
import os
from get_prisma_token import get_auth_token

def get_pipeline_risks(api_url, auth_token):
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {auth_token}"
    }
    
    response = requests.post(f"{api_url}/code/api/v1/pipeline-risks", headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    api_url = os.environ.get('PRISMA_API_URL')
    username = os.environ.get('PRISMA_ACCESS_KEY')
    password = os.environ.get('PRISMA_SECRET_KEY')

    if not all([api_url, username, password]):
        raise ValueError("One or more required environment variables are not set. Please set PRISMA_API_URL, PRISMA_ACCESS_KEY, and PRISMA_SECRET_KEY.")

    auth_token = get_auth_token(api_url, username, password)
    
    pipeline_risks = get_pipeline_risks(api_url, auth_token)
    
    if pipeline_risks and 'data' in pipeline_risks:
        print("Pipeline Risks:")
        for risk in pipeline_risks['data']:
            print(f"\nPolicy ID: {risk['policyId']}")
            print(f"Name: {risk['name']}")
            print(f"Severity: {risk['severity']}")
            print(f"System: {risk['system']}")
            print(f"Category: {risk['category']}")
            print(f"Level: {risk['level']}")
            print(f"Total Alerts: {risk['totalAlerts']}")
            print(f"Open Alerts: {risk['openAlerts']}")
            print(f"Fixed Alerts: {risk['fixedAlerts']}")
            print(f"Suppressed Alerts: {risk['suppressedAlerts']}")
            print(f"Last Alert On: {risk['lastAlertOn']}")
            print(f"Repository ID: {risk['repoId']}")
    else:
        print("No pipeline risks found or an error occurred.")

if __name__ == "__main__":
    main()
