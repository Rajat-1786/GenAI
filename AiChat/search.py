from fastapi import APIRouter, Query, HTTPException, Depends, Request
from model import QueryResponse
from typing import List
from voyage_ai_embed import voyage_ai
from chunking import chunk
router = APIRouter(
    tags=['extract']
)


def get_voyage_ai_client(request: Request) -> voyage_ai:
    return voyage_ai(request.app.state.voyageai_client)

def get_chromadb_client(request: Request):
    return request.app.state.chroma_collection

@router.get("/search", response_model=List[QueryResponse])
def extract(query: str = Query(..., min_length=1, pattern=r"\S"), 
            voyage_ai_client: voyage_ai=Depends(get_voyage_ai_client),
            chroma_client = Depends(get_chromadb_client)):
    chunk_obj = chunk(voyage_ai_client, chroma_client)
    try:

        results = chunk_obj.find_most_similar_chunk(query)
    except Exception as e:
        raise HTTPException(detail=f"API call failed: {e}", status_code=502)

    return [
        QueryResponse(
            text=doc,
            source=meta["source"],
            page=meta["page"],
            score=1 - dist,  # cosine distance -> similarity
        )
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]

