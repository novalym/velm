# Path: core/lsp/base/features/folding_range/contracts.py
# -------------------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Any
from .models import FoldingRange
from ...document import TextDocument

class FoldingRangeProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF COMPRESSION (INTERFACE)                                 ==
    =============================================================================
    Every spatial compressor must sign this contract.
    It defines how to identify collapsible regions within a document.
    """

    def __init__(self, server: Any = None):
        self.server = server

    @property
    def name(self) -> str:
        """The identifier of the folding strategy (e.g. 'IndentationStrategy')."""
        return self.__class__.__name__

    @abstractmethod
    def provide_folding_ranges(self, doc: TextDocument) -> List[FoldingRange]:
        """
        [THE RITE OF COLLAPSE]
        Scans the scripture and returns a list of FoldingRanges.
        """
        pass