import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

HARBOR_URL = os.getenv('HARBOR_URL')
HARBOR_API_KEY = os.getenv("HARBOR_API_KEY", None)

harbor_session = requests.Session()

if HARBOR_API_KEY:
    harbor_session.headers.update({"Authorization": f"token {HARBOR_API_KEY}"})


def get_harbor_projects():
    response = harbor_session.get(f"{HARBOR_URL}/api/v2.0/projects")
    return response.json()


def get_harbor_repositories(project_name):
    # Get the list of projects
    projects = get_harbor_projects()

    # Find the project with the given name
    project = next((project for project in projects if project['name'] == project_name), None)

    # If the project was found, get its ID
    if project is not None:
        project_id = project['project_id']
    else:
        raise ValueError(f"No project found with name {project_name}")

    # Make the API request
    response = harbor_session.get(f"{HARBOR_URL}/api/v2.0/projects/{project_id}/repositories")
    return response.json()


def get_harbor_artifacts(repository_name):
    response = harbor_session.get(f"{HARBOR_URL}/api/v2.0/projects/{repository_name}/artifacts")
    return response.json()


def get_harbor_artifact_vulnerabilities(repository_name, reference):
    response = harbor_session.get(
        f"{HARBOR_URL}/api/v2.0/projects/{repository_name}/repositories/{reference}/vulnerabilities")
    return response.json()


def describe_harbor_repository(repository_name):
    response = harbor_session.get(
        f"{HARBOR_URL}/api/v2.0/projects/{repository_name}/repositories/{repository_name}")
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
