import json
import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

HARBOR_URL = os.getenv('HARBOR_URL')
HARBOR_API_KEY = os.getenv("HARBOR_API_KEY", None)

if HARBOR_API_KEY is None:
    raise ValueError("HARBOR_API_KEY is not defined")

headers = {
    "Accept": "application/json",
    "Authorization": f"Basic {HARBOR_API_KEY}"
}


def get_harbor_projects():
    response = requests.get(f"{HARBOR_URL}/api/v2.0/projects", headers=headers)
    return response.json()


def get_harbor_repositories(project_name):
    response = requests.get(f"{HARBOR_URL}/api/v2.0/projects/{project_name}/repositories", headers=headers)
    return response.json()


def get_harbor_artifacts(repository_name):
    response = requests.get(f"{HARBOR_URL}/api/v2.0/projects/{repository_name}/artifacts", headers=headers)
    return response.json()


def get_harbor_artifact_vulnerabilities(repository_name, reference):
    response = requests.get(
        f"{HARBOR_URL}/api/v2.0/projects/{repository_name}/repositories/{reference}/vulnerabilities", headers=headers)
    return response.json()


def describe_harbor_repository(repository_name):
    response = requests.get(
        f"{HARBOR_URL}/api/v2.0/projects/{repository_name}/repositories/{repository_name}", headers=headers)
    return response.json()


harbor_functions = {
    "get_harbor_projects": get_harbor_projects,
    "get_harbor_repositories": get_harbor_repositories,
    "get_harbor_artifacts": get_harbor_artifacts,
    "get_harbor_artifact_vulnerabilities": get_harbor_artifact_vulnerabilities,
    "describe_harbor_repository": describe_harbor_repository
}

harbor_function_definitions = [
    {
        "name": "get_harbor_projects",
        "description": "Get information about Harbor projects",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_harbor_repositories",
        "description": "Get the repositories of a Harbor project or all repositories",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "description": "The name of the project (optional)"}
            },
            "required": []
        }
    },
    {
        "name": "get_harbor_artifacts",
        "description": "Get the artifacts of a Harbor repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repository_name": {"type": "string", "description": "The nameof the repository"}
            },
            "required": ["repository_name"]
        }
    },
    {
        "name": "get_harbor_vulnerabilities",
        "description": "Get the vulnerabilities of a Harbor artifact",
        "parameters": {
            "type": "object",
            "properties": {
                "artifact_reference": {"type": "string", "description": "The reference of the artifact"}
            },
            "required": ["artifact_reference"]
        }
    },
    {
        "name": "get_harbor_repository",
        "description": "Get information about a Harbor repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repository_name": {"type": "string", "description": "The name of the repository"}
            },
            "required": ["repository_name"]
        }
    }
]
