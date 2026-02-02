# Path: core/lsp/features/inlay_hint/contracts.py
# -----------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from .models import InlayHint
from ...document import TextDocument
from ...types.primitives import Range

class InlayHintProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF REVELATION (INTERFACE)                                  ==
    =============================================================================
    Every language-specific ghost-writer must sign this contract.
    It defines how to project annotations within a specific spacetime range.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the hint source."""
        pass

    @property
    def priority(self) -> int:
        """Determines the order of manifestation (0-100)."""
        return 50

    @abstractmethod
    def provide_hints(self, doc: TextDocument, range: Range) -> List[InlayHint]:
        """
        [THE RITE OF PROJECTION]
        Scans the provided range and returns a list of spectral InlayHints.
        """
        pass