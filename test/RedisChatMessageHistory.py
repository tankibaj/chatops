from langchain.memory import RedisChatMessageHistory

history = RedisChatMessageHistory(url="redis://localhost:6379/0", ttl=600, session_id="my-session")

# Add user and AI messages to the history
history.add_user_message("Hi!")
history.add_ai_message("Hello!")
history.add_user_message("How are you?")
history.add_ai_message("I'm good, thanks!")

# Add messages to the history
history.add_user_message("Hi!")
history.add_ai_message("What's up?")
history.add_user_message("I have a question.")

# Truncate messages to a token limit of 100
history.truncate_messages(token_limit=100)

# Get the updated chat history
messages = history.messages

# Print the updated chat history
for message in history.messages:
    print(message)