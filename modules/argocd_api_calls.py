import requests
import json
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ARGOCD_API_URL = os.getenv('ARGOCD_URL')
ARGOCD_API_KEY = os.getenv("ARGOCD_API_KEY", None)

session = requests.Session()

if ARGOCD_API_KEY:
    session.headers.update({"Authorization": f"Bearer {ARGOCD_API_KEY}"})


def get_argocd_applications():
    response = session.get(f"{ARGOCD_API_URL}/api/v1/applications")
    applications = response.json()["items"]
    return {
        app['metadata']['name']: {
            'sync_status': app['status']['sync']['status'],
            'health_status': app['status']['health']['status'],
            'sync_errors': app['status']['sync'].get('errorMessage', 'No sync errors'),
            'description': app['spec'].get('description', 'No description provided'),
            'project': app['spec']['project'],
            'source_repo': app['spec']['source']['repoURL'],
            'source_type': app['spec']['source']['chart'] if 'chart' in app['spec']['source'] else 'Git',
            'destination_server': app['spec']['destination']['server'],
            'destination_namespace': app['spec']['destination']['namespace']
        } for app in applications
    }


api_functions = {
    "get_argocd_applications": get_argocd_applications
}
