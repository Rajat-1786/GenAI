class voyage_ai:
    def __init__(self, client):
        self.client = client

    def embed_text(self, text: list[str], batch_size=14):
        embed_result = []
        for i in range(0, len(text), batch_size) :
            batch = text[i:i+batch_size]
            result = self.client.embed(batch, model="voyage-4", input_type="document")
            embed_result.extend(result.embeddings)
        return embed_result

    def embed_query(self, query: str):
        result = self.client.embed([query], model="voyage-4", input_type="query")
        return result.embeddings


