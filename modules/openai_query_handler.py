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

    def count_token(self, text):
        num_token = len(self.tokenizer.encode(text))
        return num_token

    def chunkify_text(self, text):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            length_function=self.count_token,
            separators=['.', '\n', ' ', '\n\n', ',', '}', ']'],
            chunk_overlap=0
        )
        chunks = splitter.split_text(text)
        return chunks

    def initiate_openai_conversation(self, query):
        response = openai.ChatCompletion.create(
            model=self.openai_model,
            messages=[{"role": "user", "content": query}],
            functions=self.openai_function_definitions,
        )
        openai_message = response["choices"][0]["message"]
        return openai_message

    def process_openai_function_call(self, openai_message):
        if openai_message.get("function_call"):
            function_name = openai_message["function_call"]["name"]
            function_args_json = openai_message["function_call"].get("arguments", {})
            function_args = json.loads(function_args_json)

            selected_function = self.custom_toolkit_functions.get(function_name)

            if selected_function:
                result = str(selected_function(**function_args))
                return function_name, result
            else:
                print(f"Function {function_name} not found")
        return None, None

    def construct_openai_query_response(self, query):
        chunks = self.chunkify_text(query)
        response = ""
        for chunk in chunks:
            openai_message = self.initiate_openai_conversation(chunk)
            function_name, result = self.process_openai_function_call(openai_message)
            if function_name and result:
                second_response = openai.ChatCompletion.create(
                    model=self.openai_model,
                    messages=[
                        {"role": "user", "content": chunk},
                        openai_message,
                        {
                            "role": "function",
                            "name": function_name,
                            "content": result
                        }
                    ]
                )
                response += second_response.choices[0].message['content']
            else:
                response += openai_message['content']
        return response

