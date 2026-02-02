# Path: core/lsp/__init__.py
# -------------------------
# LIF: INFINITY | ROLE: SOVEREIGN_LIBRARY_GATEWAY | RANK: MASTER
# =================================================================================
# == GNOSTIC LSP FRAMEWORK (V-Ω-MODULAR-SINGULARITY)                             ==
# =================================================================================

__version__ = "1.0.0-IRON-CORE"

# --- 1. THE KERNEL & ORGANS (The Core Engine) ---
from .base import (
    BaseLSPServer,
    NeuralDispatcher,
    DocumentLibrarian,
    KineticFoundry,
    LifecycleGovernor
)

# --- 2. THE PROTOCOL & PHYSICS (The Communication Layer) ---
from .base.protocol import JsonRpcEndpoint, StdioStream, SocketStream
from .base.rpc import JsonRpcError, ErrorCodes

# --- 3. THE GNOSTIC CONTRACTS (For Building Features) ---
from .base.features.hover import HoverProvider, HoverContext
from .base.features.completion import CompletionProvider, CompletionContext
from .base.features.definition import DefinitionRule
from .base.features.symbols import SymbolProvider
from .base.features.linter import LinterRule
from .base.features.code_action import CodeActionProvider
from .base.features.rename import RenameMutator, RenameValidator
# ... (and so on for other features)

# --- 4. THE UNIVERSAL ATOMS (The LSP 3.17 Type System) ---
from .base.types import (
    # Primitives
    Position, Range, Location, LocationLink, Command, TextEdit,
    MarkupKind, MarkupContent, DocumentUri,
    # Lifecycle & Sync
    InitializeParams, InitializeResult, ServerCapabilities,
    DidOpenTextDocumentParams, DidChangeTextDocumentParams,
    # Diagnostics
    Diagnostic, DiagnosticSeverity,
    # Intelligence
    CompletionItem, CompletionList, CompletionItemKind,
    Hover,
    DocumentSymbol, SymbolKind,
    SignatureHelp, SignatureInformation,
    InlayHint,
    CodeAction, CodeActionKind,
    # Workspace
    WorkspaceFolder, FileEvent, ExecuteCommandParams
)

# --- 5. THE ALCHEMICAL TOOLS (Utilities) ---
from .base.utils import UriUtils, TextUtils

# =================================================================================
# == THE SOVEREIGN CENSUS (`__all__`)                                            ==
# =================================================================================
# This is the definitive public API of the Gnostic LSP Framework.

__all__ = [
    # Kernel & Organs
    "BaseLSPServer",
    "NeuralDispatcher",
    "DocumentLibrarian",
    "KineticFoundry",
    "LifecycleGovernor",

    # Protocol & Physics
    "JsonRpcEndpoint",
    "StdioStream",
    "SocketStream",
    "JsonRpcError",
    "ErrorCodes",

    # Gnostic Contracts (For Plugin Devs)
    "HoverProvider",
    "CompletionProvider",
    "DefinitionRule",
    "SymbolProvider",
    "LinterRule",
    "CodeActionProvider",
    "RenameMutator",
    "RenameValidator",
    "HoverContext",
    "CompletionContext",

    # Universal Atoms (LSP Types)
    "Position",
    "Range",
    "Location",
    "LocationLink",
    "Command",
    "TextEdit",
    "MarkupKind",
    "MarkupContent",
    "DocumentUri",
    "InitializeParams",
    "InitializeResult",
    "ServerCapabilities",
    "DidOpenTextDocumentParams",
    "DidChangeTextDocumentParams",
    "Diagnostic",
    "DiagnosticSeverity",
    "CompletionItem",
    "CompletionList",
    "CompletionItemKind",
    "Hover",

    "DocumentSymbol",
    "SymbolKind",
    "SignatureHelp",
    "SignatureInformation",
    "InlayHint",
    "CodeAction",
    "CodeActionKind",
    "WorkspaceFolder",
    "FileEvent",
    "ExecuteCommandParams",

    # Alchemical Tools
    "UriUtils",
    "TextUtils",
]

# === SCRIPTURE SEALED: THE LIBRARY IS SOVEREIGN ===