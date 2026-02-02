# Path: core/lsp/base/features/symbols/contracts.py
# -------------------------------------------------

from abc import ABC, abstractmethod
from typing import Optional, Any
from ...types import DocumentSymbol, SymbolKind, Range, Position


class SymbolProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF THE MAP (INTERFACE)                                     ==
    =============================================================================
    Every language-specific scanner must sign this contract.

    [CAPABILITIES]:
    1. EXTRACT: The abstract rite of identifying a symbol in a line of text.
    2. FORGE: The concrete utility for constructing valid LSP DocumentSymbols.
    """

    def __init__(self, server: Any):
        self.server = server

    @abstractmethod
    def extract(self, line_num: int, raw_line: str, stripped: str) -> Optional[DocumentSymbol]:
        """
        [THE RITE OF EXTRACTION]
        Gazes at a line of scripture and identifies if a symbol is born there.
        Returns None if the line is mundane.
        """
        pass

    def forge_vessel(self,
                     name: str,
                     detail: str,
                     kind: SymbolKind,
                     line: int,
                     start_col: int,
                     length: int) -> DocumentSymbol:
        """
        [HELPER]: Forges a standard DocumentSymbol with safe geometric ranges.
        Ensures strict compliance with the Pydantic V2 schema defined in Primitives.
        """
        # Range of the name for highlighting
        selection_range = Range(
            start=Position(line=line, character=start_col),
            end=Position(line=line, character=start_col + length)
        )

        # Full range of the line definition
        # We extend arbitrary length to the right to capture arguments/comments
        full_range = Range(
            start=Position(line=line, character=0),
            end=Position(line=line, character=start_col + length + 50)
        )

        return DocumentSymbol(
            name=name,
            detail=detail,
            kind=kind,
            range=full_range,
            selectionRange=selection_range,  # Maps to 'selectionRange' via alias
            children=[]  # Must be initialized empty
        )