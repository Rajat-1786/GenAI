from fastapi import FastAPI
from model import ChatRequest, ChatResponse
from execute_query import execute_query

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chatRequest: ChatRequest):
    print(f"Received user input: {chatRequest.user_input}")
    executor = execute_query()
    user_output = executor.execute(chatRequest.user_input)
    return ChatResponse(user_output=user_output)