from pypdf import PdfReader
import os
from fastapi import HTTPException


class chunk:
    def __init__(self, voyage_ai_client, collections):
        self.voyage_ai_client = voyage_ai_client
        self.collections = collections

    def chunk_by_size(self, text: str, chunk_size: int, page=0, source="", overlap: int = 150):
        chunks =[]
        start = 0
        n=0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            chunks.append({"text":chunk, "source": source, "page": page, "n":n})
            n+=1
            start = end - overlap if end < len(text) else len(text)

        return chunks

    def load_documents_from_file(self, file_path: str):
        if file_path.lower().endswith('.pdf'):
            reader = PdfReader(file_path)
            chunks= []
            for i,page in enumerate(reader.pages):
                chunks += self.chunk_by_size(page.extract_text() or "", 1500, page=i+1, source=os.path.basename(file_path), overlap=200)
        else:
            raise HTTPException(detail="file type not supported", status_code= 502)
        return chunks

    def save_embed_to_db(self,filename):
        chunks  = self.load_documents_from_file(filename)
        embed_tokens = self.voyage_ai_client.embed_text([c['text'] for c in chunks])

        self.collections.upsert(
            ids=[f"{c['source']}:{c['page']}:{c['n']}" for c in chunks],
            documents=[c["text"] for c in chunks],
            embeddings=embed_tokens,                                   # from embed_in_batches
            metadatas=[{"source": c["source"], "page": c["page"]} for c in chunks],
        )

    def find_most_similar_chunk(self, query:str):
        query_tokens = self.voyage_ai_client.embed_query(query)
        results = self.collections.query(query_embeddings=query_tokens, n_results = 5)
        return results





