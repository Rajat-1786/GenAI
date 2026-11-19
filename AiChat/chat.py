from fastapi import HTTPException
import json
from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import StreamingResponse
from model import ChatRequest, ChatResponse, JobDescriptionRequest, JobDescriptionResponse
from execute_query import execute_query
from data import add_user_message, add_assistant_message, messages, remove_last_user_message
from pydantic import ValidationError

chat_router = APIRouter(
    tags=["Chat"]
)

def get_executor(request: Request)-> execute_query:
    return execute_query(client=request.app.state.anthropic_client)

@chat_router.post("/chat", status_code=status.HTTP_200_OK, response_model=ChatResponse)
async def chat(chat_request: ChatRequest, executor: execute_query = Depends(get_executor)):
    
    print(f"User {chat_request.user_name} is asking: {chat_request.user_input}")
    
    user = chat_request.user_name
    add_user_message(user, chat_request.user_input)
    
    try:
        user_output = await executor.chat(messages[chat_request.user_name], chat_request.system_prompt)
    except Exception as e:
        remove_last_user_message(user)
        raise e
    
    add_assistant_message(user, user_output["message"])

    return ChatResponse(
        user_output=user_output["message"],
        input_tokens=user_output["input_tokens"],
        output_tokens=user_output["output_tokens"]
    )

@chat_router.post("/stream", status_code=status.HTTP_200_OK)
async def chat_stream(chat_request: ChatRequest, executor: execute_query = Depends(get_executor)):
    print(f"User {chat_request.user_name} is asking: {chat_request.user_input}")
       
    user = chat_request.user_name
    add_user_message(user, chat_request.user_input)

    async def event_generator():
        message = ""
        try:
            async for text in executor.stream(messages[chat_request.user_name], chat_request.system_prompt):
                message += text
                yield text
        except Exception as e:
            remove_last_user_message(user)
            raise e
        finally:
            if message:
                add_assistant_message(user, message)

    return StreamingResponse(event_generator(), media_type="text/plain")
           
        
@chat_router.get("/generate/policy/{description}", status_code=status.HTTP_200_OK)
async def generate_policy(description: str, executor: execute_query = Depends(get_executor)):
    system_prompt = "You are a helpful aws expert. Generate a event bridge policy based on the following description: " + description
    last_exception = None
    for i in range(2):
        temp = 0.0 if i == 0 else 0.3
        try:
            policy =await executor.get_json_response(description, system_prompt, temperature=temp)
            result_policy = json.loads(policy)
            return result_policy
        except (json.JSONDecodeError, ValidationError) as e:
            last_exception = e
    raise HTTPException(status_code=422, detail=f"Error generating policy: {last_exception}")


@chat_router.post("/extract", status_code=status.HTTP_200_OK, response_model=JobDescriptionResponse)
async def extract(job_description_request: JobDescriptionRequest, executor: execute_query = Depends(get_executor)):
    description = job_description_request.description
    system_prompt = """You are a helpful assistant. Extract the title, skills and Years of Experience from the following job description and return only JSON with keys title, skills, years_of_experience" \
            Rule:
            1.  Treat No specific experience requirement as null for years_of_experience.
            2.  if Years of experience is in range then fetch the lowest value 
            3.  if job Description seems incorrect return the empty list of skills 
        """
    last_exception = None
    for i in range(2):
        temp = 0.0 if i == 0 else 0.3
        try:
            extracted_info = await executor.get_json_response(description, system_prompt=system_prompt, temperature=temp)
            extracted_info_json = json.loads(extracted_info)
            result = JobDescriptionResponse(**extracted_info_json)
            return result
        except (json.JSONDecodeError, ValidationError) as e:
            last_exception = e
    raise HTTPException(status_code=422, detail=f"Error extracting information: {last_exception}")

