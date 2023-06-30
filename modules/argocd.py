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


def count_argocd_apps():
    applications = get_argocd_applications()
    return len(applications)


def get_argocd_app_names():
    applications = get_argocd_applications()
    return [app['metadata']['name'] for app in applications]


def get_status_apps(status):
    applications = get_argocd_applications()
    return [app for app in applications if app['status']['sync']['status'] == status]


def count_status_apps(status):
    return len(get_status_apps(status))


def get_status_app_names(status):
    apps = get_status_apps(status)
    return [app['metadata']['name'] for app in apps]


def get_sync_errors():
    applications = get_argocd_applications()
    return [app['status']['sync'].get('errorMessage', 'No sync errors') for app in applications if
            app['status']['sync']['status'] == 'OutOfSync']


def get_destination_server():
    applications = get_argocd_applications()
    return [app['spec']['destination'].get('server', 'No server provided') for app in applications]


argocd_functions = {
    "get_argocd_applications": get_argocd_applications,
    "count_argocd_apps": count_argocd_apps,
    "get_argocd_app_names": get_argocd_app_names,
    "get_status_apps": get_status_apps,
    "count_status_apps": count_status_apps,
    "get_status_app_names": get_status_app_names,
    "get_sync_errors": get_sync_errors,
    "get_destination_server": get_destination_server,
}

argocd_function_definitions = [
    {
        "name": "get_argocd_applications",
        "description": "Fetches all ArgoCD applications from the ArgoCD server.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "count_argocd_apps",
        "description": "Counts the total number of ArgoCD applications.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_argocd_app_names",
        "description": "Retrieves a list of all ArgoCD application names.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_status_apps",
        "description": "Retrieves applications with a specific sync status.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "The sync status to filter applications by. Should be one of 'Synced', "
                                   "'OutOfSync', or 'Unknown'."
                }
            },
            "required": ["status"]
        }
    },
    {
        "name": "count_status_apps",
        "description": "Counts the number of applications with a specific sync status.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "The sync status to count applications by. Should be one of 'Synced', 'OutOfSync', "
                                   "or 'Unknown'."
                }
            },
            "required": ["status"]
        }
    },
    {
        "name": "get_status_app_names",
        "description": "Retrieves a list of application names with a specific sync status.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "The sync status to filter application names by. Should be one of 'Synced', "
                                   "'OutOfSync', or 'Unknown'."
                }
            },
            "required": ["status"]
        }
    },
    {
        "name": "get_sync_errors",
        "description": "Retrieves sync error messages for applications that are out of sync.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_destination_server",
        "description": "Retrieves the destination server of each application.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

