import json
import os
from dotenv import find_dotenv, load_dotenv
import openai
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter


class OpenAIQueryHandler:
    def __init__(self, custom_toolkit_functions, openai_function_definitions, openai_model="gpt-4-0613"):
        load_dotenv(find_dotenv())
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

        self.custom_toolkit_functions = custom_toolkit_functions
        self.openai_function_definitions = openai_function_definitions
        self.openai_model = openai_model
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

    def initiate_openai_conversation(self, query):
        first_response = openai.ChatCompletion.create(
            model=self.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are ChatOps, a DevOps chatbot developed by Naim, designed to "
                               "assist with answering questions, providing information, and engaging "
                               "in conversation on a wide range of DevOps topics. Please provide short answers to "
                               "user queries unless asked to answer in detail. You can retrieve the latest "
                               "information by using the function calling feature."
                },
                {"role": "user", "content": query}
            ],
            functions=self.openai_function_definitions,
        )
        first_response = first_response["choices"][0]["message"]
        return first_response

    def process_openai_function_call(self, first_response):
        if first_response.get("function_call"):
            function_name = first_response["function_call"]["name"]
            function_args_json = first_response["function_call"].get("arguments", {})
            function_args = json.loads(function_args_json)

            selected_function = self.custom_toolkit_functions.get(function_name)

            if selected_function:
                result = str(selected_function(**function_args))
                return function_name, result
            else:
                print(f"Function {function_name} not found")
        return None, None

    def construct_openai_query_response(self, query):
        first_response = self.initiate_openai_conversation(query)
        function_name, function_response = self.process_openai_function_call(first_response)
        if function_name and function_response:
            second_response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "Please provide short answers to user queries unless asked to "
                                                  "answer in detail."},
                    {"role": "user", "content": query},
                    first_response,
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response
                    }
                ]
            )
            response = second_response.choices[0].message['content']
        else:
            response = first_response['content']
        return response
