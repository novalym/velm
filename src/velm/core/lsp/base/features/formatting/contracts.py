# Path: core/lsp/features/formatting/contracts.py
# ---------------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from .models import TextEdit, FormattingOptions
from ...document import TextDocument
from ...types.primitives import Range

class FormattingProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF PURITY (INTERFACE)                                      ==
    =============================================================================
    Every language-specific purifier must sign this contract.
    It defines how to calculate the delta required for geometric perfection.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the formatting source."""
        pass

    @property
    def priority(self) -> int:
        """Determines the order of execution (0-100)."""
        return 50

    @abstractmethod
    def format_document(self, doc: TextDocument, options: FormattingOptions) -> List[TextEdit]:
        """
        [THE RITE OF FULL TRANSMUTATION]
        Calculates edits for the entire file.
        """
        pass

    @abstractmethod
    def format_range(self, doc: TextDocument, range: Range, options: FormattingOptions) -> List[TextEdit]:
        """
        [THE RITE OF FOCUSED TRANSMUTATION]
        Calculates edits for a specific range.
        """
        pass