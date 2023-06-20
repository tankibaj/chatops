import os
import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", None)

github_session = requests.Session()

if GITHUB_API_TOKEN:
    github_session.headers.update({"Authorization": f"token {GITHUB_API_TOKEN}"})


def get_github_latest_release(owner, repo):
    response = github_session.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest")
    return response.json()


def get_github_release_by_tag(owner, repo, tag):
    response = github_session.get(f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}")
    return response.json()


def compare_github_releases(owner, repo, tag1, tag2):
    release1 = get_github_release_by_tag(owner, repo, tag1)
    release2 = get_github_release_by_tag(owner, repo, tag2)
    return {
        "release1": release1,
        "release2": release2
    }


github_functions = {
    "get_github_latest_release": get_github_latest_release,
    "get_github_release_by_tag": get_github_release_by_tag,
    "compare_github_releases": compare_github_releases
}

github_function_definitions = [
    {
        "name": "get_github_latest_release",
        "description": "Get the latest release of a GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "The owner of the repository"},
                "repo": {"type": "string", "description": "The name of the repository"}
            },
            "required": ["owner", "repo"]
        }
    },
    {
        "name": "get_github_release_by_tag",
        "description": "Get a release of a GitHub repository by tag name",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "The owner of the repository"},
                "repo": {"type": "string", "description": "The name of the repository"},
                "tag": {"type": "string", "description": "The tag name of the release"}
            },
            "required": ["owner", "repo", "tag"]
        }
    },
    {
        "name": "compare_github_releases",
        "description": "Compare two releases of a GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "The owner of the repository"},
                "repo": {"type": "string", "description": "The name of the repository"},
                "tag1": {"type": "string", "description": "Thetag name of the first release"},
                "tag2": {"type": "string", "description": "The tag name of the second release"}
            },
            "required": ["owner", "repo", "tag1", "tag2"]
        }
    }
]
