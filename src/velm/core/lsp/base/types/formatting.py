# Path: core/lsp/types/formatting.py
# ----------------------------------
from typing import Optional, List, Any, Dict
from pydantic import Field
from .base import LspModel
from .primitives import TextDocumentIdentifier, TextEdit

class FormattingOptions(LspModel):
    tab_size: int = Field(..., alias="tabSize")
    insert_spaces: bool = Field(..., alias="insertSpaces")
    trim_trailing_whitespace: Optional[bool] = Field(None, alias="trimTrailingWhitespace")
    insert_final_newline: Optional[bool] = Field(None, alias="insertFinalNewline")
    trim_final_newlines: Optional[bool] = Field(None, alias="trimFinalNewlines")

class DocumentFormattingParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    options: FormattingOptions

class DocumentRangeFormattingParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    range: Any # Range model
    options: FormattingOptions