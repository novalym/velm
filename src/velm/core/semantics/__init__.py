# Path: core/semantics/__init__.py
# --------------------------------

"""
=================================================================================
== THE SEMANTIC CORTEX (V-Ω-CORE-FACULTY)                                      ==
=================================================================================
This sanctum houses the faculties of Intent Analysis, Semantic Retrieval, and
Relevance Reranking. It is the engine's ability to understand "Meaning" beyond
mere syntax.
"""

from .engine import SemanticEngine
from .contracts import UserIntent, SemanticHit, QueryIntent
from .retriever import SemanticRetriever
from .intent import IntentAnalyzer
from .reranker import RelevanceReranker

__all__ = [
    "SemanticEngine",
    "UserIntent",
    "SemanticHit",
    "QueryIntent",
    "SemanticRetriever",
    "IntentAnalyzer",
    "RelevanceReranker"
]