# Path: scaffold/core/ai/rag/__init__.py
# --------------------------------------

"""
=================================================================================
== THE SACRED GATEWAY TO MEMORY (V-Ω-MODULAR-ACCESS)                           ==
=================================================================================
This scripture unifies the Gnostic Librarian (Dynamic Memory) and the
Knowledge Base (Static Wisdom).

It replaces the old monolithic `rag.py`.
"""

# 1. Summon the High Priest (The Orchestrator)
from .librarian import TheLibrarian

# 2. Summon the Data Contracts
from .librarian.contracts import RAGQuery, RAGContext, RAGChunk, QueryIntent

# 3. Summon the Static Wisdom
from .knowledge import get_static_knowledge

__all__ = [
    "TheLibrarian",
    "RAGQuery",
    "RAGContext",
    "RAGChunk",
    "QueryIntent",
    "get_static_knowledge"
]