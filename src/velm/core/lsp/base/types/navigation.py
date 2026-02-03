# Path: core/lsp/types/navigation.py
# ----------------------------------

from enum import Enum, IntEnum
from typing import Optional, Union, List, Any
from pydantic import Field
from .base import LspModel
from .primitives import Range, TextDocumentIdentifier, Position

# --- DEFINITION, REFERENCES, RENAME, HIGHLIGHT ---
class SignatureHelpOptions(LspModel):
    """
    [THE ORACLE OF ARGS]
    LIF: 100x | ROLE: INVOCATION_SENTINEL

    Defines the server's capability to provide help during function or macro invocation.
    It tells the client which characters trigger the revelation of parameter gnosis.
    """

    trigger_characters: Optional[List[str]] = Field(
        None,
        alias="triggerCharacters",
        description="List of characters that trigger signature help automatically (e.g., '(', ',')."
    )

    retrigger_characters: Optional[List[str]] = Field(
        None,
        alias="retriggerCharacters",
        description="List of characters that re-trigger signature help while it is already active."
    )

    work_done_progress: Optional[bool] = Field(
        None,
        alias="workDoneProgress",
        description="Whether the server supports reporting progress for signature help."
    )

    @classmethod
    def default_gnostic(cls) -> "SignatureHelpOptions":
        """Forges a default instance tuned for Scaffold/Symphony."""
        return cls(
            triggerCharacters=["(", ",", "|"],
            retriggerCharacters=[")"],
            workDoneProgress=True
        )
class DefinitionOptions(LspModel):
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")

class DefinitionParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position

class ReferenceContext(LspModel):
    include_declaration: bool = Field(..., alias="includeDeclaration")

class ReferenceParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position
    context: ReferenceContext

class ReferenceOptions(LspModel):
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")

class RenameOptions(LspModel):
    prepare_provider: Optional[bool] = Field(None, alias="prepareProvider")
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")

class RenameParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position
    new_name: str = Field(..., alias="newName")

class PrepareRenameParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position

class DocumentHighlightKind(IntEnum):
    Text = 1
    Read = 2
    Write = 3

class DocumentHighlight(LspModel):
    range: Range
    kind: Optional[DocumentHighlightKind] = None

class DocumentHighlightParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position

class DocumentHighlightOptions(LspModel):
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")

# --- HOVER ---

class Hover(LspModel):
    contents: Any # MarkupContent or str
    range: Optional[Range] = None

class HoverParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position

class HoverOptions(LspModel):
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")