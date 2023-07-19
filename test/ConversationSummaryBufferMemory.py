import os
from dotenv import find_dotenv, load_dotenv
import openai
from langchain.memory import ConversationSummaryBufferMemory, RedisChatMessageHistory, CombinedMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

load_dotenv(find_dotenv())

openai.api_key = os.environ.get("OPENAI_API_KEY")
# If the API key is not found, raise an error
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# -- Simple Conversation History Memory
# llm = OpenAI()
memory = ConversationSummaryBufferMemory(llm=OpenAI(), max_token_limit=10)
# Adding a system message
memory.save_context({"input": "System message"}, {"output": "System response"})

# Adding a user message
memory.save_context({"input": "User message"}, {"output": "User response"})
# memory.save_context({"input": "hi"}, {"output": "whats up"})
# memory.save_context({"input": "not much you"}, {"output": "not much"})

# Save system message to the memory
# memory.save_context({"input": "System message"}, {"output": ""})


# -- Redis Chat Message History
# llm = OpenAI()
#
# summary_memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=10)
# redis_memory = RedisChatMessageHistory(url="redis://localhost:6379/0", ttl=600, session_id="my-session")
#
# memory = CombinedMemory(memories=[summary_memory, redis_memory])
#
# conversation = ConversationChain(llm=llm, memory=memory)

if __name__ == "__main__":
    print(memory.load_memory_variables({}))
