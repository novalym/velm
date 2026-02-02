# Path: core/lsp/types/semantic_tokens.py
# ---------------------------------------

from typing import List, Optional, Union, Dict, Any
from pydantic import Field
from .base import LspModel
from .primitives import TextDocumentIdentifier

class SemanticTokensLegend(LspModel):
    token_types: List[str] = Field(..., alias="tokenTypes")
    token_modifiers: List[str] = Field(..., alias="tokenModifiers")

class SemanticTokens(LspModel):
    result_id: Optional[str] = Field(None, alias="resultId")
    data: List[int]

class SemanticTokensPartialResult(LspModel):
    data: List[int]

class SemanticTokensEdit(LspModel):
    start: int
    delete_count: int = Field(..., alias="deleteCount")
    data: Optional[List[int]] = None

class SemanticTokensDelta(LspModel):
    result_id: Optional[str] = Field(None, alias="resultId")
    edits: List[SemanticTokensEdit]

class SemanticTokensParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")

class SemanticTokensDeltaParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    previous_result_id: str = Field(..., alias="previousResultId")

class SemanticTokensRangeParams(LspModel):
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    range: Any # Type Range, avoiding circular import

class SemanticTokensOptions(LspModel):
    legend: SemanticTokensLegend
    range: Optional[Union[bool, Dict[str, Any]]] = None
    full: Optional[Union[bool, Dict[str, Any]]] = None
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")