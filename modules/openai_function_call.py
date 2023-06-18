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
        "description": "Get all projects in Harbor",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_harbor_artifacts",
        "description": "Get all artifacts in a specific Harbor project",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "description": "The name of the Harbor project"}
            },
            "required": ["project_name"]
        }
    },
    {
        "name": "get_artifact_vulnerabilities",
        "description": "Get vulnerabilities of a specific artifact in Harbor",
        "parameters": {
            "type": "object",
            "properties": {
                "artifact_name": {"type": "string", "description": "The name of the Harbor artifact"}
            },
            "required": ["artifact_name"]
        }
    },
    {
        "name": "get_artifact_details",
        "description": "Get details of a specific artifact in Harbor",
        "parameters": {
            "type": "object",
            "properties": {
                "artifact_name": {"type": "string", "description": "The name of the Harbor artifact"}
            },
            "required": ["artifact_name"]
        }
    }
]
