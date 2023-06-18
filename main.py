from fastapi import FastAPI
import uvicorn
from modules.chatbot_call import chatbot_functions
from modules.openai_query_handler import OpenAIQueryHandler
from modules.openai_function_call import openai_function_definitions

assistant = OpenAIQueryHandler(chatbot_functions, openai_function_definitions)

app = FastAPI()


@app.post("/query")
async def query_endpoint(query: str):
    response = assistant.generate_response_to_query(query)
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
# http://127.0.0.1:5000/docs


# -- Enable CLI ChatOps
# def main():
#     while True:
#         query = input("You: ")
#         print("Assistant: ", assistant.generate_response_to_query(query))
#
#
# if __name__ == "__main__":
#     main()
