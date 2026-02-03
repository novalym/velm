# Path: core/lsp/base/features/hover/models.py
# --------------------------------------------
from ...types import (
    Hover,
    HoverParams,
    HoverOptions,
    MarkupContent,
    Range,
    Position,
    TextDocumentIdentifier
)

# [ASCENSION]: ALIASING FOR BACKWARD COMPATIBILITY
# The Engine expects 'HoverResult', which is synonymous with the LSP 'Hover' object.
HoverResult = Hover

__all__ = [
    "Hover",
    "HoverResult", # <--- The Missing Link Restored
    "HoverParams",
    "HoverOptions",
    "MarkupContent"
]