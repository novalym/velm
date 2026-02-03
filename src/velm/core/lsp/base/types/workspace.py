# Path: core/lsp/base/types/workspace.py
# --------------------------------------

from enum import IntEnum
from typing import List, Optional, Dict, Union, Any, Literal
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import TextEdit, DocumentUri, Command, AnnotatedTextEdit
from .sync import OptionalVersionedTextDocumentIdentifier

# =================================================================================
# == I. THE MUTATION OF REALITY (EDITS)                                          ==
# =================================================================================

class TextDocumentEdit(LspModel):
    """
    [THE VERSIONED DELTA]
    Describes a batch of edits applied to a specific version of a document.
    Essential for 'atomic' refactoring where version consistency is mandatory.
    """
    model_config = ConfigDict(populate_by_name=True)

    text_document: OptionalVersionedTextDocumentIdentifier = Field(..., alias="textDocument")
    edits: List[Union[TextEdit, AnnotatedTextEdit]]

class CreateFileOptions(LspModel):
    overwrite: Optional[bool] = None
    ignore_if_exists: Optional[bool] = Field(None, alias="ignoreIfExists")

class CreateFile(LspModel):
    """[GENESIS ATOM] Creation of a new scripture."""
    kind: Literal["create"] = "create"
    uri: DocumentUri
    options: Optional[CreateFileOptions] = None
    annotation_id: Optional[str] = Field(None, alias="annotationId")

class RenameFileOptions(LspModel):
    overwrite: Optional[bool] = None
    ignore_if_exists: Optional[bool] = Field(None, alias="ignoreIfExists")

class RenameFile(LspModel):
    """[TRANSLOCATION ATOM] Moving a scripture."""
    kind: Literal["rename"] = "rename"
    old_uri: DocumentUri = Field(..., alias="oldUri")
    new_uri: DocumentUri = Field(..., alias="newUri")
    options: Optional[RenameFileOptions] = None
    annotation_id: Optional[str] = Field(None, alias="annotationId")

class DeleteFileOptions(LspModel):
    recursive: Optional[bool] = None
    ignore_if_not_exists: Optional[bool] = Field(None, alias="ignoreIfNotExists")

class DeleteFile(LspModel):
    """[ANNIHILATION ATOM] Removing a scripture."""
    kind: Literal["delete"] = "delete"
    uri: DocumentUri
    options: Optional[DeleteFileOptions] = None
    annotation_id: Optional[str] = Field(None, alias="annotationId")

class WorkspaceEdit(LspModel):
    """
    [THE CHRONICLE OF CHANGE]
    Represents a transactional change to the workspace.
    Used by Refactoring, QuickFixes, and the History Engine.
    """
    # Simple edits: Map[URI, Edits]
    changes: Optional[Dict[str, List[TextEdit]]] = None

    # Complex edits (TextDocumentEdit | Create | Rename | Delete)
    # [ASCENSION 1]: Added TextDocumentEdit to the Union
    document_changes: Optional[List[Union[TextDocumentEdit, CreateFile, RenameFile, DeleteFile]]] = Field(
        None, alias="documentChanges"
    )

    # Metadata for the History view
    change_annotations: Optional[Dict[str, Any]] = Field(None, alias="changeAnnotations")

class ApplyWorkspaceEditParams(LspModel):
    """The plea to the Client to execute the change."""
    label: Optional[str] = None
    edit: WorkspaceEdit

class ApplyWorkspaceEditResult(LspModel):
    applied: bool
    failure_reason: Optional[str] = Field(None, alias="failureReason")
    failed_change: Optional[int] = Field(None, alias="failedChange")

# =================================================================================
# == II. THE KINETIC COMMANDS                                                    ==
# =================================================================================

class ExecuteCommandParams(LspModel):
    """The plea to execute a server-side Kinetic Rite."""
    command: str
    arguments: Optional[List[Any]] = None

class ExecuteCommandOptions(LspModel):
    commands: List[str]
    work_done_progress: Optional[bool] = Field(None, alias="workDoneProgress")

# =================================================================================
# == III. THE OBSERVATORY (WATCHERS & CONFIG)                                    ==
# =================================================================================

class WorkspaceFolder(LspModel):
    uri: str
    name: str

class WorkspaceFoldersChangeEvent(LspModel):
    added: List[WorkspaceFolder]
    removed: List[WorkspaceFolder]

class DidChangeWorkspaceFoldersParams(LspModel):
    event: WorkspaceFoldersChangeEvent

class FileChangeType(IntEnum):
    Created = 1
    Changed = 2
    Deleted = 3

class FileEvent(LspModel):
    uri: str
    type: FileChangeType

class DidChangeWatchedFilesParams(LspModel):
    changes: List[FileEvent]

class FileOperationPattern(LspModel):
    glob: str
    matches: Optional[str] = None  # file/folder
    options: Optional[Any] = None

class FileOperationFilter(LspModel):
    scheme: Optional[str] = None
    pattern: FileOperationPattern

class FileOperationRegistrationOptions(LspModel):
    filters: List[FileOperationFilter]

class WorkspaceSymbolParams(LspModel):
    query: str

class DidChangeConfigurationParams(LspModel):
    """
    [THE SHIFT OF LAW]
    Sent by the client when configuration settings change.
    """
    settings: Any

class ConfigurationItem(LspModel):
    scope_uri: Optional[str] = Field(None, alias="scopeUri")
    section: Optional[str] = None

class ConfigurationParams(LspModel):
    items: List[ConfigurationItem]