# Path: scaffold/artisans/distill/core/slicer/languages/base.py
# -------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Set
from ..contracts import SymbolNode


class LanguageAdapter(ABC):
    """
    The Gnostic Translator.
    Converts raw Tree-sitter ASTs into our SemanticGraph nodes.
    """

    @abstractmethod
    def parse(self, content: str) -> List[SymbolNode]:
        """Extracts the symbol tree from the scripture."""
        pass

    @abstractmethod
    def extract_dependencies(self, content: str, node: SymbolNode) -> Set[str]:
        """
        Scans the body of a node to find what other symbols it invokes.
        """
        pass

