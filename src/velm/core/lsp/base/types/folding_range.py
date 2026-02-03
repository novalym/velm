# Path: core/lsp/base/types/folding_range.py
# ------------------------------------------
from __future__ import annotations
from enum import Enum
from typing import Optional, List, Union
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import (
    TextDocumentIdentifier,
    WorkDoneProgressOptions,
    WorkDoneProgressParams,
    PartialResultParams
)


# =================================================================================
# == I. THE KIND OF COLLAPSE                                                     ==
# =================================================================================

class FoldingRangeKind(str, Enum):
    """
    [THE NATURE OF THE FOLD]
    Categorizes the folded region for semantic styling.
    """
    Comment = "comment"  # A block of silence.
    Imports = "imports"  # A block of dependencies.
    Region = "region"  # A manually defined sanctum.


# =================================================================================
# == II. THE ATOM OF COMPRESSION                                                 ==
# =================================================================================

class FoldingRange(LspModel):
    """
    [THE FOLD]
    Defines a region of text that can be compressed into a singularity.

    The range includes the start line and the end line.
    If characters are omitted, it defaults to the entire line.
    """
    model_config = ConfigDict(populate_by_name=True)

    start_line: int = Field(..., alias="startLine", description="The zero-based start line of the range to fold.")

    start_character: Optional[int] = Field(
        None,
        alias="startCharacter",
        description="The zero-based character offset where the fold starts. If missing, it defaults to the length of the start line."
    )

    end_line: int = Field(..., alias="endLine", description="The zero-based end line of the range to fold.")

    end_character: Optional[int] = Field(
        None,
        alias="endCharacter",
        description="The zero-based character offset where the fold ends. If missing, it defaults to the length of the end line."
    )

    kind: Optional[FoldingRangeKind] = Field(None, description="The semantic category of the fold.")

    collapsed_text: Optional[str] = Field(
        None,
        alias="collapsedText",
        description="The text to display when the range is collapsed. (LSP 3.17+)"
    )


# =================================================================================
# == III. THE PLEA (REQUEST)                                                     ==
# =================================================================================

class FoldingRangeParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA FOR COMPRESSION]
    Sent by the Client to request all foldable regions in a document.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument",
                                                  description="The scripture to be analyzed.")


# =================================================================================
# == IV. THE CAPABILITY (OPTIONS)                                                ==
# =================================================================================

class FoldingRangeOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY OF FOLDING]
    Server capabilities regarding 'Folding Range'.
    """
    pass