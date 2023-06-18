import requests
import json
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ARGOCD_API_URL = os.getenv('ARGOCD_URL')
ARGOCD_API_KEY = os.getenv("ARGOCD_API_KEY", None)
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", None)

argocd_session = requests.Session()
github_session = requests.Session()

if ARGOCD_API_KEY:
    argocd_session.headers.update({"Authorization": f"Bearer {ARGOCD_API_KEY}"})

if GITHUB_API_TOKEN:
    github_session.headers.update({"Authorization": f"token {GITHUB_API_TOKEN}"})


def get_argocd_applications():
    response = argocd_session.get(f"{ARGOCD_API_URL}/api/v1/applications")
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


def get_latest_release(owner, repo):
    response = github_session.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest")
    return response.json()


def get_release_by_tag(owner, repo, tag):
    response = github_session.get(f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}")
    return response.json()


def compare_releases(owner, repo, tag1, tag2):
    release1 = get_release_by_tag(owner, repo, tag1)
    release2 = get_release_by_tag(owner, repo, tag2)
    return {
        "release1": release1,
        "release2": release2
    }


chatbot_functions = {
    "get_argocd_applications": get_argocd_applications,
    "get_latest_release": get_latest_release,
    "get_release_by_tag": get_release_by_tag,
    "compare_releases": compare_releases
}
