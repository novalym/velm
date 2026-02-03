# Path: core/lsp/base/types/code_lens.py
# --------------------------------------
from typing import Optional, Any
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import Range, Command, TextDocumentIdentifier

class CodeLens(LspModel):
    """
    [LSP 3.17 COMPLIANT]
    An interactive lens manifest in the UI.
    """
    model_config = ConfigDict(populate_by_name=True)

    range: Range
    command: Optional[Command] = None
    data: Optional[Any] = None  # Data used for resolving the command later

class CodeLensParams(LspModel):
    """The plea for lens revelation."""
    model_config = ConfigDict(populate_by_name=True)

    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")