openai_function_definitions = [
    {
        "name": "get_argocd_applications",
        "description": "Get information about ArgoCD applications",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_latest_release",
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
        "name": "get_release_by_tag",
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
        "name": "compare_releases",
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
    },
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
