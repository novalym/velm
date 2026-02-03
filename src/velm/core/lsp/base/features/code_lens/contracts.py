# Path: core/lsp/features/code_lens/contracts.py
# -----------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from .models import CodeLens
from ...document import TextDocument

class CodeLensProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF ACTION (INTERFACE)                                      ==
    =============================================================================
    Every language-specific lens-maker must sign this contract.
    It defines how to detect lens anchors and how to resolve their final intent.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the lens source."""
        pass

    @property
    def priority(self) -> int:
        """Determines the order of vertical manifestation."""
        return 50

    @abstractmethod
    def provide_lenses(self, doc: TextDocument) -> List[CodeLens]:
        """
        [THE RITE OF DETECTION]
        Scans the scripture and returns a list of CodeLenses with 'data' payloads.
        """
        pass

    @abstractmethod
    def resolve_lens(self, lens: CodeLens, doc: TextDocument) -> CodeLens:
        """
        [THE RITE OF RESOLUTION]
        Hydrates the 'command' field based on the 'data' payload.
        """
        return lens