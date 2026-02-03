# Path: core/lsp/base/types/type_hierarchy.py
# -----------------------------------------------------
from __future__ import annotations
from typing import List, Optional, Any
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import (
    Range, Position, DocumentUri,
    TextDocumentIdentifier, WorkDoneProgressParams, PartialResultParams, WorkDoneProgressOptions
)
from .symbols import SymbolKind, SymbolTag



# =================================================================================
# == I. THE ATOM OF INHERITANCE                                                  ==
# =================================================================================

class TypeHierarchyItem(LspModel):
    """
    [THE NODE OF LINEAGE]
    Represents a type (Class, Interface, Trait) in the hierarchy.
    """
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., description="The name of this item.")
    kind: SymbolKind = Field(..., description="The kind of this item.")
    tags: Optional[List[SymbolTag]] = None
    detail: Optional[str] = Field(None, description="More detail for this item, e.g. the signature.")
    uri: DocumentUri = Field(..., description="The resource identifier of this item.")
    range: Range = Field(..., description="The range enclosing this symbol.")
    selection_range: Range = Field(..., alias="selectionRange",
                                   description="The range that should be selected and revealed.")

    # [ASCENSION]: STATE PRESERVATION
    # A data holder that is passed back in super/sub requests.
    data: Optional[Any] = None


# =================================================================================
# == II. THE PLEAS (REQUESTS)                                                    ==
# =================================================================================

class TypeHierarchyPrepareParams(WorkDoneProgressParams):
    model_config = ConfigDict(populate_by_name=True)
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position


class TypeHierarchySupertypesParams(WorkDoneProgressParams, PartialResultParams):
    model_config = ConfigDict(populate_by_name=True)
    item: TypeHierarchyItem


class TypeHierarchySubtypesParams(WorkDoneProgressParams, PartialResultParams):
    model_config = ConfigDict(populate_by_name=True)
    item: TypeHierarchyItem


# =================================================================================
# == III. THE CAPABILITY (OPTIONS)                                               ==
# =================================================================================

class TypeHierarchyOptions(WorkDoneProgressOptions):
    pass