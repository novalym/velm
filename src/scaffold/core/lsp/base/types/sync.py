# Path: core/lsp/base/types/sync.py
# --------------------------------

from enum import IntEnum
from typing import Optional, List
from pydantic import Field
from .base import LspModel
from .primitives import DocumentUri, Range, TextDocumentIdentifier

class TextDocumentItem(LspModel):
    """A full scripture manifest for the didOpen rite."""
    uri: DocumentUri
    language_id: str = Field(..., alias="languageId")
    version: int
    text: str

class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """An identifier for a specific version of a scripture."""
    version: int

class OptionalVersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """An identifier for a possibly versioned scripture."""
    version: Optional[int] = None

class TextDocumentContentChangeEvent(LspModel):
    """[THE DELTA] A single splice operation in the didChange rite."""
    range: Optional[Range] = None
    range_length: Optional[int] = Field(None, alias="rangeLength")
    text: str

class DidOpenTextDocumentParams(LspModel):
    """The plea for the Rite of Genesis."""
    text_document: TextDocumentItem = Field(..., alias="textDocument")

class DidChangeTextDocumentParams(LspModel):
    """The plea for the Rite of Mutation."""
    text_document: VersionedTextDocumentIdentifier = Field(..., alias="textDocument")
    content_changes: List[TextDocumentContentChangeEvent] = Field(..., alias="contentChanges")

class TextDocumentSaveReason(IntEnum):
    """The Architect's intent behind the save."""
    Manual = 1
    AfterDelay = 2
    FocusOut = 3

class WillSaveTextDocumentParams(LspModel):
    """The plea before the Rite of Persistence."""
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    reason: TextDocumentSaveReason

class DidSaveTextDocumentParams(LspModel):
    """The plea for the Rite of Persistence."""
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    text: Optional[str] = Field(None, description="The full content of the file on save.")

class DidCloseTextDocumentParams(LspModel):
    """The plea for the Rite of Oblivion."""
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")