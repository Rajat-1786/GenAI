from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
from model import ChatRequest, ChatResponse
from execute_query import execute_query
from data import add_user_message, add_assistant_message, messages

chat_router = APIRouter(
    tags=["Chat"],
    prefix="/chat"
)

@chat_router.post("/", status_code=status.HTTP_200_OK, response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    
    print(f"User {chat_request.user_name} is asking: {chat_request.user_input}")
    
    user = chat_request.user_name
    add_user_message(user, chat_request.user_input)
    
    executor = execute_query()
    user_output = await executor.chat(messages[chat_request.user_name], chat_request.system_prompt)
    
    add_assistant_message(user, user_output["message"])

    return ChatResponse(
        user_output=user_output["message"],
        input_tokens=user_output["input_tokens"],
        output_tokens=user_output["output_tokens"]
    )

@chat_router.post("/stream", status_code=status.HTTP_200_OK)
async def chat_stream(chat_request: ChatRequest):
    print(f"User {chat_request.user_name} is asking: {chat_request.user_input}")
       
    user = chat_request.user_name
    add_user_message(user, chat_request.user_input)
    
    executor = execute_query()

    async def event_generator():
        message = ""
        try:
            async for text in executor.stream(messages[chat_request.user_name], chat_request.system_prompt):
                message += text
                yield text
        finally:
            if message:
                add_assistant_message(user, message)

    return StreamingResponse(event_generator(), media_type="text/plain")
           
        
@chat_router.get("/generate/policy/{description}", status_code=status.HTTP_200_OK)
async def generate_policy(description: str):
    executor = execute_query()
    system_prompt = "You are a helpful aws expert. Generate a event bridge policy based on the following description: " + description
    policy =await executor.generate_policy(description, system_prompt)
    return policy