# Path: core/lsp/base/features/selection_range/contracts.py
# ---------------------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Any
from .models import SelectionRange
from ...document import TextDocument
from ...types.primitives import Position

class SelectionRangeProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF EXPANSION (INTERFACE)                                   ==
    =============================================================================
    Every geometric expander must sign this contract.
    It defines how to grow a selection from a singularity (cursor) to the cosmos.
    """

    def __init__(self, server: Any = None):
        self.server = server

    @property
    def name(self) -> str:
        """The identifier of the expansion strategy."""
        return self.__class__.__name__

    @abstractmethod
    def provide_selection_ranges(self, doc: TextDocument, positions: List[Position]) -> List[SelectionRange]:
        """
        [THE RITE OF GROWTH]
        Scans the scripture and returns a hierarchy of ranges for each position.
        """
        pass