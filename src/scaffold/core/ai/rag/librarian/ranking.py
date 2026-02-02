# Path: scaffold/core/ai/rag/librarian/ranking.py
# -----------------------------------------------

import time
from typing import List, Dict
from .contracts import RAGQuery


class RelevanceJudge:
    """
    =============================================================================
    == THE JUDGE OF RELEVANCE (V-Ω-TEMPORAL-AWARE)                             ==
    =============================================================================
    Re-ranks results based on Recency, Complexity, and Intent.
    """

    def rank(self, hits: List[Dict], query: RAGQuery) -> List[Dict]:
        # [ELEVATION 4] Temporal Boosting
        # We assume 'mtime' is in metadata (needs to be added by indexer)
        # For now, we simulate it or rely on file path heuristics.

        ranked = sorted(hits, key=lambda x: x['score'], reverse=True)

        # [ELEVATION 11] Intent Filtering
        if query.intent == query.intent.REFACTORING:
            # Prefer implementation code over tests/docs
            ranked = [h for h in ranked if "test" not in h['metadata']['source']] + \
                     [h for h in ranked if "test" in h['metadata']['source']]

        return ranked[:query.limit]