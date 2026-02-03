# Path: core/daemon/nexus/engine.py
# ---------------------------------
import socket
import threading
import json
import time
import os
import sys
import uuid
import gc
import logging
import traceback
from pathlib import Path
from typing import Optional, Dict, Any, List

# --- GNOSTIC INTERNAL UPLINKS ---
from ..constants import (
    PROTOCOL_VERSION, MAX_CONNECTIONS, DEFAULT_HOST,
    DEFAULT_PORT, HEARTBEAT_INTERVAL, CRASH_DUMP_FILE
)


class GnosticNexus:
    """
    =================================================================================
    == THE SOVEREIGN COORDINATOR (V-Ω-KINETIC-CORE-RESTORED)                       ==
    =================================================================================
    @gnosis:title The Gnostic Nexus (Kinetic Core)
    @gnosis:summary The Central Nervous System. Purified to handle ONLY Kinetic Rites.
                     LSP Intelligence has been exiled to a sibling process.
    @gnosis:LIF INFINITY
    @gnosis:auth_code: Ω_NEXUS_KINETIC_PURE

    This is the **Kinetic Engine**. It manages the heavy lifting: File Generation,
    Project Analysis, Docker Orchestration, and Shadow Realities.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Great Severance:** The `LSPKernel` and high-frequency `Hover/Completion`
        logic have been surgically removed. This process is now dedicated solely to
        Heavy Operations, preventing UI typing lag caused by background processing.
    2.  **Primordial Consecration (THE FIX):** `plugins` and `shadow` rites are loaded
        SYNCHRONOUSLY during ignition. The UI cannot race against them.
    3.  **Hyper-V Boot:** Garbage Collection is DISABLED (`gc.disable()`) during the
        heavy import phase to accelerate startup time.
    4.  **Forensic Crash Dump:** If `ignite()` fails, it writes a `daemon_crash.json`
        to disk immediately for post-mortem analysis.
    5.  **Socket Pre-Flight:** Verifies `localhost` resolution before binding to avoid
        IPv6/IPv4 timeouts.
    6.  **The Neural Fuse (Auto-Reset):** The broadcast circuit breaker self-heals
        after 5 seconds of silence.
    7.  **The Golden Handshake:** Raw stdout JSON injection for atomic CLI discovery.
    8.  **Memory Wall Enforcement:** Active RSS monitoring triggers aggressive GC.
    9.  **Parent Tether:** OS-level zombie process prevention via `kill(0)`.
    10. **Contextual Anchoring:** Atomic environment switching for Multi-Project support.
    11. **Trace ID Propagation:** Distributed tracing for every packet.
    12. **IO Stream Stabilization:** UTF-8 enforcement on Windows streams.
    """

    def __init__(self,
                 host: str = DEFAULT_HOST,
                 port: int = DEFAULT_PORT,
                 allow_remote: bool = False,
                 max_connections: int = MAX_CONNECTIONS,
                 auth_token: str = None,
                 instance_id: str = None,
                 parent_pid: int = None,
                 pulse_file: str = None,
                 memory_limit_mb: int = 1024,
                 **kwargs):

        # [ASCENSION 12]: IO STREAM STABILIZATION
        try:
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
            if hasattr(sys.stderr, 'reconfigure'):
                sys.stderr.reconfigure(line_buffering=True, encoding='utf-8')
        except Exception:
            pass

        self._lock = threading.RLock()
        self._start_time = time.time()
        self._shutdown_event = threading.Event()
        self.running = False

        # Identity Matrix
        self.instance_id = instance_id or f"nexus-{os.urandom(4).hex()}"
        self.host = "0.0.0.0" if allow_remote else host
        self.port = port
        self.max_connections = max_connections
        self.auth_token = auth_token or os.urandom(32).hex()
        self.parent_pid = parent_pid
        self.pulse_file = pulse_file
        self.memory_limit_mb = memory_limit_mb

        # The Lazy Organ Containers
        self._engine = None
        self._akashic = None
        self._surveyor = None
        self._dispatcher = None
        self._gatekeeper = None
        self._cortex = None
        # [NOTE]: _lsp_kernel is GONE.

        self.REQUEST_MAP = {}
        self.is_consecrated = False
        self.server_socket: Optional[socket.socket] = None
        self.reaper_thread: Optional[threading.Thread] = None

        # [ASCENSION 6]: FUSE STATE
        self._fuse_tripped = False
        self._fuse_reset_time = 0.0

        from ....logger import Scribe
        self.logger = Scribe("GnosticNexus")
        Scribe.register_hook(lambda pkt: self._filtered_broadcast(pkt))

        if kwargs:
            self.logger.debug(f"Nexus absorbed extra DNA: {list(kwargs.keys())}")

    # =========================================================================
    # == 1. THE LAZY ORGANS (JIT MATERIALIZATION)                            ==
    # =========================================================================

    @property
    def akashic(self):
        if self._akashic is None:
            from ..akashic import AkashicRecord
            self._akashic = AkashicRecord(persistence_path=".scaffold/akashic.jsonl")
        return self._akashic

    @property
    def engine(self):
        if self._engine is None:
            from ...runtime.engine import ScaffoldEngine
            # Disable auto-register to strictly control loading order
            self._engine = ScaffoldEngine(auto_register=False, silent=True)
            self._engine.akashic = self.akashic
            self._engine.nexus = self
        return self._engine

    @property
    def cortex(self):
        """
        [THE MIND]: The Gnostic Cortex.
        Retained here for `analyze` and `distill` rites (Heavy Analysis).
        Not used for LSP responsiveness.
        """
        if self._cortex is None:
            from ...cortex.engine import GnosticCortex
            self._cortex = GnosticCortex(Path(os.getcwd()))
        return self._cortex

    @property
    def dispatcher(self):
        """[THE BRAIN]: The Rite Dispatcher."""
        if self._dispatcher is None:
            from ..dispatcher import GnosticDispatcher
            self._dispatcher = GnosticDispatcher(self.engine, self.REQUEST_MAP)
        return self._dispatcher

    @property
    def gatekeeper(self):
        """[THE WARDEN]: The Network Interface."""
        if self._gatekeeper is None:
            if not self.server_socket:
                raise RuntimeError("Heresy: Cannot summon Gatekeeper before Socket Binding.")
            from .gatekeeper import Gatekeeper
            self._gatekeeper = Gatekeeper(
                self.server_socket,
                self.akashic,
                self.dispatcher,
                lambda: self.engine.project_root,
                self,
                max_connections=self.max_connections
            )
        return self._gatekeeper

    @property
    def surveyor(self):
        """[THE EYE]: The Workspace Monitor."""
        if self._surveyor is None:
            from ..surveyor.engine import GrandSurveyor
            self._surveyor = GrandSurveyor(self.akashic)
        return self._surveyor

    # =========================================================================
    # == 2. THE IGNITION RITE (STARTUP)                                      ==
    # =========================================================================

    def ignite(self):
        """
        =============================================================================
        == THE GRAND RITE OF IGNITION (V-Ω-TOTALITY-SESSION-AWARE)                 ==
        =============================================================================
        LIF: 10,000,000,000 | ROLE: REALITY_CONSECRATOR | RANK: SOVEREIGN

        [THE CURE]: This version anchors the Daemon into the Session-Scoped Akasha.
        It materializes the Network, Memory, and Logic layers as a single,
        forensically isolated reality.
        =============================================================================
        """
        with self._lock:
            if self.running:
                return

            # [ASCENSION 1]: TEMPORAL ANCHORING
            # High-precision timing to measure the "Snap" of inception.
            boot_start_ns = time.perf_counter_ns()

            # [ASCENSION 2]: HYPER-V METABOLIC SUPPRESSION
            # We silence the GC to prevent pauses during the heavy module import phase.
            import gc
            gc.disable()

            try:
                # --- MOVEMENT I: SPATIAL COORDINATION ---
                # [ASCENSION 3]: ISOMORPHIC PATH PURITY
                # We normalize the Sanctum Root for universal consistency.
                raw_root = self.project_root or os.getcwd()
                scaffold_root = Path(raw_root).resolve()
                self.project_root = str(scaffold_root).replace('\\', '/')

                # --- MOVEMENT II: AKASHIC INCEPTION ---
                # [ASCENSION 1]: THE CURE - SESSION-AWARE PERSISTENCE
                # We initialize the Akasha. It will automatically birth its own
                # SessionVault and 'traffic.jsonl' within .scaffold/sessions/
                from ..akashic import AkashicRecord
                self._akashic = AkashicRecord(
                    persistence_path=str(scaffold_root / ".scaffold" / "akashic.jsonl")
                )

                session_id = self._akashic.vault.id
                self.logger.success(f"Akashic Session Manifest: [cyan]{session_id}[/cyan]")

                # --- MOVEMENT III: NETWORK CONSECRATION ---
                # [ASCENSION 5]: FREQUENCY BINDING (Scout)
                from .scout import Scout
                self.server_socket = Scout.bind(self.host, self.port)
                # Capture actual port if auto-assigned via Port 0
                self.port = self.server_socket.getsockname()[1]

                # [ASCENSION 7]: GATEKEEPER VIGIL
                # Start the warden loop to manage incoming TCP synapses.
                self.gatekeeper.start_vigil()

                # --- MOVEMENT IV: SKILL AWAKENING ---
                # [ASCENSION 4]: PARALLEL CONTRACT INCEPTION
                # We load the essential artisans required for the first handshake.
                self._import_primordial_contracts()

                # [ASCENSION 6]: THE GOLDEN HANDSHAKE
                # Proclaim existence to the Electron Hypervisor via raw stdout.
                self._announce_presence()

                # --- MOVEMENT V: VITALITY VIGIL ---
                # [ASCENSION 10]: ZOMBIE REAPER SUMMONING
                # Ensures the Daemon does not survive its creator.
                self.reaper_thread = threading.Thread(
                    target=self._reaper_loop,
                    name="NexusReaper",
                    daemon=True
                )
                self.reaper_thread.start()

                # --- MOVEMENT VI: COGNITIVE PRE-WARM ---
                # [ASCENSION 9]: MERKLE CACHE WARMING
                # If we have a warm cortex, start indexing the filesystem in the background.
                if self._cortex:
                    threading.Thread(
                        target=self._background_awakening,
                        name="GnosticAwakening",
                        daemon=True
                    ).start()

                # --- FINALE: REALITY STABILIZED ---
                self.running = True

                # [ASCENSION 2b]: RESTORE METABOLISM
                gc.enable()

                boot_duration_ms = (time.perf_counter_ns() - boot_start_ns) / 1_000_000
                self.logger.success(
                    f"Nexus Ignition Complete. Port: {self.port}. Velocity: {boot_duration_ms:.2f}ms",
                    tags=["BOOT", "STABLE"]
                )

            except Exception as e:
                # [ASCENSION 11]: THE FORENSIC SARCOPHAGUS
                # Capture the exact coordinates of the inception failure.
                self._dump_crash_report(e)
                self.logger.critical(f"Ignition Fracture: {str(e)}")
                self.shutdown()
                raise e

    def _announce_presence(self):
        """[ASCENSION 7]: THE GOLDEN HANDSHAKE."""
        handshake = {
            "port": self.port,
            "token": self.auth_token,
            "pid": os.getpid(),
            "version": PROTOCOL_VERSION,
            "status": "WARM",
            "instance_id": self.instance_id,
            "capabilities": ["RITES", "SHADOW", "KINETIC"]
        }
        json_str = json.dumps(handshake)
        payload = f"\nDAEMON_JSON:{json_str}\n"

        try:
            if sys.__stdout__:
                sys.__stdout__.write(payload)
                sys.__stdout__.flush()
        except Exception:
            print(payload, flush=True)

    def _background_awakening(self):
        try:
            start = time.perf_counter()

            # The Consecrator loads the rest of the Grimoire (Generators, etc.)
            from ..registry.consecrator import PantheonConsecrator
            count = PantheonConsecrator.ignite(self)
            self.is_consecrated = True

            # Pre-Warm Cortex (for Analyze commands)
            _ = self.cortex

            gc.collect()

            duration = (time.perf_counter() - start) * 1000
            self.logger.success(f"Pantheon Fully Manifested in {duration:.2f}ms.")

        except Exception as e:
            self.logger.error(f"Background Awakening failed: {e}")

    def _import_primordial_contracts(self):
        """
        =============================================================================
        == THE RITE OF PRIMORDIAL CONSECRATION (V-Ω-TOTALITY-V2)                   ==
        =============================================================================
        LIF: INFINITY | ROLE: CONTRACT_ANCHOR | RANK: SOVEREIGN

        Registers the absolute essentials for System Management, Kinetic Rites,
        and the Workspace Observatory. These skills are manifest at the moment
        of ignition to prevent "Method Not Found" paradoxes during the Boot Storm.
        """
        self.logger.info("Awakening Primordial Contracts: System, Kinetic, and Observatory.")

        try:
            # --- 1. MATERIALIZE INTERFACE CONTRACTS (PYDANTIC) ---
            # We import the models used by the Dispatcher for Triage.
            from ....interfaces.requests import (
                InitializeRequest,
                IntrospectionRequest,
                GrandSurveyRequest,
                CliDispatchRequest,
                PluginsRequest,
                ShadowCloneRequest,
                AnalyzeRequest,
                WorkspaceRequest  # [ASCENSION 1]: Hoisted Workspace Contract
            )

            # --- 2. MATERIALIZE THE ARTISAN PANTHEON ---
            # We summon the hands that perform the work.
            from ....artisans.initialize.artisan import InitializeArtisan
            from ....artisans.surveyor.artisan import GrandSurveyArtisan
            from ....artisans.introspect.conductor import IntrospectionArtisan
            from ....artisans.cli_bridge.artisan import CliBridgeArtisan
            from ....artisans.plugins.artisan import PluginsArtisan
            from ....artisans.shadow_clone.artisan import ShadowCloneArtisan
            from ....artisans.analyze.artisan import AnalyzeArtisan
            from ....artisans.workspace.artisan import WorkspaceArtisan  # [ASCENSION 1]: Hoisted Workspace Artisan

            # --- 3. BIND THE REQUEST MAP (THE BRAIN) ---
            # Used by the TriageOfficer to validate incoming JSON payloads.
            self.REQUEST_MAP['initialize'] = InitializeRequest
            self.REQUEST_MAP['introspect'] = IntrospectionRequest
            self.REQUEST_MAP['grandSurvey'] = GrandSurveyRequest
            self.REQUEST_MAP['cli/dispatch'] = CliDispatchRequest
            self.REQUEST_MAP['plugins'] = PluginsRequest
            self.REQUEST_MAP['shadow'] = ShadowCloneRequest
            self.REQUEST_MAP['analyze'] = AnalyzeRequest
            self.REQUEST_MAP['workspace'] = WorkspaceRequest  # [ASCENSION 4]: Direct Binding

            # [ASCENSION 2]: THE ALIAS MULTICAST
            # We map multiple dialects to the same core contracts to satisfy diverse clients.
            self.REQUEST_MAP['scaffold/grandSurvey'] = GrandSurveyRequest
            self.REQUEST_MAP['scaffold/get-plugins'] = PluginsRequest
            self.REQUEST_MAP['scaffold/analyze'] = AnalyzeRequest
            self.REQUEST_MAP['scaffold/workspace'] = WorkspaceRequest
            self.REQUEST_MAP['observatory/list'] = WorkspaceRequest
            self.REQUEST_MAP['workspace/list'] = WorkspaceRequest

            # --- 4. CONSECRATE THE ARTISAN REGISTRY (THE HAND) ---
            # We instantiate the artisans and bind them to their respective requests.
            # Using the engine.register_artisan rite ensures the spine is synchronized.
            reg = self.engine.register_artisan

            reg(InitializeRequest, InitializeArtisan(self.engine))
            reg(GrandSurveyRequest, GrandSurveyArtisan(self))
            reg(IntrospectionRequest, IntrospectionArtisan(self.engine))
            reg(CliDispatchRequest, CliBridgeArtisan(self.engine))
            reg(PluginsRequest, PluginsArtisan(self.engine))
            reg(ShadowCloneRequest, ShadowCloneArtisan(self))
            reg(AnalyzeRequest, AnalyzeArtisan(self.engine))

            # [ASCENSION 3]: Atomic Workspace Activation
            reg(WorkspaceRequest, WorkspaceArtisan(self.engine))

            self.logger.success("Primordial Core is Whole. Observatory Link: [green]CONSECRATED[/green].")

        except Exception as e:
            # [ASCENSION 11]: CATASTROPHIC BOOT WARD
            # If the primordial contracts fail, the machine cannot function.
            self.logger.critical(f"Primordial Inception Fracture: {str(e)}")
            import traceback
            self.logger.debug(traceback.format_exc())
            # We do not raise here to allow the engine to attempt recovery or provide diagnostics.


    def _reaper_loop(self):
        """[ASCENSION 8 & 9]: ZOMBIE KILLER"""
        while self.running and not self._shutdown_event.is_set():
            try:
                # 1. Parent Watchdog
                if self.parent_pid:
                    try:
                        os.kill(self.parent_pid, 0)
                    except OSError:
                        self.logger.critical(f"Parent PID {self.parent_pid} dissolved. Terminal exit.")
                        self.shutdown()
                        os._exit(0)

                # 2. Memory Watchdog
                try:
                    import psutil
                    process = psutil.Process(os.getpid())
                    rss_mb = process.memory_info().rss / 1024 / 1024
                    if rss_mb > self.memory_limit_mb:
                        self.logger.warn(f"Critical Memory Ceiling [{rss_mb:.1f}MB]. Invoking GC.")
                        gc.collect()
                except ImportError:
                    pass

                # 3. Pulse Modulation
                tick_rate = HEARTBEAT_INTERVAL
                try:
                    if self.akashic:
                        vitals = self.akashic.get_telemetry
                        active_links = vitals.get("network", {}).get("active_witnesses", 0)
                        if active_links == 0: tick_rate *= 2
                except:
                    pass

                self._shutdown_event.wait(timeout=tick_rate)

            except Exception as e:
                time.sleep(2)

    def _filtered_broadcast(self, packet: Dict[str, Any]):
        """[ASCENSION 6]: THE NEURAL FUSE (Auto-Reset)"""
        if self._fuse_tripped:
            if time.time() - self._fuse_reset_time > 5.0:
                self._fuse_tripped = False  # Auto-Reset
                sys.stderr.write("[NEXUS] Broadcast Fuse Reset.\n")
            else:
                return

        try:
            if 'trace_id' not in packet:
                packet['trace_id'] = self.instance_id
            if self._akashic:
                self.akashic.broadcast(packet)
        except Exception:
            self._fuse_tripped = True
            self._fuse_reset_time = time.time()
            sys.stderr.write("[NEXUS] Broadcast Fuse Tripped. Silence Protocol Engaged.\n")

    def _dump_crash_report(self, error: Exception):
        """[ASCENSION 4]: FORENSIC REPORT"""
        try:
            report = {
                "error": str(error),
                "traceback": traceback.format_exc(),
                "timestamp": time.time(),
                "cwd": os.getcwd()
            }
            dump_path = Path(CRASH_DUMP_FILE)
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            dump_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        except:
            pass

    def shutdown(self):
        """[ASCENSION 12]: ATOMIC DISSOLUTION"""
        with self._lock:
            if not self.running: return
            self.running = False
            self._shutdown_event.set()

            if self._gatekeeper: self._gatekeeper.stop_vigil()
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
            if self._dispatcher: self._dispatcher.shutdown()
            if self._akashic: self._akashic.shutdown()

            self.logger.system("Nexus Dissolved.")

    @property
    def project_root(self):
        return self.engine.project_root

    @project_root.setter
    def project_root(self, path: str):
        """[ASCENSION 10]: CONTEXTUAL ANCHORING"""
        if path:
            clean_path = str(path).replace("\\", "/")
            self.engine.project_root = clean_path
            os.environ["SCAFFOLD_PROJECT_ROOT"] = clean_path

            # Re-anchor the Kinetic Cortex
            if self._cortex:
                self._cortex.root = Path(clean_path).resolve()
            self._last_anchor_ts = time.time()  # [NEW TRIGGER]
            self.logger.info(f"Nexus Anchor shifted to: {clean_path}")

    @property
    def active_connections(self) -> List[socket.socket]:
        try:
            return list(self.akashic.congregation._registry.keys())
        except:
            return []

    def __enter__(self):
        self.ignite()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()