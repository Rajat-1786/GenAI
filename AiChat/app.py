from fastapi import FastAPI
from model import ChatRequest, ChatResponse
from execute_query import execute_query
from data import add_user_message, add_assistant_message, messages

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chatRequest: ChatRequest):

    print(f"User {chatRequest.user_name} is asking: {chatRequest.user_input}")
    
    user = chatRequest.user_name
    add_user_message(user, chatRequest.user_input)
    
    executor = execute_query()
    user_output = executor.execute(messages[chatRequest.user_name], chatRequest.system_prompt)
    
    add_assistant_message(user, user_output["message"])

    return ChatResponse(
        user_output=user_output["message"],
        input_tokens=user_output["input_tokens"],
        output_tokens=user_output["output_tokens"]
    )