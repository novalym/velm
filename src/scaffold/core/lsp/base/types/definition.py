# Path: core/lsp/base/types/definition.py
# ---------------------------------------
from __future__ import annotations
from typing import Optional, Union, List
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
# == I. THE RITE OF DEFINITION (GO TO SOURCE)                                    ==
# =================================================================================

class DefinitionOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY OF ORIGIN]
    Server capabilities regarding 'Go to Definition'.
    """
    pass

class DefinitionParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA FOR GENESIS]
    Sent by the client when the Architect demands to know the origin of a symbol.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument", description="The scripture containing the reference.")
    position: Position = Field(..., description="The exact coordinates of the cursor.")


# =================================================================================
# == II. THE RITE OF TYPE DEFINITION (GO TO SCHEMA)                              ==
# =================================================================================

class TypeDefinitionOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY OF FORM]
    Server capabilities regarding 'Go to Type Definition'.
    """
    pass

class TypeDefinitionParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA FOR STRUCTURE]
    Sent when the Architect seeks the interface or class definition of a variable.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position


# =================================================================================
# == III. THE RITE OF IMPLEMENTATION (GO TO REALITY)                             ==
# =================================================================================

class ImplementationOptions(WorkDoneProgressOptions):
    """
    [THE CAPABILITY OF ACTION]
    Server capabilities regarding 'Go to Implementation'.
    """
    pass

class ImplementationParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA FOR SUBSTANCE]
    Sent when the Architect seeks the concrete manifestation of an abstract interface.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position

# =================================================================================
# == NOTE ON RETURN TYPES                                                        ==
# =================================================================================
# The return type for all the above requests is typically:
# Location | List[Location] | List[LocationLink] | None
#
# These atomic return vessels (`Location`, `LocationLink`) are defined in
# `core.lsp.base.types.primitives` to prevent circular dependencies
# and ensure they remain the immutable bedrock of the protocol.