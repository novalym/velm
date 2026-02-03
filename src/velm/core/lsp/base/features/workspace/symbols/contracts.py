# Path: core/lsp/features/workspace/symbols/contracts.py
# ------------------------------------------------------
from abc import ABC, abstractmethod
from typing import List
from .models import WorkspaceSymbol

class SymbolScryer(ABC):
    """
    The abstract soul of a search vector.
    Could be Local (Disk), Remote (Daemon), or Neural (AI).
    """
    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def scan(self, query: str) -> List[WorkspaceSymbol]:
        """The search rite."""
        pass