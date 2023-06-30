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
    data = response.json()
    applications = data["items"]
    return applications


def get_argocd_app_names():
    applications = get_argocd_applications()
    return [app['metadata']['name'] for app in applications]


def count_argocd_apps():
    applications = get_argocd_app_names()
    return len(applications)


def get_status_apps(status):
    applications = get_argocd_applications()
    return [app['metadata']['name'] for app in applications if app['status']['sync']['status'] == status]


def count_status_apps(status):
    return len(get_status_apps(status))


def get_sync_errors():
    applications = get_argocd_applications()
    return [app['status']['sync'].get('errorMessage', 'No sync errors') for app in applications if
            app['status']['sync']['status'] == 'OutOfSync']


def get_destination_server(app_name):
    applications = get_argocd_applications()
    for app in applications:
        if app['metadata']['name'] == app_name:
            return app['spec']['destination'].get('server', 'No server provided')
    return "Application not found"


argocd_functions = {
    "get_argocd_app_names": get_argocd_app_names,
    "count_argocd_apps": count_argocd_apps,
    "get_status_apps": get_status_apps,
    "count_status_apps": count_status_apps,
    "get_sync_errors": get_sync_errors,
    "get_destination_server": get_destination_server,
}

argocd_function_definitions = [
    {
        "name": "get_argocd_app_names",
        "description": "Retrieves names of all ArgoCD applications.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
    },
    {
        "name": "count_argocd_apps",
        "description": "Counts the total number of ArgoCD applications.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
    },
    {
        "name": "get_status_apps",
        "description": "Retrieves applications with a specific synchronization status.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "The synchronization status to filter applications by. Should be one of 'Synced', "
                                   "'OutOfSync', or 'Unknown'."
                }
            },
            "required": ["status"]
        },
    },
    {
        "name": "count_status_apps",
        "description": "Counts the number of applications with a specific synchronization status.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "The synchronization status to count applications by. Should be one of 'Synced', "
                                   "'OutOfSync', or 'Unknown'."
                }
            },
            "required": ["status"]
        },
    },
    {
        "name": "get_sync_errors",
        "description": "Retrieves synchronization error messages for applications that are out of sync.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        },
    },
    {
        "name": "get_destination_server",
        "description": "Retrieves the destination server of a specific application.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application."
                }
            },
            "required": ["app_name"]
        },
    }
]

