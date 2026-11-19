from fastapi import FastAPI
from contextlib import asynccontextmanager
from chat import chat_router
from auth import auth_router
from search import router
from anthropic import AsyncAnthropic
import voyageai
import chromadb 
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.anthropic_client = AsyncAnthropic()
    app.state.voyageai_client = voyageai.Client()
    app.state.chroma = chromadb.PersistentClient(path="chroma_db")
    app.state.chroma_collection = app.state.chroma.get_or_create_collection(
    name="docs",
    metadata={"hnsw:space": "cosine"},                    # cosine distance
)
    yield
    await app.state.anthropic_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(router)

