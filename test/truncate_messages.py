import tiktoken


def count_tokens(text):
    tokenizer = tiktoken.encoding_for_model(self.openai_model)
    token_count = len(list(tokenizer.encode(text)))
    return token_count


def truncate_messages(max_tokens):
    total_tokens = 0
    messages_to_remove = []

    for message in reversed(self.messages):
        message_tokens = count_tokens(message.content)
        total_tokens += message_tokens

        if total_tokens > max_tokens:
            messages_to_remove.append(message)
        else:
            break

    for message in messages_to_remove:
        self.messages.remove(message)
