# Path: scaffold/core/ai/rag/librarian/contracts.py
# -------------------------------------------------

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import List, Dict, Optional, Any, Set

class QueryIntent(Enum):
    """The Soul of the Question."""
    EXPLANATION = auto()  # "How does X work?"
    GENERATION = auto()   # "Write a function to..."
    REFACTORING = auto()  # "Fix this bug..."
    UNKNOWN = auto()

@dataclass
class RAGQuery:
    """The Vessel of Inquiry."""
    raw_text: str
    expanded_terms: List[str] = field(default_factory=list)
    intent: QueryIntent = QueryIntent.UNKNOWN
    filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 5
    threshold: float = 0.4

@dataclass
class RAGChunk:
    """A single atom of Gnosis."""
    id: str
    content: str
    file_path: str
    start_line: int
    end_line: int
    type: str  # 'function', 'class', 'text', 'code'
    language: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    score: float = 0.0  # Relevance score

@dataclass
class RAGContext:
    """The assembled wisdom ready for the LLM."""
    chunks: List[RAGChunk]
    total_tokens: int
    formatted_text: str
    sources: List[str]