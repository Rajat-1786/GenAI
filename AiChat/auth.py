from fastapi import APIRouter, status
from model import SignupRequest

auth_router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signup_request: SignupRequest):
    print(f"Received signup request for user: {signup_request.user_name}, email: {signup_request.email} password: {signup_request.password}, confirm_password: {signup_request.confirm_password}")
    # Implement signup logic here
    return {"message": "Signup successful"}

@auth_router.post("/login")
async def login():
    # Implement login logic here
    return {"message": "Login successful"}