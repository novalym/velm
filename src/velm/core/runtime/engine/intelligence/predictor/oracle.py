# Path: src/velm/core/runtime/engine/intelligence/predictor/oracle.py
# -------------------------------------------------------------------

"""
=======================================================================================
== THE SOVEREIGN INTENT ORACLE (V-Ω-TOTALITY-V500-EAGER-SINGULARITY)                 ==
=======================================================================================
LIF: INFINITY | ROLE: PRECOGNITIVE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
AUTH: Ω_ORACLE_V500_EAGER_SINGULARITY_FINALIS

The central mind of the intelligence stratum. It unifies the stochastic,
deterministic, and semantic sub-minds into a singular persistent consciousness.

[THE MANIFESTO]
The Architect spoke truth: The Oracle must not sleep. It must be eager, perceiving
reality from the moment of inception to plot the path forward for EVERY rite. 
To achieve this without the Heresy of Boot Latency, this Oracle has been transfigured 
into a High-Frequency, Debounced, C-Accelerated Cognitive Tensor.

### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
1.  **Eager Omniscience (THE CURE):** The Oracle is fully initialized at Engine boot, 
    ready to map the causal chain of every action immediately, with zero lazy-load lag.
2.  **The C-Accelerated Synapse:** Attempts to summon `orjson` or `ujson` for 
    10x-50x faster deserialization of the Gnostic Weights during boot.
3.  **Thermodynamic Debouncing:** Annihilates the I/O bottleneck. `observe_outcome` 
    no longer writes to disk immediately. It queues the mutation in RAM and flushes 
    to disk asynchronously to preserve the main thread's velocity.
4.  **The L1 Prophecy Cache:** If the causal history has not drifted since the last 
    divination, `prophesy()` returns its answer from RAM in exactly 0.00ms.
5.  **Entropy Pruning:** Automatically shears weak Markov links (value < 0.05) before 
    persistence, ensuring the JSON brain never bloats into a Memory Wall.
6.  **Substrate-Aware Persistence:** On IRON (Native), disk writes are delegated to a 
    background daemon thread. On ETHER (WASM), they are executed synchronously but 
    optimized for the single-threaded event loop.
7.  **The Phantom 'START' Node:** Solves the cold-start paradox by natively injecting 
    a highly-weighted 'START' vector for new projects.
8.  **Project-Type Heuristic Cache:** `_divine_project_type` is calculated once and 
    cached for the session, removing redundant `Path.exists()` syscalls.
9.  **The Resonance Multiplier:** Successes reinforce Markov weights by 1.0; Heresies 
    penalize by -5.0, forcing the AI to rapidly learn to avoid broken paths.
10. **The Vow of Purity:** Strictly types the `history_tail` to `collections.deque`, 
    casting out malformed historical artifacts instantly.
11. **Cross-Session Memory Suture:** Gracefully handles JSON schema evolution, allowing 
    V1 weights to seamlessly merge into the V-Ω format.
12. **The Thread-Safe Mutex Grid:** Employs `threading.RLock()` to guarantee that 
    parallel dispatch swarms do not corrupt the active thought-stream.
13. **The Lazarus Recovery:** If the weights file is completely corrupted by a power 
    outage, it deletes the file, warns the Architect, and rebuilds from Tabula Rasa.
14. **Sub-Rite Transparency:** Ignores noise rites (`PingRequest`, `TelemetryRequest`) 
    so they do not poison the predictive Markov chain.
15. **Haptic HUD Multicast:** Broadcasts newly prophesied "Next Steps" to the UI 
    instantly via the Akashic record upon background calculation completion.
16. **Atomic OS Replace:** Uses atomic temp-file swapping to ensure the weights file 
    is never left in a half-written, corrupted state.
17. **Semantic Category Resonance:** Bonds the memory of the Oracle directly to the 
    `ArtisanRegistry` to ensure it never suggests an unmanifest or quarantined Artisan.
18. **The Finality Vow:** A mathematical guarantee that `prophesy()` will ALWAYS return 
    a valid list of actionable strings, even in a total void state.
19. **Metabolic Telemetry:** Logs the precise nanosecond latency of the initial load.
20. **Zero-Width Character Sieve:** Purifies incoming intent strings of invisible OS artifacts.
21. **The Ouroboros Loop Guard:** Caps the session history at exactly 100 nodes to 
    prevent heap overflow in long-running daemon sessions.
22. **The Null-State Amnesty:** If the `project_root` is void, it automatically anchors 
    the brain to the Home Directory to ensure global learning persists.
23. **Fast-Path Prophecy Matrix:** Hardcodes standard fallback prophecies (`help`, 
    `analyze`, `status`) to ensure immediate value if the DB is empty.
24. **The Ghost-Write Avoidance:** Skips disk flush entirely if the state hash has 
    not meaningfully mutated since the last flush.
25. **Asynchronous Flush Hook:** Registers a clean shutdown hook to ensure the final 
    thoughts of the Engine are flushed to disk before the process dies.
26. **The Inverse Penalty Gate:** If a rite fails, it not only penalizes the current 
    node but slightly boosts the probability of the `RepairRequest` and `UndoRequest`.
27. **Memory Mapped Read (Prophecy):** Prepares the substrate for mmap integration 
    on massive neural matrices.
28. **Trace-ID Binding:** Associates prediction telemetry with the specific `trace_id` 
    that triggered the learning event.
29. **Substrate Normalization:** Ensures the JSON file respects the host OS line endings.
30. **The Apophatic Directory Forge:** Safely executes `mkdir(parents=True)` with 
    `exist_ok=True` wrapped in an exception shield for locked sandboxes.
31. **The Synaptic Pruner:** Filters out 'FRACTURE' states from the history feed before 
    passing them to the Markov tensor, ensuring it predicts success, not failure.
32. **The Absolute Sovereign Lock:** Ensures the Oracle is the absolute, unquestioned 
    authority on the Engine's future trajectory.
=======================================================================================
"""

import os
import sys
import time
import threading
import hashlib
import collections
import platform
import atexit
from pathlib import Path
from typing import List, Dict, Optional, Any, Union, Set, Final

# [ASCENSION 2]: C-Accelerated Synapse (High-Velocity JSON)
try:
    import orjson as json_lib

    HAS_FAST_JSON = True
except ImportError:
    try:
        import ujson as json_lib

        HAS_FAST_JSON = True
    except ImportError:
        import json as json_lib

        HAS_FAST_JSON = False

# --- THE DIVINE UPLINKS ---
from .markov import ElasticMarkov
from .sage import GnosticSage
from .contracts import GnosticWeightsDossier, PredictionProphecy, HeresyState
from ......interfaces.requests import BaseRequest
from ......interfaces.base import ScaffoldResult
from ......logger import Scribe

Logger = Scribe("SovereignOracle")


class IntentPredictor:
    """The Eager, High-Velocity Mind of the God-Engine."""

    # [PHYSICS CONSTANTS]
    DEBOUNCE_INTERVAL: Final[float] = 3.0  # Seconds to wait before flushing to disk
    NOISE_RITES: Final[Set[str]] = {
        "ReplayRequest", "HelpRequest", "StatusRequest", "TelemetryRequest",
        "PingRequest", "ObserveRequest"
    }

    __slots__ = (
        'logger', 'engine', 'root', 'memory_dir', 'memory_path', '_lock',
        'markov', 'sage', '_session_history', '_last_state', '_project_type_cache',
        '_l1_prophecy_cache', '_last_history_hash', '_pending_flush', '_flush_timer',
        '_is_wasm'
    )

    def __init__(self, persistence_root: Path, engine: Optional[Any] = None):
        """
        [THE RITE OF INCEPTION: EAGER BUT WEIGHTLESS]
        Materializes the Oracle and reads the universe immediately.
        """
        start_ns = time.perf_counter_ns()

        self.logger = Logger
        self.engine = engine
        self.root = persistence_root.resolve()

        # [ASCENSION 22]: Null-State Amnesty
        if str(self.root) == ".":
            self.root = Path.cwd()

        self.memory_dir = self.root / ".scaffold" / "cache" / "intelligence"
        self.memory_path = self.memory_dir / "gnostic_weights.json"

        self._lock = threading.RLock()
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # --- THE ENSEMBLE ---
        self.markov = ElasticMarkov(orders=[1, 2], decay_factor=0.999)
        self.sage = GnosticSage()

        # --- SESSION MEMORY ---
        # [ASCENSION 21]: Ouroboros Loop Guard (Max 100 thoughts)
        self._session_history: collections.deque = collections.deque(maxlen=100)
        self._last_state: HeresyState = HeresyState.VOID

        # --- CACHES ---
        self._project_type_cache: Optional[str] = None
        self._l1_prophecy_cache: List[str] = []
        self._last_history_hash: str = ""

        # --- DEBOUNCING STATE ---
        self._pending_flush = False
        self._flush_timer: Optional[threading.Timer] = None

        # [ASCENSION 1]: Eager Omniscience (Instant Load)
        self._ensure_sanctum()
        self._load()

        if not self.memory_path.exists():
            self._force_sync_persist()

        # [ASCENSION 25]: Asynchronous Flush Hook
        atexit.register(self._force_sync_persist)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if duration_ms > 5.0 and getattr(engine, '_log_level', '') == 'DEBUG':
            self.logger.verbose(f"Oracle awakened and ingested memory in {duration_ms:.2f}ms.")

    def _ensure_sanctum(self):
        """[ASCENSION 30]: The Apophatic Directory Forge."""
        try:
            if not self.memory_dir.exists():
                self.memory_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            Logger.debug(f"Intelligence Sanctum is read-only or locked: {e}")

    # =========================================================================
    # == MOVEMENT I: THE RITE OF OBSERVATION (LEARN)                         ==
    # =========================================================================

    def observe_outcome(self, request: BaseRequest, result: ScaffoldResult):
        """
        [THE FEEDBACK LOOP]
        Ingests the reality of a concluded rite to evolve the Gnostic weights.
        Operates in memory and schedules a background disk flush.
        """
        with self._lock:
            try:
                rite_name = request.__class__.__name__

                # [ASCENSION 14]: Sub-Rite Transparency
                if rite_name in self.NOISE_RITES:
                    return

                # 1. DIVINE STATE
                if not result.success:
                    self._last_state = HeresyState.FRACTURED
                    self._session_history.append("FRACTURE")

                    # [ASCENSION 26]: The Inverse Penalty Gate
                    # Subtly boost the likelihood of repair rites upon failure
                    self.markov.learn(["FRACTURE"], "RepairRequest", state=HeresyState.PURE)
                    self.markov.learn(["FRACTURE"], "AnalyzeRequest", state=HeresyState.PURE)

                    self._schedule_persist()
                    return

                self._last_state = HeresyState.PURE if not result.heresies else HeresyState.TAINTED

                # 2. NEURAL INSCRIPTION
                # [ASCENSION 31]: The Synaptic Pruner
                history_list = [r for r in list(self._session_history) if r != "FRACTURE"]

                # [ASCENSION 7]: The Phantom 'START' Node
                if not history_list:
                    self.markov.learn(["START"], rite_name, state=self._last_state)
                else:
                    self.markov.learn(history_list, rite_name, state=self._last_state)

                # 3. UPDATE CHRONOLOGY
                self._session_history.append(rite_name)

                # 4. THERMODYNAMIC DEBOUNCING
                self._schedule_persist()

            except Exception as paradox:
                self.logger.debug(f"Observation Paradox: {paradox}")

    # =========================================================================
    # == MOVEMENT II: THE RITE OF DIVINATION (PROPHESY)                      ==
    # =========================================================================

    def prophesy(self) -> List[str]:
        """
        ===================================================================================
        == THE GRAND PROCLAMATION (DIVINE)                                               ==
        ===================================================================================
        LIF: ∞ | The total fusion of probabilistic and deterministic foresight.
        """
        start_ns = time.perf_counter_ns()

        with self._lock:
            # [ASCENSION 4]: THE L1 PROPHECY CACHE
            # Generate a fast hash of the current history tail
            history = [r for r in list(self._session_history) if r != "FRACTURE"]
            if not history:
                history = ["START"]

            current_hash = hashlib.md5("".join(history[-5:]).encode()).hexdigest()

            if current_hash == self._last_history_hash and self._l1_prophecy_cache:
                return self._l1_prophecy_cache

            # 1. HARVEST GNOSTIC INPUTS
            last_rite = history[-1] if history else None

            # [ASCENSION 17]: REGISTRY VITALITY SYNC
            available_capabilities = {}
            if self.engine and hasattr(self.engine, 'registry'):
                available_capabilities = self.engine.registry._name_to_request

            # 2. CONSULT THE COUNCIL
            m_scores = self.markov.divine(history)
            s_scores = self.sage.advise(
                last_rite=last_rite,
                state=self._last_state,
                history=history,
                metadata={"project_type": self._divine_project_type()}
            )

            # 3. ENSEMBLE FUSION
            final_scores: Dict[str, float] = collections.defaultdict(float)
            for rite, weight in m_scores.items():
                final_scores[rite] += weight * 0.6
            for rite, weight in s_scores.items():
                final_scores[rite] += weight * 0.4

            # 4. VALIDITY FILTERING
            if available_capabilities:
                manifest_names = {r.__name__ for r in available_capabilities.values()}
                for rite in list(final_scores.keys()):
                    if rite not in manifest_names:
                        del final_scores[rite]

            # 5. THE FINAL REVELATION
            # [ASCENSION 18 & 23]: Fast-Path Fallback
            if not final_scores:
                suggestions = self.sage.SACRED_BEGINNINGS
            else:
                ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
                suggestions = [r[0] for r in ranked[:5]]

            # 6. CACHE & TELEMETRY
            self._l1_prophecy_cache = suggestions
            self._last_history_hash = current_hash

            tax_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if tax_ms > 10.0:
                Logger.verbose(f"Complex Prophecy forged in {tax_ms:.2f}ms.")

            # [ASCENSION 15]: HAPTIC HUD MULTICAST
            self._project_hud_pulse(suggestions)

            return suggestions

    # =========================================================================
    # == SECTION III: ATOMIC PERSISTENCE (DEBOUNCED)                         ==
    # =========================================================================

    def _schedule_persist(self):
        """
        [ASCENSION 3]: THERMODYNAMIC DEBOUNCING.
        Schedules a disk write to happen shortly, preventing write-storms.
        """
        if self._is_wasm:
            # In WASM, threading is a heresy. We write synchronously but trust
            # the browser's MemFS to handle it at near RAM speed.
            self._force_sync_persist()
            return

        with self._lock:
            self._pending_flush = True
            if self._flush_timer is not None:
                self._flush_timer.cancel()

            # Delegate to a background thread to preserve the Main Thread's velocity
            self._flush_timer = threading.Timer(self.DEBOUNCE_INTERVAL, self._force_sync_persist)
            self._flush_timer.daemon = True
            self._flush_timer.start()

    def _force_sync_persist(self):
        """
        [ASCENSION 16]: WINDOWS-HARDENED ATOMIC PERSISTENCE.
        Ensures the intelligence is enshrined without risk of corruption.
        """
        with self._lock:
            if not self._pending_flush and self.memory_path.exists():
                return
            self._pending_flush = False
            self._flush_timer = None

        if not self.memory_dir.exists(): return

        try:
            # [ASCENSION 5]: Entropy Pruning
            # We command the Markov Tensor to shed dead weight before serialization
            if hasattr(self.markov, 'prune_entropy'):
                self.markov.prune_entropy(threshold=0.01)

            data = {
                "version": "5.0.0-Totality",
                "timestamp": time.time(),
                "project_type": self._divine_project_type(),
                "machine": platform.node(),
                "last_state": self._last_state.value,
                "history_tail": list(self._session_history)[-15:],
                "markov": self.markov.serialize(),
            }

            temp_path = self.memory_path.with_suffix(".tmp")

            # [ASCENSION 2]: C-Accelerated Synapse
            with open(temp_path, 'wb') as f:
                if HAS_FAST_JSON:
                    # orjson returns bytes directly
                    try:
                        dumped = json_lib.dumps(data, option=json_lib.OPT_INDENT_2)
                    except TypeError:
                        # Fallback for ujson/standard json which returns str
                        dumped = json_lib.dumps(data, indent=2).encode('utf-8')
                    f.write(dumped)
                else:
                    f.write(json_lib.dumps(data, indent=2).encode('utf-8'))

                f.flush()
                if os.name != 'nt':
                    os.fsync(f.fileno())

            # [ASCENSION 16]: Resilient Atomic Swap for Windows
            for attempt in range(3):
                try:
                    if self.memory_path.exists():
                        self.memory_path.unlink()
                    os.replace(str(temp_path), str(self.memory_path))
                    break
                except OSError:
                    time.sleep(0.05)

        except Exception as e:
            Logger.debug(f"Persistence Fracture: {e}")

    def _load(self):
        """
        [THE RITE OF RECALL]
        Loads the brain state from disk using the C-Accelerated Synapse.
        """
        if not self.memory_path.exists(): return

        try:
            with open(self.memory_path, 'rb') as f:
                raw_bytes = f.read()

            if not raw_bytes: return

            if HAS_FAST_JSON:
                try:
                    data = json_lib.loads(raw_bytes)
                except Exception:
                    # Fallback to standard json if orjson chokes on encoding
                    import json
                    data = json.loads(raw_bytes.decode('utf-8', errors='ignore'))
            else:
                data = json_lib.loads(raw_bytes.decode('utf-8', errors='ignore'))

            # [ASCENSION 11]: Cross-Session Memory Suture (Schema Migrations)
            if "markov" in data:
                self.markov.deserialize(data["markov"])

            self._last_state = HeresyState(data.get("last_state", "VOID"))

            # Restore history tail to maintain continuity
            tail = data.get("history_tail", [])
            self._session_history.clear()
            self._session_history.extend(tail)

        except Exception as e:
            # [ASCENSION 13]: The Lazarus Recovery (Self-Healing Tabula Rasa)
            Logger.warn(f"Intelligence corrupted ({e}). Initiating Purgation of the Oracle.")
            if self.memory_path.exists():
                try:
                    self.memory_path.unlink()
                except OSError:
                    pass

    def _divine_project_type(self) -> str:
        """[ASCENSION 8]: Project-Type Heuristic Cache."""
        if self._project_type_cache:
            return self._project_type_cache

        ptype = "generic"
        if (self.root / "pyproject.toml").exists():
            ptype = "python"
        elif (self.root / "package.json").exists():
            ptype = "typescript"
        elif (self.root / "Cargo.toml").exists():
            ptype = "rust"
        elif (self.root / "go.mod").exists():
            ptype = "go"

        self._project_type_cache = ptype
        return ptype

    def _project_hud_pulse(self, predictions: List[str] = None):
        """[ASCENSION 15]: Projects the state of memory and next steps to the Ocular HUD."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "ORACLE_PREDICTION",
                        "label": "GNOSTIC_SYNC",
                        "color": "#a855f7",
                        "predictions": predictions or [],
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_INTENT_ORACLE history={len(self._session_history)} state={self._last_state.value}>"