import os
import logging
import tiktoken
from dotenv import find_dotenv, load_dotenv
import openai
from typing import List, Dict
from collections import deque


class ConversationHistory:
    def __init__(self, conversation_token_limit=500, summary_word_limit=300, openai_model="gpt-3.5-turbo"):
        # Load environment variables
        load_dotenv(find_dotenv())
        # Get the OpenAI API key from environment variables
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        # If the API key is not found, raise an error
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        self.openai_model = openai_model
        self.tokenizer = tiktoken.encoding_for_model(self.openai_model)
        self.conversation_token_limit = conversation_token_limit
        self.summary_word_limit = summary_word_limit
        self.conversation_history = deque()
        self.token_count = 0

        # Set up logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def count_tokens(self, text):
        token_count = len(list(self.tokenizer.encode(text)))
        return token_count

    def add_message(self, role: str, content: str):
        if content is None:
            print("Warning: Tried to add a message with None content.")
            return

        message = {"role": role, "content": content}
        message_token_count = self.count_tokens(content)
        self.logger.debug(f"Adding message. Token count: {message_token_count}. Token limit: {self.conversation_token_limit}")

        if self.token_count + message_token_count > self.conversation_token_limit:
            # Create a summary of the current conversation history
            self.logger.debug("Token limit exceeded. Summarizing conversation history.")
            conversation_text = self.get_conversation_text()
            summary = self.summarize(conversation_text)
            self.logger.debug(f"Summary: {summary}  ({self.count_tokens(summary)} tokens)")

            # Clear the conversation history and add the summary as a system message
            self.conversation_history.clear()
            self.conversation_history.append({"role": "system", "content": summary})
            self.token_count = self.count_tokens(summary)

        # Add the new message
        self.conversation_history.append(message)
        self.token_count += message_token_count

    def get_conversation_text(self):
        return " ".join([message["content"] for message in self.conversation_history])

    def summarize(self, text):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"You are a professional summarizer with expertise in preserving context. Your goal is to make the "
                   f"summary as concise as possible, without losing any critical information. The summary must be no "
                   f"more than {self.summary_word_limit} words and ensuring that the summary retains the essential "
                   f"context and is written in a way that can be comprehended by OpenAI GPT3.5-turbo or GPT4. Provide "
                   f"a summary the following conversations: ``` {text} ```"
        )
        summary = response.choices[0].text
        return summary

    def get_conversation_history(self) -> List[Dict[str, str]]:
        return list(self.conversation_history)
