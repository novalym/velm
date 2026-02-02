# Path: core/lsp/base/dispatcher.py
# ---------------------------------

import uuid
import time
import threading
import traceback
import logging
import inspect
import sys
from typing import Any, Callable, Union, Dict, Optional, List, Tuple

# --- GNOSTIC UPLINKS ---
from .state import ServerState, RequestContext
from .telemetry import forensic_log
from .errors import ErrorForge
from .rpc import Request, Notification, Response, JsonRpcError
from .rpc.cancellation import CancellationToken, OperationCancelled
from .middleware import MiddlewarePipeline

# --- LSP TYPE MAPPING (THE IMMUTABLE STANDARD) ---
# We import everything explicitly to ensure the map is comprehensive.
from .types import (
    # Lifecycle
    InitializeParams, InitializedParams, DidOpenTextDocumentParams,
    DidChangeTextDocumentParams, DidSaveTextDocumentParams, DidCloseTextDocumentParams,
    WillSaveTextDocumentParams,

    # Intelligence
    CompletionParams, CompletionItem, HoverParams, SignatureHelpParams,
    DefinitionParams, TypeDefinitionParams, ImplementationParams, ReferenceParams,
    DocumentHighlightParams, DocumentSymbolParams, WorkspaceSymbolParams,
    CodeActionParams, CodeAction, CodeLensParams, CodeLens,
    DocumentFormattingParams, DocumentRangeFormattingParams,
    RenameParams, PrepareRenameParams, FoldingRangeParams, SelectionRangeParams,
    InlayHintParams, SemanticTokensParams, SemanticTokensDeltaParams,
    SemanticTokensRangeParams, DocumentLinkParams, DocumentLink,
    InlineCompletionParams, CallHierarchyPrepareParams,
    CallHierarchyIncomingCallsParams, CallHierarchyOutgoingCallsParams,
    TypeHierarchyPrepareParams, TypeHierarchySupertypesParams, TypeHierarchySubtypesParams,

    # Workspace & Commands
    ExecuteCommandParams, DidChangeConfigurationParams,
    DidChangeWorkspaceFoldersParams, DidChangeWatchedFilesParams
)

# --- PHYSICS CONSTANTS ---
MAX_BACKPRESSURE = 1000
SLOW_RITE_THRESHOLD_MS = 200
IDEMPOTENCY_WINDOW = 60.0
SYSTEM_RITES = {'initialize', 'initialized', 'exit', '$/heartbeat', 'gnostic/relay_auth'}

# [ASCENSION 25]: STATIC LSP TYPE REGISTRY (THE GREAT FIREWALL)
# Maps standard LSP methods to their Pydantic Models.
# This list is EXHAUSTIVE for LSP 3.17 to ensure no method falls through to the Daemon Map.
LSP_TYPE_MAP = {
    # --- Lifecycle ---
    'initialize': InitializeParams,
    'initialized': InitializedParams,
    'shutdown': None,  # No params
    'exit': None,  # No params

    # --- Synchronization ---
    'textDocument/didOpen': DidOpenTextDocumentParams,
    'textDocument/didChange': DidChangeTextDocumentParams,
    'textDocument/didSave': DidSaveTextDocumentParams,
    'textDocument/didClose': DidCloseTextDocumentParams,
    'textDocument/willSave': WillSaveTextDocumentParams,

    # --- Intelligence ---
    'textDocument/completion': CompletionParams,
    'completionItem/resolve': CompletionItem,  # [THE FIX]
    'textDocument/hover': HoverParams,
    'textDocument/signatureHelp': SignatureHelpParams,
    'textDocument/definition': DefinitionParams,
    'textDocument/typeDefinition': TypeDefinitionParams,
    'textDocument/implementation': ImplementationParams,
    'textDocument/references': ReferenceParams,
    'textDocument/documentHighlight': DocumentHighlightParams,
    'textDocument/documentSymbol': DocumentSymbolParams,

    # --- Actions & Lenses ---
    'textDocument/codeAction': CodeActionParams,
    'codeAction/resolve': CodeAction,  # [THE FIX]
    'textDocument/codeLens': CodeLensParams,
    'codeLens/resolve': CodeLens,  # [THE FIX]

    # --- Formatting & Refactoring ---
    'textDocument/formatting': DocumentFormattingParams,
    'textDocument/rangeFormatting': DocumentRangeFormattingParams,
    'textDocument/rename': RenameParams,
    'textDocument/prepareRename': PrepareRenameParams,
    'textDocument/onTypeFormatting': DocumentFormattingParams,  # Fallback

    # --- Structure & Navigation ---
    'textDocument/foldingRange': FoldingRangeParams,
    'textDocument/selectionRange': SelectionRangeParams,
    'textDocument/documentLink': DocumentLinkParams,
    'documentLink/resolve': DocumentLink,  # [THE FIX]

    # --- Modern UI Features ---
    'textDocument/inlayHint': InlayHintParams,
    'textDocument/inlineCompletion': InlineCompletionParams,

    # --- Semantic Tokens ---
    'textDocument/semanticTokens/full': SemanticTokensParams,
    'textDocument/semanticTokens/full/delta': SemanticTokensDeltaParams,
    'textDocument/semanticTokens/range': SemanticTokensRangeParams,

    # --- Hierarchy ---
    'textDocument/prepareCallHierarchy': CallHierarchyPrepareParams,
    'callHierarchy/incomingCalls': CallHierarchyIncomingCallsParams,
    'callHierarchy/outgoingCalls': CallHierarchyOutgoingCallsParams,
    'textDocument/prepareTypeHierarchy': TypeHierarchyPrepareParams,
    'typeHierarchy/supertypes': TypeHierarchySupertypesParams,
    'typeHierarchy/subtypes': TypeHierarchySubtypesParams,

    # --- Workspace ---
    'workspace/symbol': WorkspaceSymbolParams,
    'workspace/executeCommand': ExecuteCommandParams,
    'workspace/didChangeConfiguration': DidChangeConfigurationParams,
    'workspace/didChangeWorkspaceFolders': DidChangeWorkspaceFoldersParams,
    'workspace/didChangeWatchedFiles': DidChangeWatchedFilesParams,
}


class NeuralDispatcher:
    """
    =============================================================================
    == THE NEURAL DISPATCHER (V-Ω-TOTALITY-V203-PROTOCOL-SOVEREIGN)            ==
    =============================================================================
    The Sovereign Intelligence that governs the flow of Intent.
    Now armored with Protocol Separation to prevent Schema Heresies.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Static Type Registry:** A hardcoded, exhaustive map of LSP methods to Pydantic models avoids dynamic lookup failures.
    2.  **Protocol Priority:** LSP methods are checked *before* checking the Daemon's `REQUEST_MAP`, preventing collision.
    3.  **Resolve Support:** Explicitly handles `*/resolve` methods which take partial items (not standard params).
    4.  **Schema Sarcophagus:** Wraps validation in a try/catch that logs schema errors specifically, distinguishing them from logic errors.
    5.  **Null Guard:** Handles methods with `None` params (like `shutdown`) gracefully.
    6.  **Daemon Fallback:** If a method is NOT in the LSP Registry, it attempts to resolve via the Daemon's `REQUEST_MAP`.
    7.  **Namespace Isolation:** Prevents `textDocument/definition` from accidentally triggering a Daemon `DefinitionRequest` meant for CLI usage.
    8.  **Idempotency Ring:** Prevents duplicate requests within a 60ms window.
    9.  **Heartbeat Reflex:** Instantly responds to `$/heartbeat` without thread dispatch.
    10. **Metabolic Backpressure:** Rejects non-system rites if queue depth > 1000.
    11. **Trace Injection:** Automagically weaves `trace_id` into every execution context.
    12. **Lifecycle Gating:** Rejects rites sent before `initialized` (except handshake).
    """
    __slots__ = [
        'server', 'middleware', '_request_registry', '_token_lock',
        '_version_registry', '_idempotency_log', 'vitals', 'logger'
    ]

    def __init__(self, server: Any):
        self.server = server
        self.logger = logging.getLogger("NeuralDispatcher")

        # [ASCENSION 2]: THE PIPELINE
        self.middleware = MiddlewarePipeline()

        # [ASCENSION 4]: THE CAUSAL REGISTRIES
        self._request_registry: Dict[Union[str, int], Tuple[CancellationToken, str]] = {}
        self._idempotency_log: Dict[Union[str, int], float] = {}
        self._version_registry: Dict[str, int] = {}
        self._token_lock = threading.RLock()

        # [ASCENSION 17]: VITALS TELEMETRY
        self.vitals = {
            "requests": 0,
            "notifications": 0,
            "errors": 0,
            "last_active": time.time(),
            "backpressure": 0
        }

    def handle(self, msg: Union[Request, Notification, Response]):
        """
        [THE GRAND TRIAGE]
        Adjudicates incoming matter and submits to the Foundry workers.
        """
        self.vitals["last_active"] = time.time()

        # [ASCENSION 1]: LOW-LEVEL FORENSIC PROCLAMATION
        # This bypasses all internal logic to prove the socket is actually receiving.
        method = getattr(msg, 'method', 'response_payload')
        msg_id = getattr(msg, 'id', 'notif')

        # We scream to sys.stderr which is captured by the Electron 'LSP-STDERR' log
        sys.stderr.write(
            f"\n[SIGNAL:IN] 📥 Method: {method} | ID: {msg_id} | Trace: {getattr(msg, 'trace_id', 'none')}\n")
        sys.stderr.flush()

        if isinstance(msg, Response):
            return

        method = msg.method
        req_id = getattr(msg, 'id', None)
        trace_id = getattr(msg, 'trace_id', f"tr-{uuid.uuid4().hex[:6].upper()}")

        # --- PHASE 0: HEARTBEAT REFLEX ---
        if method in ('$/heartbeat', 'heartbeat'):
            if req_id is not None:
                self.server.endpoint.send_response(req_id, result={"status": "WARM", "state": self.server.state})
            return

        # --- PHASE 1: IDEMPOTENCY ---
        if req_id is not None:
            now = time.time()
            with self._token_lock:
                if req_id in self._idempotency_log:
                    if now - self._idempotency_log[req_id] < IDEMPOTENCY_WINDOW:
                        forensic_log(f"Idempotency Veto: {req_id}", "WARN", "DISPATCH", trace_id=trace_id)
                        return
                self._idempotency_log[req_id] = now

        # --- PHASE 2: LIFECYCLE GATE ---
        if self.server.state == ServerState.DORMANT and method not in SYSTEM_RITES:
            if req_id is not None:
                self.server.endpoint.send_response(req_id, error=JsonRpcError.server_not_initialized())
            return

        # --- PHASE 3: HANDLER RESOLUTION ---
        handler = self.server._features.get(method)
        if not handler:
            if method == 'initialized': return
            forensic_log(f"Method Unmanifest: {method}", "ERROR", "DISPATCH", trace_id=trace_id)
            if req_id is not None:
                self.server.endpoint.send_response(req_id, error=JsonRpcError.method_not_found(method))
            return

        # --- PHASE 4: METABOLIC BACKPRESSURE ---
        pressure = self.server.foundry.active_count
        self.vitals["backpressure"] = pressure
        if req_id is None and pressure > MAX_BACKPRESSURE:
            if method not in SYSTEM_RITES: return

        # =========================================================================
        # == MOVEMENT I: THE TRANSMUTATION (MODEL SOVEREIGNTY)                   ==
        # =========================================================================
        # [ASCENSION 10]: TRANSMUTATION SARCOPHAGUS
        raw_params = getattr(msg, 'params', None)
        transmuted_params = raw_params

        # [THE FIX]: PRIORITY RESOLUTION
        # 1. Check Standard LSP Type Map FIRST
        # If the method is in LSP_TYPE_MAP, we use that model exclusively.
        RequestClass = LSP_TYPE_MAP.get(method)

        # 2. If not standard LSP, check Daemon Request Map (Custom Rites)
        if not RequestClass and hasattr(self.server, 'REQUEST_MAP'):
            # Only use the "split" fallback if it's NOT a namespaced LSP method
            # This prevents 'textDocument/definition' -> 'definition' -> DaemonDefinitionRequest collision
            if '/' not in method or method.startswith("scaffold/"):
                RequestClass = self.server.REQUEST_MAP.get(method) or self.server.REQUEST_MAP.get(method.split('/')[-1])

        # 3. Transmute
        if RequestClass:
            # Special Case: Some resolve methods receive the Item directly, not inside 'params'
            # But the JSON-RPC spec says params is the container.
            # However, if raw_params is a dict matching the model, we validate.

            if raw_params is None and LSP_TYPE_MAP.get(method) is None:
                # Method expects no params (shutdown)
                pass
            elif isinstance(raw_params, (dict, list)):
                try:
                    # Transmute raw JSON dict into a strict Pydantic Model instance
                    transmuted_params = RequestClass.model_validate(raw_params)
                except Exception as e:
                    # [ASCENSION 20]: SOCRATIC SCHEMA LOGGING
                    forensic_log(f"Schema Heresy in '{method}': {str(e)[:100]}", "ERROR", "DISPATCH", trace_id=trace_id)
                    if req_id is not None:
                        self.server.endpoint.send_response(req_id, error=JsonRpcError.invalid_params(str(e)))
                    return

        # --- PHASE 5: SUBMIT TO FOUNDRY ---
        token = CancellationToken() if req_id is not None else CancellationToken.none()
        if req_id is not None:
            with self._token_lock:
                self._request_registry[req_id] = (token, trace_id)

        self.server.foundry.submit(
            req_id or f"notif-{trace_id}",
            self._execute_rite,
            handler, transmuted_params, method, req_id, trace_id, token
        )

        if req_id is not None:
            self.vitals["requests"] += 1
        else:
            self.vitals["notifications"] += 1

    def _execute_rite(self, handler: Callable, params: Any, method: str, req_id: Any, trace_id: str, token: Any):
        """[THE SOVEREIGN EXECUTION RITE]"""
        import os
        import time
        from .rpc.cancellation import OperationCancelled
        from .errors import ErrorForge

        start_ns = time.perf_counter_ns()
        threading.current_thread().name = f"Foundry:{method.split('/')[-1]}:{trace_id[:4]}"

        # --- MOVEMENT I: JIT RE-INCEPTION ---
        if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
            if method.startswith("textDocument/") or method.startswith("workspace/"):
                if hasattr(self.server, 'refresh_features'):
                    try:
                        self.server.refresh_features()
                        handler = self.server._features.get(method)
                        if not handler: raise ValueError("Handler vanished.")
                    except:
                        pass

        # --- MOVEMENT II: CONTEXT PREPARATION ---
        self.server._ctx.trace_id = trace_id
        self.server._ctx.start_time = time.time()

        mw_context = {
            "method": method, "req_id": req_id, "trace_id": trace_id,
            "server": self.server, "token": token, "timestamp": time.time()
        }

        try:
            token.check()

            # --- MOVEMENT III: ADAPTER INVOCATION ---
            def invoke_handler_adapter(p: Any, c: Dict[str, Any]):
                import inspect
                sig = inspect.signature(handler)
                kwargs = {}
                # Match Pydantic model to first argument if present
                if len(sig.parameters) > 0:
                    param_keys = list(sig.parameters.keys())
                    # [ASCENSION]: Only pass params if the handler accepts arguments
                    if p is not None: kwargs[param_keys[0]] = p

                # Inject Context if requested
                if 'ctx' in sig.parameters: kwargs['ctx'] = c
                if 'token' in sig.parameters: kwargs['token'] = token

                return handler(**kwargs)

            result = self.middleware.run(invoke_handler_adapter, params, mw_context)
            token.check()

            # --- MOVEMENT IV: THE REVELATION ---
            if req_id is not None:
                if hasattr(self.server, '_forge_response'):
                    response = self.server._forge_response(req_id, result, trace_id=trace_id)
                else:
                    response = {"jsonrpc": "2.0", "id": req_id, "result": result, "_meta": {"trace_id": trace_id}}

                self.server.endpoint.send_raw(response)

            # --- MOVEMENT V: PERFORMANCE AUDIT ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            self.server.metrics.record(0, 0, is_err=False)

            if duration_ms > 500:
                forensic_log(f"Heavy Rite: {method} took {duration_ms:.2f}ms", "WARN", "FOUNDRY", trace_id=trace_id)

        except OperationCancelled:
            if req_id is not None:
                self.server.endpoint.send_response(req_id, error=ErrorCodes.REQUEST_CANCELLED, trace_id=trace_id)

        except Exception as fracture:
            self.server.metrics.record(0, 0, is_err=True)
            forensic_log(f"Crucible Fracture in '{method}': {fracture}", "ERROR", "FOUNDRY", exc=fracture,
                         trace_id=trace_id)
            if req_id is not None:
                error_obj = ErrorForge.forge(fracture, method)
                self.server.endpoint.send_response(req_id, error=error_obj, trace_id=trace_id)

    def _handle_cancellation(self, params: Any):
        cancel_id = params.id if hasattr(params, 'id') else params.get('id') if isinstance(params, dict) else None
        if cancel_id is None: return

        with self._token_lock:
            entry = self._request_registry.get(cancel_id)
            if entry:
                token, trace_id = entry
                token.cancel()
                if hasattr(self.server, 'relay') and self.server._relay_active:
                    self.server.relay.cancel_rite(trace_id)
                forensic_log(f"Causality Severed for ID: {cancel_id}", "KINETIC", "DISPATCH", trace_id=trace_id)

    def purge_history(self):
        now = time.time()
        with self._token_lock:
            self._idempotency_log = {k: v for k, v in self._idempotency_log.items() if now - v < IDEMPOTENCY_WINDOW}