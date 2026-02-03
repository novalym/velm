# Path: core/lsp/base/types/selection_range.py
# --------------------------------------------
from __future__ import annotations
from typing import Optional, List
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
# == I. THE ATOM OF SCOPE                                                        ==
# =================================================================================

class SelectionRange(LspModel):
    """
    [THE RECURSIVE ENCLOSURE]
    Represents a hierarchy of selection ranges.
    Each range wraps its child, allowing the Editor to 'expand selection' outward.
    """
    model_config = ConfigDict(populate_by_name=True)

    range: Range = Field(..., description="The range of this selection.")

    parent: Optional['SelectionRange'] = Field(
        None,
        description="The parent selection range containing this range."
    )


# Enable recursive type definition for Pydantic
SelectionRange.model_rebuild()


# =================================================================================
# == II. THE PLEA (REQUEST)                                                      ==
# =================================================================================

class SelectionRangeParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA FOR EXPANSION]
    Sent by the Client to calculate the selection hierarchy at specific positions.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(
        ...,
        alias="textDocument",
        description="The scripture to be analyzed."
    )

    positions: List[Position] = Field(
        ...,
        description="The cursor positions for which to compute selection ranges."
    )


# =================================================================================
# == III. THE CAPABILITY (OPTIONS)                                               ==
# =================================================================================

class SelectionRangeOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY OF SCOPE]
    Server capabilities regarding 'Smart Select'.
    """
    pass