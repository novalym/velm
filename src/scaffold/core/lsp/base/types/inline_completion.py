# Path: core/lsp/base/types/inline_completion.py
# ----------------------------------------------

from typing import Optional, Union, List, Any
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import (
    TextDocumentIdentifier,
    Position,
    Range,
    Command,
    MarkupContent,
    WorkDoneProgressParams
)

# =================================================================================
# == I. THE PROPOSAL (BETA SPEC)                                                 ==
# =================================================================================

class InlineCompletionTriggerKind(int):
    Invoked = 0
    Automatic = 1

class InlineCompletionContext(LspModel):
    """
    [THE SITUATION]
    Describes why the ghost text was summoned.
    """
    trigger_kind: InlineCompletionTriggerKind = Field(..., alias="triggerKind")
    selected_completion_info: Optional[Any] = Field(None, alias="selectedCompletionInfo")

class InlineCompletionParams(WorkDoneProgressParams):
    """
    [THE PLEA FOR FORESIGHT]
    Sent by the client to request ghost text at the cursor.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position
    context: InlineCompletionContext

class InlineCompletionItem(LspModel):
    """
    [THE GHOST TEXT]
    A single predictive branch of reality.
    """
    insert_text: str = Field(..., alias="insertText")
    filter_text: Optional[str] = Field(None, alias="filterText")
    range: Optional[Range] = None
    command: Optional[Command] = None

class InlineCompletionList(LspModel):
    """
    [THE PROPHECY]
    A collection of potential futures.
    """
    items: List[InlineCompletionItem]

class InlineCompletionOptions(LspModel):
    """
    [THE CAPABILITY]
    Server advertising its ability to prophesy.
    """
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")