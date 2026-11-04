from typing import List

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

class JobDescriptionRequest(BaseModel):
    user_name: str = Field(..., description="The username of the user making the request")
    description: str = Field(..., description="The job description for which to extract the title, skills, and years of experience")

class JobDescriptionResponse(BaseModel):
    title: str = Field(..., description="The title of the job")
    skills: List[str] = Field(..., description="A list of skills required for the job")
    years_of_experience: int | None = None
    