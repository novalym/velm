# Path: core/lsp/base/features/code_action/models.py
# --------------------------------------------------

from ...types import (
    CodeAction,
    CodeActionKind,
    CodeActionParams,
    CodeActionContext,
    CodeActionOptions,
    WorkspaceEdit,
    Diagnostic,
    TextEdit, # [THE CURE]: The Missing Link restored
    Range,
    Command,
    TextDocumentIdentifier
)