# Path: core/lsp/base/features/selection_range/models.py
# ------------------------------------------------------
from __future__ import annotations
from typing import Optional, List
from pydantic import Field, ConfigDict
from ...types.base import LspModel
from ...types.primitives import Range, Position, TextDocumentIdentifier, WorkDoneProgressParams, PartialResultParams

# =================================================================================
# == THE ATOM OF SCOPE                                                           ==
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

class SelectionRangeOptions(LspModel):
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")