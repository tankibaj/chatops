import json
import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ARGOCD_URL = os.getenv('ARGOCD_URL')
ARGOCD_API_KEY = os.getenv("ARGOCD_API_KEY", None)

if ARGOCD_API_KEY is None:
    raise ValueError("ARGOCD_API_KEY is not defined")

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {ARGOCD_API_KEY}"
}


def get_argocd_applications():
    response = requests.get(f"{ARGOCD_URL}/api/v1/applications", headers=headers)
    # return response.json()
    data = response.json()
    applications = data["items"]
    results = []

    for app in applications:
        app_info = {
            'name': app['metadata']['name'],
            'sync_status': app['status']['sync']['status'],
            'health_status': app['status']['health']['status'],
            'sync_errors': app['status']['sync'].get('errorMessage', 'No sync errors'),
            # -- To prevent hit OpenAI token limit only passing the above fields.
            # 'project': app['spec']['project'],
            # 'source_repo': app['spec']['source']['repoURL'],
            # 'source_type': app['spec']['source'].get('chart', 'Git'),
            'destination_server': app['spec']['destination'].get('server', 'No server provided'),
            # 'destination_namespace': app['spec']['destination']['namespace']
        }
        results.append(app_info)

    return json.dumps(results)


argocd_functions = {
    "get_argocd_applications": get_argocd_applications,
}

argocd_function_definitions = [
    {
        "name": "get_argocd_applications",
        "description": "Get information about ArgoCD applications",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]
