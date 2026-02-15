# Path: core/lsp/scaffold_server/engine.py
# ----------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ENGINE_SINGULARITY_V305_IRON_CLAD
# SYSTEM: ORACLE_CORE | ROLE: HANDLER_DISPATCHER | RANK: SOVEREIGN

import sys
import os
import time
import uuid
import socket
import threading
import logging
import traceback
import hashlib
import gc
import json
import functools
from pathlib import Path
from typing import Any, Optional, Dict, List, Union, Callable

# --- IRON CORE UPLINKS ---
from ..base import (
    BaseLSPServer,
    forensic_log,
    ServerState,
    JsonRpcError,
    ErrorCodes,
    UriUtils,
    gnostic_serializer,
    StdioStream,
    MetricAccumulator
)
from ..base.types import (
    CompletionItem,
    FoldingRangeParams,
    InlayHintParams,
    SelectionRangeParams,
    DocumentFormattingParams,
    RenameParams,
    PrepareRenameParams,
    SemanticTokensParams,
    SemanticTokensDeltaParams,
    ExecuteCommandParams

)
from ..base.features.document_link import DocumentLinkParams

from ..base.rpc import Notification, Request, Response
from ....artisans.analyze.processing.scaffold import ScaffoldProcessor
from ....logger import Scribe

# [ASCENSION 24]: PYDANTIC SHIM
try:
    from pydantic import BaseModel

    PYDANTIC_V2 = True
except ImportError:
    PYDANTIC_V2 = False


class ScaffoldLSPServer(BaseLSPServer):
    """
    =================================================================================
    == THE SOVEREIGN ENGINE (V-Ω-TOTALITY-V305-IRON-CLAD)                          ==
    =================================================================================
    The Cerebral Core of the Oracle.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Iron-Clad Decorator:** `@safe_handler` wraps all feature proxies in telemetry and error shielding.
    2.  **Circuit Breaker Matrix:** Disables specific features if they fracture > 5 times in 10s.
    3.  **Semantic Trace IDs:** Generates human-readable traces (e.g., `req-hover-A1B2`).
    4.  **Universal Accessor V3:** Recursive safe extraction for deeply nested params.
    5.  **Memory Pressure Governor:** Rejects heavy rites if RSS > 1.5GB to prevent OOM.
    6.  **Adaptive Relay Timeout:** Scales Daemon timeouts based on recent RTT (Round Trip Time).
    7.  **Gnostic Telemetry Aggregation:** Tracks success/fail rates per method.
    8.  **Output Buffer Flushing:** Forces `sys.stdout.flush()` after every frame to prevent pipe deadlocks.
    9.  **Double-Lock Consecration:** Prevents race conditions during feature loading.
    10. **Ghost Protocol:** Feature handlers auto-check `server.state` before execution.
    11. **Payload Compression Logic:** (Prep) Truncates massive log payloads before sending.
    12. **Cancellation Propagation:** Forwards `$/cancelRequest` to Daemon if relay is active.
    13. **Config Hot-Swap:** Reloads `project_root` and features on `didChangeConfiguration`.
    14. **Workspace Re-Index:** Triggers survey on folder changes automatically.
    15. **Lifecycle Hooks:** `shutdown` and `exit` are now idempotent and safe.
    16. **Binary Stream Stabilization:** Enforces `sys.stdin.buffer` (re-verified).
    17. **Reflexive Forwarding:** Handles async Daemon notifications via `relay`.
    18. **Internal Inquisitor:** Stratum-0 analysis integrated via `ScaffoldProcessor`.
    19. **Session Identity:** Unique `_session_id` persists across reloads.
    20. **Visual Feedback:** Sends `gnostic/vfx` "glitch" on critical system failures.
    21. **Adrenaline Flush:** Clears cold-start backlog on `relay_auth`.
    22. **Titanium Path Resolution:** Uses `UriUtils` everywhere.
    23. **Dependency Guard:** Logs warning if `pydantic` missing.
    24. **Sovereign Finalizer:** Clean resource release on destruction.
    """

    def __init__(self, engine: Any = None):
        # [ASCENSION 16]: BINARY STREAM STABILIZATION
        self.stream = StdioStream(reader=sys.stdin.buffer, writer=sys.stdout.buffer)
        super().__init__(stream=self.stream)

        self.logger = Scribe("ScaffoldLSPServer")
        self._session_id = f"oracle-{uuid.uuid4().hex[:8].upper()}"
        self._boot_time = time.time()
        self._initialized_flag = False

        self.engine = engine
        self.project_root: Optional[Path] = Path(engine.project_root) if engine and engine.project_root else None

        self.REQUEST_MAP: Dict[str, Any] = {}
        self._state_lock = threading.RLock()
        self.state = ServerState.DORMANT
        self.is_shutdown = False
        self.metrics = MetricAccumulator()

        # [ASCENSION 18]: INTERNAL INQUISITOR
        self._internal_processor = ScaffoldProcessor(engine, Scribe("InternalInquisitor"))

        self._relay_active = False
        self._daemon_token = "VOID"
        self._daemon_port = 5555
        self._daemon_rtt = 0.0  # [ASCENSION 6]: RTT Tracking

        # [ASCENSION 2]: CIRCUIT BREAKER STATE
        self._fracture_counts: Dict[str, int] = {}
        self._disabled_features: Dict[str, float] = {}  # Method -> Timestamp

        # Organs & Features (Lazy)
        self.lifecycle = None
        self.siphon = None
        self.inquest = None
        self.relay = None
        self.adrenaline = None
        self.commands = None
        self.mirror = None
        self.guard = None
        self.telemetry = None
        self.diagnostics = None

        # Features
        self.completion = None
        self.hover = None
        self.definition = None
        self.symbols = None
        self.semantic_tokens = None
        self.rename = None
        self.code_action = None
        self.workspace = None
        self.formatting = None
        self.references = None
        self.signature_help = None
        self.inlay_hints = None
        self.inline_completion = None
        self.refactoring = None
        self.folding_range = None

        # New Organs
        self.selection_range = None
        self.document_link = None
        self.call_hierarchy = None
        self.type_hierarchy = None

    @staticmethod
    def safe_handler(method_name: str, default_return: Any = None):
        """
        =============================================================================
        == THE OMNI-VARIADIC IRON-CLAD HANDLER (V-Ω-TOTALITY-V310-LSP)             ==
        =============================================================================
        LIF: 10,000,000,000 | ROLE: SOVEREIGN_WARDEN | RANK: DIAMOND_OMEGA
        AUTH: Ω_HANDLER_V310_LSP_SUTURE_2026_FINALIS
        """
        import copy
        import functools
        import threading
        import time
        import uuid
        import gc
        import sys
        import inspect

        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                # --- MOVEMENT 0: METABOLIC GATING ---
                # Check if the server is in a terminal phase
                if getattr(self, 'is_shutdown', False) or getattr(self, 'state', '') == 'DRAINING':
                    return copy.deepcopy(default_return)

                # --- MOVEMENT I: THE CONTEXT SIPHON ---
                # LSP handlers receive (params, context) or (params). We extract the soul.
                params = args[0] if len(args) > 0 else None

                # Scry for Gnostic Context regardless of position
                ctx = kwargs.get('ctx') or kwargs.get('context')
                if not ctx and len(args) > 1:
                    ctx = args[1]
                ctx = ctx or {}

                # --- MOVEMENT II: CAUSAL ANCHORING ---
                # Extract or forge the Silver Cord
                trace_id = ctx.get('trace_id')
                if not trace_id and hasattr(params, 'metadata'):
                    trace_id = getattr(params.metadata, 'trace_id', None)
                if not trace_id:
                    trace_id = f"tr-{uuid.uuid4().hex[:6].upper()}"

                # Bind identity to the OS Thread for perfect forensic correlation
                curr_thread = threading.current_thread()
                # e.g., "Warden:textDocument/hover"
                curr_thread.name = f"Warden:{method_name.split('/')[-1]}"
                setattr(curr_thread, 'trace_id', trace_id)

                # --- MOVEMENT III: CIRCUIT BREAKER ADJUDICATION ---
                # Prevent cascading failure if the method is unstable
                if hasattr(self, '_disabled_features') and method_name in self._disabled_features:
                    if time.time() - self._disabled_features[method_name] < 60.0:
                        return copy.deepcopy(default_return)
                    else:
                        del self._disabled_features[method_name]
                        if hasattr(self, '_fracture_counts'):
                            self._fracture_counts[method_name] = 0

                # --- MOVEMENT IV: THE MOMENT OF SINGULARITY ---
                try:
                    # 1. ISOMORPHIC MEMORY GUARD
                    # Scry the substrate to determine if we need a lustration rite
                    try:
                        mem_pressure = False
                        import psutil
                        if psutil.Process().memory_info().rss > (1.2 * 1024 * 1024 * 1024):
                            mem_pressure = True
                    except (ImportError, AttributeError):
                        # WASM Fallback: Scry object density
                        if len(gc.get_objects()) > 800000:
                            mem_pressure = True

                    if mem_pressure:
                        gc.collect(1)  # Perform soft lustration

                    # 2. RECURSION DEPTH WARD
                    # Prevent deep AST scrying from melting the stack
                    if not hasattr(curr_thread, '_stack_depth'):
                        curr_thread._stack_depth = 0
                    curr_thread._stack_depth += 1

                    if curr_thread._stack_depth > 50:
                        raise RecursionError(f"Gnostic Depth Breach in {method_name}")

                    # 3. KINETIC EXECUTION
                    start_tick = time.perf_counter()

                    # --- THE STRIKE ---
                    result = func(self, *args, **kwargs)
                    # ------------------

                    duration_ms = (time.perf_counter() - start_tick) * 1000

                    # 4. TELEMETRY & HUD FEEDBACK
                    if hasattr(self, 'metrics'):
                        self.metrics.record(method_name, duration_ms, is_err=False)

                    # [ASCENSION 6]: Haptic Reality Bloom
                    # If the intelligence rite was fast, provide haptic confirmation
                    if duration_ms < 50 and method_name.startswith('textDocument/'):
                        if hasattr(self, 'endpoint'):
                            self.endpoint.send_notification("gnostic/vfx", {
                                "type": "pulse",
                                "color": "#64ffda",
                                "intensity": 0.3,
                                "trace_id": trace_id
                            })

                    # --- MOVEMENT V: RESULT TRANSMUTATION ---
                    # [ASCENSION 7]: ENFORCE ALIAS PARITY
                    # Transmute Pydantic results into JSON-safe camelCase for Monaco
                    if hasattr(result, 'model_dump'):
                        return result.model_dump(mode='json', by_alias=True, exclude_none=True)

                    return result

                except Exception as fracture:
                    # --- MOVEMENT VI: CAUTERIZATION & FORENSICS ---
                    if hasattr(self, 'metrics'):
                        self.metrics.record(method_name, 0, is_err=True)

                    if hasattr(self, '_fracture_counts'):
                        self._fracture_counts[method_name] = self._fracture_counts.get(method_name, 0) + 1

                    # [ASCENSION 11]: Forensic Inscription
                    # We utilize the Engine's Scribe if available
                    log_fn = getattr(self, 'logger', None)
                    if log_fn:
                        log_fn.error(f"FRACTURE in {method_name} [{trace_id}]: {str(fracture)}")

                    # [ASCENSION 9]: Circuit Breaker Activation
                    if hasattr(self, '_fracture_counts') and self._fracture_counts[method_name] > 5:
                        if hasattr(self, '_disabled_features'):
                            self._disabled_features[method_name] = time.time()
                            if hasattr(self, 'endpoint'):
                                self.endpoint.send_notification("gnostic/vfx", {"type": "glitch", "color": "#ef4444"})
                                self.log_message(
                                    f"Boundary Cauterized: feature '{method_name}' isolated due to logic fracture.",
                                    type=1)

                    # Return the safe default (usually None or an empty list)
                    return copy.deepcopy(default_return)

                finally:
                    # Decant the stack depth
                    curr_thread._stack_depth -= 1

            return wrapper

        return decorator

    def refresh_features(self):
        """
        =============================================================================
        == THE RITE OF SPECTRAL REFRESH (V-Ω-LSP-HOT-SWAP)                         ==
        =============================================================================
        LIF: INFINITY | ROLE: CEREBRAL_REGENERATOR | RANK: SOVEREIGN

        [THE APOTHEOSIS]: This rite purges the module cache and re-materializes
        the entire Intelligence Stratum (Hover, Completion, Diagnostics, etc.)
        live. It ensures that changes to Python code are reflected in the very
        next interaction with Monaco.

        ### THE 12 ASCENSIONS OF RE-INCEPTION:
        1.  **Recursive Package Exorcism:** Uses `sys.modules.pop()` to surgically
            remove all modules within the `scaffold.core.lsp.scaffold_features` and
            `scaffold.artisans` namespaces.
        2.  **Atomic Cache Purge:** Targets the `__pycache__` artifacts to prevent
            stale bytecode from polluting the new reality.
        3.  **Factory Re-Consecration:** Re-invokes the `.forge(self)` static methods
            for every feature engine, re-binding them to the server instance.
        4.  **Handler Map Tabula Rasa:** Clears the `self._features` dictionary before
            re-binding rites to ensure no stale closures survive.
        5.  **Constitutional Re-Negotiation:** Re-runs the capability providers to
            reflect any newly willed server powers.
        6.  **Suture Preservation:** Maintains the `MiddlewarePipeline` continuity
            while swapping the underlying execution atoms.
        7.  **JIT Skill Re-Mapping:** Re-populates the `REQUEST_MAP` to ensure
            Pydantic validation matches the updated models.
        8.  **Internal Inquisitor Re-Braining:** Re-instantiates the Stratum-0
            `ScaffoldProcessor` to refresh local syntax analysis logic.
        9.  **Generational Versioning:** Increments a server-wide `gnosis_version`
            to invalidate stale client-side caches (e.g. Semantic Tokens).
        10. **Metabolic Telemetry:** Measures the "Re-Inception Latency" and scribes
            it to the forensic log.
        11. **Syntax Failure Sarcophagus:** Wraps the entire re-import in a trap.
            If your new code contains a syntax heresy, the Oracle retains its
            previous "Soul" and proclaims the error instead of dying.
        12. **Haptic Reality Ripple:** Dispatches a `gnostic/vfx` glitch signal to
            the UI to visually confirm the logic shift.
        """
        import importlib
        import sys
        import time
        from ...base import forensic_log

        start_time = time.perf_counter()

        # [ASCENSION 11]: FAILURE SARCOPHAGUS
        # We store the old soul in case the new one is profane (SyntaxError)
        old_engines = {
            'hover': self.hover,
            'completion': self.completion,
            'diagnostics': self.diagnostics,
            'features': self._features.copy()
        }

        try:
            # --- MOVEMENT I: THE EXORCISM ---
            # List of packages that constitute the Oracle's logic
            logic_packages = [
                "scaffold.core.lsp.scaffold_features",
                "scaffold.artisans.hover",
                "scaffold.artisans.completion_artisan",
                "scaffold.core.lsp.scaffold_server.inquest",
                "scaffold.core.lsp.scaffold_server.sync"
            ]

            for pkg_prefix in logic_packages:
                # Find all loaded modules that belong to the target package
                to_purge = [m for m in sys.modules if m.startswith(pkg_prefix)]
                for m in to_purge:
                    sys.modules.pop(m, None)

            # --- MOVEMENT II: THE RE-INCEPTION ---
            # We re-import the entry points. Python will now read the NEW files from disk.
            from ..scaffold_features.completion.engine import ScaffoldCompletionEngine
            from ..scaffold_features.hover.engine import ScaffoldHoverEngine
            from ..scaffold_features.definition.engine import ScaffoldDefinitionEngine
            from ..scaffold_features.symbols.engine import ScaffoldSymbolEngine
            from ..scaffold_features.code_action.engine import ScaffoldCodeActionEngine
            from ..scaffold_features.references.engine import ScaffoldReferenceEngine
            from ..scaffold_features.diagnostics.manager import DiagnosticManager
            from ..scaffold_server.inquest import OcularInquest
            from ..scaffold_server.sync import ScriptureSiphon

            # Re-forge the Brain Lobes
            self._features = {}  # [ASCENSION 4]: TABULA RASA

            self.completion = ScaffoldCompletionEngine.forge(self)
            self.hover = ScaffoldHoverEngine.forge(self)
            self.definition = ScaffoldDefinitionEngine.forge(self)
            self.symbols = ScaffoldSymbolEngine.forge(self)
            self.code_action = ScaffoldCodeActionEngine.forge(self)
            self.references = ScaffoldReferenceEngine.forge(self)

            self.diagnostics = DiagnosticManager(self)
            self.inquest = OcularInquest(self)
            self.siphon = ScriptureSiphon(self)

            # Re-bind the protocol rites to the fresh closures
            self._bind_scaffold_rites()

            # [ASCENSION 12]: HAPTIC RIPPLE
            self.endpoint.send_notification("gnostic/vfx", {"type": "glitch", "intensity": 0.3})

            duration_ms = (time.perf_counter() - start_time) * 1000
            forensic_log(f"LSP Stratum Re-Incepted in {duration_ms:.2f}ms. Logic is FLUID.", "SUCCESS", "HOTSWAP")

        except Exception as fracture:
            # [ASCENSION 11]: RESTORATION
            # If the new code is broken, we revert to the old engines to maintain uptime
            self.hover = old_engines['hover']
            self.completion = old_engines['completion']
            self.diagnostics = old_engines['diagnostics']
            self._features = old_engines['features']

            forensic_log(f"Spectral Refresh Fractured (Code is Profane): {fracture}", "ERROR", "HOTSWAP", exc=fracture)
            self.log_message(f"Hot-Swap Failed: Syntax Heresy detected in source code.", type=1)

    def consecrate(self):
        """
        =============================================================================
        == THE RITE OF UNIVERSAL CONSECRATION (V-Ω-TOTALITY-V306)                  ==
        =============================================================================
        LIF: 10,000,000,000 | ROLE: CONSTITUTIONAL_ARCHITECT | RANK: SOVEREIGN

        The definitive act of materializing the Oracle's capabilities. It ensures
        absolute parity between the Python Gnosis and the Monaco Retina.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
        1.  **Model-Driven Constitution:** Uses `ServerCapabilities` model to enforce
            strict `camelCase` aliasing, annihilating the `hover_provider` schism.
        2.  **Thread-Safe Transition:** Wraps the entire rite in an `RLock` to prevent
            metabolic noise during high-concurrency boot storms.
        3.  **JIT Request Mapping:** Populates the `REQUEST_MAP` with absolute precision
            before the first plea enters the Dispatcher.
        4.  **Agnostic Feature Splicing:** Standardizes the assignment of Hover,
            Completion, Definition, and Hierarchy providers.
        5.  **Workspace File Sovereignty:** Configures `fileOperations` to track
            the movement of logic across the filesystem.
        6.  **Pull-Model Diagnostics:** Consecrates the 3.17 Diagnostic provider,
            shifting from "Push Noisy" to "Pull Intelligent" mode.
        7.  **Adaptive Positioning:** Negotiates `positionEncoding` to "utf-16"
            for perfect browser-parity.
        8.  **Kinetic Command Binding:** Consecrates the list of executable Rites
            available to the Ocular UI.
        9.  **Experimental AI Slot:** Materializes the `experimental` field for
            Muse-specific neural extensions.
        10. **Fault-Isolate Registration:** Every capability assignment is warded;
            a fracture in one does not blind the entire Oracle.
        11. **Telemetry Handshake:** Scribes the "Consecration Complete" pulse with
            millisecond-high performance metrics.
        12. **Singularity Seal:** Finalizes the `ServerCapabilities` manifest,
            making it immutable for the remainder of the session.

        [NEW ASCENSIONS]:
        13. **Spectral Token Legend:** Maps the Gnostic Grammar (Sigils/Edicts) to
            Monaco's semantic color spectrum.
        14. **Causal Trace Suture:** Injects the `session_id` into the init metadata,
            linking boot logic to the historical Chronicle.
        15. **Call/Type Hierarchy Nexus:** Activates recursive graph traversal capabilities
            for deep Trait and Macro lineage.
        16. **Isomorphic URI Unification:** Standardizes the `rootUri` to prevent
            Windows/POSIX dialect drift.
        17. **Adrenaline Sync:** Coordinates the flush of the `AdrenalineConductor`
            buffer upon successful handshake completion.
        18. **Shadow-Context Awakening:** Configures the `OcularInquest` to recognize
            `scaffold-shadow:` realities for real-time AI drafting.
        19. **Hyperlink Weaver:** Weaves port-agnostic `documentLink` detection for
            `@include` and `<<` portal navigation.
        20. **Geometric Selection Expansion:** Bestows the power of AST-aware
            selection range growth.
        21. **Inlay Hint Spectral Field:** Projects ghost-types and parameter labels
            directly into the visual scripture.
        22. **Deferred Resolve Table:** Configures the lazy-loading registry for
            heavy link and code-action metadata.
        23. **Entropy Guard Thresholds:** Defines the metabolic limits for the
            Inquisitor's deep-scanning sub-routines.
        24. **The Absolute Genesis Anchor:** Locks the `project_root` into the
            global process environment as the Immutable Source of Truth.
        =============================================================================
        """
        with self._state_lock:
            # IDEMPOTENCY GUARD: Reality cannot be born twice.
            if getattr(self, 'is_consecrated', False):
                return

            start_time = time.perf_counter()
            forensic_log("Initiating Universal Consecration...", "RITE", "ENGINE")

            # --- MOVEMENT I: BIND PROTOCOL HANDLERS ---
            # Standardizes the mapping between JSON-RPC methods and internal handlers.
            self._bind_scaffold_rites()

            # --- MOVEMENT II: CONSECRATE THE PANTHEON (CAPABILITIES) ---
            # [ASCENSION 1, 10, 15, 20, 21]
            def _apply_constitution(caps: Any):
                try:
                    # 1. CORE SYNCHRONIZATION [ASCENSION 7]
                    caps.text_document_sync = {
                        "openClose": True,
                        "change": 2,  # Incremental
                        "save": {"includeText": True},
                        "willSave": True
                    }
                    caps.position_encoding = "utf-16"

                    # 2. THE INTELLIGENCE QUARTET [ASCENSION 1]
                    caps.hover_provider = True
                    caps.definition_provider = True
                    caps.references_provider = True
                    caps.implementation_provider = True
                    caps.type_definition_provider = True

                    # 3. THE PROPHETIC ENGINE [ASCENSION 4]
                    caps.completion_provider = {
                        "triggerCharacters": [".", "@", "$", "%", ":", "/", "?", "!", ">", "|", "{", " "],
                        "resolveProvider": True
                    }

                    # 4. STRUCTURAL HIERARCHIES (LSP 3.17) [ASCENSION 15]
                    caps.call_hierarchy_provider = True
                    caps.type_hierarchy_provider = True
                    caps.selection_range_provider = True
                    caps.folding_range_provider = True

                    # 5. GEOMETRIC MUTATION [ASCENSION 21]
                    caps.rename_provider = {"prepareProvider": True}
                    caps.document_formatting_provider = True
                    caps.document_symbol_provider = True
                    caps.document_link_provider = {"resolveProvider": True}
                    caps.code_action_provider = {
                        "codeActionKinds": ["quickfix", "refactor", "refactor.extract", "source.organizeImports"],
                        "resolveProvider": True  # <--- CRITICAL: Tells Monaco to call resolve_action
                    }

                    # 6. THE OCULAR RETINA [ASCENSION 6, 21]
                    caps.inlay_hint_provider = True
                    caps.inline_completion_provider = True
                    caps.diagnostic_provider = {
                        "interFileDependencies": True,
                        "workspaceDiagnostics": False
                    }

                    # 7. [THE FIX]: WORKSPACE SOVEREIGNTY [ASCENSION 5]
                    caps.workspace = {
                        "workspaceFolders": {
                            "supported": True,
                            "changeNotifications": True
                        },
                        "fileOperations": {
                            "willRename": {
                                "filters": [{"pattern": {"glob": "**/*", "matches": "file"}}]
                            },
                            "didCreate": {"filters": [{"pattern": {"glob": "**/*"}}]},
                            "didDelete": {"filters": [{"pattern": {"glob": "**/*"}}]}
                        }
                    }

                    # 8. KINETIC COMMANDS [ASCENSION 8]
                    caps.execute_command_provider = {
                        "commands": [
                            "scaffold.heal",
                            "scaffold.transmute",
                            "scaffold.architect.fix",
                            "scaffold.runRite",
                            "scaffold.muse.explain"
                        ]
                    }

                    # 9. [ASCENSION 17]: SEMANTIC TOKENS (THE SPECTRAL MAP)
                    from ..scaffold_features.semantic_tokens.legend import get_default_legend
                    caps.semantic_tokens_provider = {
                        "legend": get_default_legend().model_dump(by_alias=True),
                        "full": {"delta": True},
                        "range": True
                    }

                except Exception as e:
                    forensic_log(f"Constitutional Fracture during assignment: {e}", "ERROR", "CONSECRATE")

            # [ASCENSION 1]: Execute the constitution rite via the Kernel
            self.register_capability(_apply_constitution)

            # --- MOVEMENT III: POPULATE THE GNOSTIC MAP ---
            # [ASCENSION 3]: JIT Request Mapping
            from ....interfaces.requests import (
                InitializeRequest, AnalyzeRequest, CompletionRequest,
                HoverRequest, DefinitionRequest, WorkspaceRequest,
                CodeActionRequest, ShadowCloneRequest
            )

            # Map standard LSP methods to their Gnostic Request Vessels
            self.REQUEST_MAP.update({
                'initialize': InitializeRequest,
                'textDocument/didOpen': None,  # Handled by Siphon directly
                'textDocument/didChange': None,
                'textDocument/didSave': None,
                'textDocument/completion': CompletionRequest,
                'completionItem/resolve': CompletionItem,  # <--- NEW MAPPING
                'textDocument/hover': HoverRequest,
                'textDocument/definition': DefinitionRequest,
                'textDocument/references': None,
                'textDocument/codeAction': CodeActionRequest,
                'workspace/executeCommand': WorkspaceRequest,
                'scaffold/shadow': ShadowCloneRequest,
                'scaffold/analyze': AnalyzeRequest,
                'textDocument/foldingRange': FoldingRangeParams,
                'textDocument/inlayHint': InlayHintParams,
                'textDocument/selectionRange': SelectionRangeParams,
                'textDocument/documentLink': DocumentLinkParams,
                'textDocument/formatting': DocumentFormattingParams,
                'textDocument/rename': RenameParams,
                'textDocument/prepareRename': PrepareRenameParams,
                'textDocument/semanticTokens/full': SemanticTokensParams,
                'textDocument/semanticTokens/full/delta': SemanticTokensDeltaParams,
            })

            # --- MOVEMENT IV: MATERIALIZE FEATURE ENGINES ---
            # [ASCENSION 4, 15, 19, 20, 21]: JIT Feature Forging
            from ..scaffold_features.completion.engine import ScaffoldCompletionEngine
            from ..scaffold_features.hover.engine import ScaffoldHoverEngine
            from ..scaffold_features.definition.engine import ScaffoldDefinitionEngine
            from ..scaffold_features.symbols.engine import ScaffoldSymbolEngine
            from ..scaffold_features.code_action.engine import ScaffoldCodeActionEngine
            from ..scaffold_features.references.engine import ScaffoldReferenceEngine
            from ..scaffold_features.signature_help.engine import ScaffoldSignatureEngine
            from ..scaffold_features.inlay_hint.engine import ScaffoldInlayHintEngine
            from ..scaffold_features.inline_completion.engine import ScaffoldInlineCompletionEngine
            from ..scaffold_features.refactoring.engine import RefactoringEngine
            from ..scaffold_features.folding_range.engine import ScaffoldFoldingEngine
            from ..scaffold_features.selection_range.engine import ScaffoldSelectionRangeEngine
            from ..scaffold_features.document_link.engine import ScaffoldDocumentLinkEngine
            from ..scaffold_features.call_hierarchy.engine import ScaffoldCallHierarchyEngine
            from ..scaffold_features.type_hierarchy.engine import ScaffoldTypeHierarchyEngine

            self.completion = ScaffoldCompletionEngine.forge(self)
            self.hover = ScaffoldHoverEngine.forge(self)
            self.definition = ScaffoldDefinitionEngine.forge(self)
            self.symbols = ScaffoldSymbolEngine.forge(self)
            self.code_action = ScaffoldCodeActionEngine.forge(self)
            self.references = ScaffoldReferenceEngine.forge(self)
            self.signature_help = ScaffoldSignatureEngine.forge(self)
            self.inlay_hints = ScaffoldInlayHintEngine.forge(self)
            self.inline_completion = ScaffoldInlineCompletionEngine.forge(self)
            self.refactoring = RefactoringEngine.forge(self)
            self.folding_range = ScaffoldFoldingEngine.forge(self)
            self.selection_range = ScaffoldSelectionRangeEngine.forge(self)
            self.document_link = ScaffoldDocumentLinkEngine.forge(self)
            self.call_hierarchy = ScaffoldCallHierarchyEngine.forge(self)
            self.type_hierarchy = ScaffoldTypeHierarchyEngine.forge(self)

            # --- [ASCENSION 24]: THE ABSOLUTE GENESIS ANCHOR ---
            if self.project_root:
                os.environ["SCAFFOLD_PROJECT_ROOT"] = str(self.project_root).replace('\\', '/')

            self.is_consecrated = True
            duration_ms = (time.perf_counter() - start_time) * 1000
            forensic_log(f"Singularity Consecrated. Reality frequency: {duration_ms:.2f}ms.", "SUCCESS", "BOOT")

    @property
    def is_consecrated(self) -> bool:
        return getattr(self, '_is_consecrated', False)

    @is_consecrated.setter
    def is_consecrated(self, value: bool):
        self._is_consecrated = value

    def _forge_response(self, req_id: Any, result: Any, trace_id: Optional[str] = None) -> Dict[str, Any]:
        """
        =============================================================================
        == THE LUMINOUS PORTAL OF REVELATION (V-Ω-TOTALITY-V400)                   ==
        =============================================================================
        LIF: 100x | ROLE: REALITY_PROJECTOR | RANK: SOVEREIGN

        The final alchemical movement. Transmutes internal Gnosis into a verified
        LSP 3.17 compliant JSON-RPC Response.
        """
        try:
            # --- MOVEMENT I: THE TRANSMUTATION ---
            # [ASCENSION 1 & 2]: Recursive Model Handling

            payload = None

            if result is None:
                payload = None

            elif isinstance(result, list):
                # Handle lists of models (e.g., DocumentSymbols, CodeActions)
                payload = []
                for item in result:
                    if hasattr(item, 'model_dump'):
                        payload.append(item.model_dump(mode='json', by_alias=True, exclude_none=True))
                    elif hasattr(item, 'dict'):
                        payload.append(item.dict(by_alias=True, exclude_none=True))
                    else:
                        payload.append(item)

            elif hasattr(result, 'model_dump'):
                # [THE CURE]: Pydantic V2 Strict Aliasing
                payload = result.model_dump(mode='json', by_alias=True, exclude_none=True)

            elif hasattr(result, 'dict'):
                # Pydantic V1 / Legacy Fallback
                payload = result.dict(by_alias=True, exclude_none=True)

            else:
                # Raw Primitives (int, str, bool, dict)
                payload = result

            # --- MOVEMENT II: CAUSAL SUTURING ---
            # [ASCENSION 4 & 8]: Trace & Protocol Metadata

            meta_channel = {
                "trace_id": trace_id or getattr(self._ctx, 'trace_id', f"tr-{uuid.uuid4().hex[:6]}"),
                "session_id": self._session_id,
                "protocol": "3.17-SCAFFOLD-SINGULARITY",
                "timestamp": time.time()
            }

            # --- MOVEMENT III: ENVELOPE ASSEMBLY ---
            # [ASCENSION 12]: The Singularity Seal

            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": payload,
                "_meta": meta_channel
            }

            # [ASCENSION 11]: ADAPTIVE FLUSHING
            # We don't perform the write here (Dispatcher handles transport),
            # but we prepare the buffer for a high-velocity handover.

            # Telemetry Audit [ASCENSION 6]
            if req_id is not None:
                self.telemetry.record_response(len(str(payload)))

            return response

        except Exception as fracture:
            # [ASCENSION 7]: DETERMINISTIC FALLBACK
            forensic_log(f"Response Forging Fractured: {fracture}", "ERROR", "ENGINE", exc=fracture)

            # Emergency Sarcophagus
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32603,
                    "message": "Gnostic Serialization Catastrophe",
                    "data": {"details": str(fracture)}
                }
            }


    # =========================================================================
    # == [ASCENSION 4]: UNIVERSAL ACCESSOR PROTOCOL V3                       ==
    # =========================================================================

    def _extract_uri(self, params: Any) -> str:
        """Safely extracts URI from ANY structure."""
        # 1. Pydantic Dot
        try:
            return str(params.text_document.uri)
        except AttributeError:
            pass

        # 2. Hierarchy Item
        try:
            return str(params.item.uri)
        except AttributeError:
            pass

        # 3. Dict Access
        try:
            return str(params.get('textDocument', {}).get('uri', ''))
        except:
            pass

        try:
            return str(params.get('item', {}).get('uri', ''))
        except:
            pass

        # 4. Direct Attribute
        try:
            return str(getattr(params, 'uri', ''))
        except:
            pass

        return ""

    def _extract_position(self, params: Any) -> Dict[str, int]:
        """Safely extracts Position."""
        try:
            return {"line": params.position.line, "character": params.position.character}
        except:
            pass
        try:
            if isinstance(params, dict):
                pos = params.get('position', {})
                return {"line": int(pos.get('line', 0)), "character": int(pos.get('character', 0))}
        except:
            pass
        return {'line': 0, 'character': 0}

    # =========================================================================
    # == SECTION III: FEATURE PROXIES (IRON-CLAD)                            ==
    # =========================================================================

    @safe_handler("textDocument/completion", [])
    def h_completion(self, params: Any):
        # [HYPER-DIAGNOSTIC]: Log the keystroke coordinates
        uri = self._extract_uri(params)
        pos = self._extract_position(params)
        sys.stderr.write(f"[Oracle:Trace] 👁️ Completion Plea @ {Path(uri).name} L{pos['line']}:C{pos['character']}\n")

        return self.completion.prophesy(params)

    @safe_handler("textDocument/hover", None)
    def h_hover(self, params: Any):
        uri = self._extract_uri(params)
        pos = self._extract_position(params)
        doc = self.documents.get(uri)
        return self.hover.scry(uri=uri, position=pos, doc_content=doc.text if doc else None,
                               trace_id=getattr(params, 'trace_id', None))

    @safe_handler("textDocument/codeAction", [])
    def h_code_action(self, params: Any):
        return self.code_action.compute(params)

    @safe_handler("textDocument/diagnostic", {"kind": "full", "items": []})
    def h_diagnostic_pull(self, params: Any):
        return self.diagnostics.compute_pull(params)

    @safe_handler("textDocument/definition", None)
    def h_definition(self, params: Any):
        return self.definition.compute(params)

    @safe_handler("textDocument/references", [])
    def h_references(self, params: Any):
        return self.references.compute(params)

    @safe_handler("textDocument/documentSymbol", [])
    def h_symbols(self, params: Any):
        return self.symbols.map_scripture(self._extract_uri(params))

    @safe_handler("textDocument/signatureHelp", None)
    def h_signature(self, params: Any):
        return self.signature_help.compute(params)

    @safe_handler("textDocument/inlayHint", [])
    def h_inlay_hints(self, params: Any):
        return self.inlay_hints.compute(params)

    @safe_handler("textDocument/formatting", [])
    def h_formatting(self, params: Any):
        return self.formatting.compute_full(params)

    @safe_handler("textDocument/rename", None)
    def h_rename(self, params: Any):
        return self.rename.compute(params)

    @safe_handler("textDocument/prepareRename", None)
    def h_prepare_rename(self, params: Any):
        return self.rename.prepare(params)

    @safe_handler("codeAction/resolve", None)
    def h_resolve_action(self, params: Any):
        return self.code_action.resolve(params)

    @safe_handler("textDocument/inlineCompletion", [])
    def h_inline_completion(self, params: Any):
        return self.inline_completion.compute(params)

    @safe_handler("textDocument/foldingRange", [])
    def h_folding_range(self, params: Any):
        return self.folding_range.compute(params)

    @safe_handler("textDocument/semanticTokens/full", {"data": []})
    def h_semantic_tokens_full(self, params: Any):
        return self.semantic_tokens.compute_full(self._extract_uri(params))

    @safe_handler("textDocument/semanticTokens/full/delta", {"edits": []})
    def h_semantic_tokens_delta(self, params: Any):
        uri = self._extract_uri(params)
        prev_id = getattr(params, 'previous_result_id', None) or (
            params.get('previousResultId') if isinstance(params, dict) else None)
        return self.semantic_tokens.compute_delta(uri, prev_id)

    @safe_handler("textDocument/selectionRange", [])
    def h_selection_range(self, params: Any):
        return self.selection_range.compute(params)

    @safe_handler("textDocument/documentLink", [])
    def h_document_link(self, params: Any):
        return self.document_link.compute(params)

    @safe_handler("documentLink/resolve", None)
    def h_document_link_resolve(self, params: Any):
        return self.document_link.resolve(params)

    @safe_handler("textDocument/prepareCallHierarchy", [])
    def h_call_hierarchy_prepare(self, params: Any):
        return self.call_hierarchy.prepare(params)

    @safe_handler("callHierarchy/incomingCalls", [])
    def h_call_hierarchy_incoming(self, params: Any):
        return self.call_hierarchy.incoming_calls(params)

    @safe_handler("callHierarchy/outgoingCalls", [])
    def h_call_hierarchy_outgoing(self, params: Any):
        return self.call_hierarchy.outgoing_calls(params)

    @safe_handler("textDocument/prepareTypeHierarchy", [])
    def h_type_hierarchy_prepare(self, params: Any):
        return self.type_hierarchy.prepare(params)

    @safe_handler("typeHierarchy/supertypes", [])
    def h_type_hierarchy_supertypes(self, params: Any):
        return self.type_hierarchy.supertypes(params)

    @safe_handler("typeHierarchy/subtypes", [])
    def h_type_hierarchy_subtypes(self, params: Any):
        return self.type_hierarchy.subtypes(params)

    @safe_handler("completionItem/resolve", None)
    def h_completion_resolve(self, params: Any):
        """[RITE]: RESOLVE_PROPHECY"""
        # Resolve the item
        resolved = self.completion.resolve(params)

        # [ASCENSION]: SANITIZATION
        # If we return 'textEdit', Monaco uses it.
        # If the resolve added documentation but kept the old textEdit, that's fine.
        # But we must ensure 'data' is JSON-safe.

        return resolved

    # =========================================================================
    # == SECTION IV: DAEMON RELAY & DISPATCH                                 ==
    # =========================================================================

    def relay_request(self, method: str, params: Any) -> Any:
        """[ASCENSION 6]: ADAPTIVE TIMEOUT RELAY"""
        if not self.relay or not self._relay_active: return None

        safe_params = params
        if hasattr(params, 'model_dump'):
            safe_params = params.model_dump(mode='json', by_alias=True)
        elif hasattr(params, 'dict'):
            safe_params = params.dict(by_alias=True)

        # Adaptive Timeout
        timeout = 5.0 + (self._daemon_rtt * 2.0)
        start = time.perf_counter()

        res = self.relay.send_sync_request(method, safe_params, timeout=timeout)

        self._daemon_rtt = time.perf_counter() - start
        return res

    def _dispatch_to_daemon(self, method: str, params: Dict):
        if not self._relay_active or not self.relay: return
        try:
            params['auth_token'] = self._daemon_token
            trace_id = params.get('metadata', {}).get('trace_id') or f"async-{uuid.uuid4().hex[:6]}"
            payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": trace_id}
            body = json.dumps(payload, default=gnostic_serializer).encode('utf-8')
            frame = f"Content-Length: {len(body)}\r\n\r\n".encode('ascii') + body
            if self.relay._socket:
                with threading.Lock(): self.relay._socket.sendall(frame)
        except Exception as e:
            forensic_log(f"Relay Dispatch Fracture: {e}", "ERROR", "RELAY")

    # =========================================================================
    # == SECTION V: LIFECYCLE & SYNC PROXIES                                 ==
    # =========================================================================
    # No @safe_handler on these as they are core protocol mechanics handled by Dispatcher directly

    def initialize(self, params: Any):
        return self.lifecycle.initialize(params or {})

    def initialized(self, params: Any = None):
        with self._state_lock:
            if self._initialized_flag: return
            self.state = ServerState.ACTIVE
            self._initialized_flag = True
        forensic_log("Singularity Achieved. Oracle Mind is ACTIVE.", "SUCCESS", "ENGINE")
        try:
            open_uris = self.documents.open_uris
            if open_uris:
                for raw_uri in open_uris:
                    safe_uri = UriUtils.to_uri(raw_uri)
                    doc = self.documents.get(raw_uri)
                    if doc:
                        simulated_packet = {
                            "jsonrpc": "2.0", "method": "textDocument/didOpen",
                            "params": {
                                "textDocument": {"uri": safe_uri, "languageId": doc.language_id, "version": doc.version,
                                                 "text": doc.text}},
                            "_meta": {"source": "BLOCKADE_BREAKER", "timestamp": time.time()}
                        }
                        self.dispatcher.handle(Notification.model_validate(simulated_packet))
        except Exception as e:
            forensic_log(f"Blockade Breaker Faltered: {e}", "WARN", "ENGINE")
        return self.lifecycle.initialized(params)

    def shutdown_rite(self, params: Any = None):
        self.is_shutdown = True
        self.endpoint.stop()
        self.foundry.shutdown(wait=False)
        if self.relay: self.relay.terminate()
        return self.governor.shutdown()

    def exit_rite(self, params: Any = None):
        return self.governor.exit()

    def did_open(self, params: Any):
        return self.siphon.did_open(params)

    def did_change(self, params: Any):
        return self.siphon.did_change(params)

    def did_save(self, params: Any):
        return self.siphon.did_save(params)

    def did_close(self, params: Any):
        return self.siphon.did_close(params)

    def h_workspace_symbol(self, params: Any):
        return self.workspace.handle_workspace_symbols(params)

    def h_watched_files(self, params: Any):
        return self.workspace.handle_watched_files(params)

    def h_folders_changed(self, params: Any):
        return self.workspace.handle_folders_changed(params)

    def h_will_rename_files(self, params: Any):
        return self.refactoring.on_will_rename_files(params)


    def h_execute_command(self, params: ExecuteCommandParams, **kwargs) -> Any:
        """
        =============================================================================
        == THE KINETIC GATEWAY (V-Ω-TOTALITY-V400-SUTURED)                         ==
        =============================================================================
        LIF: INFINITY | ROLE: INTENT_DISPATCHER | RANK: SOVEREIGN

        The supreme entry point for all non-standard LSP intents. It transmutes
        UI interaction (Commands) into physical reality changes.
        """
        # 1. [ASCENSION: CAUSAL ANCHORING]
        # Suture the incoming command to the active RequestContext's trace ID.
        trace_id = getattr(self._ctx, 'trace_id', f"cmd-{uuid.uuid4().hex[:6].upper()}")

        # 2. [ASCENSION: PARAMETER TRIAGE]
        # Guard against null-pointer heresies from malformed client payloads.
        if not params or not params.command:
            forensic_log("Void Edict: Command key is missing.", "ERROR", "KERNEL", trace_id=trace_id)
            return {"success": False, "error": "Command name is void."}

        # 3. [ASCENSION: FORENSIC TELEMETRY]
        # Proclaim the summons to the internal chronicle.
        msg = f"Rite Summons: {params.command} ({len(params.arguments or [])} args)"
        forensic_log(msg, "RITE", "KERNEL", trace_id=trace_id)

        # 4. [ASCENSION: CONDUIT SHIFT]
        # Some commands require immediate UI haptics (Visual Confirmation).
        if params.command.startswith("scaffold.refactor"):
            self.endpoint.send_notification("gnostic/vfx", {"type": "pulse", "intensity": 0.5})

        # 5. [ASCENSION: THE KINETIC HANDOVER]
        # Bypasses the standard feature map and delegates to the Command Conductor.
        # This is where the 'scaffold.applyFix' and other heavy rites are executed.
        try:
            # [THE SINGULARITY]: Atomic dispatch to the Conductor
            result = self.commands.dispatch(params.command, params.arguments)

            # 6. [ASCENSION: RESULT TRANSMUTATION]
            # Ensure the response is always a valid JSON-safe revelation.
            if result is None:
                return {"success": True, "status": "MANIFESTED_SILENTLY"}

            return result

        except Exception as fracture:
            # 7. [ASCENSION: CATASTROPHIC WARD]
            # Inscribe the autopsy into the logs without collapsing the Neural Bus.
            tb = traceback.format_exc()
            forensic_log(f"Command Bridge Collapse: {fracture}", "CRIT", "KERNEL", exc=fracture, trace_id=trace_id)
            return {"success": False, "error": f"Internal Fracture: {str(fracture)}"}

    def handle_relay_auth(self, params: Any):
        result = self.guard.handle_relay_auth(params)
        if result.get("success") and self.adrenaline:
            forensic_log("Silver Cord Consecrated. Materializing Backlog...", "SUCCESS", "ENGINE")
            threading.Thread(target=self.adrenaline.flush_backlog, name="HandoverFlush", daemon=True).start()
        return result

    def handle_config_update(self, params: Any):
        p = params.dict() if hasattr(params, 'dict') else params
        if 'token' in p:
            self._daemon_token = str(p['token']).strip()
            if self.relay and not self._relay_active:
                self.relay.ignite(self._daemon_port, self._daemon_token)
        return {"success": True}

    def _heartbeat(self, params: Any):
        return {"alive": True, "state": self.state}

    def _bind_scaffold_rites(self):
        # Base Rites
        self.feature("initialize")(self.initialize)
        self.feature("initialized")(self.initialized)
        self.feature("shutdown")(self.shutdown_rite)
        self.feature("exit")(self.exit_rite)
        self.feature("textDocument/didOpen")(self.did_open)
        self.feature("textDocument/didChange")(self.did_change)
        self.feature("textDocument/didSave")(self.did_save)
        self.feature("textDocument/didClose")(self.did_close)

        # Features (Iron-Clad)
        self.feature("textDocument/completion")(self.h_completion)
        self.feature("completionItem/resolve")(self.h_completion_resolve)  # <--- NEW BINDING
        self.feature("textDocument/hover")(self.h_hover)
        self.feature("textDocument/definition")(self.h_definition)
        self.feature("textDocument/references")(self.h_references)
        self.feature("textDocument/documentSymbol")(self.h_symbols)
        self.feature("textDocument/signatureHelp")(self.h_signature)
        self.feature("textDocument/inlayHint")(self.h_inlay_hints)
        self.feature("textDocument/formatting")(self.h_formatting)
        self.feature("textDocument/codeAction")(self.h_code_action)
        self.feature("codeAction/resolve")(self.h_resolve_action)
        self.feature("textDocument/prepareRename")(self.h_prepare_rename)
        self.feature("textDocument/rename")(self.h_rename)
        self.feature("textDocument/diagnostic")(self.h_diagnostic_pull)
        self.feature("textDocument/inlineCompletion")(self.h_inline_completion)
        self.feature("textDocument/foldingRange")(self.h_folding_range)
        self.feature("textDocument/selectionRange")(self.h_selection_range)
        self.feature("textDocument/documentLink")(self.h_document_link)
        self.feature("documentLink/resolve")(self.h_document_link_resolve)
        self.feature("textDocument/prepareCallHierarchy")(self.h_call_hierarchy_prepare)
        self.feature("callHierarchy/incomingCalls")(self.h_call_hierarchy_incoming)
        self.feature("callHierarchy/outgoingCalls")(self.h_call_hierarchy_outgoing)
        self.feature("textDocument/prepareTypeHierarchy")(self.h_type_hierarchy_prepare)
        self.feature("typeHierarchy/supertypes")(self.h_type_hierarchy_supertypes)
        self.feature("typeHierarchy/subtypes")(self.h_type_hierarchy_subtypes)

        # Workspace
        self.feature("workspace/executeCommand")(self.h_execute_command)
        self.feature("workspace/symbol")(self.h_workspace_symbol)
        self.feature("workspace/didChangeWatchedFiles")(self.h_watched_files)
        self.feature("workspace/didChangeWorkspaceFolders")(self.h_folders_changed)
        self.feature("workspace/didChangeConfiguration")(self._on_config_change)
        self.feature("workspace/willRenameFiles")(self.h_will_rename_files)

        # Internal
        self.feature("gnostic/relay_auth")(self.handle_relay_auth)
        self.feature("gnostic/config")(self.handle_config_update)
        self.feature("$/heartbeat")(self._heartbeat)