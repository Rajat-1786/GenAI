from fastapi import FastAPI
from chat import chat_router
from auth import auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)

