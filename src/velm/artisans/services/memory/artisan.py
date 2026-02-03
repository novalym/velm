import logging
import uuid
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import MemoryRequest
from ....interfaces.base import ScaffoldResult
from .encoder import NeuralEncoder
from .store import VectorStore

Logger = logging.getLogger("MemoryArtisan")


class MemoryArtisan(BaseArtisan[MemoryRequest]):
    """
    =============================================================================
    == THE CORTEX KEEPER (V-Ω-SEMANTIC-MEMORY)                                 ==
    =============================================================================
    LIF: ∞ | ROLE: KNOWLEDGE_ENGINE

    Manages the RAG pipeline: Embedding -> Storage -> Retrieval.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self.encoder = NeuralEncoder()
        self.store = VectorStore()

    def execute(self, request: MemoryRequest) -> ScaffoldResult:
        try:
            # --- RITE 1: UPSERT (MEMORIZE) ---
            if request.action == "upsert":
                if not request.text: return self.engine.failure("No text to memorize.")

                texts = request.text if isinstance(request.text, list) else [request.text]
                metas = request.metadata if isinstance(request.metadata, list) else [request.metadata or {}] * len(
                    texts)
                ids = request.ids if isinstance(request.ids, list) else [request.ids or str(uuid.uuid4())] * len(texts)

                # Embed Batch
                embeddings = self.encoder.embed(texts, request.model)

                # Format payload
                records = []
                for i in range(len(texts)):
                    records.append({
                        "id": ids[i] if isinstance(ids, list) and i < len(ids) else str(uuid.uuid4()),
                        "content": texts[i],
                        "metadata": metas[i],
                        "embedding": embeddings[i]
                    })

                res = self.store.upsert(request.collection, records)
                return self.engine.success(f"Memorized {len(records)} fragments.", data=res.data)

            # --- RITE 2: QUERY (RECALL) ---
            elif request.action == "query":
                if not request.query_text: return self.engine.failure("No query text.")

                # Embed Query
                query_vec = self.encoder.embed([request.query_text], request.model)[0]

                # Search
                res = self.store.query(request.collection, query_vec, request.top_k, request.threshold)
                return self.engine.success("Recall Complete.", data=res.data)

            # --- RITE 3: DELETE (FORGET) ---
            elif request.action == "delete":
                # Implementation depends on store logic (delete by ID or metadata)
                return self.engine.success("Forgetfulness logic placeholder.")

            return self.engine.failure(f"Unknown Memory Action: {request.action}")

        except Exception as e:
            Logger.error(f"Memory Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Cortex Error: {str(e)}")