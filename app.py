import requests
import json
import openai
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def get_pizza_info(pizza_name):
    # This would normally be a database query.
    # Here we just return a mocked object.
    return json.dumps({
        'name': pizza_name,
        'price': 10.99  # Mocked price
    })


def chat_with_openai(query):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "user", "content": query}
        ],
        functions=[
            {
                "name": "get_pizza_info",
                "description": "Get information about a specific pizza",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pizza_name": {
                            "type": "string",
                            "description": "The name of the pizza"
                        }
                    },
                    "required": ["pizza_name"]
                }
            }
        ]
    )

    message = response.choices[0].message
    if 'function_call' in message:
        function_name = message['function_call']['name']
        arguments = json.loads(message['function_call']['arguments'])
        if function_name == 'get_pizza_info':
            function_response = get_pizza_info(**arguments)
            response2 = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": None, "function_call": message['function_call']},
                    {"role": "function", "name": function_name, "content": function_response}
                ]
            )
            return response2.choices[0].message['content']
    else:
        return message['content']


# print(chat_with_openai("What is the price of pizza salami?"))


def main():
    while True:
        prompt = input("You: ")
        print("Assistant: ", chat_with_openai(prompt))


if __name__ == "__main__":
    main()
