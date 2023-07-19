import json
import os
from dotenv import find_dotenv, load_dotenv
import openai
import logging
from modules.conversation_history import ConversationHistory
from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms import OpenAI


class OpenAIQueryHandler:
    # Initialize the class with necessary parameters and configurations
    def __init__(self, custom_toolkit_functions, openai_function_definitions, openai_model="gpt-4-0613"):
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
        self.openai_model = openai_model
        self.logger = logging.getLogger(__name__)
        self.memory = ConversationSummaryBufferMemory(llm=OpenAI(), max_token_limit=100)

    # Method to initiate a conversation with the OpenAI API
    def initiate_conversation(self, query):
        try:
            convo_history = self.memory.load_memory_variables({})
            # Create a chat completion with the OpenAI API
            first_response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are ChatOps, a DevOps chatbot developed by Naim, designed to "
                                   "assist with answering questions, providing information, and engaging "
                                   "in conversation on a wide range of DevOps topics. Please provide short "
                                   "answers to user queries unless asked to answer in detail. You can retrieve "
                                   "the real time information about ArgoCD apps, Harbor and Github by using the "
                                   "function calling feature."
                    },
                    {"role": "user", "content": f"Here is context: {convo_history}"},
                    {"role": "user", "content": query},
                ],
                functions=self.openai_function_definitions,
            )
            # Extract the first response message
            first_response = first_response["choices"][0]["message"]
            return first_response
        except openai.error.InvalidRequestError as e:
            if 'maximum context length' in str(e):
                print("Error: The conversation exceeded the maximum token limit in first model.")
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
    # Method to construct the final response to the user query
    def construct_openai_query_response(self, query):
        # Initiate the conversation with the OpenAI API
        first_response = self.initiate_conversation(query)

        # Process the function call from the first response
        function_name, function_response = self.process_openai_function_call(first_response)

        # If a function call was made and a response was obtained
        if function_name and function_response:
            try:
                # Continue the conversation with the OpenAI API using the function response
                second_response = openai.ChatCompletion.create(
                    model=self.openai_model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are ChatOps, a DevOps chatbot developed by Naim, designed to "
                                       "assist with answering questions, providing information, and engaging "
                                       "in conversation on a wide range of DevOps topics. Please provide short "
                                       "answers to user queries unless asked to answer in detail. You can retrieve "
                                       "the real time information about ArgoCD apps, Harbor and Github by using the "
                                       "function calling feature."
                        },
                        {
                            "role": "function",
                            "name": function_name,
                            "content": function_response
                        }
                    ]
                )
                # Extract the final response from the second response
                response = second_response.choices[0].message['content']

                # Save the final response to the conversation history
                if response is not None:
                    self.memory.save_context({"input": query}, {"output": response})
                    # self.logger.debug(self.memory.load_memory_variables({}))
            except openai.error.InvalidRequestError as e:
                # Handle the token limit error specifically
                if 'maximum context length' in str(e):
                    print("Error: The conversation exceeded the maximum token limit in second model.")
                else:
                    print(f"Error communicating with OpenAI API: {e}")
                response = None
        else:
            # If no function call was made, use the content from the first response as the final response
            response = first_response['content'] if first_response else None

            # Save the final response to the conversation history
            if response is not None:
                self.memory.save_context({"input": query}, {"output": response})
                # self.logger.debug(self.memory.load_memory_variables({}))

        # Return the final response
        return response
