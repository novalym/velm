# Path: scaffold/core/ai/rag/librarian/indexers/base.py
# -----------------------------------------------------

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from ..contracts import RAGChunk

class BaseIndexer(ABC):
    """The Sacred Contract for all Indexers."""

    def __init__(self, root: Path):
        self.root = root

    @abstractmethod
    def chunk(self, path: Path, content: str) -> List[RAGChunk]:
        """Transmutes a file into semantic atoms."""
        pass