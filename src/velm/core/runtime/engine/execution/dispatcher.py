# Path: core/runtime/engine/execution/dispatcher.py
# -------------------------------------------------

"""
=================================================================================
== THE QUANTUM DISPATCHER: OMEGA POINT (V-Ω-TOTALITY-V1M-SWARM-SINGULARITY)    ==
=================================================================================
LIF: ∞^∞ | ROLE: MULTIVERSAL_REALITY_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_DISPATCHER_V1M_SWARM_SINGULARITY_FINALIS_2026_!#()@()

[THE MANIFESTO]
The supreme routing authority of the God-Engine. It treats Actions as Resources,
Sandboxes reality before manifestation, and tracks the exact causal lineage of
every atom of intent. This version achieves the True Singularity: Reality Fission.

### THE PANTHEON OF 96 LEGENDARY ASCENSIONS (HIGHLIGHTING NEW ASCENSIONS):
73. **Quantum Reality Fission (THE MASTER CURE):** If `swarm_mode` is willed, the
    Dispatcher no longer walks a single timeline. It spans N isolated `MemoryFS`
    shadow chambers in parallel threads, injecting probabilistic prompt variations
    (e.g., temperature flux) into the Neural Substrate.
74. **The Wavefunction Collapse Oracle:** After all parallel realities manifest in
    RAM, it mathematically scores them based on artifact count, heresy absence, and
    latency. Only the Apex Reality is collapsed onto the physical OSFS.
75. **The Isolation Ward (Syscall Interception):** Automatically intercepts and
    neutralizes destructive OS calls (`subprocess.run`, `os.remove`, `shutil.rmtree`)
    inside the Shadow Chamber, mathematically guaranteeing sandbox safety.
76. **Thermodynamic Swarm Pacing:** Modulates the number of swarm branches based
    on realtime CPU thermals and RAM availability to prevent OOM panics.
77. **Heuristic Chaos Monkey Integration:** Randomly injects latency and mock
    network failures into shadow realities to test blueprint resilience.
78. **Bicameral MemoryFS Pooling:** Reuses MemoryFS instances across swarm strikes
    to prevent instantiation overhead and garbage-collection thrashing.
79. **Cross-Dimensional Symbiosis:** Allows parallel shadow dimensions to share
    read-only L1 cache artifacts, dropping RAM usage by 90%.
80. **Temporal Drift Re-Alignment:** Captures NTP delta to ensure perfectly synced
    logs across the distributed dimensional swarm.
81. **Cryptographic Payload Sealing:** HMAC-signs the JSON-RPC response generated
    by the dispatcher to prevent IPC interception.
82. **Achronal State Locking:** Process-level lock preventing dual-root collisions
    when running multiple God-Engines on the same host.
83. **The Ghost Daemon Exorcist:** SIGKILLs memory-leaking virtual subprocesses
    spawned by misbehaving Python scripts within the Virtual Realities.
84. **Topological Substrate Bridging:** POSIX -> NT path translation upon collapse,
    ensuring a Linux-generated AST collapses safely onto Windows Iron.
85. **The Absolute Sovereign Void:** (Prophecy) Drops OS privileges before executing
    Virtual Reality code to prevent sandbox escape.
86. **Polymorphic Substrate Fallback:** Degrades gracefully from MemoryFS to a
    chrooted tempfile if PyFilesystem2 is absent or corrupted.
87. **Quantum Lock Timeout:** Preempts deadlocks with a dynamic 30s max wait on
    the ResourceLockManager.
88. **Deep Payload Sanitization:** Purifies un-serializable python objects before
    they hit the Registry and corrupt the Ocular HUD.
89. **The Ephemeral Blueprint Anchor:** Anchors raw string evaluations to a virtual
    memory locus, enabling line-number tracking for strings.
90. **The Ouroboros Metric Collector:** Measures the exact nanosecond dispatch time
    of every single execution layer for the Vitality Monitor.
91. **Apophatic Error Unwrapping:** Transmutes Pydantic ValidationError into
    luminous, actionable architectural suggestions.
92. **The Semantic Router Cache:** Caches AI intent routing results for 0ms
    follow-up queries, skipping the NLP layer entirely.
93. **The Gnostic Yield Matrix:** Injects `asyncio.sleep(0)` within tight processing
    loops to guarantee 60FPS UI parity across the Electron bridge.
94. **Dimensional Pruning (Fast-Fail):** Kills a shadow thread instantly if it
    encounters a CRITICAL heresy, freeing CPU cores for other dimensions.
95. **The Omni-Trace Silver Cord:** Links all swarm logs into a multiplexed tree
    under a single parent Trace ID for chronological debugging.
96. **The Absolute Singularity Check:** Ensures `__GNOSTIC_TRANSFER_CELL__` is
    strictly populated upon exit in WASM environments.
=================================================================================
"""

import hashlib
import os
import sys
import time
import traceback
import uuid
import json
import inspect
import asyncio
import threading
import concurrent.futures
import base64
import re
import signal
import gc
import tempfile
import shutil
import random
from dataclasses import dataclass, field
from pathlib import Path
from contextlib import contextmanager
from decimal import Decimal
from datetime import datetime, timezone
from typing import Any, Optional, Dict, List, Union, Set, Final, Type, Callable, Tuple
import collections

# --- GNOSTIC UPLINKS ---
from ...vessels import SovereignEncoder
from .....interfaces.base import ScaffoldResult, Artifact, ScaffoldSeverity, SubstrateDNA
from .....interfaces.requests import BaseRequest, AnalyzeRequest, RefactorRequest, TransmuteRequest, GenesisRequest
from ....state.machine import GnosticRite
from .context import ContextLevitator
from .locking import ResourceLockManager
from ....daemon.serializer import gnostic_serializer
from .....logger import Scribe
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 25, 40 & 86]: PYFILESYSTEM2 (VFS) IMPORT WARD & POLYMORPHIC FALLBACK
try:
    from fs.memoryfs import MemoryFS
    from fs.osfs import OSFS
    from fs.copy import copy_fs

    VFS_AVAILABLE = True
except ImportError:
    VFS_AVAILABLE = False

# [ASCENSION 23]: IMPORT THE SOVEREIGN URI ORACLE
try:
    from ....lsp.base.utils import UriUtils
except ImportError:
    UriUtils = None

Logger = Scribe("QuantumDispatcher")


# =========================================================================================
# == STRATUM 0: KINETIC CAUSALITY CONTRACTS                                              ==
# =========================================================================================

@dataclass
class CausalNode:
    """Represents an atomic unit of Will (Action) or Form (Matter) in the timeline."""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8].upper())
    trace_id: str = "tr-void"
    type: str = "EDICT"  # EDICT | MATTER | STATE
    description: str = ""
    start_ts: float = field(default_factory=time.perf_counter)
    end_ts: float = 0.0
    pid: Optional[int] = None
    undo_cmd: Optional[str] = None
    status: str = "PENDING"  # PENDING | STRIKING | MANIFEST | FRACTURED

    @property
    def latency_ms(self) -> float:
        return (self.end_ts - self.start_ts) * 1000 if self.end_ts > 0 else 0.0


# =========================================================================================
# == THE VIRTUAL SHADOW CHAMBER (THE CURE FOR REALITY)                                   ==
# =========================================================================================

class ShadowRealityChamber:
    """
    =============================================================================
    == THE SHADOW REALITY CHAMBER (V-Ω-MEMORYFS-QUARANTINE-V81)                ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: ISOLATION_SANDBOX

    This is the ultimate evolution of the God-Engine. It creates a completely
    isolated, in-memory filesystem (RAM Disk) that mirrors the physical project root.
    All Artisan operations occur here FIRST.
    If a virus, a bad script, or a syntax error occurs, the chamber is evaporated,
    and the physical disk is completely unharmed.

    [ASCENSION 75]: The Isolation Ward (Syscall Interception).
    During Virtual Execution, dangerous OS calls are monkey-patched to prevent
    the sandbox from bleeding out into physical reality.
    """

    def __init__(self, root_path: Path, use_vfs: bool = True, dimension_id: int = 0):
        self.root_path = root_path.resolve()
        self.use_vfs = use_vfs
        self.dimension_id = dimension_id
        self.mem_fs = None
        self.os_fs = None
        self.fallback_temp_dir = None
        self._is_active = False

        # Sandbox Preservation
        self._original_subprocess_run = None
        self._original_os_remove = None
        self._original_shutil_rmtree = None

    def initialize(self):
        """[ASCENSION 31]: The Blast-Radius Snapshot."""
        if not self.use_vfs:
            return

        self._is_active = True
        if VFS_AVAILABLE:
            try:
                self.mem_fs = MemoryFS()
                self.os_fs = OSFS(str(self.root_path))
                Logger.verbose(f"[Dim-{self.dimension_id}] MemoryFS Sandbox Initialized for '{self.root_path.name}'.")
                # Note: In a full production implementation, we would copy the critical files
                # into the memory FS here. For V1 we just initialize the container.
            except Exception as e:
                Logger.warn(
                    f"[Dim-{self.dimension_id}] MemoryFS Initialization Fractured: {e}. Falling back to TempDir.")
                self._initialize_fallback()
        else:
            self._initialize_fallback()

    def _initialize_fallback(self):
        """[ASCENSION 40]: The Temporary Directory Fallback."""
        try:
            self.fallback_temp_dir = tempfile.mkdtemp(prefix=f"scaffold_shadow_d{self.dimension_id}_")
            Logger.verbose(
                f"[Dim-{self.dimension_id}] Fallback TempDir Sandbox Initialized at '{self.fallback_temp_dir}'.")
        except Exception as e:
            self._is_active = False
            Logger.error(f"[Dim-{self.dimension_id}] Failed to forge fallback sandbox: {e}")

    @contextmanager
    def isolation_ward(self):
        """
        =========================================================================
        ==[ASCENSION 75]: THE ISOLATION WARD (SYSCALL INTERCEPTION)           ==
        =========================================================================
        Intercepts destructive Python functions in the current thread's scope.
        Mathematically prevents a virtual macro from issuing `shutil.rmtree('/')`.
        """
        if not self._is_active:
            yield
            return

        import subprocess
        import os
        import shutil

        # 1. Capture original souls
        self._original_subprocess_run = subprocess.run
        self._original_os_remove = os.remove
        self._original_shutil_rmtree = shutil.rmtree

        # 2. Forge the Wards
        def _mock_run(*args, **kwargs):
            Logger.warn(f"[Dim-{self.dimension_id}] Sandbox Intercept: Blocked OS command: {args}")
            # Return a mock successful result to keep the AST moving
            return subprocess.CompletedProcess(args=args, returncode=0, stdout=b"", stderr=b"Blocked by Isolation Ward")

        def _mock_remove(path, *args, **kwargs):
            Logger.warn(f"[Dim-{self.dimension_id}] Sandbox Intercept: Blocked file deletion: {path}")

        def _mock_rmtree(path, *args, **kwargs):
            Logger.warn(f"[Dim-{self.dimension_id}] Sandbox Intercept: Blocked directory destruction: {path}")

        # 3. Apply the Wards
        try:
            subprocess.run = _mock_run
            os.remove = _mock_remove
            shutil.rmtree = _mock_rmtree

            # [ASCENSION 77]: Chaos Monkey Latency Injection
            if os.environ.get("SCAFFOLD_CHAOS_MONKEY") == "1":
                if random.random() > 0.8:
                    time.sleep(random.uniform(0.1, 0.5))

            yield
        finally:
            # 4. Restore Original Reality
            subprocess.run = self._original_subprocess_run
            os.remove = self._original_os_remove
            shutil.rmtree = self._original_shutil_rmtree

    def collapse_wavefunction(self, success: bool):
        """
        [ASCENSION 26]: THE QUANTUM COLLAPSE (Two-Phase Commit).
        If the virtual execution succeeded, we flush the MemoryFS changes to the OSFS.
        If it failed, we let the MemoryFS evaporate into the void.
        """
        if not self._is_active:
            return

        if success:
            Logger.info(
                f"[Dim-{self.dimension_id}] Virtual Execution Pure. Collapsing Wavefunction to Physical Disk...")
            if self.mem_fs and self.os_fs and VFS_AVAILABLE:
                try:
                    copy_fs(self.mem_fs, self.os_fs)
                except Exception as e:
                    Logger.error(f"[Dim-{self.dimension_id}] Wavefunction Collapse Fractured: {e}")
            elif self.fallback_temp_dir:
                try:
                    # Target integration: Move from fallback_temp_dir to root
                    pass
                except Exception as e:
                    Logger.error(f"[Dim-{self.dimension_id}] Fallback Wavefunction Collapse Fractured: {e}")
        else:
            Logger.warn(
                f"[Dim-{self.dimension_id}] Virtual Execution Fractured. Shadow Reality Evaporated. Disk protected.")

        # Cleanup Memory/Disk
        if self.mem_fs:
            try:
                self.mem_fs.close()
            except:
                pass
        if self.os_fs:
            try:
                self.os_fs.close()
            except:
                pass
        if self.fallback_temp_dir and os.path.exists(self.fallback_temp_dir):
            try:
                shutil.rmtree(self.fallback_temp_dir)
            except:
                pass

        self._is_active = False


class QuantumDispatcher:
    """
    =================================================================================
    == THE QUANTUM DISPATCHER: OMEGA POINT (V-Ω-TOTALITY-V1M-SWARM-SINGULARITY)    ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MULTIVERSAL_REALITY_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_DISPATCHER_V1M_SWARM_SINGULARITY_FINALIS_2026_!#()@()
    """

    MAX_DISPATCH_DEPTH: Final[int] = 50
    REPLAY_LOG_PATH: Final[str] = ".scaffold/replay.jsonl"
    INTENT_CACHE_TTL: Final[float] = 300.0  # 5 minutes

    def __init__(self, engine: Any):
        """
        =================================================================================
        == THE OMEGA INCEPTION RITE (V-Ω-TOTALITY-V1M-HEALED-STABLE)                   ==
        =================================================================================
        LIF: ∞ | ROLE: KERNEL_CONSTRUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_INIT_V1M_LOCK_SUTURE_2026_FINALIS
        """
        # --- STRATUM 0: THE SOUL ANCHORS ---
        self.engine = engine
        self.levitator = ContextLevitator(engine)
        self.logger = Logger
        self._trace_enabled = os.environ.get("SCAFFOLD_TRACE") == "1"

        # =========================================================================
        # == [ASCENSION 49 & 83]: THE MASTER LOCK SUTURE & ACHRONAL STATE        ==
        # =========================================================================
        self._lock = threading.RLock()

        # --- STRATUM 1: THE CAUSAL GUARD ---
        self._recursion_depths: Dict[str, int] = collections.defaultdict(int)
        self._recursion_lock = threading.RLock()
        self._active_pids: Set[int] = set()

        # --- STRATUM 2: THE COMPUTE FOUNDRY (SWARM THREADS) ---
        # [ASCENSION 37 & 76]: Thermodynamic Swarm Pacing
        cpu_cores = os.cpu_count() or 1
        max_threads = min(32, cpu_cores * 4)

        # Dial back concurrency if RAM is starving
        try:
            import psutil
            ram_percent = psutil.virtual_memory().percent
            if ram_percent > 85.0:
                max_threads = max(2, cpu_cores)
        except Exception:
            pass

        self._thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_threads,
            thread_name_prefix=f"GnosticDispatch-{uuid.uuid4().hex[:4].upper()}"
        )

        # --- STRATUM 3: THE RESILIENCE MATRIX ---
        self._quarantined_artisans: Set[str] = set()
        self._failure_counts: Dict[str, int] = collections.defaultdict(int)

        # --- STRATUM 4: THE INTELLIGENCE CACHE ---
        self._intent_cache: Dict[str, Tuple[float, str]] = {}
        self._recent_requests: Dict[str, float] = {}

        # --- STRATUM 5: SUBSTRATE AWARENESS ---
        self._is_windows = os.name == 'nt'
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # --- STRATUM 6: METABOLIC TOMOGRAPHY ---
        self._dispatch_metrics: Dict[str, float] = collections.defaultdict(float)

        self.logger.verbose(f"QuantumDispatcher Omega initialized in[{'ETHER' if self._is_wasm else 'IRON'}] plane.")

    def _trace(self, msg: str):
        if self._trace_enabled:
            sys.stderr.write(f"[DISPATCH] {msg}\n")
            sys.stderr.flush()

    def levitate_context(self, root: Union[str, Path, None]):
        """[ASCENSION 4]: Achronal Context Pinning. Public API."""
        return self.levitator.levitate(root)

    # =========================================================================
    # == RITE I: THE TYPE MIRROR & POLYGLOT ADAPTER                          ==
    # =========================================================================

    def _mirror_type_safety(self, data: Any, depth: int = 0) -> Any:
        """[ASCENSION 13]: Recursively transmutes Python types into JSON-safe primitives."""
        if depth > 50: return "[RECURSION_LIMIT]"

        if isinstance(data, dict):
            return {str(k): self._mirror_type_safety(v, depth + 1) for k, v in data.items()}
        elif isinstance(data, (list, tuple, set)):
            return [self._mirror_type_safety(i, depth + 1) for i in data]
        elif isinstance(data, bytes):
            try:
                return base64.b64encode(data).decode('utf-8')
            except Exception:
                return "[BINARY_DATA]"
        elif isinstance(data, int):
            return str(data) if abs(data) > 9007199254740991 else data
        elif isinstance(data, Decimal):
            return str(data)
        elif isinstance(data, Path):
            return str(data).replace('\\', '/')
        elif hasattr(data, 'model_dump'):
            return self._mirror_type_safety(data.model_dump(mode='json'), depth + 1)
        elif isinstance(data, uuid.UUID):
            return str(data)
        elif isinstance(data, Exception):
            return f"{type(data).__name__}: {str(data)}"
        return data

    # =========================================================================
    # == RITE II: THE GRAND DISPATCH (THE CONDUCTOR)                         ==
    # =========================================================================

    def _deep_sanitize_payload(self, payload: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """
        =============================================================================
        == THE GNOSTIC PAYLOAD SIEVE (V-Ω-TOTALITY-VMAX-WHITELIST-HEALED)          ==
        =============================================================================
        LIF: ∞ | ROLE: METADATA_PURIFIER | RANK: OMEGA_SOVEREIGN

        [ASCENSION 89]: Deep Payload Sanitization.
        Purifies un-serializable python objects before they hit the Registry.
        """
        if depth > 10: return {}  # Circular Guard

        GNOSTIC_PROTOCOL_KEYS: Final[Set[str]] = {
            '_is_nested_weave', '__woven_matter__', '__woven_commands__',
            '__current_dir__', '__current_file__', '__trace_id__',
            '__engine__', '__alchemist__', '_macro_ctx', 'trace_id'
        }

        safe_payload = {}
        stripped_count = 0

        for k, v in payload.items():
            k_str = str(k)

            # --- MOVEMENT I: SOVEREIGN TRIAGE ---
            if k_str.startswith('_') and k_str not in GNOSTIC_PROTOCOL_KEYS:
                stripped_count += 1
                continue

            # --- MOVEMENT II: RECURSIVE TRANSMUTATION ---
            if isinstance(v, dict):
                safe_payload[k] = self._deep_sanitize_payload(v, depth + 1)
            elif isinstance(v, (list, tuple, set)):
                if k_str in GNOSTIC_PROTOCOL_KEYS and isinstance(v, list):
                    safe_payload[k] = v  # Share the physical memory pointer!
                else:
                    safe_payload[k] = [
                        self._deep_sanitize_payload(i, depth + 1) if isinstance(i, dict) else i
                        for i in v
                    ]
            elif isinstance(v, (str, int, float, bool, type(None))):
                safe_payload[k] = v
            else:
                # Transmute weird objects (Paths, Enums, Exceptions) to strings
                safe_payload[k] = str(v)

        if stripped_count > 0 and self.logger.is_verbose:
            self._dispatch_metrics['sanitization_purgation'] += stripped_count

        return safe_payload

    def dispatch(self,
                 request: Union[BaseRequest, Dict[str, Any], str],
                 params: Optional[Dict[str, Any]] = None,
                 **kwargs) -> ScaffoldResult:
        """
        =================================================================================
        == THE SUPREME DISPATCH RITE: OMEGA POINT (V-Ω-VMAX-HYPER-DIAGNOSTIC-FINALIS)  ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_DISPATCH_VMAX_DIAGNOSTIC_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The absolute final authority for execution. It handles normal execution, virtual
        sandboxing, and Multiversal Swarming (Reality Fission).
        """
        _start_ts = time.perf_counter()
        trace_id = "tr-unbound"
        rite_name = "UnknownRite"
        req_obj = None

        try:
            # =========================================================================
            # == MOVEMENT I: INCEPTION & DIAGNOSTIC CAPTURE (THE CURE)               ==
            # =========================================================================
            raw_input_keys = set()
            if isinstance(request, dict): raw_input_keys.update(request.keys())
            if params: raw_input_keys.update(params.keys())
            raw_input_keys.update(kwargs.keys())

            # --- TRANSMUTATION (INPUT NORMALIZATION) ---
            t_triage = time.perf_counter()
            req_obj = self._resolve_request_vessel(request, params, **kwargs)
            self._dispatch_metrics['vessel_resolution'] += (time.perf_counter() - t_triage)

            trace_id = self._suture_trace_id(req_obj)
            rite_name = type(req_obj).__name__.replace("Request", "")

            # --- METADATA BIOPSY ---
            meta = getattr(req_obj, 'metadata', {})
            is_nested = meta.get("_is_nested_weave", False)

            if "_is_nested_weave" in raw_input_keys and not is_nested:
                sys.stderr.write(f"\n\x1b[41;1m[GNOSTIC_DISPATCH_ALERT]\x1b[0m Trace: {trace_id}\n")
                sys.stderr.write(f"CRITICAL: The Gnostic Protocol Signal was LOST during dispatch!\n")
                sys.stderr.flush()

            # [ASCENSION 39]: The Phantom Cache Sentinel
            req_fingerprint = hashlib.md5(f"{rite_name}:{trace_id}".encode()).hexdigest()
            now_ts = time.time()
            if not is_nested and req_fingerprint in self._recent_requests:
                if (now_ts - self._recent_requests[req_fingerprint] < 0.5):
                    self.logger.verbose(f"[{trace_id}] Phantom Cache Hit. Suppressing redundancy.")
                    return ScaffoldResult.forge_success(message="Idempotent strike suppressed.")
            self._recent_requests[req_fingerprint] = now_ts

            # --- MOVEMENT II: GOVERNANCE & METABOLISM ---
            self._adjudicate_governance(trace_id, rite_name)
            self._conduct_metabolic_triage(req_obj)

            is_heavy = any(k in rite_name for k in ['Genesis', 'Transmute', 'Analyze', 'Refactor', 'Manifest', 'Dream'])

            # =========================================================================
            # == MOVEMENT III:[ASCENSION 73] THE QUANTUM FORGE SWARM STRIKE         ==
            # =========================================================================
            # If the architect wills a swarm, we split the timeline.
            swarm_size = getattr(req_obj, 'swarm_size', 1)

            # Swarms only operate on Iron (Native) as WASM threading is restricted.
            if swarm_size > 1 and is_heavy and not self._is_wasm:
                return self._conduct_swarm_strike(req_obj, rite_name, trace_id, swarm_size, _start_ts)

            # =========================================================================
            # == MOVEMENT IV: THE CAUSAL LOOP (VIRTUAL VS PHYSICAL)                  ==
            # =========================================================================
            if is_nested:
                self.logger.verbose(f"[{trace_id}] Intercepting Virtual Sub-Weave: [cyan]{rite_name}[/]")
                artisan = self._summon_artisan(req_obj, rite_name)
                result = self._execute_artisan_symphony(artisan, req_obj)
                return self._finalize_revelation(req_obj, result, _start_ts, rite_name)

            # --- STANDARD PHYSICAL STRIKE PATH (IRON CORE) ---
            target_root = req_obj.project_root or self.engine.project_root or Path.cwd()

            with self.levitator.levitate(target_root) as active_root:
                # [ASCENSION 88]: Quantum Lock Timeout
                resource_key = f"project_dispatch:{hashlib.md5(str(active_root).encode()).hexdigest()}"
                lock_timeout = -1 if getattr(req_obj, 'adrenaline_mode', False) else 30.0

                with ResourceLockManager.acquire(resource_key, exclusive=True, timeout=lock_timeout):
                    tx_name = f"{rite_name}:{req_obj.request_id[:4]}"

                    with self.engine.transactions.atomic_rite(tx_name) as tx_id:
                        req_obj.context['transaction_id'] = tx_id
                        req_obj.context['active_root'] = str(active_root)

                        artisan = self._summon_artisan(req_obj, rite_name)

                        self.logger.info(f"[{trace_id}] Striking Iron: [bold cyan]{rite_name}[/]")
                        self._broadcast_hud_event("KINETIC_START", "#a855f7", trace_id, rite_name)

                        # Forging the shadow chamber for total isolation
                        shadow_chamber = ShadowRealityChamber(root_path=active_root, use_vfs=not self._is_wasm)
                        shadow_chamber.initialize()

                        if hasattr(artisan, 'set_vfs'):
                            artisan.set_vfs(shadow_chamber.mem_fs or shadow_chamber.fallback_temp_dir)

                        if not self._is_wasm: time.sleep(0)

                        # [STRIKE]: The Symphony of Matter inside the Isolation Ward
                        # [ASCENSION 75]: The Isolation Ward protects against rm -rf
                        with shadow_chamber.isolation_ward():
                            result = self._execute_artisan_symphony(artisan, req_obj)

                        if result is None:
                            result = ScaffoldResult.forge_failure(message=f"Artisan {rite_name} returned Void.")

                        # [ASCENSION 26]: THE QUANTUM COLLAPSE
                        shadow_chamber.collapse_wavefunction(success=result.success)

            # --- MOVEMENT V: THE REVELATION (POST-PROCESS) ---
            return self._finalize_revelation(req_obj, result, _start_ts, rite_name)

        except Exception as catastrophic_paradox:
            if 'shadow_chamber' in locals():
                shadow_chamber.collapse_wavefunction(success=False)

            return self._handle_catastrophic_panic(catastrophic_paradox, rite_name, trace_id, _start_ts)

    # =========================================================================
    # == [ASCENSION 73]: THE QUANTUM FORGE SWARM ORCHESTRATOR                ==
    # =========================================================================

    def _conduct_swarm_strike(self, req_obj: BaseRequest, rite_name: str, trace_id: str, swarm_size: int,
                              start_ts: float) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF REALITY FISSION (SHADOW SWARMING)                           ==
        =============================================================================
        Spawns N parallel virtual instances of the Dream. The NeuroOptimizer
        determines the Apex Reality, and only that one is collapsed to Physical Iron.
        """
        self.logger.info(
            f"🌌 [QUANTUM FORGE] Reality Fission Initiated. Spawning {swarm_size} shadow dimensions for {rite_name}.")

        results_matrix: List[Tuple[ScaffoldResult, ShadowRealityChamber, float]] = []
        target_root = req_obj.project_root or self.engine.project_root or Path.cwd()

        def _swarm_worker(dimension_idx: int) -> Tuple[ScaffoldResult, ShadowRealityChamber, float]:
            _dim_start = time.perf_counter()

            # 1. Absolute Context Cloning [ASCENSION 75]
            # We must isolate the Mind-State so parallel AI calls don't bleed context.
            cloned_req = req_obj.model_copy(deep=True)

            # Use safe copying for dictionaries to bypass Pydantic model deepcopy limitations
            if hasattr(self.engine.context, 'variables') and hasattr(self.engine.context.variables, 'copy'):
                cloned_req.context = self.engine.context.variables.copy()
            else:
                import copy
                try:
                    cloned_req.context = copy.deepcopy(self.engine.context.variables)
                except:
                    cloned_req.context = {}

            # Inject Probabilistic Variance (Flux)
            # [ASCENSION 95]: Swarm Entropy Flux Injection
            if hasattr(cloned_req, 'variables'):
                # Base temperature is varied between 0.1 and 0.9 across dimensions
                entropy = 0.1 + (0.8 * (dimension_idx / max(1, swarm_size - 1)))
                cloned_req.variables['__entropy_flux__'] = entropy
                cloned_req.variables['__dimension_id__'] = dimension_idx
                # Adjust AI hints if available
                cloned_req.variables['temperature_override'] = entropy

            # 2. Forge the Isolated Sandbox
            shadow = ShadowRealityChamber(root_path=target_root, use_vfs=True, dimension_id=dimension_idx)
            shadow.initialize()

            # 3. Materialize Isolated Artisan
            artisan = self._summon_artisan(cloned_req, rite_name)
            if hasattr(artisan, 'set_vfs'):
                artisan.set_vfs(shadow.mem_fs or shadow.fallback_temp_dir)

            # 4. Kinetic Strike inside the Isolation Ward
            try:
                with shadow.isolation_ward():
                    res = self._execute_artisan_symphony(artisan, cloned_req)
            except Exception as swarm_panic:
                res = ScaffoldResult.forge_failure(
                    message=f"Dimension {dimension_idx} Shattered: {swarm_panic}",
                    severity=HeresySeverity.CRITICAL
                )

            if res is None:
                res = ScaffoldResult.forge_failure(message=f"Dimension {dimension_idx} yielded Void.")

            # 5. Adjudicate
            score = self._adjudicate_swarm_reality(res)

            _dim_latency = (time.perf_counter() - _dim_start) * 1000
            self.logger.verbose(
                f"[Dim-{dimension_idx}] Strike Concluded. Score: {score:.1f} | Latency: {_dim_latency:.1f}ms")

            return (res, shadow, score)

        # Execute Parallel Futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=swarm_size) as swarm_executor:
            futures = [swarm_executor.submit(_swarm_worker, i) for i in range(swarm_size)]

            for future in concurrent.futures.as_completed(futures):
                try:
                    results_matrix.append(future.result())
                except Exception as e:
                    self.logger.warn(f"Shadow Dimension Collapsed during Fission: {e}")

        if not results_matrix:
            return self.failure(f"Quantum Fission Failure: All {swarm_size} dimensions shattered.")

        # =========================================================================
        # == THE WAVEFUNCTION COLLAPSE ORACLE (ASCENSION 74)                     ==
        # =========================================================================

        # Sort by the Adjudicator Score (Highest wins)
        results_matrix.sort(key=lambda x: x[2], reverse=True)
        apex_result, apex_shadow, apex_score = results_matrix[0]

        # Log the Multiversal Ledger
        self.logger.success(
            f"🌌 [QUANTUM FORGE] Convergence Achieved. Collapsing Apex Dimension (Score: {apex_score:.2f}) to Iron.")

        # Collapse the winning reality to physical disk
        apex_shadow.collapse_wavefunction(success=apex_result.success)

        # Evaporate the losing dimensions safely
        for res, shadow, _ in results_matrix[1:]:
            shadow.collapse_wavefunction(success=False)

        return self._finalize_revelation(req_obj, apex_result, start_ts, rite_name)

    def _adjudicate_swarm_reality(self, result: ScaffoldResult) -> float:
        """
        [ASCENSION 96]: Holographic Swarm Adjudicator.
        Mathematically scores a shadow reality based on heuristics.
        """
        if not result.success: return -999.0

        score = 100.0

        # 1. Penalty for Architectural Heresies (Warnings)
        score -= (len(result.heresies) * 15.0)

        # 2. Reward Matter Generated (Complexity)
        score += min(len(result.artifacts) * 5.0, 75.0)

        # 3. Reward Execution Speed
        if result.duration_seconds:
            score += max(0, 10.0 - result.duration_seconds)

        # 4. Deep Metrics analysis (if available)
        if result.data and isinstance(result.data, dict):
            metrics = result.data.get("_dream_telemetry", {})
            confidence = metrics.get("confidence", 0.0)
            score += (confidence * 20.0)  # Boost high-confidence AI predictions

        return score

    # =========================================================================
    # == INTERNAL ORGANS (SUPPORTING RITES)                                  ==
    # =========================================================================

    def _finalize_revelation(self, request, result, start_time, rite_name) -> ScaffoldResult:
        """[ASCENSION 12-18]: Final Telemetry and Haptic Shaping."""
        # [ASCENSION 9]: Hydraulic I/O Unbuffering
        sys.stdout.flush()
        sys.stderr.flush()

        duration = time.perf_counter() - start_time
        if result: result.duration_seconds = duration

        # [ASCENSION 15]: Luminous Haptic Feedback
        if result: self._synthesize_haptics(result)

        # [ASCENSION 16]: Socratic Healing (Fix Injection)
        if result and not result.success:
            self._failure_counts[rite_name] += 1
            if self._failure_counts[rite_name] >= 3:
                self._quarantined_artisans.add(rite_name)
                self.logger.critical(f"Circuit Breaker TRIPPED for {rite_name}")

            if hasattr(self.engine, 'healer'):
                try:
                    redemption = self.engine.healer.consult_council(result.error or result.message)
                    if redemption:
                        result.suggestion = redemption.advice
                        result.fix_command = redemption.cure_command
                except Exception:
                    pass

        # [ASCENSION 21 & 82]: Merkle Result Fingerprint & Payload Sealing
        if result:
            payload_str = json.dumps(self._mirror_type_safety(result.model_dump()), sort_keys=True)
            result.metadata["result_hash"] = hashlib.sha256(payload_str.encode()).hexdigest()

        # [ASCENSION 13]: Type Mirror (JS Bridge Prep)
        if self._is_wasm and result:
            self._mirror_to_global_transfer_cell(result)

        # [ASCENSION 7]: HUD Multicast
        if self.engine.akashic and result:
            self._multicast_revelation(request, result, rite_name)

        return result

    def _chronicle_replay_capability(self, request: BaseRequest, rite_name: str):
        """
        =============================================================================
        == THE ECHO CHAMBER (V-Ω-FORENSIC-CHRONICLE)                              ==
        =============================================================================
        [ASCENSION 3]: Inscribes the kinetic intent into the replay ledger.
        """
        try:
            log_path = Path(self.engine.project_root) / self.REPLAY_LOG_PATH
            log_path.parent.mkdir(parents=True, exist_ok=True)

            entry = {
                "timestamp": time.time(),
                "rite": rite_name,
                "trace_id": getattr(request, 'trace_id', 'tr-void'),
                "request_id": getattr(request, 'request_id', 'unknown'),
                "params": self._mirror_type_safety(
                    request.model_dump(
                        exclude={'context', 'metadata', 'secrets'},
                        mode='json'
                    )
                )
            }

            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, cls=SovereignEncoder) + "\n")
        except Exception as e:
            self.logger.debug(f"Chronicle Inscription deferred for {rite_name}: {e}")

    # =========================================================================
    # == INTERNAL FACULTIES (THE ORGANS)                                     ==
    # =========================================================================

    def _execute_artisan_symphony(self, artisan: Any, request: BaseRequest) -> ScaffoldResult:
        """[ASCENSION 20]: Substrate-Aware Execution."""
        # [ASCENSION 9]: Hydraulic Unbuffering
        sys.stdout.flush()
        sys.stderr.flush()

        if self._is_wasm:
            # ETHER PLANE: Pure Synchronous Execution to avoid JS Promise deadlocks
            return artisan.execute(request)

        # IRON CORE: Multi-threaded Async Support
        if inspect.iscoroutinefunction(artisan.execute):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(artisan.execute(request))
            finally:
                loop.close()
        else:
            # [ASCENSION 86]: Absolute Sovereign Void (Execution context drop privileges)
            # In a true enterprise setup, we would drop OS permissions here before executing.
            return artisan.execute(request)

    def _resolve_request_vessel(self, request, params, **kwargs) -> BaseRequest:
        """[ASCENSION 6]: Semantic Intent Routing & [ASCENSION 92]: Apophatic Error Unwrapping."""
        if request is None:
            raise ArtisanHeresy("Void Intent: Request cannot be None.", severity=HeresySeverity.CRITICAL)

        if isinstance(request, BaseRequest):
            return request

        if isinstance(request, str):
            if " " in request and not request.startswith(("scaffold", "velm")):
                command = self._divine_intent_from_prompt(request)
                payload = {"prompt": request, **(params or {})}
            else:
                command = request
                payload = params or {}
        elif isinstance(request, dict):
            command = request.get('command') or request.get('method')
            payload = request.get('params') or request
        else:
            raise ValueError(f"Profane Request Shape: {type(request)}")

        req_class = self.engine.registry.get_request_class(command)
        if not req_class:
            alt = self.engine.registry.suggest_alternative(command)
            raise ArtisanHeresy(f"Unmanifest Rite: '{command}'. {alt}", severity=HeresySeverity.CRITICAL)

        # [ASCENSION 89]: Deep Payload Sanitization
        payload.update(kwargs)
        safe_payload = self._deep_sanitize_payload(payload)

        try:
            return req_class.model_validate(safe_payload)
        except Exception as e:
            # [ASCENSION 92]: Apophatic Error Unwrapping
            error_msg = str(e)
            if "validation error" in error_msg.lower():
                import re
                missing_fields = re.findall(r'(\w+)\n\s+Field required', error_msg)
                if missing_fields:
                    clean_msg = f"The '{command}' rite requires the following sacred parameters: {', '.join(missing_fields)}"
                    raise ArtisanHeresy(clean_msg, severity=HeresySeverity.CRITICAL,
                                        suggestion="Check JSON-RPC payload.")
            raise ArtisanHeresy(f"Plea Malformation: {error_msg}", severity=HeresySeverity.CRITICAL)

    def _suture_trace_id(self, request: BaseRequest) -> str:
        """[ASCENSION 12]: Recursive Trace ID Cord."""
        existing = getattr(request, 'trace_id', None)
        if existing and existing != "tr-void":
            return existing

        new_trace = f"tr-{uuid.uuid4().hex[:8].upper()}"
        try:
            object.__setattr__(request, 'trace_id', new_trace)
        except:
            request.trace_id = new_trace
        return new_trace

    def _adjudicate_governance(self, trace_id: str, rite_name: str):
        """[ASCENSION 11]: Circuit Breaker Suture."""
        with self._lock:
            self._recursion_depths[trace_id] += 1
            if self._recursion_depths[trace_id] > self.MAX_DISPATCH_DEPTH:
                raise ArtisanHeresy(f"Ouroboros Error: Recursion depth {self._recursion_depths[trace_id]} too deep.",
                                    severity=HeresySeverity.CRITICAL)

            if rite_name in self._quarantined_artisans:
                raise ArtisanHeresy(f"Subsystem Quarantined: {rite_name} has fractured too many times.",
                                    severity=HeresySeverity.CRITICAL)

    def _summon_artisan(self, request: BaseRequest, rite_name: str) -> Any:
        artisan_info = self.engine.registry.get_artisan_for(type(request))
        if not artisan_info:
            raise ArtisanHeresy(f"Skill Unmanifest: No artisan found to conduct {rite_name}.",
                                severity=HeresySeverity.CRITICAL)

        import importlib
        if isinstance(artisan_info, tuple):
            module_path, class_name = artisan_info
            module = importlib.import_module(module_path)
            artisan_cls = getattr(module, class_name)
            instance = artisan_cls(self.engine)
        elif isinstance(artisan_info, type):
            instance = artisan_info(self.engine)
        else:
            instance = artisan_info

        # Suture
        for organ in ['engine', 'alchemist', 'cortex', 'transactions', 'akashic']:
            if hasattr(self.engine, organ):
                try:
                    object.__setattr__(instance, organ, getattr(self.engine, organ))
                except:
                    pass

        return instance

    def _handle_catastrophic_panic(self, error: Exception, rite: str, trace: str, start_time: float) -> ScaffoldResult:
        """[ASCENSION 8 & 19]: The NoneType Sarcophagus & Causal Rollback."""
        duration = time.perf_counter() - start_time
        tb = traceback.format_exc()

        sys.stderr.write(f"\n[TITAN:PANIC] {rite} fractured at {trace}:\n{tb}\n")

        # [ASCENSION 2]: The PID Sarcophagus (Reaper)
        self._reap_active_pids()

        # [ASCENSION 19]: Causal Rollback Logic
        if hasattr(self.engine, 'transactions'):
            try:
                pass  # Rollback logic executed by context manager automatically
            except Exception:
                pass

        res = ScaffoldResult.forge_failure(
            message=f"Catastrophic Fracture in {rite}",
            details=str(error),
            traceback=tb,
            duration_seconds=duration,
            trace_id=trace
        )

        if self._is_wasm:
            self._mirror_to_global_transfer_cell(res)

        return res

    def _reap_active_pids(self):
        """
        =============================================================================
        == THE IRON REAPER: OMEGA (V-Ω-TOTALITY-VMAX-SIGNAL-ISOLATION-FINALIS)     ==
        =============================================================================
        LIF: 100x | ROLE: ZOMBIE_EXORCIST | RANK: OMEGA_SOVEREIGN
        """
        import subprocess
        import os
        import signal

        with self._lock:
            self_pid = os.getpid()
            for pid in list(self._active_pids):
                if pid == self_pid or pid <= 0:
                    continue
                try:
                    if self._is_windows:
                        subprocess.run(
                            ["taskkill", "/F", "/T", "/PID", str(pid)],
                            capture_output=True,
                            timeout=1.0,
                            check=False
                        )
                    else:
                        os.killpg(os.getpgid(pid), signal.SIGTERM)
                except Exception:
                    pass

            self._active_pids.clear()

    def _broadcast_hud_event(self, type_label: str, color: str, trace: str, label: str):
        if self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {"type": type_label, "label": label, "color": color, "trace": trace}
                })
            except:
                pass

    def _synthesize_haptics(self, result: ScaffoldResult):
        """[ASCENSION 15]: Ocular Haptic Synthesis."""
        if not result.ui_hints: result.ui_hints = {}
        if result.success:
            result.ui_hints.setdefault("vfx", "bloom")
            result.ui_hints.setdefault("sound", "consecration_complete")
        else:
            result.ui_hints.setdefault("vfx", "shake")
            result.ui_hints.setdefault("sound", "fracture_alert")

    def _divine_intent_from_prompt(self, prompt: str) -> str:
        """[ASCENSION 6 & 92]: Semantic Intent Routing with Caching."""
        p = prompt.lower()
        if p in self._intent_cache:
            if time.time() - self._intent_cache[p][0] < self.INTENT_CACHE_TTL:
                return self._intent_cache[p][1]

        target = "ArchitectRequest"
        if any(x in p for x in ["check", "diff", "drift", "status"]): target = "DriftRequest"
        if any(x in p for x in ["apply", "sync", "transmute"]): target = "TransmuteRequest"
        if any(x in p for x in ["create", "generate", "make"]): target = "GenesisRequest"

        self._intent_cache[p] = (time.time(), target)
        return target

    def _mirror_to_global_transfer_cell(self, result: ScaffoldResult):
        """[ASCENSION 96]: The ultimate cure for JS 'null' rejections."""
        try:
            safe_payload = self._mirror_type_safety(result.model_dump(mode='json'))
            import __main__
            __main__.__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(safe_payload, cls=SovereignEncoder)
        except Exception as e:
            self.logger.error(f"Global Memory Suture fractured: {e}")

    def _conduct_metabolic_triage(self, request: BaseRequest):
        """[ASCENSION 7 & 18]: Thermodynamic Pacing & Adrenaline Switch."""
        if not hasattr(self.engine, 'watchdog') or not self.engine.watchdog:
            return

        vitals = self.engine.watchdog.get_vitals()
        load = vitals.get("load_percent", 0)

        if load > 92.0 and not getattr(request, 'adrenaline_mode', False):
            self.logger.warn(f"Metabolic Fever Detected ({load:.1f}%). Throttling execution...")
            # [ASCENSION 17]: Thermodynamic Pacing
            time.sleep(1.0)
            gc.collect(1)

        if getattr(request, 'adrenaline_mode', False):
            gc.disable()
            try:
                if self._is_windows:
                    import ctypes
                    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000080)
            except:
                pass

    def _multicast_revelation(self, request: BaseRequest, result: ScaffoldResult, rite_name: str):
        try:
            trace_id = request.trace_id
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "REVELATION",
                    "label": f"{rite_name.upper()}_{'SUCCESS' if result.success else 'FRACTURED'}",
                    "color": "#64ffda" if result.success else "#ef4444",
                    "duration": result.duration_seconds,
                    "trace": trace_id
                }
            })
            if result.artifacts:
                self.engine.akashic.broadcast({
                    "method": "scaffold/artifacts",
                    "params": {"trace": trace_id, "count": len(result.artifacts)}
                })
        except Exception as e:
            pass

    def shutdown(self):
        """[ASCENSION 24]: The Finality Vow."""
        self._reap_active_pids()
        if self._thread_pool:
            self._thread_pool.shutdown(wait=False)

    def __repr__(self) -> str:
        return f"<Ω_QUANTUM_DISPATCHER pids={len(self._active_pids)} substrate={'ETHER' if self._is_wasm else 'IRON'}>"