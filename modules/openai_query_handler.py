import json
import os
from dotenv import find_dotenv, load_dotenv
import openai
import tiktoken


class OpenAIQueryHandler:
    # Initialize the class with necessary parameters and configurations
    def __init__(self, custom_toolkit_functions, openai_function_definitions, openai_model4="gpt-4-0613",
                 openai_model3="gpt-3.5-turbo-0613"):
        # Load environment variables
        load_dotenv(find_dotenv())
        # Get the OpenAI API key from environment variables
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        # If the API key is not found, raise an error
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

        # Initialize class variables
        self.custom_toolkit_functions = custom_toolkit_functions
        self.openai_function_definitions = openai_function_definitions
        self.openai_model4 = openai_model4
        self.openai_model3 = openai_model3
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

    # count token length
    def count_tokens(self, text):
        token_count = len(list(self.tokenizer.encode(text)))
        return token_count

    # Method to initiate a conversation with the OpenAI API
    def initiate_openai_conversation(self, query):
        try:
            # Create a chat completion with the OpenAI API
            first_response = openai.ChatCompletion.create(
                model=self.openai_model3,
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
            # Extract the first response message
            first_response = first_response["choices"][0]["message"]
            return first_response
        except openai.error.InvalidRequestError as e:
            if 'maximum context length' in str(e):
                print("Error: The conversation exceeded the maximum token limit.")
            else:
                print(f"Error communicating with OpenAI API: {e}")
            return None

    # Method to process a function call from the OpenAI API response
    def process_openai_function_call(self, first_response):
        if first_response and first_response.get("function_call"):
            function_name = first_response["function_call"]["name"]
            function_args_json = first_response["function_call"].get("arguments", {})
            function_args = json.loads(function_args_json)

            # Get the selected function from the custom toolkit functions
            selected_function = self.custom_toolkit_functions.get(function_name)

            # If the selected function exists, call it with the arguments and return the result
            if selected_function:
                result = str(selected_function(**function_args))
                return function_name, result
            else:
                print(f"Function {function_name} not found")
        return None, None

    # Method to construct the final response to the user query
    def construct_openai_query_response(self, query):
        # Initiate the conversation with the OpenAI API
        first_response = self.initiate_openai_conversation(query)
        # Process the function call from the first response
        function_name, function_response = self.process_openai_function_call(first_response)

        # If a function call was made and a response was obtained
        if function_name and function_response:
            try:
                # Continue the conversation with the OpenAI API using the function response
                second_response = openai.ChatCompletion.create(
                    model=self.openai_model4,
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
                # Extract the final response from the second response
                response = second_response.choices[0].message['content']
            except openai.error.InvalidRequestError as e:
                # Handle the token limit error specifically
                if 'maximum context length' in str(e):
                    print("Error: The conversation exceeded the maximum token limit.")
                else:
                    print(f"Error communicating with OpenAI API: {e}")
                response = None
        else:
            # If no function call was made, use the content from the first response as the final response
            response = first_response['content'] if first_response else None

        # Return the final response
        return response
