from fastapi import FastAPI
from contextlib import asynccontextmanager
from chat import chat_router
from auth import auth_router
from anthropic import AsyncAnthropic

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.anthropic_client = AsyncAnthropic()
    yield
    await app.state.anthropic_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(chat_router)

