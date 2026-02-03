# Path: core/lsp/base/types/completion.py
# ---------------------------------------

from __future__ import annotations
from enum import IntEnum
from typing import Optional, List, Union, Any, Dict
from pydantic import Field, ConfigDict, field_validator
from .base import LspModel
from .primitives import (
    TextEdit,
    Command,
    MarkupContent,
    TextDocumentIdentifier,
    Position,
    Range
)


# =================================================================================
# == I. THE ENUMS OF FORESIGHT                                                   ==
# =================================================================================

class CompletionItemKind(IntEnum):
    """
    [THE NATURE OF THE VISION]
    """
    Text = 1
    Method = 2
    Function = 3
    Constructor = 4
    Field = 5
    Variable = 6
    Class = 7
    Interface = 8
    Module = 9
    Property = 10
    Unit = 11
    Value = 12
    Enum = 13
    Keyword = 14
    Snippet = 15
    Color = 16
    File = 17
    Reference = 18
    Folder = 19
    EnumMember = 20
    Constant = 21
    Struct = 22
    Event = 23
    Operator = 24
    TypeParameter = 25


class CompletionItemTag(IntEnum):
    """
    [THE METADATA MARK]
    """
    Deprecated = 1


class InsertTextFormat(IntEnum):
    """
    [THE FORMAT OF INSERTION]
    """
    PlainText = 1
    Snippet = 2  # Allows $1, $0, ${1:placeholder}


class CompletionTriggerKind(IntEnum):
    """
    [THE CAUSE OF PROPHECY]
    """
    Invoked = 1
    TriggerCharacter = 2
    TriggerForIncompleteCompletions = 3


# =================================================================================
# == II. THE CONTEXTUAL SOUL                                                     ==
# =================================================================================

class CompletionContext(LspModel):
    """
    [THE MOMENT OF TRIGGER]
    Describes how the completion was triggered.

    [ASCENSION]: Now fortified with a Pre-Validator to handle client heresies
    (e.g. sending '0' or invalid enums).
    """
    model_config = ConfigDict(populate_by_name=True)

    trigger_kind: CompletionTriggerKind = Field(..., alias="triggerKind")
    trigger_character: Optional[str] = Field(None, alias="triggerCharacter")

    @field_validator('trigger_kind', mode='before')
    @classmethod
    def sanitize_trigger_kind(cls, v: Any) -> int:
        """
        [THE SANITIZER]
        Intercepts invalid trigger kinds (like 0) and transmutes them to Invoked (1).
        This prevents Pydantic from rejecting the entire request due to client-side drift.
        """
        try:
            val = int(v)
            # If value is within sacred bounds, accept it.
            if val in (1, 2, 3):
                return val
            # Otherwise, force 'Invoked'
            return 1
        except (ValueError, TypeError):
            # If garbage, force 'Invoked'
            return 1


class CompletionItemLabelDetails(LspModel):
    """
    [ASCENSION 1: LSP 3.17 DETAIL]
    Additional details for the label (e.g. parameter types).
    """
    detail: Optional[str] = Field(None, description="Appended to the label (e.g. signature).")
    description: Optional[str] = Field(None, description="Appended to the label (e.g. package).")


# =================================================================================
# == III. THE ATOM OF PROPHECY (ITEM)                                            ==
# =================================================================================

class CompletionItem(LspModel):
    """
    [THE PROPHECY]
    A single suggestion for the Architect.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Strict Aliasing:** `sort_text` <-> `sortText` mapping is enforced via Pydantic.
    2.  **Label Details:** Support for LSP 3.17 extended labels.
    3.  **Union Documentation:** Accepts `str` or `MarkupContent` (Markdown).
    4.  **Snippet Support:** `insert_text_format` defaults to PlainText but allows Snippets.
    5.  **Edit Unions:** `text_edit` supports `TextEdit` (and future `InsertReplaceEdit`).
    6.  **State Preservation:** `data` field holds arbitrary Gnosis for the `resolve` rite.
    7.  **Auto-Sorting:** `sort_text` dictates order in the UI.
    8.  **Filtering:** `filter_text` overrides fuzzy matching logic.
    9.  **Commit Characters:** Defines which keys (e.g. `.`) accept the suggestion.
    10. **Command Linkage:** Can trigger a `Command` (e.g. auto-import) upon acceptance.
    11. **Tags:** Supports `Deprecated` styling.
    12. **Preselection:** Can force this item to be the default choice.
    """
    model_config = ConfigDict(populate_by_name=True)

    label: str = Field(..., description="The label of this completion item.")

    label_details: Optional[CompletionItemLabelDetails] = Field(None, alias="labelDetails")

    kind: Optional[CompletionItemKind] = Field(None, description="The kind of this completion item.")

    tags: Optional[List[CompletionItemTag]] = None

    detail: Optional[str] = Field(None,
                                  description="A human-readable string with additional information about this item.")

    documentation: Optional[Union[str, MarkupContent]] = Field(None,
                                                               description="A human-readable string that represents a doc-comment.")

    deprecated: Optional[bool] = None

    preselect: Optional[bool] = None

    # [THE CRITICAL ALIASES]
    sort_text: Optional[str] = Field(None, alias="sortText")
    filter_text: Optional[str] = Field(None, alias="filterText")
    insert_text: Optional[str] = Field(None, alias="insertText")

    insert_text_format: Optional[InsertTextFormat] = Field(
        None,
        alias="insertTextFormat",
        description="The format of the insert text."
    )

    text_edit: Optional[Union[TextEdit, Any]] = Field(None, alias="textEdit")

    additional_text_edits: Optional[List[TextEdit]] = Field(None, alias="additionalTextEdits")

    commit_characters: Optional[List[str]] = Field(None, alias="commitCharacters")

    command: Optional[Command] = None

    data: Optional[Any] = Field(None,
                                description="A data entry field that is preserved on a completion item between a completion and a completion resolve request.")


# =================================================================================
# == IV. THE LIST & PARAMS                                                       ==
# =================================================================================

class CompletionList(LspModel):
    """
    [THE SCROLL OF FUTURES]
    A collection of CompletionItems.
    """
    is_incomplete: bool = Field(..., alias="isIncomplete")

    # [ASCENSION 10]: ITEM DEFAULTS (LSP 3.17)
    # Optimization to share data across all items
    item_defaults: Optional[Dict[str, Any]] = Field(None, alias="itemDefaults")

    items: List[CompletionItem]


class CompletionParams(LspModel):
    """
    [THE PLEA FOR FORESIGHT]
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    position: Position
    context: Optional[CompletionContext] = None


class CompletionOptions(LspModel):
    """
    [THE CAPABILITY OF PROPHECY]
    """
    model_config = ConfigDict(populate_by_name=True)

    trigger_characters: Optional[List[str]] = Field(None, alias="triggerCharacters")
    all_commit_characters: Optional[List[str]] = Field(None, alias="allCommitCharacters")
    resolve_provider: Optional[bool] = Field(None, alias="resolveProvider")

    # [ASCENSION 11]: WORK DONE SUPPORT
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")