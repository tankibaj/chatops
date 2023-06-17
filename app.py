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
    return json.dumps({
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
    })


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
                "name": "get_argocd_applications",
                "description": "Get information about ArgoCD applications",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
    )

    message = response.choices[0].message
    if 'function_call' in message:
        function_name = message['function_call']['name']
        arguments = json.loads(message['function_call']['arguments'])
        if function_name == 'get_argocd_applications':
            function_response = get_argocd_applications()
            response2 = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": None, "function_call": message['function_call']},
                    {"role": "function", "name": function_name, "content": function_response}
                ]
            )
            return response2.choices[0].message['content']
    else:
        return message['content']


def main():
    while True:
        prompt = input("You: ")
        print("Assistant: ", chat_with_openai(prompt))


if __name__ == "__main__":
    main()