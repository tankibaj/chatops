from fastapi import FastAPI
import uvicorn
from modules.openai_query_handler import OpenAIQueryHandler
from modules.argocd import argocd_functions, argocd_function_definitions
from modules.github import github_functions, github_function_definitions
from modules.harbor import harbor_functions, harbor_function_definitions

# Combine all the functions from different modules
chatbot_functions = {**argocd_functions, **github_functions, **harbor_functions}
openai_function_definitions = argocd_function_definitions + github_function_definitions + harbor_function_definitions

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
