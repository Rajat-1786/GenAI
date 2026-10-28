from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_name: str
    user_input: str
    system_prompt: str = "You are a helpful assistant."

class ChatResponse(BaseModel):
    user_output: str
    input_tokens: int
    output_tokens: int