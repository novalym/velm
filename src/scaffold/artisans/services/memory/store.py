import os
from supabase import create_client


class VectorStore:
    """[THE MEMORY BANK] Interacts with Supabase pgvector."""

    def __init__(self):
        url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
        key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        self.sb = create_client(url, key)

    def upsert(self, collection: str, vectors: list):
        # vectors = [{id, content, metadata, embedding}]
        # Assuming table name is 'documents' or passed via 'collection'
        return self.sb.table(collection).upsert(vectors).execute()

    def query(self, collection: str, embedding: list[float], top_k: int, threshold: float):
        # Calls a Postgres RPC function 'match_documents' (Standard Supabase Pattern)
        params = {
            "query_embedding": embedding,
            "match_threshold": threshold,
            "match_count": top_k
        }
        return self.sb.rpc(f"match_{collection}", params).execute()