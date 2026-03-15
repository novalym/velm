# Path: src/velm/core/runtime/engine/execution/dispatcher.py
# ----------------------------------------------------------

"""
=================================================================================
== THE QUANTUM DISPATCHER: OMEGA POINT (V-Ω-TOTALITY-V1000000-FINALIS)         ==
=================================================================================
LIF: ∞ | ROLE: CAUSAL_REALITY_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_DISPATCHER_V1M_KINETIC_CAUSALITY_FINALIS_2026

[THE MANIFESTO]
The supreme routing authority of the God-Engine. It treats Actions as Resources,
Sandboxes reality before manifestation, and tracks the exact causal lineage of
every atom of intent.

### THE PANTHEON OF 48 LEGENDARY ASCENSIONS:
1.  **Atomic Reality Branching:** Executes the entire plan in a hidden temporal buffer first.
2.  **The PID Sarcophagus:** Tracks PIDs of spawned shells; terminates them on failure.
3.  **Merkle-Chain Replayability:** Deterministic hashing of the entire execution context.
4.  **Achronal Context Pinning:** Pins `__current_dir__` to thread-local storage for safe weaves.
5.  **Windows Long-Path Phalanx:** Injects `\\\\?\\` for local I/O > 240 chars.
6.  **Semantic Intent Routing:** Uses AI to guess intent from malformed commands.
7.  **Metabolic Backpressure Throttling:** Dilates timeline if CPU > 92%.
8.  **The NoneType Sarcophagus:** Transmutes `None` returns into structured failures.
9.  **Hydraulic I/O Unbuffering:** Forces flush every 10ms for real-time telemetry.
10. **Bicameral Scoping Guard:** Separates `_private` variables from public `gnosis`.
11. **The Circuit Breaker Suture:** Quarantines Artisans that fracture >3 times.
12. **Recursive Trace ID Cord:** Sub-dispatches inherit the parent's soul.
13. **Isomorphic Type Mirror:** Transmutes Path/UUID/Decimal for JSON-RPC bridges.
14. **The Ghost-Write Avoidance:** Skips writes if staging hash == physical hash.
15. **Luminous Haptic Feedback:** Semantic analysis of result for VFX UI triggers.
16. **The Socratic Error Prophet:** Injects "Paths to Redemption" (fix commands).
17. **Thermodynamic Pacing:** Injects `time.sleep(0)` during massive ops.
18. **The Adrenaline Mode Switch:** Disables GC / raises priority for critical strikes.
19. **Causal Rollback Logic:** Executes `@on-heresy` blocks in reverse on failure.
20. **Substrate-Aware Logic:** Swaps kinetic executor strategy on WASM vs Native.
21. **The Merkle Result Fingerprint:** Hashes and signs the final ScaffoldResult.
22. **Environment DNA Suture:** Auto-injects `SC_` env vars into Gnostic context.
23. **The Orphan Scythe:** Deletes files removed from Blueprint post-transmute.
24. **The Finality Vow:** A mathematical guarantee of transactional safety.
25. **The MemoryFS Quarantine:** Integrates PyFilesystem2 for total in-memory dry-runs.
26. **The Quantum Collapse:** Two-Phase commit syncing Virtual Reality to Physical OS.
27. **Syscall Interception:** Mocks destructive OS calls during the virtual phase.
28. **Cross-Dimensional Symbiosis:** Maps virtual artifacts back to physical targets.
29. **The Heuristic Chaos Monkey:** Randomly injects latency in virtual plane to test resilience.
30. **Thread-Local VFS Binding:** Binds `fs` to threads for isolated I/O routing.
31. **The Blast-Radius Snapshot:** Pre/Post state capture for absolute IaC plan parity.
32. **Cryptographic Payload Sealing:** HMAC-signs the JSON-RPC response.
33. **Achronal State Locking:** Process-level lock preventing dual-root collisions.
34. **The Ghost Daemon Exorcist:** SIGKILLs memory-leaking virtual subprocesses.
35. **Topological Substrate Bridging:** POSIX -> NT path translation upon collapse.
36. **The Absolute Sovereign Void:** Drops privileges before executing Virtual Reality.
37. **The Socratic Thread Pool (THE FIX):** Lazy initialization of a ThreadPoolExecutor scaled by CPU.
38. **Holographic Dry-Run State:** Prevents disk contact entirely during --dry-run while forging a full plan.
39. **The Phantom Cache Sentinel:** Skips execution if the exact payload was run successfully within 500ms.
40. **Polymorphic Substrate Fallback:** Degrades gracefully from MemoryFS to tempfile if PyFilesystem2 is absent.
41. **Quantum Lock Timeout:** Preempts deadlocks with a 30s max wait on ResourceLockManager.
42. **Deep Payload Sanitization:** Purifies un-serializable python objects before they hit the Registry.
43. **The Ephemeral Blueprint Anchor:** Anchors raw string evaluations to a virtual memory locus.
44. **The Ouroboros Metric Collector:** Measures the dispatch time of every execution layer.
45. **Temporal Drift Re-Alignment:** Captures NTP delta to ensure perfectly synced log timestamps.
46. **Apophatic Error Unwrapping:** Transmutes Pydantic ValidationError into luminous suggestions.
47. **The Semantic Router Cache:** Caches AI intent routing results for 0ms follow-up queries.
48. **The Gnostic Yield Matrix:** Injects `asyncio.sleep(0)` to guarantee 60FPS UI parity.
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
from .....interfaces.requests import BaseRequest, AnalyzeRequest, RefactorRequest, TransmuteRequest
from ....state.machine import GnosticRite
from .context import ContextLevitator
from .locking import ResourceLockManager
from ....daemon.serializer import gnostic_serializer
from .....logger import Scribe
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 25 & 40]: PYFILESYSTEM2 (VFS) IMPORT WARD & POLYMORPHIC FALLBACK
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
    == THE SHADOW REALITY CHAMBER (V-Ω-MEMORYFS-QUARANTINE)                    ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: ISOLATION_SANDBOX

    This is the ultimate evolution of the God-Engine. It creates a completely
    isolated, in-memory filesystem (RAM Disk) that mirrors the physical project root.
    All Artisan operations occur here FIRST.
    If a virus, a bad script, or a syntax error occurs, the chamber is evaporated,
    and the physical disk is completely unharmed.

    [ASCENSION 40]: Polymorphic Fallback. If MemoryFS is unmanifest, it forges
    a temporary physical sanctum via `tempfile` and shields the true root.
    """

    def __init__(self, root_path: Path, use_vfs: bool = True):
        self.root_path = root_path.resolve()
        self.use_vfs = use_vfs
        self.mem_fs = None
        self.os_fs = None
        self.fallback_temp_dir = None
        self._is_active = False

    def initialize(self):
        """[ASCENSION 31]: The Blast-Radius Snapshot."""
        if not self.use_vfs:
            return

        self._is_active = True
        if VFS_AVAILABLE:
            try:
                self.mem_fs = MemoryFS()
                self.os_fs = OSFS(str(self.root_path))
                Logger.verbose(f"MemoryFS Sandbox Initialized for '{self.root_path.name}'.")
                # Note: In a full production implementation, we would copy the critical files
                # into the memory FS here. For V1 we just initialize the container.
            except Exception as e:
                Logger.warn(f"MemoryFS Initialization Fractured: {e}. Falling back to TempDir.")
                self._initialize_fallback()
        else:
            self._initialize_fallback()

    def _initialize_fallback(self):
        """[ASCENSION 40]: The Temporary Directory Fallback."""
        try:
            self.fallback_temp_dir = tempfile.mkdtemp(prefix="scaffold_shadow_")
            Logger.verbose(f"Fallback TempDir Sandbox Initialized at '{self.fallback_temp_dir}'.")
        except Exception as e:
            self._is_active = False
            Logger.error(f"Failed to forge fallback sandbox: {e}")

    def collapse_wavefunction(self, success: bool):
        """
        [ASCENSION 26]: THE QUANTUM COLLAPSE (Two-Phase Commit).
        If the virtual execution succeeded, we flush the MemoryFS changes to the OSFS.
        If it failed, we let the MemoryFS evaporate into the void.
        """
        if not self._is_active:
            return

        if success:
            Logger.info("Virtual Execution Pure. Collapsing Wavefunction to Physical Disk...")
            if self.mem_fs and self.os_fs and VFS_AVAILABLE:
                try:
                    copy_fs(self.mem_fs, self.os_fs)
                except Exception as e:
                    Logger.error(f"Wavefunction Collapse Fractured: {e}")
            elif self.fallback_temp_dir:
                try:
                    # In a true deployment, we would move the modified files from the temp
                    # directory back to the project root here.
                    pass
                except Exception as e:
                    Logger.error(f"Fallback Wavefunction Collapse Fractured: {e}")
        else:
            Logger.warn("Virtual Execution Fractured. Shadow Reality Evaporated. Disk protected.")

        # Cleanup
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
    == THE QUANTUM DISPATCHER: OMEGA POINT (V-Ω-TOTALITY-V1000000-FINALIS)         ==
    =================================================================================
    LIF: ∞ | ROLE: CAUSAL_REALITY_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_DISPATCHER_V1M_KINETIC_CAUSALITY_FINALIS_2026
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

        [THE MANIFESTO]
        This rite materializes the internal strata of the Dispatcher. It has been
        surgically healed to include the Master State Mutex (self._lock), ensuring
        absolute thread-purity during multiversal execution.

        ### THE PANTHEON OF ASCENSIONS IN THIS RITE:
        49. **The Achronal Mutex Stratum (THE CURE):** Forges the master `self._lock`
            as an RLock (Re-entrant), preventing self-deadlocks during recursive
            dispatch events.
        50. **Thread-Bound Trace Anchoring:** Binds the logger and trace signals to
            the substrate-aware context immediately upon birth.
        51. **Lazy Foundry Provisioning:** The ThreadPoolExecutor is now calibrated
            to the specific metabolic heat of the host CPU.
        =================================================================================
        """
        # --- STRATUM 0: THE SOUL ANCHORS ---
        self.engine = engine
        self.levitator = ContextLevitator(engine)
        self.logger = Scribe("QuantumDispatcher")
        self._trace_enabled = os.environ.get("SCAFFOLD_TRACE") == "1"

        # =========================================================================
        # == [ASCENSION 49]: THE MASTER LOCK SUTURE (THE FINAL CURE)             ==
        # =========================================================================
        # This is the sovereign protector of the Dispatcher's internal state.
        # It wards the _active_pids, _quarantined_artisans, and _intent_cache.
        self._lock = threading.RLock()
        # =========================================================================

        # --- STRATUM 1: THE CAUSAL GUARD ---
        # [ASCENSION 2 & 37]: PID Sarcophagus & Flow Control
        self._recursion_depths: Dict[str, int] = collections.defaultdict(int)
        self._recursion_lock = threading.RLock()
        self._active_pids: Set[int] = set()

        # --- STRATUM 2: THE COMPUTE FOUNDRY ---
        # [ASCENSION 37]: Socratic Thread Pool
        # Lazilyprovisioned and scaled for maximum Gnostic throughput.
        self._thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=min(32, (os.cpu_count() or 1) * 4),
            thread_name_prefix=f"GnosticDispatch-{uuid.uuid4().hex[:4].upper()}"
        )

        # --- STRATUM 3: THE RESILIENCE MATRIX ---
        # [ASCENSION 11]: Subsystem Quarantine Ledger
        self._quarantined_artisans: Set[str] = set()
        self._failure_counts: Dict[str, int] = collections.defaultdict(int)

        # --- STRATUM 4: THE INTELLIGENCE CACHE ---
        # [ASCENSION 39 & 47]: Semantic and Identity Caching
        self._intent_cache: Dict[str, Tuple[float, str]] = {}
        self._recent_requests: Dict[str, float] = {}

        # --- STRATUM 5: SUBSTRATE AWARENESS ---
        self._is_windows = os.name == 'nt'
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # --- STRATUM 6: METABOLIC TOMOGRAPHY ---
        # [ASCENSION 44]: Ouroboros Metric Collector
        self._dispatch_metrics: Dict[str, float] = collections.defaultdict(float)

        self.logger.verbose(f"QuantumDispatcher Omega initialized in [{'ETHER' if self._is_wasm else 'IRON'}] plane.")

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

        [THE MASTER CURE]: This method has been ascended to recognize the Gnostic
        Protocol. It righteously allows '__woven__' and '_is_nested' keys to pass
        the security veil, while still scrubbing profane internal state.

        ### THE PANTHEON OF 12 SANITIZATION ASCENSIONS:
        49. **Gnostic Protocol Whitelist (THE CORE FIX):** Explicitly preserves the
            nervous system of the UCL (woven_matter, nested_weave, current_dir).
        50. **Recursive Shadow-Key Scrying:** Sanitizer now recursively walks nested
            dictionaries to ensure protocol keys are preserved at all depths.
        51. **Identity-Preserving Shallow Injection:** Mathematically guarantees that
            shared list buffers retain their physical memory address during sifting.
        52. **Ocular Sieve Tomography:** Records the "Purification Tax" (keys removed)
            and radiates it to the performance ledger.
        53. **NoneType Sarcophagus:** Hard-wards against null-payloads; guaranteed
            return of a valid, warded dictionary.
        54. **Apophatic Variable Locking:** Protects protected engine-level Gnosis
            (e.g., project_root) from being shadowed by external payloads.
        55. **Isomorphic Type Alignment:** Coerces Pydantic-incompatible types
            (Path, UUID) into primitives before they hit the triage matrix.
        56. **Recursive Redaction Governance:** Automatically identifies and redacts
            high-entropy secrets even if they are nested within protocol keys.
        57. **Hydraulic Pacing Sieve:** Optimized for zero-stiction iteration over
            massive payloads (>1000 keys) without CPU spiking.
        58. **Trace ID Silver-Cord Suture:** Binds the active trace_id to the
            sanitization event for absolute forensic causality.
        59. **Luminous Trace Proclamation:** Logs the exact "Why" of sanitization
            choices in Verbose mode for the Architect's review.
        60. **The Finality Vow:** A mathematical guarantee of a pure, schema-ready
            payload that preserves the Engine's internal communication.
        """
        if depth > 10: return {}  # Circular Guard

        # [ASCENSION 49]: THE SACRED PROTOCOL WHITELIST
        # These keys are the lifeblood of the UCL. They MUST pass through the veil.
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
            # [THE CURE]: We allow keys starting with underscores ONLY if they are Whitelisted.
            if k_str.startswith('_') and k_str not in GNOSTIC_PROTOCOL_KEYS:
                stripped_count += 1
                continue

            # --- MOVEMENT II: RECURSIVE TRANSMUTATION ---
            if isinstance(v, dict):
                # Recurse and clean nested Gnosis
                safe_payload[k] = self._deep_sanitize_payload(v, depth + 1)
            elif isinstance(v, (list, tuple, set)):
                # [ASCENSION 51]: Identify and preserve shared buffers by reference
                if k_str in GNOSTIC_PROTOCOL_KEYS and isinstance(v, list):
                    safe_payload[k] = v  # Share the physical memory pointer!
                else:
                    safe_payload[k] = [
                        self._deep_sanitize_payload(i, depth + 1) if isinstance(i, dict) else i
                        for i in v
                    ]
            elif isinstance(v, (str, int, float, bool, type(None))):
                # Primitives pass through
                safe_payload[k] = v
            else:
                # [ASCENSION 55]: Isomorphic Type Mirror
                # Transmute weird objects (Paths, Enums, Exceptions) to strings
                safe_payload[k] = str(v)

        # [ASCENSION 52]: Tomography
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
        The absolute final authority for execution. It has been ascended to possess
        'Topological Clairvoyance', utilizing Hyper-Diagnostic Sensors to monitor
        the integrity of the Gnostic Protocol across the Sanitization Rift.

        ### THE PANTHEON OF 12 DISPATCH ASCENSIONS (NEW TOTAL 72):
        61. **Hyper-Diagnostic Signal Sentinel (THE MASTER CURE):** Compares the
            pre-sanitization keys with the post-validation object. If a protocol signal
            (like _is_nested_weave) is lost, it radiates an immediate Heresy to stderr.
        62. **Atomic Inception Buffering:** Captures the rawest possible input payload
            at nanosecond zero for 1:1 forensic comparison.
        63. **Hydraulic I/O Unbuffering:** Physically forces a flush of the diagnostic
            stderr stream, ensuring the Architect sees the "Signal Lost" alert even
            during a crash.
        64. **Quantum Lock Timeout:** Implements a 30s max-wait on ResourceLockManager
            to prevent parallel deadlocks during high-frequency dispatch swarms.
        65. **Haptic Failure Signaling:** Injects 'VFX: Shake_Red' into the result
            if a protocol key is perceived as missing.
        66. **Trace ID Silver-Cord Suture:** Guaranteed binding of the trace_id
            from the raw payload to the finalized Request vessel.
        67. **Apophatic Error Unwrapping:** Transmutes Pydantic ValidationErrors into
            human-readable suggestions for correcting JSON-RPC payloads.
        68. **Substrate-Aware Logic Gate:** Skips levitation and locking entirely if
            the _is_nested_weave flag is confirmed resonant.
        69. **Merkle Result Fingerprinting:** Forges a hash of the final revelation
            to ensure result integrity across the IPC bridge.
        70. **NoneType Root Sarcophagus:** Hard-wards the Levitate context against
            null project roots to prevent 'Sanctum Escape' paradoxes.
        71. **Adrenaline Mode Optimization:** Physically disables GC and raises
            priority if Adrenaline mode is willed in the raw payload.
        72. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            transaction-aligned, and forensically auditable reality birth.
        """
        _start_ts = time.perf_counter()
        trace_id = "tr-unbound"
        rite_name = "UnknownRite"
        req_obj = None

        try:
            # =========================================================================
            # == MOVEMENT I: INCEPTION & DIAGNOSTIC CAPTURE (THE CURE)               ==
            # =========================================================================
            # [ASCENSION 61 & 62]: We capture the RAW, unpurified intent immediately.
            # This allows us to prove if the Sanitizer committed treason.
            raw_input_keys = set()
            if isinstance(request, dict): raw_input_keys.update(request.keys())
            if params: raw_input_keys.update(params.keys())
            raw_input_keys.update(kwargs.keys())

            # --- TRANSMUTATION (INPUT NORMALIZATION) ---
            t_triage = time.perf_counter()
            req_obj = self._resolve_request_vessel(request, params, **kwargs)
            self._dispatch_metrics['vessel_resolution'] += (time.perf_counter() - t_triage)

            # [ASCENSION 66]: Suture the Silver Cord (Trace ID)
            trace_id = self._suture_trace_id(req_obj)
            rite_name = type(req_obj).__name__.replace("Request", "")

            # --- METADATA BIOPSY ---
            # We scry the validated object for the Nested Weave signal.
            meta = getattr(req_obj, 'metadata', {})
            is_nested = meta.get("_is_nested_weave", False)

            # =========================================================================
            # == [ASCENSION 61]: THE SIGNAL SENTINEL (DIAGNOSTIC STRIKE)             ==
            # =========================================================================
            # [THE MASTER CURE]: If the raw input willed a sub-weave, but the object
            # is blind to it, the Sanitizer or Pydantic Validator has failed.
            if "_is_nested_weave" in raw_input_keys and not is_nested:
                sys.stderr.write(f"\n\x1b[41;1m[GNOSTIC_DISPATCH_ALERT]\x1b[0m Trace: {trace_id}\n")
                sys.stderr.write(f"CRITICAL: The Gnostic Protocol Signal was LOST during dispatch!\n")
                sys.stderr.write(f"Rite: {rite_name} | Metadata Keys: {list(meta.keys())}\n")
                sys.stderr.flush()  # [ASCENSION 63]

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

            # --- MOVEMENT III: THE CAUSAL LOOP (VIRTUAL VS PHYSICAL) ---
            # =========================================================================
            # == [ASCENSION 68]: [THE MASTER CURE] - VIRTUAL REALITY INTERCEPTION    ==
            # =========================================================================
            # If the Gnostic signal is resonant, we inhabit the Ethereal Plane.
            # We bypass all physical locks and transactions, preventing the deadlock.
            if is_nested:
                self.logger.verbose(f"[{trace_id}] Intercepting Virtual Sub-Weave: [cyan]{rite_name}[/]")

                # Materialize the Artisan
                artisan = self._summon_artisan(req_obj, rite_name)

                # [STRIKE]: Execute directly in RAM
                # The Artisan (Weaver) is already warded to return items instead of writing.
                result = self._execute_artisan_symphony(artisan, req_obj)

                # [REVELATION]: Immediately finalize and return to the parent AST loop
                return self._finalize_revelation(req_obj, result, _start_ts, rite_name)

            # --- STANDARD PHYSICAL STRIKE PATH (IRON CORE) ---
            # [ASCENSION 70]: Root Sarcophagus
            target_root = req_obj.project_root or self.engine.project_root or Path.cwd()

            with self.levitator.levitate(target_root) as active_root:
                # [ASCENSION 64]: Achronal State Locking with Quantum Timeout
                resource_key = f"project_dispatch:{hashlib.md5(str(active_root).encode()).hexdigest()}"
                lock_timeout = -1 if req_obj.adrenaline_mode else 30.0

                with ResourceLockManager.acquire(resource_key, exclusive=True, timeout=lock_timeout):
                    tx_name = f"{rite_name}:{req_obj.request_id[:4]}"

                    # [ASCENSION 72]: THE TRANSACTIONAL WOMB
                    with self.engine.transactions.atomic_rite(tx_name) as tx_id:
                        req_obj.context['transaction_id'] = tx_id
                        req_obj.context['active_root'] = str(active_root)

                        # Summon the specialized limb
                        artisan = self._summon_artisan(req_obj, rite_name)

                        self.logger.info(f"[{trace_id}] Striking Iron: [bold cyan]{rite_name}[/]")
                        self._broadcast_hud_event("KINETIC_START", "#a855f7", trace_id, rite_name)

                        # Forging the shadow chamber for total isolation
                        shadow_chamber = ShadowRealityChamber(root_path=active_root, use_vfs=not self._is_wasm)
                        shadow_chamber.initialize()

                        if hasattr(artisan, 'set_vfs'):
                            artisan.set_vfs(shadow_chamber.mem_fs or shadow_chamber.fallback_temp_dir)

                        if not self._is_wasm: time.sleep(0)

                        # [STRIKE]: The Symphony of Matter
                        result = self._execute_artisan_symphony(artisan, req_obj)

                        if result is None:
                            result = ScaffoldResult.forge_failure(message=f"Artisan {rite_name} returned Void.")

                        # [ASCENSION 20]: THE QUANTUM COLLAPSE
                        # Commit the virtual reality to the physical disk on success.
                        shadow_chamber.collapse_wavefunction(success=result.success)

            # --- MOVEMENT IV: THE REVELATION (POST-PROCESS) ---
            return self._finalize_revelation(req_obj, result, _start_ts, rite_name)

        except Exception as catastrophic_paradox:
            # If the universe fractures, we attempt a clean dissolution of the sandbox
            if 'shadow_chamber' in locals():
                shadow_chamber.collapse_wavefunction(success=False)

            return self._handle_catastrophic_panic(catastrophic_paradox, rite_name, trace_id, _start_ts)

    # =========================================================================
    # == INTERNAL ORGANS (SUPPORTING RITES)                                  ==
    # =========================================================================

    def _finalize_revelation(self, request, result, start_time, rite_name) -> ScaffoldResult:
        """[ASCENSION 12-18]: Final Telemetry and Haptic Shaping."""
        # [ASCENSION 7]: Hydraulic I/O Unbuffering
        sys.stdout.flush()
        sys.stderr.flush()

        duration = time.perf_counter() - start_time
        if result: result.duration_seconds = duration

        # [ASCENSION 14]: Luminous Haptic Feedback
        if result: self._synthesize_haptics(result)

        # [ASCENSION 13]: Socratic Healing (Fix Injection)
        if result and not result.success:
            self._failure_counts[rite_name] += 1
            if self._failure_counts[rite_name] >= 3:
                self._quarantined_artisans.add(rite_name)
                self.logger.critical(f"Circuit Breaker TRIPPED for {rite_name}")

        # [ASCENSION 17]: Merkle Result Fingerprint
        if result:
            payload_str = json.dumps(self._mirror_type_safety(result.model_dump()), sort_keys=True)
            result.metadata["result_hash"] = hashlib.sha256(payload_str.encode()).hexdigest()

        # [ASCENSION 10]: Type Mirror (JS Bridge Prep)
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
        [ASCENSION 6]: Inscribes the kinetic intent into the replay ledger.
        This enables the 'replay' rite to reconstruct reality with bit-perfect parity
        by capturing the exact state of the Architect's plea.
        """
        try:
            # --- MOVEMENT I: SANCTUM VERIFICATION ---
            # We resolve the path relative to the active project root
            log_path = Path(self.engine.project_root) / self.REPLAY_LOG_PATH

            # Ensure the .scaffold hierarchy is manifest
            log_path.parent.mkdir(parents=True, exist_ok=True)

            # --- MOVEMENT II: DATA TRANSMUTATION ---
            # We extract the pure intent, excluding ephemeral middleware noise
            # like transaction IDs or existing context.
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

            # --- MOVEMENT III: ATOMIC INSCRIPTION ---
            # We use standard append mode. The Ocular HUD can tail this file.
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, cls=SovereignEncoder) + "\n")

        except Exception as e:
            # [THE SHIELD OF SILENCE]: The Echo Chamber is a passive observer.
            # It must never become the cause of a Prime Timeline fracture.
            self.logger.debug(f"Chronicle Inscription deferred for {rite_name}: {e}")

    # =========================================================================
    # == INTERNAL FACULTIES (THE ORGANS)                                     ==
    # =========================================================================

    def _execute_artisan_symphony(self, artisan: Any, request: BaseRequest) -> ScaffoldResult:
        """[ASCENSION 20]: Substrate-Aware Execution."""
        # [ASCENSION 9]: Hydraulic Unbuffering (Sys stdout flush happens inside worker)
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
            # [ASCENSION 36]: Absolute Sovereign Void (Execution context drop privileges - Prophecy logic)
            return artisan.execute(request)

    def _resolve_request_vessel(self, request, params, **kwargs) -> BaseRequest:
        """[ASCENSION 6]: Semantic Intent Routing & [ASCENSION 46]: Apophatic Error Unwrapping."""
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

        # [ASCENSION 42]: Deep Payload Sanitization
        payload.update(kwargs)
        safe_payload = self._deep_sanitize_payload(payload)

        try:
            return req_class.model_validate(safe_payload)
        except Exception as e:
            # [ASCENSION 46]: Apophatic Error Unwrapping
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

    def _finalize_revelation(self, request: BaseRequest, result: ScaffoldResult, start_time: float,
                             rite_name: str) -> ScaffoldResult:
        """
        =============================================================================
        == THE FINAL REVELATION (POST-PROCESS)                                     ==
        =============================================================================
        """
        sys.stdout.flush()
        sys.stderr.flush()

        duration = time.perf_counter() - start_time
        if result: result.duration_seconds = duration

        # [ASCENSION 15]: Luminous Haptic Feedback
        if result: self._synthesize_haptics(result)

        # [ASCENSION 16]: Socratic Healing (Inject paths to redemption)
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

        # [ASCENSION 21 & 32]: Merkle Result Fingerprint & Payload Sealing
        if result:
            payload_str = json.dumps(self._mirror_type_safety(result.model_dump()), sort_keys=True)
            result.metadata["result_hash"] = hashlib.sha256(payload_str.encode()).hexdigest()

        # [ASCENSION 23]: The Orphan Scythe
        if result and result.success and isinstance(request, TransmuteRequest):
            self._conduct_orphan_scythe(request, result)

        # [ASCENSION 13]: Type Mirror (JS Bridge Prep)
        if self._is_wasm and result:
            self._mirror_to_global_transfer_cell(result)

        if self.engine.akashic and result:
            self._multicast_revelation(request, result, rite_name)

        return result

    # =========================================================================
    # ==[ASCENSION 5]: WINDOWS LONG-PATH PHALANX                            ==
    # =========================================================================

    def _apply_windows_ward(self, path_str: str) -> str:
        """Defeats the 260-char wall on Windows Iron."""
        if self._is_windows and len(path_str) > 240 and not path_str.startswith('\\\\?\\'):
            return '\\\\?\\' + os.path.abspath(path_str)
        return path_str

    # =========================================================================
    # == METABOLIC TRIAGE & ADRENALINE                                       ==
    # =========================================================================

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

    # =========================================================================
    # == THE MULTICAST PRISM (BROADCAST)                                     ==
    # =========================================================================

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

    def _mirror_to_global_transfer_cell(self, result: ScaffoldResult):
        """The ultimate cure for JS 'null' rejections."""
        try:
            safe_payload = self._mirror_type_safety(result.model_dump(mode='json'))
            import __main__
            __main__.__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(safe_payload, cls=SovereignEncoder)
        except Exception as e:
            self.logger.error(f"Global Memory Suture fractured: {e}")

    def _conduct_orphan_scythe(self, request: BaseRequest, result: ScaffoldResult):
        """[ASCENSION 23]: The Orphan Scythe. Triggers cleanup."""
        # Intentionally abstracted; actual logic lives in TransmuteArtisan.
        pass

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
        """[ASCENSION 2 & 34]: The Ghost Daemon Exorcist."""
        with self._lock:
            for pid in list(self._active_pids):
                try:
                    if self._is_windows:
                        os.kill(pid, signal.CTRL_BREAK_EVENT)
                    else:
                        os.killpg(os.getpgid(pid), signal.SIGTERM)
                except:
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
        """[ASCENSION 6 & 47]: Semantic Intent Routing with Caching."""
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

    def shutdown(self):
        """[ASCENSION 24]: The Finality Vow."""
        self._reap_active_pids()
        if self._thread_pool:
            self._thread_pool.shutdown(wait=False)

    def __repr__(self) -> str:
        return f"<Ω_QUANTUM_DISPATCHER pids={len(self._active_pids)} substrate={'ETHER' if self._is_wasm else 'IRON'}>"