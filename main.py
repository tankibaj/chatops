from fastapi import FastAPI
import uvicorn
from modules.openai_function_definitions import function_definitions
from modules.argocd_api_calls import api_functions
from modules.openai_query_handler import OpenAIQueryHandler

app = FastAPI()
handler = OpenAIQueryHandler(api_functions, function_definitions)


@app.post("/query")
async def query_endpoint(query: str):
    response = handler.generate_response_to_query(query)
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
# http://127.0.0.1:5000/docs
