import json
import os
import openai
from dotenv import find_dotenv, load_dotenv


class OpenAIQueryHandler:
    def __init__(self, api_functions, openai_function_definitions, openai_model="gpt-4-0613"):
        load_dotenv(find_dotenv())
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

        self.api_functions = api_functions
        self.openai_function_definitions = openai_function_definitions
        self.openai_model = openai_model

    def send_query_to_openai(self, query):
        response = openai.ChatCompletion.create(
            model=self.openai_model,
            messages=[{"role": "user", "content": query}],
            functions=self.openai_function_definitions,
        )
        message_from_openai = response["choices"][0]["message"]
        return message_from_openai

    def process_openai_function_call(self, message_from_openai):
        if message_from_openai.get("function_call"):
            function_name = message_from_openai["function_call"]["name"]
            function_args_json = message_from_openai["function_call"].get("arguments", {})
            function_args = json.loads(function_args_json)

            api_function = self.api_functions.get(function_name)

            if api_function:
                result = str(api_function(**function_args))
                return function_name, result
            else:
                print(f"Function {function_name} not found")
        return None, None

    def generate_response_to_query(self, query):
        message_from_openai = self.send_query_to_openai(query)
        function_name, result = self.process_openai_function_call(message_from_openai)

        if function_name and result:
            second_response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[
                    {"role": "user", "content": query},
                    message_from_openai,
                    {
                        "role": "function",
                        "name": function_name,
                        "content": result
                    }
                ]
            )
            return second_response.choices[0].message['content']
        else:
            return message_from_openai['content']
