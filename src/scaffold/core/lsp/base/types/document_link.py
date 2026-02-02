# Path: core/lsp/base/types/document_link.py
# ----------------------------------------------------
from __future__ import annotations
from typing import Optional, Any
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import Range, DocumentUri, TextDocumentIdentifier, WorkDoneProgressParams, PartialResultParams, Position


class DocumentLink(LspModel):
    """
    [THE WORMHOLE]
    A range in a text document that links to an internal or external resource.
    """
    model_config = ConfigDict(populate_by_name=True)

    range: Range = Field(..., description="The range this link applies to.")

    target: Optional[str] = Field(
        None,
        description="The uri this link points to. If missing, a resolve call is sent."
    )

    tooltip: Optional[str] = Field(
        None,
        description="The tooltip text when you hover over this link."
    )

    data: Optional[Any] = Field(
        None,
        description="A data holder that is preserved for the resolve request."
    )


class DocumentLinkParams(WorkDoneProgressParams, PartialResultParams):
    """
    [THE PLEA FOR LINKS]
    """
    model_config = ConfigDict(populate_by_name=True)
    text_document: TextDocumentIdentifier = Field(..., alias="textDocument")


class DocumentLinkOptions(LspModel):
    resolve_provider: Optional[bool] = Field(None, alias="resolveProvider")
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")



