# Path: core/lsp/base/types/references.py
# ---------------------------------------
from __future__ import annotations
from typing import Optional, List, Union, Any
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import (
    TextDocumentIdentifier,
    Position,
    WorkDoneProgressOptions,
    WorkDoneProgressParams,
    PartialResultParams
)


# =================================================================================
# == I. THE CONTEXT OF THE ECHO                                                  ==
# =================================================================================

class ReferenceContext(LspModel):
    """
    [THE FILTER]
    Defines the scope of the resonance search.
    """
    model_config = ConfigDict(populate_by_name=True)

    include_declaration: bool = Field(
        ...,
        alias="includeDeclaration",
        description="If true, the original definition of the symbol is included in the echoes."
    )


# =================================================================================
# == II. THE PLEA FOR RESONANCE (REQUEST)                                        ==
# =================================================================================

class ReferenceParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA]
    Sent by the Client to find all references to the symbol at the cursor position.
    Inherits Progress tokens to support long-running, project-wide scans.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(
        ...,
        alias="textDocument",
        description="The scripture containing the symbol to be traced."
    )

    position: Position = Field(
        ...,
        description="The exact coordinates of the symbol."
    )

    context: ReferenceContext = Field(
        ...,
        description="Configuration for the search filter."
    )


# =================================================================================
# == III. THE CAPABILITY (OPTIONS)                                               ==
# =================================================================================

class ReferenceOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY]
    Server capabilities regarding 'Find References'.
    """
    pass

# =================================================================================
# == NOTE ON RETURN TYPES                                                        ==
# =================================================================================
# The return type for `textDocument/references` is `List[Location]`.
# The atomic `Location` vessel is defined in `core.lsp.base.types.primitives`
# to ensure it remains the immutable standard for all spatial pointers.