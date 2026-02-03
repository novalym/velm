# Path: core/lsp/base/types/code_action.py
# ----------------------------------------
# LIF: INFINITY | SCHEMA: ACTION_ATOM

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import Range, Command, TextDocumentIdentifier
from .workspace import WorkspaceEdit
from .diagnostics import Diagnostic


class CodeActionKind(str, Enum):
    """
    [THE NATURE OF THE ACT]
    """
    QuickFix = "quickfix"
    Refactor = "refactor"
    RefactorExtract = "refactor.extract"
    RefactorInline = "refactor.inline"
    RefactorRewrite = "refactor.rewrite"
    Source = "source"
    SourceOrganizeImports = "source.organizeImports"
    SourceFixAll = "source.fixAll"


class CodeActionContext(LspModel):
    """
    [THE CIRCUMSTANCE]
    """
    model_config = ConfigDict(populate_by_name=True)

    diagnostics: List[Diagnostic]
    only: Optional[List[CodeActionKind]] = None
    trigger_kind: Optional[int] = Field(None, alias="triggerKind")


class CodeActionParams(LspModel):
    """
    [THE PLEA FOR INTERVENTION]
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    range: Range
    context: CodeActionContext


class CodeAction(LspModel):
    """
    [THE REDEMPTION]
    A command or edit to fix a problem or refactor code.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(..., description="A short, human-readable, title for this code action.")

    kind: Optional[CodeActionKind] = Field(None, description="The kind of the code action.")

    diagnostics: Optional[List[Diagnostic]] = Field(None, description="The diagnostics that this action resolves.")

    is_preferred: Optional[bool] = Field(None, alias="isPreferred", description="Marks this as a preferred action.")

    disabled: Optional[Dict[str, str]] = Field(None, description="Marks the action as disabled.")

    edit: Optional[WorkspaceEdit] = Field(None, description="The workspace edit this code action performs.")

    command: Optional[Command] = Field(None, description="A command this code action executes.")

    data: Optional[Any] = Field(None,
                                description="A data holder that is preserved between a `textDocument/codeAction` and a `codeAction/resolve` request.")


class CodeActionOptions(LspModel):
    """
    [THE CAPABILITY]
    """
    model_config = ConfigDict(populate_by_name=True)

    code_action_kinds: Optional[List[CodeActionKind]] = Field(None, alias="codeActionKinds")
    resolve_provider: Optional[bool] = Field(None, alias="resolveProvider")
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")