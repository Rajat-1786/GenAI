from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_name: str
    user_input: str
    system_prompt: str = "You are a helpful assistant."

class ChatResponse(BaseModel):
    user_output: str
    input_tokens: int
    output_tokens: int

class SignupRequest(BaseModel):
    user_name: str = Field(..., description="The username for the new user")
    email: str = Field(..., description="The email address for the new user")
    password: str = Field(..., description="The password for the new user")
    confirm_password: str = Field(..., description="The confirmation of the password for the new user")