# Path: core/lsp/types/symbols.py
# -------------------------------

from enum import IntEnum
from typing import List, Optional, Any
from pydantic import Field
from .base import LspModel
from .primitives import Range, Location, TextDocumentIdentifier

class SymbolKind(IntEnum):
    File = 1; Module = 2; Namespace = 3; Package = 4; Class = 5; Method = 6; Property = 7;
    Field = 8; Constructor = 9; Enum = 10; Interface = 11; Function = 12; Variable = 13;
    Constant = 14; String = 15; Number = 16; Boolean = 17; Array = 18; Object = 19; Key = 20;
    Null = 21; EnumMember = 22; Struct = 23; Event = 24; Operator = 25; TypeParameter = 26

class SymbolTag(IntEnum):
    Deprecated = 1

class DocumentSymbol(LspModel):
    name: str
    detail: Optional[str] = None
    kind: SymbolKind
    tags: Optional[List[SymbolTag]] = None
    deprecated: Optional[bool] = None
    range: Range
    selection_range: Range = Field(..., alias="selectionRange")
    children: Optional[List['DocumentSymbol']] = None

DocumentSymbol.model_rebuild()

class DocumentSymbolParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")

class SymbolInformation(LspModel):
    name: str
    kind: SymbolKind
    tags: Optional[List[SymbolTag]] = None
    deprecated: Optional[bool] = None
    location: Location
    container_name: Optional[str] = Field(None, alias="containerName")

class WorkspaceSymbolParams(LspModel):
    query: str

class DocumentSymbolOptions(LspModel):
    label: Optional[str] = None
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")