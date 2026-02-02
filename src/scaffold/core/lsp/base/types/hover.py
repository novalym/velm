# Path: core/lsp/base/types/hover.py
# ----------------------------------
from __future__ import annotations
from typing import Union, List, Any, Optional, Dict
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import (
    Range,
    Position,
    TextDocumentIdentifier,
    MarkupContent,
    MarkupKind,
    WorkDoneProgressOptions,
    WorkDoneProgressParams
)

# =================================================================================
# == I. THE LEGACY ARTIFACTS (COMPATIBILITY LAYER)                               ==
# =================================================================================

class MarkedString(LspModel):
    """
    [DEPRECATED BUT IMMORTAL]
    A legacy vessel for code-blocks. Kept alive for ancient clients.
    """
    language: str
    value: str

# The Raw Matter of Knowledge
# Can be a string, a MarkedString object, a MarkupContent object, or a list of any.
HoverContent = Union[MarkupContent, str, MarkedString, List[Union[str, MarkedString]]]


# =================================================================================
# == II. THE ATOM OF KNOWLEDGE (HOVER)                                           ==
# =================================================================================

class Hover(LspModel):
    """
    [LSP 3.17 COMPLIANT]
    The manifestation of wisdom that appears when the Architect gazes upon a symbol.
    """
    model_config = ConfigDict(populate_by_name=True)

    # Contents can be a single string, a MarkedString (deprecated), a MarkupContent, or a list of any.
    # We use a broad Union to ensure we never crash on complex Markdown structures.
    contents: HoverContent = Field(
        ...,
        description="The hover's content, typically Markdown or Plaintext."
    )

    range: Optional[Range] = Field(
        None,
        description="The range inside the text document that is used to visualize the hover, e.g. by changing the background color."
    )

    # --- FACTORY RITES ---

    @classmethod
    def from_markdown(cls, text: str, range: Optional[Range] = None) -> 'Hover':
        """
        [RITE]: FORGE_MARKDOWN
        Instantly creates a Markdown-based Hover.
        """
        return cls(
            contents=MarkupContent(kind=MarkupKind.Markdown, value=text),
            range=range
        )

    @classmethod
    def from_text(cls, text: str, range: Optional[Range] = None) -> 'Hover':
        """
        [RITE]: FORGE_PLAINTEXT
        Instantly creates a Plaintext-based Hover.
        """
        return cls(
            contents=MarkupContent(kind=MarkupKind.PlainText, value=text),
            range=range
        )


# =================================================================================
# == III. THE PLEA (REQUEST)                                                     ==
# =================================================================================

class HoverParams(WorkDoneProgressParams):
    """
    [THE PLEA FOR WISDOM]
    Sent by the Client to request documentation for the symbol at a given position.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument",
                                                  description="The scripture containing the symbol.")
    position: Position = Field(..., description="The cursor position.")


# =================================================================================
# == IV. THE CAPABILITY (OPTIONS)                                                ==
# =================================================================================

class HoverOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY OF SIGHT]
    Server capabilities regarding 'Hover'.
    """
    pass