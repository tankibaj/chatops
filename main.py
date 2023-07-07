from fastapi import FastAPI
import uvicorn
import logging
from modules.openai_query_handler import OpenAIQueryHandler
from modules.argocd import argocd_functions, argocd_function_definitions
from modules.github import github_functions, github_function_definitions
from modules.harbor import harbor_functions, harbor_function_definitions

logging.basicConfig(level=logging.DEBUG)

# Combine all the functions from different modules
custom_toolkit_functions = {**argocd_functions, **github_functions, **harbor_functions}
openai_function_definitions = argocd_function_definitions + github_function_definitions + harbor_function_definitions

llm = OpenAIQueryHandler(custom_toolkit_functions, openai_function_definitions)

# app = FastAPI()


# @app.post("/query")
# async def query_endpoint(query: str):
#     response = llm.construct_openai_query_response(query)
#     return {"response": response}
#
#
# if __name__ == "__main__":
#     uvicorn.run("main:app", port=5000, log_level="info")
# http://127.0.0.1:5000/docs


# -- Enable CLI ChatOps
def main():
    while True:
        query = input("You: ")
        print("Assistant: ", llm.construct_openai_query_response(query))


if __name__ == "__main__":
    main()
