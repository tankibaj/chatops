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
        self.max_tokens = 4096  # Set this to half of your maximum token limit

    def count_token(self, text):
        num_token = len(self.tokenizer.encode(text))
        return num_token

    def chunkify_text(self, text):
        chunks = []
        current_chunk = ""
        for word in text.split():
            if self.count_token(current_chunk + " " + word) <= self.max_tokens:
                current_chunk += " " + word
            else:
                chunks.append(current_chunk)
                current_chunk = word
        chunks.append(current_chunk)  # Append the last chunk
        return chunks

    def initiate_openai_conversation(self, query):
        responses = []
        chunks = self.chunkify_text(query)
        for chunk in chunks:
            response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[{"role": "user", "content": chunk}],
                functions=self.openai_function_definitions,
            )
            openai_message = response["choices"][0]["message"]
            responses.append(openai_message)
        return responses

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
        responses = self.initiate_openai_conversation(query)
        response_text = ""
        for response in responses:
            function_name, result = self.process_openai_function_call(response)
            if function_name and result:
                second_query_chunks = self.chunkify_text(query)
                for chunk in second_query_chunks:
                    second_response = openai.ChatCompletion.create(
                        model=self.openai_model,
                        messages=[
                            {"role": "user", "content": chunk},
                            response,
                            {
                                "role": "function",
                                "name": function_name,
                                "content": result
                            }
                        ]
                    )
                    response_text += second_response.choices[0].message['content']
            else:
                response_text += response['content']
        return response_text

