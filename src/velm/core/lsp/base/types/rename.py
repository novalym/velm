# Path: core/lsp/base/types/rename.py
# -----------------------------------
from __future__ import annotations
from typing import Optional
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import (
    TextDocumentIdentifier,
    Position,
    WorkDoneProgressOptions,
    WorkDoneProgressParams
)

# =================================================================================
# == I. THE CAPABILITY (OPTIONS)                                                 ==
# =================================================================================

class RenameOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY OF TRANSMUTATION]
    Server capabilities regarding 'Rename'.
    """
    prepare_provider: Optional[bool] = Field(
        None,
        alias="prepareProvider",
        description="Renames can be checked for validity before execution."
    )


# =================================================================================
# == II. THE PREPARATION (PRE-FLIGHT)                                            ==
# =================================================================================

class PrepareRenameParams(LspModel):
    """
    [THE PLEA FOR PERMISSION]
    Sent by the Client to test the validity of a rename location.
    The result is a Range (if valid) or null (if invalid).
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument", description="The scripture containing the symbol.")
    position: Position = Field(..., description="The cursor position of the symbol to be tested.")


# =================================================================================
# == III. THE EXECUTION (REQUEST)                                                ==
# =================================================================================

class RenameParams(WorkDoneProgressParams):
    """
    [THE PLEA FOR CHANGE]
    The command to rewrite the name of a symbol across the entire workspace.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument", description="The scripture containing the symbol.")
    position: Position = Field(..., description="The cursor position of the symbol.")
    new_name: str = Field(..., alias="newName", description="The new identity for the symbol.")


