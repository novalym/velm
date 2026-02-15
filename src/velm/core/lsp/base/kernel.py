# Path: core/lsp/base/kernel.py
# ----------------------------
# LIF: INFINITY | ROLE: HEART_OF_THE_ENGINE | RANK: SOVEREIGN
# =================================================================================
# == THE GNOSTIC KERNEL (V-Ω-TOTALITY-V24-ORCHESTRATOR)                          ==
# =================================================================================

import os
import sys
import time
import signal
import threading
import uuid
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, Callable, Union, List, Type, Set

# --- BASE ORGANS ---
from .state import ServerState, RequestContext
from .telemetry import forensic_log
from .foundry import KineticFoundry
from .dispatcher import NeuralDispatcher
from .manager import DocumentLibrarian
from .governor import LifecycleGovernor
from .contracts import BaseGnosticObject
from .errors import JsonRpcError, ErrorCodes

# --- PROTOCOL UPLINKS ---
from .protocol import JsonRpcEndpoint, LspStream, StdioStream
from .types import (
    ServerCapabilities, ClientCapabilities, InitializeParams,
    MessageType, ShowMessageParams, LogMessageParams,
    WorkDoneProgressOptions, ProgressToken
)


class BaseLSPServer(BaseGnosticObject):
    """
    =============================================================================
    == THE UNIVERSAL MIND (V-Ω-KERNEL-ULTIMA)                                  ==
    =============================================================================
    A high-performance, modular foundation for all Gnostic Language Servers.
    It orchestrates the physical transport, the execution foundry, and the
    dynamic negotiation of capabilities.
    """

    def __init__(self, stream: Optional[LspStream] = None):
        super().__init__(name="BaseLSPServer")

        # --- 1. THE BODILY ORGANS ---
        self.stream = stream or StdioStream()
        self.endpoint = JsonRpcEndpoint(stream=self.stream)

        # --- 2. THE NEURAL STRATA ---
        self.foundry = KineticFoundry()
        self.dispatcher = NeuralDispatcher(self)
        self.documents = DocumentLibrarian(self)
        self.governor = LifecycleGovernor(self)

        # --- 3. STATE & REGISTRY ---
        self._features: Dict[str, Callable] = {}
        self._commands: Dict[str, Callable] = {}
        self._capability_providers: List[Callable[[ServerCapabilities], None]] = []
        self._event_listeners: Dict[str, List[Callable]] = {}

        self._state_lock = threading.RLock()
        self._ctx = RequestContext()

        self.state = ServerState.DORMANT
        self.is_shutdown = False
        self.client_capabilities: Optional[ClientCapabilities] = None
        self.client_info: Optional[Any] = None
        self.project_root: Optional[Path] = None

        # --- 4. CONSECRATION ---
        self._bind_foundational_rites()

    def use(self, middleware: Callable):
        """
        [RITE]: INJECT_MIDDLEWARE
        Registers a global interceptor for all requests.
        Example: server.use(logging_middleware)
        """
        self.dispatcher.use(middleware)

    def _bind_foundational_rites(self):
        """Maps the immutable laws of the protocol to the Governor and Siphon."""
        # Lifecycle (Handled by Governor)
        self.feature("initialize")(self.governor.initialize)
        self.feature("initialized")(self.governor.initialized)
        self.feature("shutdown")(self.governor.shutdown)
        self.feature("exit")(self.governor.exit)

        # Vitality
        self.feature("$/heartbeat")(self._heartbeat)

        # Resource Management
        self.feature("$/cancelRequest")(self.foundry.cancel)

        # Document Sync (Handled by Librarian/Siphon)
        self.feature("textDocument/didOpen")(self.documents.open)
        self.feature("textDocument/didChange")(self.documents.change)
        self.feature("textDocument/didClose")(self.documents.close)

        # Workspace
        self.feature("workspace/didChangeConfiguration")(self._on_config_change)
        self.feature("workspace/didChangeWorkspaceFolders")(self._on_workspace_folders_change)

    # =============================================================================
    # == ASCENSION 1 & 2: THE DECORATOR PANTHEON                                 ==
    # =============================================================================

    def feature(self, method: str):
        """
        [DECORATOR]
        Registers a handler for a specific LSP method (e.g. 'textDocument/hover').
        """

        def decorator(func: Callable):
            with self._state_lock:
                self._features[method] = func
            return func

        return decorator

    def command(self, command_name: str):
        """
        [DECORATOR]
        Registers a handler for a specific Workspace Command (e.g. 'scaffold.run').
        """

        def decorator(func: Callable):
            with self._state_lock:
                self._commands[command_name] = func
            return func

        return decorator

    def on(self, event_name: str):
        """
        [DECORATOR]
        Registers an internal event listener (e.g. 'file_saved').
        """

        def decorator(func: Callable):
            with self._state_lock:
                if event_name not in self._event_listeners:
                    self._event_listeners[event_name] = []
                self._event_listeners[event_name].append(func)
            return func

        return decorator

    # =============================================================================
    # == ASCENSION 3: DYNAMIC CAPABILITY SYNTHESIS                               ==
    # =============================================================================

    def register_capability(self, provider: Callable[[ServerCapabilities], None]):
        """
        [THE RITE OF EMPOWERMENT]
        Registers a callback that will mutate the ServerCapabilities object during initialization.
        Modules call this to announce their powers.
        """
        with self._state_lock:
            self._capability_providers.append(provider)

    def get_capabilities(self) -> ServerCapabilities:
        """
        [THE PROCLAMATION]
        Forges the Capabilities Manifest by aggregating all registered powers.
        """
        caps = ServerCapabilities(
            textDocumentSync=2,  # Incremental Sync by default
            workspace={
                "workspaceFolders": {
                    "supported": True,
                    "changeNotifications": True
                }
            }
        )

        # Poll all registered features to populate the manifest
        for provider in self._capability_providers:
            try:
                provider(caps)
            except Exception as e:
                forensic_log(f"Capability Provider Fracture: {e}", "ERROR", "KERNEL")

        return caps

    # =============================================================================
    # == THE MAIN EXECUTION LOOP                                                 ==
    # =============================================================================

    def run(self):
        """
        [THE EVENT HORIZON]
        The eternal read loop. Blocks the process and sustains the server's soul.
        """
        # --- 1. KERNEL PREPARATION ---
        # [ASCENSION 16]: BINARY GUARD
        if sys.platform == "win32":
            import msvcrt
            try:
                msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
                msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                forensic_log("Binary mode enforced for Windows IO.", "SUCCESS", "KERNEL")
            except Exception as e:
                forensic_log(f"Binary mode shift failed: {e}", "CRIT", "KERNEL")

        # [ASCENSION 24]: IDENTITY ASSUMPTION
        try:
            import setproctitle
            setproctitle.setproctitle("scaffold: oracle-lsp")
        except ImportError:
            pass

        # --- 2. SIGNAL INTERCEPTION ---
        # [ASCENSION 23]: GRACEFUL DISSOLUTION
        def _on_signal(sig, frame):
            forensic_log(f"Kernel Signal {signal.Signals(sig).name} intercepted.", "WARN", "LIFECYCLE")
            self.stop()
            sys.exit(0)

        if sys.platform != 'win32':
            signal.signal(signal.SIGINT, _on_signal)
            signal.signal(signal.SIGTERM, _on_signal)

        # --- 3. BIND SENSORS ---
        # Any packet arriving at the Endpoint is routed to the Neural Dispatcher
        self.endpoint.on_request = self.dispatcher.handle
        self.endpoint.on_notification = self.dispatcher.handle

        forensic_log(f"Oracle Heartbeat ignited. Channel: {self.stream.name()}", "SUCCESS", "KERNEL")

        # --- 4. THE ETERNAL SIPHON ---
        try:
            # This blocks until EOF or protocol dissolution
            self.endpoint.start()
        except Exception as catastrophic:
            forensic_log(f"Reality Collapse: {catastrophic}", "CRIT", "KERNEL", exc=catastrophic)
        finally:
            self.stop()

    def stop(self):
        """[THE FINAL RELEASE] Gracefully dissolves all modular organs."""
        with self._state_lock:
            if self.state == ServerState.VOID: return
            self.state = ServerState.VOID
            self.is_shutdown = True

            # [ASCENSION 22]: THE DRAIN
            self.foundry.shutdown(wait=True)

            self.endpoint.stop()
            self.documents.clear()

            forensic_log("Gnostic Kernel returned to the Void.", "SUCCESS", "KERNEL")

    # =============================================================================
    # == ASCENSION 6 & 7: COMMUNICATIONS & RELAY                                 ==
    # =============================================================================

    def show_message(self, message: str, type: MessageType = MessageType.Info):
        """[THE HERALD] Sends a toast notification to the Client."""
        params = ShowMessageParams(type=type, message=message)
        self.endpoint.send_notification("window/showMessage", params.model_dump(mode='json'))

    def log_message(self, message: str, type: MessageType = MessageType.Log):
        """[THE WHISPER] Sends a log message to the Client's output panel."""
        params = LogMessageParams(type=type, message=message)
        self.endpoint.send_notification("window/logMessage", params.model_dump(mode='json'))

    def report_progress(self, token: Union[int, str], title: str, percentage: Optional[int] = None,
                        message: Optional[str] = None, cancellable: bool = False):
        """[ASCENSION 5]: THE PROGRESS ORACLE"""
        payload = {
            "kind": "report",
            "message": message,
            "percentage": percentage
        }
        # Initial creation if needed, then update
        # Simplified for V1: Just send progress notification
        self.endpoint.send_notification("$/progress", {
            "token": token,
            "value": payload
        })

    def relay_request(self, method: str, params: Any) -> Any:
        """
        [ASCENSION 7]: THE SILVER CORD
        Hooks for subclasses to implement synchronous communication with the Daemon.
        Base implementation returns None.
        """
        return None

    def emit(self, event_name: str, payload: Any):
        """[ASCENSION 10]: THE EVENT BUS"""
        listeners = self._event_listeners.get(event_name, [])
        for listener in listeners:
            try:
                listener(payload)
            except Exception as e:
                forensic_log(f"Event Listener '{event_name}' fractured: {e}", "ERROR", "KERNEL")

    # =============================================================================
    # == ASCENSION 8-15: INTERNAL HANDLERS                                      ==
    # =============================================================================

    def _heartbeat(self, params: Any):
        """[ASCENSION 13]: VITALITY PULSE"""
        return {"alive": True, "state": self.state}

    def _on_config_change(self, params: Any):
        """[ASCENSION 8]: CONFIGURATION WATCHER"""
        settings = params.get("settings", {})
        # Dispatch internal event
        self.emit("configuration_changed", settings)
        # Check memory
        self._check_memory_pressure()

    def _on_workspace_folders_change(self, params: Any):
        """[ASCENSION 9]: WORKSPACE TRACKER"""
        event = params.get("event", {})
        added = event.get("added", [])
        removed = event.get("removed", [])

        # Delegate to Document Librarian
        if hasattr(self.documents, 'update_roots'):
            self.documents.update_roots(added, removed)

        forensic_log(f"Workspace Shift: +{len(added)} / -{len(removed)} sanctums.", "INFO", "KERNEL")

    def _check_memory_pressure(self):
        """
        =============================================================================
        == THE METABOLIC LUSTRATION INQUEST (V-Ω-TOTALITY-V20000.14-ISOMORPHIC)    ==
        =============================================================================
        LIF: 100x | ROLE: HEAP_SOVEREIGN_SENTINEL | RANK: OMEGA_SUPREME
        AUTH: Ω_MEMORY_V20000_HEAP_SUTURE_2026_FINALIS
        """
        import gc
        import os
        import sys
        import time

        # [ASCENSION 8]: HYSTERESIS WARD
        # Prevents "GC Thrashing" by enforcing a 2-second cooldown between lustrations.
        now = time.monotonic()
        if now - getattr(self, '_last_lustration_ts', 0) < 2.0:
            return

        try:
            # --- MOVEMENT I: SENSORY ADJUDICATION ---
            rss_mb = 0.0
            is_critical = False
            substrate = "IRON"

            try:
                # [THE HIGH PATH]: IRON CORE (NATIVE)
                import psutil
                process = psutil.Process()
                rss_mb = process.memory_info().rss / (1024 * 1024)
                # Adjudicate against the 1GB Native Wall
                if rss_mb > 1024:
                    is_critical = True
            except (ImportError, AttributeError, Exception):
                # [THE WASM PATH]: ETHEREAL PLANE (ETHER)
                # In WASM, physical RSS is veiled. We scry the Gnostic Mass.
                substrate = "ETHER"
                # Heuristic: 1 block in Pyodide is roughly 150-200 bytes of overhead
                # sys.getallocatedblocks() is part of the core Python Mind.
                blocks = sys.getallocatedblocks()
                rss_mb = (blocks * 0.0002)  # Crude estimate of Megabytes

                # Browser tabs have much lower ceilings. We trigger at 450MB.
                if rss_mb > 450:
                    is_critical = True

            # --- MOVEMENT II: THE RITE OF LUSTRATION ---
            if is_critical:
                self._last_lustration_ts = now

                # 1. THE HERALD'S CRY
                msg = f"Metabolic Wall Breached: {rss_mb:.2f}MB on [{substrate}]. Initiating Lustration..."
                # We use the internal forensic_log if manifest, else a standard log
                if 'forensic_log' in globals():
                    forensic_log(msg, "WARN", "KERNEL")
                else:
                    self.logger.warn(msg)

                # 2. CACHE EVAPORATION
                # Command the Alchemist to clear its template memory
                if hasattr(self, 'alchemist'):
                    try:
                        self.alchemist.env.cache.clear()
                    except:
                        pass

                # 3. THE GREAT LUSTRATION
                # Force a full, multi-generational garbage collection sweep.
                gc.collect()

                # 4. HUD RESONANCE
                # Multicast the event to the Ocular HUD via the Akashic link
                akashic = getattr(self.engine, 'akashic', None) if hasattr(self, 'engine') else None
                if akashic:
                    try:
                        akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {
                                "type": "MEMORY_PURGE",
                                "label": "METABOLIC_CLEANSING",
                                "color": "#f59e0b",
                                "value": rss_mb
                            }
                        })
                    except:
                        pass

            elif rss_mb > (512 if substrate == "IRON" else 256):
                # [ASCENSION 3]: THE LESSER LUSTRATION
                # Perform a Generation 1 collect to keep the heap lean without a full pause.
                gc.collect(1)

        except Exception as paradox:
            # [ASCENSION 9]: FAULT-ISOLATED PERCEPTION
            # The sentinel must be silent in failure to protect the primary Rite.
            pass

    # =============================================================================
    # == ASCENSION 21: TYPE-SAFE ROUTING HELPER                                  ==
    # =============================================================================

    @classmethod
    def diagnostic_route(cls, name: str):
        """
        A helper for tagging methods that are diagnostic routes.
        Useful for metadata extraction.
        """

        def wrapper(func):
            func._is_diagnostic_route = True
            func._route_name = name
            return func

        return wrapper