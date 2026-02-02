# Path: core/lsp/types/inlay_hint.py
# ----------------------------------
from enum import IntEnum
from typing import List, Optional, Union, Any
from pydantic import Field
from .base import LspModel
from .primitives import Position, Range, TextDocumentIdentifier, MarkupContent, Command

class InlayHintKind(IntEnum):
    Type = 1
    Parameter = 2

class InlayHintLabelPart(LspModel):
    value: str
    tooltip: Optional[Union[str, MarkupContent]] = None
    location: Optional[Any] = None # Location
    command: Optional[Command] = None

class InlayHint(LspModel):
    position: Position
    label: Union[str, List[InlayHintLabelPart]]
    kind: Optional[InlayHintKind] = None
    text_edits: Optional[List[Any]] = Field(None, alias="textEdits") # TextEdit[]
    tooltip: Optional[Union[str, MarkupContent]] = None
    padding_left: Optional[bool] = Field(None, alias="paddingLeft")
    padding_right: Optional[bool] = Field(None, alias="paddingRight")
    data: Optional[Any] = None

class InlayHintParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    range: Range