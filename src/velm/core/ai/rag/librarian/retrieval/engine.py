# Path: scaffold/core/ai/rag/librarian/retrieval/engine.py
# --------------------------------------------------------

from typing import List, Dict
from pathlib import Path
from .....cortex.vector import VectorCortex
from ..contracts import RAGQuery, RAGChunk


class HybridRetriever:
    """
    =============================================================================
    == THE HYBRID SEEKER (V-Ω-VECTOR-LEXICAL-FUSION)                           ==
    =============================================================================
    Combines Vector Search (Semantic) with Keyword Matching (Lexical).
    """

    def __init__(self, root: Path):
        self.vector_cortex = VectorCortex(root)

    def search(self, query: RAGQuery) -> List[Dict]:
        # 1. Vector Search (The Deep Gaze)
        # We search for the raw text AND the expanded terms
        search_text = f"{query.raw_text} {' '.join(query.expanded_terms)}"
        vector_hits = self.vector_cortex.search(
            search_text,
            limit=query.limit * 2,
            filters=query.filters  # <--- THE CRITICAL LINK
        )

        # 2. Lexical Boost (The Literal Gaze)
        # Boost results that contain exact keywords from the query
        keywords = set(query.raw_text.lower().split())

        final_results = []
        for hit in vector_hits:
            score = hit['distance']  # Similarity (0-1)
            content = hit['content'].lower()

            # Boost for keyword matches
            matches = sum(1 for k in keywords if k in content)
            score += (matches * 0.05)  # 5% boost per keyword match

            # Boost for filename match
            if any(k in hit['metadata']['source'].lower() for k in keywords):
                score += 0.2  # 20% boost for filename match

            hit['score'] = score
            final_results.append(hit)

        return final_results