import requests
import json
import openai
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ARGOCD_API_URL = os.getenv('ARGOCD_URL')
ARGOCD_API_KEY = os.getenv("ARGOCD_API_KEY", None)

openai.api_key = OPENAI_API_KEY

session = requests.Session()

if ARGOCD_API_KEY:
    session.headers.update({"Authorization": f"Bearer {ARGOCD_API_KEY}"})


def get_argocd_applications():
    response = session.get(f"{ARGOCD_API_URL}/api/v1/applications")
    applications = response.json()["items"]
    return {app['metadata']['name']: app['status']['sync']['status'] for app in applications}


def get_out_of_sync_applications():
    applications = get_argocd_applications()
    return [name for name, status in applications.items() if status != 'Synced']


def get_synced_applications():
    applications = get_argocd_applications()
    return [name for name, status in applications.items() if status == 'Synced']


def get_argocd_application(name):
    response = session.get(f"{ARGOCD_API_URL}/api/v1/applications/{name}")
    return response.json()


def get_application_health_status(name):
    response = session.get(f"{ARGOCD_API_URL}/api/v1/applications/{name}")
    return response.json()["status"]["health"]["status"]


def get_application_errors(name):
    response = session.get(f"{ARGOCD_API_URL}/api/v1/applications/{name}")
    sync_status = response.json()["status"]["sync"]
    return sync_status.get('errorMessage', 'No sync errors')


def chat_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        temperature=0.9,
        top_p=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        functions=[
            {
                "name": "get_number_of_applications",
                "description": "Get the total number of ArgoCD applications",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_out_of_sync_applications",
                "description": "Get a list of ArgoCD applications that are out of sync",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_synced_applications",
                "description": "Get a list of ArgoCD applications that are synced",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_list_of_applications",
                "description": "Get a list of ArgoCD applications",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_application_health_status",
                "description": "Get the health status of an ArgoCD application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the ArgoCD application"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "get_application_errors",
                "description": "Get any sync error messages from an ArgoCD application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the ArgoCD application"
                        }
                    },
                    "required": ["name"]
                }
            }
        ]
    )
    if 'function_call' in response.choices[0].message:
        function_call = response.choices[0].message['function_call']
        function_name = function_call['name']
        arguments = json.loads(function_call['arguments'])
        if function_name == 'get_number_of_applications':
            return len(get_argocd_applications())
        elif function_name == 'get_list_of_applications':
            return [app['metadata']['name'] for app in get_argocd_applications()]
        elif function_name == 'get_out_of_sync_applications':
            return get_out_of_sync_applications()
        elif function_name == 'get_synced_applications':
            return get_synced_applications()
        elif function_name == 'get_application_health_status':
            return get_application_health_status(arguments['name'])
        elif function_name == 'get_application_errors':
            return get_application_errors(arguments['name'])
    else:
        return response.choices[0].message['content']


def main():
    while True:
        prompt = input("You: ")
        print("Assistant: ", chat_with_openai(prompt))


if __name__ == "__main__":
    main()
