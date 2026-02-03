# Path: core/lsp/base/types/document_highlight.py
# -----------------------------------------------
from __future__ import annotations
from enum import IntEnum
from typing import Optional, List, Union
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import (
    Range,
    Position,
    TextDocumentIdentifier,
    WorkDoneProgressOptions,
    WorkDoneProgressParams,
    PartialResultParams
)

# =================================================================================
# == I. THE KIND OF ILLUMINATION                                                 ==
# =================================================================================

class DocumentHighlightKind(IntEnum):
    """
    [THE COLOR OF CONTEXT]
    A document highlight kind.
    """
    Text = 1  # A textual occurrence.
    Read = 2  # Read-access of a symbol.
    Write = 3 # Write-access of a symbol.


# =================================================================================
# == II. THE ATOM OF HIGHLIGHT                                                   ==
# =================================================================================

class DocumentHighlight(LspModel):
    """
    [THE GLOWING MARK]
    A range inside a text document which deserves special attention.
    """
    range: Range = Field(..., description="The range this highlight applies to.")
    kind: Optional[DocumentHighlightKind] = Field(None, description="The highlight kind, default is Text.")


# =================================================================================
# == III. THE PLEA (REQUEST)                                                     ==
# =================================================================================

class DocumentHighlightParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA FOR ILLUMINATION]
    Sent by the Client to resolve document highlights for a given text document position.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument", description="The scripture to be illuminated.")
    position: Position = Field(..., description="The cursor position of the symbol to highlight.")


# =================================================================================
# == IV. THE CAPABILITY (OPTIONS)                                                ==
# =================================================================================

class DocumentHighlightOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY OF SIGHT]
    Server capabilities regarding 'Document Highlight'.
    """
    pass