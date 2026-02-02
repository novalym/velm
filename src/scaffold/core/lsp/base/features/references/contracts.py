# Path: core/lsp/features/references/contracts.py
# -----------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from .models import Location, ReferenceParams
from ...document import TextDocument
from ...utils.text import WordInfo

class ReferenceProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF ECHOES (INTERFACE)                                      ==
    =============================================================================
    Every language-specific reference seeker must sign this contract.
    It defines how to find all instances of a symbol.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the reference source."""
        pass

    @property
    def priority(self) -> int:
        """Determines the order of search (0-100)."""
        return 50

    @abstractmethod
    def find_references(self, doc: TextDocument, info: WordInfo, context: Any) -> List[Location]:
        """
        [THE RITE OF DISCOVERY]
        Scans for all occurrences of the symbol described in WordInfo.
        """
        pass