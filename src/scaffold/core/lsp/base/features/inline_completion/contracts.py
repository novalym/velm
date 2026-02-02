# Path: core/lsp/base/features/inline_completion/contracts.py
# -----------------------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Any
from .models import InlineCompletionItem, InlineCompletionParams

class InlineCompletionProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF FORESIGHT (INTERFACE)                                   ==
    =============================================================================
    Every prophet (AI, Heuristic, Snippet) must sign this contract.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the prophet."""
        pass

    @property
    def priority(self) -> int:
        """Determines the order of prophecy (0-100)."""
        return 50

    @abstractmethod
    def prophesy(self, params: InlineCompletionParams) -> List[InlineCompletionItem]:
        """
        [THE RITE OF PREDICTION]
        Returns a list of potential futures.
        """
        pass