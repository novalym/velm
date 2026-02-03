# Path: core/lsp/base/types/diagnostics.py
# ----------------------------------------

from enum import IntEnum
from typing import Optional, Union, List, Any, Literal
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import Range, Location, DocumentUri, TextDocumentIdentifier, WorkDoneProgressParams, \
    PartialResultParams


# =================================================================================
# == I. THE SCALES OF SEVERITY                                                   ==
# =================================================================================

class DiagnosticSeverity(IntEnum):
    """
    [THE JUDGMENT]
    The weight of the heresy.
    """
    Error = 1
    Warning = 2
    Information = 3
    Hint = 4


class DiagnosticTag(IntEnum):
    """
    [THE MARK]
    Metadata tags for rendering optimizations (e.g. fading out unused code).
    """
    Unnecessary = 1
    Deprecated = 2


# =================================================================================
# == II. THE EVIDENCE                                                            ==
# =================================================================================

class CodeDescription(LspModel):
    """
    [THE CITATION]
    A link to external documentation explaining the law.
    """
    href: str


class DiagnosticRelatedInformation(LspModel):
    """
    [THE CONTEXT]
    Secondary locations relevant to the diagnosis.
    """
    location: Location
    message: str


class Diagnostic(LspModel):
    """
    [THE HERESY]
    [LSP 3.17 COMPLIANT]
    A forensic report of a flaw in the code.
    """
    range: Range
    severity: Optional[DiagnosticSeverity] = None
    code: Optional[Union[int, str]] = None
    code_description: Optional[CodeDescription] = Field(None, alias="codeDescription")
    source: Optional[str] = Field("Gnostic Sentinel", description="The origin of the judgment.")
    message: str
    tags: Optional[List[DiagnosticTag]] = None
    related_information: Optional[List[DiagnosticRelatedInformation]] = Field(None, alias="relatedInformation")

    # [ASCENSION]: REDEMPTION PAYLOAD
    data: Optional[Any] = None


# =================================================================================
# == III. THE PROCLAMATION (PUSH MODEL - LEGACY)                                 ==
# =================================================================================

class PublishDiagnosticsParams(LspModel):
    """[THE VERDICT] Server pushes errors to client."""
    uri: DocumentUri
    version: Optional[int] = Field(None, description="The version of the document.")
    diagnostics: List[Diagnostic]


class DiagnosticOptions(LspModel):
    """[THE INQUISITOR'S SETTINGS]"""
    identifier: Optional[str] = None
    inter_file_dependencies: bool = Field(False, alias="interFileDependencies")
    workspace_diagnostics: bool = Field(False, alias="workspaceDiagnostics")
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")


# =================================================================================
# == IV. THE INQUEST (PULL MODEL - MODERNIY)                                     ==
# =================================================================================

class DocumentDiagnosticParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA FOR JUDGMENT]
    Client asks: "Are there heresies in this scripture?"
    """
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")
    identifier: Optional[str] = None
    previous_result_id: Optional[str] = Field(None, alias="previousResultId")


class FullDocumentDiagnosticReport(LspModel):
    """
    [THE FULL REPORT]
    Server says: "Yes, here is the list."
    """
    kind: Literal['full'] = 'full'
    result_id: Optional[str] = Field(None, alias="resultId")
    items: List[Diagnostic]


class UnchangedDocumentDiagnosticReport(LspModel):
    """
    [THE SILENCE]
    Server says: "Nothing has changed since resultId X."
    """
    kind: Literal['unchanged'] = 'unchanged'
    result_id: str = Field(..., alias="resultId")


# The Union Return Type
DocumentDiagnosticReport = Union[FullDocumentDiagnosticReport, UnchangedDocumentDiagnosticReport]