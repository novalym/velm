# Path: core/lsp/base/types/call_hierarchy.py
# -----------------------------------------------------
from __future__ import annotations
from typing import List, Optional, Any
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import (
    Range, Position, DocumentUri,
    TextDocumentIdentifier, WorkDoneProgressParams, PartialResultParams
)
from .symbols import SymbolKind, SymbolTag

class CallHierarchyItem(LspModel):
    """
    [THE NODE OF CAUSALITY]
    Represents a function, method, or symbol in the hierarchy.
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
    # A data holder that is passed back in incoming/outgoing requests.
    data: Optional[Any] = None


class CallHierarchyIncomingCall(LspModel):
    """[THE CALLER] A call pointing TO the subject."""
    model_config = ConfigDict(populate_by_name=True)

    from_: CallHierarchyItem = Field(..., alias="from")
    from_ranges: List[Range] = Field(..., alias="fromRanges", description="The ranges at which the calls appear.")


class CallHierarchyOutgoingCall(LspModel):
    """[THE CALLEE] A call pointing FROM the subject."""
    model_config = ConfigDict(populate_by_name=True)

    to: CallHierarchyItem = Field(..., alias="to")
    from_ranges: List[Range] = Field(..., alias="fromRanges", description="The range at which this item is called.")


# --- PARAMS ---

class CallHierarchyPrepareParams(WorkDoneProgressParams):
    model_config = ConfigDict(populate_by_name=True)
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position


class CallHierarchyIncomingCallsParams(WorkDoneProgressParams, PartialResultParams):
    model_config = ConfigDict(populate_by_name=True)
    item: CallHierarchyItem


class CallHierarchyOutgoingCallsParams(WorkDoneProgressParams, PartialResultParams):
    model_config = ConfigDict(populate_by_name=True)
    item: CallHierarchyItem


class CallHierarchyOptions(WorkDoneProgressParams):
    pass