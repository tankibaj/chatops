import json
import os
from dotenv import find_dotenv, load_dotenv
import openai
from modules.conversation_history import ConversationHistory

# Load environment variables
load_dotenv(find_dotenv())
# Get the OpenAI API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")
# If the API key is not found, raise an error
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

conversation_history = ConversationHistory()


def ask(query):
    try:
        # Create a chat completion with the OpenAI API
        first_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=conversation_history.get_conversation_history() + [
                {
                    "role": "system",
                    "content": "You are ChatOps, a DevOps chatbot developed by Naim, designed to "
                               "assist with answering questions, providing information, and engaging "
                               "in conversation on a wide range of DevOps topics."
                },
                {"role": "user", "content": query}
            ]
        )
        # Extract the first response message
        first_response = first_response["choices"][0]["message"]["content"]
        return first_response
    except openai.error.InvalidRequestError as e:
        if 'maximum context length' in str(e):
            print("Error: The conversation exceeded the maximum token limit in first model.")
        else:
            print(f"Error communicating with OpenAI API: {e}")
        return None


def main():
    while True:
        # print(conversation_history.get_conversation_history())
        query = input("You: ")
        conversation_history.add_message("user", query)
        response = ask(query)
        print("Assistant: " + response)
        conversation_history.add_message("assistant", response)


if __name__ == "__main__":
    main()
