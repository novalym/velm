# Path: core/lsp/base/types/__init__.py
# -------------------------------------

"""
=================================================================================
== THE GNOSTIC TYPE REGISTRY (V-Ω-CRYSTAL-LATTICE-FIXED-V4)                    ==
=================================================================================
The unified export gateway for all LSP data contracts.
Flattens the namespace for seamless access.
"""

from .base import LspModel
from .primitives import (
    Position, Range, Location, LocationLink, Command,
    TextEdit, AnnotatedTextEdit, ChangeAnnotation,
    MarkupKind, MarkupContent, DocumentUri, URI, ProgressToken,
    TextDocumentIdentifier, TraceValue,
    WorkDoneProgressOptions, WorkDoneProgressParams, PartialResultParams
)
from .lifecycle import (
    InitializeParams, InitializeResult, ServerCapabilities,
    ClientCapabilities, ServerInfo, ClientInfo,
    TextDocumentSyncKind, TextDocumentSyncOptions,
    InitializedParams
)
from .sync import (
    TextDocumentItem, VersionedTextDocumentIdentifier,
    OptionalVersionedTextDocumentIdentifier, TextDocumentContentChangeEvent,
    DidOpenTextDocumentParams, DidChangeTextDocumentParams,
    DidCloseTextDocumentParams, DidSaveTextDocumentParams,
    WillSaveTextDocumentParams, TextDocumentSaveReason
)
from .diagnostics import (
    Diagnostic, DiagnosticSeverity, DiagnosticTag,
    DiagnosticRelatedInformation, PublishDiagnosticsParams, DiagnosticOptions,
    CodeDescription, DocumentDiagnosticParams, FullDocumentDiagnosticReport,
    UnchangedDocumentDiagnosticReport, DocumentDiagnosticReport
)
from .completion import (
    CompletionItem, CompletionList, CompletionItemKind,
    CompletionItemTag, InsertTextFormat, CompletionTriggerKind,
    CompletionContext, CompletionParams, CompletionOptions
)
from .hover import (
    Hover, HoverParams, HoverOptions
)
from .signature_help import (
    SignatureHelp, SignatureInformation, ParameterInformation,
    SignatureHelpParams, SignatureHelpOptions, SignatureHelpContext,
    SignatureHelpTriggerKind
)
from .definition import (
    DefinitionParams, DefinitionOptions,
    TypeDefinitionParams, TypeDefinitionOptions,
    ImplementationParams, ImplementationOptions
)
from .references import (
    ReferenceParams, ReferenceContext, ReferenceOptions
)
from .document_highlight import (
    DocumentHighlight, DocumentHighlightKind, DocumentHighlightParams, DocumentHighlightOptions
)
from .symbols import (
    DocumentSymbol, SymbolKind, SymbolTag, DocumentSymbolParams,
    SymbolInformation, WorkspaceSymbolParams, DocumentSymbolOptions
)
from .code_action import (
    CodeAction, CodeActionKind, CodeActionParams, CodeActionContext,
    CodeActionOptions, WorkspaceEdit
)
from .code_lens import (
    CodeLens, CodeLensParams
)
from .formatting import (
    FormattingOptions, DocumentFormattingParams, DocumentRangeFormattingParams
)
from .rename import (
    RenameParams, PrepareRenameParams, RenameOptions
)
from .folding_range import (
    FoldingRange, FoldingRangeParams, FoldingRangeKind, FoldingRangeOptions
)
from .selection_range import (
    SelectionRange, SelectionRangeParams, SelectionRangeOptions
)
from .inlay_hint import (
    InlayHint, InlayHintParams, InlayHintKind, InlayHintLabelPart
)
from .semantic_tokens import (
    SemanticTokens, SemanticTokensParams, SemanticTokensRangeParams,
    SemanticTokensDelta, SemanticTokensDeltaParams, SemanticTokensEdit,
    SemanticTokensLegend, SemanticTokensOptions, SemanticTokensPartialResult
)
from .workspace import (
    WorkspaceFolder, FileEvent, FileChangeType, ExecuteCommandParams,
    ExecuteCommandOptions, DidChangeWorkspaceFoldersParams, WorkspaceFoldersChangeEvent,
    CreateFile, RenameFile, DeleteFile, CreateFileOptions, RenameFileOptions, DeleteFileOptions,
    FileOperationFilter, FileOperationPattern, FileOperationRegistrationOptions,
    DidChangeWatchedFilesParams, DidChangeConfigurationParams, ConfigurationParams,
    ApplyWorkspaceEditParams, ApplyWorkspaceEditResult,
    TextDocumentEdit  # [ASCENSION]
)
from .window import (
    ShowMessageParams, LogMessageParams, ShowMessageRequestParams,
    MessageActionItem, MessageType
)

from .inline_completion import (
    InlineCompletionParams, InlineCompletionItem, InlineCompletionList,
    InlineCompletionContext, InlineCompletionTriggerKind, InlineCompletionOptions
)
from .document_link import DocumentLinkParams, DocumentLinkOptions, DocumentLink
from .call_hierarchy import CallHierarchyOutgoingCall, CallHierarchyItem, CallHierarchyPrepareParams, \
    CallHierarchyIncomingCall, CallHierarchyOutgoingCallsParams, CallHierarchyIncomingCallsParams, CallHierarchyOptions
from .type_hierarchy import TypeHierarchySubtypesParams, TypeHierarchyPrepareParams, TypeHierarchyItem, \
    TypeHierarchyOptions, TypeHierarchySupertypesParams

__all__ = [
    # Base
    "LspModel",

    # Primitives & Capabilities
    "Position", "Range", "Location", "LocationLink", "Command",
    "TextEdit", "AnnotatedTextEdit", "ChangeAnnotation",
    "MarkupKind", "MarkupContent", "DocumentUri", "URI", "ProgressToken",
    "TextDocumentIdentifier", "TraceValue",
    "WorkDoneProgressOptions", "WorkDoneProgressParams", "PartialResultParams",

    # Lifecycle
    "InitializeParams", "InitializeResult", "ServerCapabilities",
    "ClientCapabilities", "ServerInfo", "ClientInfo",
    "TextDocumentSyncKind", "TextDocumentSyncOptions",
    "InitializedParams",

    # Sync
    "TextDocumentItem", "VersionedTextDocumentIdentifier",
    "OptionalVersionedTextDocumentIdentifier", "TextDocumentContentChangeEvent",
    "DidOpenTextDocumentParams", "DidChangeTextDocumentParams",
    "DidCloseTextDocumentParams", "DidSaveTextDocumentParams",
    "WillSaveTextDocumentParams", "TextDocumentSaveReason",

    # Features
    "Diagnostic", "DiagnosticSeverity", "DiagnosticTag", "DiagnosticRelatedInformation", "PublishDiagnosticsParams",
    "DiagnosticOptions", "CodeDescription",
    "CompletionItem", "CompletionList", "CompletionItemKind", "CompletionItemTag", "InsertTextFormat",
    "CompletionTriggerKind", "CompletionContext", "CompletionParams", "CompletionOptions",
    "Hover", "HoverParams", "HoverOptions",
    "SignatureHelp", "SignatureInformation", "ParameterInformation", "SignatureHelpParams", "SignatureHelpOptions",
    "SignatureHelpContext", "SignatureHelpTriggerKind",
    "DefinitionParams", "DefinitionOptions", "TypeDefinitionParams", "TypeDefinitionOptions", "ImplementationParams",
    "ImplementationOptions",
    "ReferenceParams", "ReferenceContext", "ReferenceOptions",
    "DocumentHighlight", "DocumentHighlightKind", "DocumentHighlightParams", "DocumentHighlightOptions",
    "DocumentSymbol", "SymbolKind", "SymbolTag", "DocumentSymbolParams", "SymbolInformation", "WorkspaceSymbolParams",
    "DocumentSymbolOptions",
    "CodeAction", "CodeActionKind", "CodeActionParams", "CodeActionContext", "CodeActionOptions", "WorkspaceEdit",
    "CodeLens", "CodeLensParams",
    "FormattingOptions", "DocumentFormattingParams", "DocumentRangeFormattingParams",
    "RenameParams", "PrepareRenameParams", "RenameOptions",
    "FoldingRange", "FoldingRangeParams", "FoldingRangeKind", "FoldingRangeOptions",
    "SelectionRange", "SelectionRangeParams", "SelectionRangeOptions",
    "InlayHint", "InlayHintParams", "InlayHintKind", "InlayHintLabelPart",
    "SemanticTokens", "SemanticTokensParams", "SemanticTokensRangeParams", "SemanticTokensDelta",
    "SemanticTokensDeltaParams", "SemanticTokensEdit", "SemanticTokensLegend", "SemanticTokensOptions",
    "SemanticTokensPartialResult", "DocumentDiagnosticParams", "FullDocumentDiagnosticReport",
    "UnchangedDocumentDiagnosticReport", "DocumentDiagnosticReport",

    # Workspace & Window
    "WorkspaceFolder", "FileEvent", "FileChangeType", "ExecuteCommandParams", "ExecuteCommandOptions",
    "DidChangeWorkspaceFoldersParams", "WorkspaceFoldersChangeEvent", "DidChangeWatchedFilesParams",
    "CreateFile", "RenameFile", "DeleteFile", "CreateFileOptions", "RenameFileOptions", "DeleteFileOptions",
    "FileOperationFilter", "FileOperationPattern", "FileOperationRegistrationOptions",
    "DidChangeConfigurationParams", "ConfigurationParams", "ApplyWorkspaceEditParams", "ApplyWorkspaceEditResult",
    "ShowMessageParams", "LogMessageParams", "ShowMessageRequestParams", "MessageActionItem", "MessageType",
    "TextDocumentEdit",  # [ASCENSION]

    # Inline Completion
    "InlineCompletionParams", "InlineCompletionItem", "InlineCompletionList", "InlineCompletionOptions",
    "InlineCompletionContext", "InlineCompletionTriggerKind",
    "DocumentLink", "DocumentLinkParams", "DocumentLinkOptions",

    # Hierarchy
    "CallHierarchyIncomingCall", "CallHierarchyOptions", "CallHierarchyOutgoingCall", "CallHierarchyPrepareParams",
    "CallHierarchyItem", "CallHierarchyOutgoingCallsParams", "CallHierarchyIncomingCallsParams",
    "TypeHierarchyItem", "TypeHierarchyOptions", "TypeHierarchySubtypesParams", "TypeHierarchyPrepareParams",
    "TypeHierarchySupertypesParams",
]