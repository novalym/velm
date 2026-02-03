# Path: core/lsp/base/types/lifecycle.py
# --------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_LIFECYCLE_TOTALITY_V9000_SINGULARITY
# SYSTEM: GNOSTIC_KERNEL | ROLE: CONSTITUTIONAL_ORCHESTRATOR

from __future__ import annotations
from enum import IntEnum
from typing import Optional, List, Dict, Union, Any
from pydantic import Field, ConfigDict
from .base import LspModel
from .primitives import DocumentUri


# =================================================================================
# == I. THE SYNC PROTOCOLS                                                       ==
# =================================================================================

class TextDocumentSyncKind(IntEnum):
    """
    [THE SYNC LAW]
    Defines how the document content is synchronized with the Oracle.
    """
    NONE = 0
    FULL = 1
    INCREMENTAL = 2


class TextDocumentSyncOptions(LspModel):
    """
    [THE SYNC CONTRACT]
    Detailed options for the high-frequency didChange heartbeat.
    """
    open_close: Optional[bool] = Field(None, alias="openClose")
    change: Optional[TextDocumentSyncKind] = None
    will_save: Optional[bool] = Field(None, alias="willSave")
    will_save_wait_until: Optional[bool] = Field(None, alias="willSaveWaitUntil")
    save: Optional[Union[bool, Dict[str, Any]]] = None


# =================================================================================
# == II. THE PANTHEON OF CAPABILITIES (THE OMEGA HANDSHAKE)                      ==
# =================================================================================
class WorkspaceCapabilities(LspModel):
    """[ASCENSION 12]: Dedicated model to prevent Dict vs Object heresies."""
    workspace_folders: Optional[Dict[str, Any]] = Field(None, alias="workspaceFolders")
    configuration: Optional[bool] = None
    file_operations: Optional[Dict[str, Any]] = Field(None, alias="fileOperations")

class ServerCapabilities(LspModel):
    """
    [THE CONSTITUTION]
    The definitive map of the Server's powers. Every field is aliased to ensure
    absolute compliance with the LSP 3.17 standard and the Ocular UI.
    """
    model_config = ConfigDict(populate_by_name=True)

    # --- 1. Synchronization Strata ---
    text_document_sync: Optional[Union[TextDocumentSyncOptions, TextDocumentSyncKind]] = Field(
        None, alias="textDocumentSync"
    )
    position_encoding: Optional[str] = Field("utf-16", alias="positionEncoding")

    # --- 2. Intelligence & Prophecy ---
    completion_provider: Optional[Any] = Field(None, alias="completionProvider")
    hover_provider: Optional[Union[bool, Any]] = Field(None, alias="hoverProvider")
    signature_help_provider: Optional[Any] = Field(None, alias="signatureHelpProvider")
    definition_provider: Optional[Union[bool, Any]] = Field(None, alias="definitionProvider")
    type_definition_provider: Optional[Union[bool, Any]] = Field(None, alias="typeDefinitionProvider")
    implementation_provider: Optional[Union[bool, Any]] = Field(None, alias="implementationProvider")
    references_provider: Optional[Union[bool, Any]] = Field(None, alias="referencesProvider")

    # --- 3. Structural Mapping ---
    document_highlight_provider: Optional[Union[bool, Any]] = Field(None, alias="documentHighlightProvider")
    document_symbol_provider: Optional[Union[bool, Any]] = Field(None, alias="documentSymbolProvider")
    code_action_provider: Optional[Union[bool, Any]] = Field(None, alias="codeActionProvider")
    code_lens_provider: Optional[Any] = Field(None, alias="codeLensProvider")
    document_link_provider: Optional[Any] = Field(None, alias="documentLinkProvider")
    color_provider: Optional[Union[bool, Any]] = Field(None, alias="colorProvider")

    # --- 4. Geometric Mutation ---
    document_formatting_provider: Optional[Union[bool, Any]] = Field(None, alias="documentFormattingProvider")
    document_range_formatting_provider: Optional[Union[bool, Any]] = Field(
        None, alias="documentRangeFormattingProvider"
    )
    document_on_type_formatting_provider: Optional[Any] = Field(None, alias="documentOnTypeFormattingProvider")
    rename_provider: Optional[Union[bool, Any]] = Field(None, alias="renameProvider")

    # --- 5. Advanced Hierarchies (LSP 3.17) ---
    folding_range_provider: Optional[Union[bool, Any]] = Field(None, alias="foldingRangeProvider")
    execute_command_provider: Optional[Any] = Field(None, alias="executeCommandProvider")
    selection_range_provider: Optional[Union[bool, Any]] = Field(None, alias="selectionRangeProvider")
    call_hierarchy_provider: Optional[Union[bool, Any]] = Field(None, alias="callHierarchyProvider")
    type_hierarchy_provider: Optional[Union[bool, Any]] = Field(None, alias="typeHierarchyProvider")
    linked_editing_range_provider: Optional[Union[bool, Any]] = Field(None, alias="linkedEditingRangeProvider")
    semantic_tokens_provider: Optional[Any] = Field(None, alias="semanticTokensProvider")
    moniker_provider: Optional[Union[bool, Any]] = Field(None, alias="monikerProvider")

    # --- 6. The Ocular Matrix ---
    inlay_hint_provider: Optional[Union[bool, Any]] = Field(None, alias="inlayHintProvider")
    inline_value_provider: Optional[Union[bool, Any]] = Field(None, alias="inlineValueProvider")
    diagnostic_provider: Optional[Any] = Field(None, alias="diagnosticProvider")
    inline_completion_provider: Optional[Union[bool, Any]] = Field(None, alias="inlineCompletionProvider")

    # --- 7. Workspace Observatory ---
    workspace_symbol_provider: Optional[Union[bool, Any]] = Field(None, alias="workspaceSymbolProvider")
    workspace: Optional[WorkspaceCapabilities] = Field(default_factory=WorkspaceCapabilities)

    # Neural Extension Slot
    experimental: Optional[Any] = None


# =================================================================================
# == III. THE IDENTITIES                                                         ==
# =================================================================================

class ClientInfo(LspModel):
    """
    [THE VISITOR]
    Metadata describing the Architect's Tool (VS Code, Cockpit).
    """
    name: str
    version: Optional[str] = None


class ServerInfo(LspModel):
    """
    [THE ORACLE]
    Metadata describing the God-Engine's current incarnation.
    """
    name: str = "Scaffold God-Engine"
    version: Optional[str] = "3.2.0-SINGULARITY"


class ClientCapabilities(LspModel):
    """
    [THE ASSET CENSUS]
    Describes what the Client is capable of perceiving.
    """
    workspace: Optional[Dict[str, Any]] = None
    text_document: Optional[Dict[str, Any]] = Field(None, alias="textDocument")
    window: Optional[Dict[str, Any]] = None
    general: Optional[Dict[str, Any]] = None
    experimental: Optional[Any] = None


# =================================================================================
# == IV. THE HANDSHAKE MESSAGES                                                  ==
# =================================================================================

class InitializeParams(LspModel):
    """
    [THE FIRST PLEA]
    Sent by the Client to establish the Neural Link.
    """
    model_config = ConfigDict(populate_by_name=True)

    process_id: Optional[int] = Field(None, alias="processId")
    client_info: Optional[ClientInfo] = Field(None, alias="clientInfo")
    locale: Optional[str] = None
    root_path: Optional[str] = Field(None, alias="rootPath")
    root_uri: Optional[DocumentUri] = Field(None, alias="rootUri")
    capabilities: ClientCapabilities
    initialization_options: Optional[Any] = Field(None, alias="initializationOptions")
    trace: Optional[str] = 'off'
    workspace_folders: Optional[List[Any]] = Field(None, alias="workspaceFolders")


class InitializeResult(LspModel):
    """
    [THE CONSTITUTIONAL RESPONSE]
    The Oracle's reply, confirming the laws of the session.
    """
    capabilities: ServerCapabilities
    server_info: Optional[ServerInfo] = Field(None, alias="serverInfo")


class InitializedParams(LspModel):
    """
    [THE CONFIRMATION]
    The final signal from the Client that the Singularity is active.
    """
    pass