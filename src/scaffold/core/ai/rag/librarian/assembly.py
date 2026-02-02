# Path: scaffold/core/ai/rag/librarian/assembly.py
# ------------------------------------------------

from typing import List, Dict
from .contracts import RAGContext, RAGChunk
from ....cortex.tokenomics import TokenEconomist


class ContextWeaver:
    """
    =============================================================================
    == THE CONTEXT WEAVER (V-Ω-TOKEN-BUDGET-AWARE)                             ==
    =============================================================================
    Assembles the final prompt context, respecting token limits.
    """

    def __init__(self):
        self.economist = TokenEconomist()

    def weave(self, hits: List[Dict], max_tokens: int = 2000) -> RAGContext:
        chunks = []
        sources = []
        current_tokens = 0
        formatted_parts = []

        for hit in hits:
            content = hit['content']
            meta = hit['metadata']
            source = meta.get('source', 'unknown')

            # Forge the Header
            header = f"--- CONTEXT: {source} (Line {meta.get('line_number', '?')}) ---"
            block = f"{header}\n{content}\n"

            cost = self.economist.estimate_cost(block)

            if current_tokens + cost > max_tokens:
                break

            current_tokens += cost
            formatted_parts.append(block)
            sources.append(source)

            # Reconstruct RAGChunk object for the record
            chunks.append(RAGChunk(
                id=hit['id'],
                content=content,
                file_path=source,
                start_line=meta.get('line_number', 0),
                end_line=0,  # Unknown from vector hit
                type=meta.get('type', 'unknown'),
                language="unknown"
            ))

        return RAGContext(
            chunks=chunks,
            total_tokens=current_tokens,
            formatted_text="\n".join(formatted_parts),
            sources=sources
        )