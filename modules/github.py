import base64
import os
import requests
import mistune
import re
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


def get_latest_release_version(owner, repo):
    latest_release = get_github_latest_release(owner, repo)
    return latest_release['tag_name']


def get_changelogs_of_release(owner, repo, tag):
    release = get_github_release_by_tag(owner, repo, tag)
    release_notes = release['body']

    # Regular expression to match URLs containing 'CHANGELOG'
    pattern = re.compile(r'https?://[^\s()<>]+CHANGELOG[^\s()<>]*', re.IGNORECASE)

    changelog_url = re.search(pattern, release_notes)
    if changelog_url:
        # Convert the URL to point to the raw content
        raw_url = changelog_url.group().replace('github.com', 'raw.githubusercontent.com').replace('/blob', '')
        response = github_session.get(raw_url)
        changelogs = response.text
        # changelogs = raw_url
    else:
        changelogs = release_notes

    return changelogs


github_functions = {
    "get_github_latest_release": get_github_latest_release,
    "get_github_release_by_tag": get_github_release_by_tag,
    "compare_github_releases": compare_github_releases,
    "get_latest_release_version": get_latest_release_version,
    "get_changelogs_of_release": get_changelogs_of_release
}

github_function_definitions = [
    {
        "name": "get_github_latest_release",
        "description": "Fetches the entire data of the latest release of a GitHub repository. This data includes "
                       "various details such as the author, the release notes, the creation date, the tag name, "
                       "and more. Use this function when you need detailed information about the latest release.",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "The owner of the repository."},
                "repo": {"type": "string", "description": "The name of the repository."}
            },
            "required": ["owner", "repo"]
        }
    },
    {
        "name": "get_github_release_by_tag",
        "description": "Fetches a specific release of a GitHub repository by tag name. This function returns detailed "
                       "information about the release, similar to get_github_latest_release, but for a specific tag. "
                       "Use this function when you need detailed information about a specific release.",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "The owner of the repository."},
                "repo": {"type": "string", "description": "The name of the repository."},
                "tag": {"type": "string", "description": "The tag name of the release."}
            },
            "required": ["owner", "repo", "tag"]
        }
    },
    {
        "name": "compare_github_releases",
        "description": "Compares two releases of a GitHub repository. This function fetches the data for two specific "
                       "releases and returns them for comparison. Use this function when you need to compare the "
                       "details of two different releases.",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "The owner of the repository."},
                "repo": {"type": "string", "description": "The name of the repository."},
                "tag1": {"type": "string", "description": "The tag name of the first release."},
                "tag2": {"type": "string", "description": "The tag name of the second release."}
            },
            "required": ["owner", "repo", "tag1", "tag2"]
        }
    },
    {
        "name": "get_latest_release_version",
        "description": "Fetches the version of the latest release of a GitHub repository. This function uses the "
                       "get_github_latest_release function to get the data of the latest release, and then extracts "
                       "the version from this data. Use this function when you only need the version of the latest "
                       "release.",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "The owner of the repository."},
                "repo": {"type": "string", "description": "The name of the repository."}
            },
            "required": ["owner", "repo"]
        }
    },
    {
        "name": "get_changelogs_of_release",
        "description": "Fetches the changelogs for a specific version of a GitHub repository by tag name. If the "
                       "changelogs are not included in the release notes, it tries to fetch the changelog file from "
                       "the CHANGELOG directory or the CHANGELOG.md file from the root directory. Use this function "
                       "when you need the changelogs for a specific release version.",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "The owner of the repository."},
                "repo": {"type": "string", "description": "The name of the repository."},
                "tag": {"type": "string", "description": "The tag name of the release."}
            },
            "required": ["owner", "repo", "tag"]
        }
    }
]
