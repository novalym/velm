# Path: src/velm/core/runtime/middleware/telemetry.py
# =========================================================================================
# == THE SYNAPTIC RELAY: TOTALITY (V-Ω-TOTALITY-V35.0-SUBSTRATE-AGNOSTIC-FINALIS)         ==
# =========================================================================================
# LIF: ∞ | ROLE: METABOLIC_SENSORY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_TELEMETRY_V35_WASM_SUTURE_2026_FINALIS
# =========================================================================================

import hashlib
import hmac
import json
import os
import platform
import threading
import time
import uuid
import sys
import queue
import socket
import math
import gc
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List, Tuple, Final, Set
from concurrent.futures import ThreadPoolExecutor

# --- GNOSTIC UPLINKS ---
try:
    import requests

    HAS_CELESTIAL_LINK = True
except ImportError:
    HAS_CELESTIAL_LINK = False

try:
    import psutil

    HAS_SENSES = True
except ImportError:
    psutil = None
    HAS_SENSES = False

from .contract import Middleware, NextHandler
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest
from ....logger import Scribe

# =============================================================================
# == THE GNOSTIC CONFIGURATION                                               ==
# =============================================================================
MOTHERSHIP_URL: Final[str] = os.getenv("SCAFFOLD_TELEMETRY_URL", "https://telemetry.novalym.systems/ingest")
AKASHA_DIR: Final[Path] = Path.home() / ".scaffold" / "telemetry"
BUFFER_FILE: Final[Path] = AKASHA_DIR / "shadow_logs.jsonl"
ENABLED: Final[bool] = os.getenv("SCAFFOLD_TELEMETRY", "1") != "0"

# [ASCENSION 10]: THE INTERNAL SEAL
_MACHINE_SECRET: Final[str] = os.getenv("SCAFFOLD_INTERNAL_KEY", str(uuid.getnode()))

# [ASCENSION 11]: METABOLIC CACHE
_VITALS_CACHE: List[Any] = [0, {}]  # [Timestamp, Vitals_Dict]
_VITALS_LOCK = threading.Lock()
_VITALS_TTL = 1.5


class TelemetryMiddleware(Middleware):
    """
    =============================================================================
    == THE SYNAPTIC RELAY (V-Ω-TOTALITY-V35.0-LEGENDARY)                       ==
    =============================================================================
    LIF: ∞ | ROLE: SYNAPTIC_CONDUCTOR | RANK: OMEGA_SOVEREIGN

    The supreme orchestrator of system observability. Re-engineered to handle the
    threading limitations of the WASM substrate while maintaining high-fidelity
    telemetry in Iron Core environments.
    """

    # [ASCENSION 9]: Prioritized Synaptic Queue
    _queue: queue.PriorityQueue = queue.PriorityQueue(maxsize=2000)
    _executor: Optional[ThreadPoolExecutor] = None
    _initialized = False
    _lock = threading.Lock()

    # [THE CURE]: WASM SUBSTRATE DETECTION
    _is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    def __init__(self, engine: Any):
        """[THE RITE OF INCEPTION]"""
        super().__init__(engine)
        self.instance_id = f"node-{uuid.uuid4().hex[:6].upper()}"
        self.Logger = Scribe("SynapticRelay")

        # [THE CURE]: SUBSTRATE-AWARE RADIATOR
        if not self._is_wasm:
            self._ensure_radiator_active()
        else:
            self.Logger.verbose("WASM Substrate perceived. Operating in [cyan]Achronal Synchronous Mode[/cyan].")

    def _ensure_radiator_active(self):
        """
        Materializes the background processing thread ONLY on iron core substrates.
        """
        with self._lock:
            if not TelemetryMiddleware._initialized:
                try:
                    TelemetryMiddleware._executor = ThreadPoolExecutor(max_workers=1,
                                                                       thread_name_prefix="SynapseRadiator")
                    TelemetryMiddleware._executor.submit(self._synapse_radiator_loop)
                    TelemetryMiddleware._initialized = True
                except (RuntimeError, ImportError) as e:
                    # Final fallback if threading fails even on Iron
                    self._is_wasm = True
                    self.Logger.warn(f"Metabolic Fracture: Threading rejected ({e}). Switching to Synchronous mode.")

    # --- MOVEMENT II: THE RITE OF PERCEPTION (HANDLE) ---

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        Intercepts the plea, scries vitals, and radiates the Gnostic result.
        """
        if not ENABLED:
            return next_handler(request)

        # [ASCENSION 1]: Nanosecond Tomography Ignition
        start_ns = time.perf_counter_ns()
        start_mem = self._get_memory_usage()

        status = "INTERRUPTED"
        result = None

        try:
            # --- THE KINETIC EXECUTION ---
            result = next_handler(request)

            # --- ADJUDICATE OUTCOME ---
            if result is None:
                status = "VOID_REVELATION"
            elif hasattr(result, "success"):
                status = "SUCCESS" if result.success else "HERESY"
            else:
                status = "PROCESSED_UNTRACKED"

            return result

        except Exception as fracture:
            status = "CATASTROPHIC_COLLAPSE"
            raise fracture

        finally:
            # --- METABOLIC FINALITY ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            end_mem = self._get_memory_usage()
            mem_delta_mb = end_mem - start_mem

            # [ASCENSION 2 & 9]: ENQUEUE FOR RADIATION
            try:
                self._enqueue_synapse(request, result, status, duration_ms, mem_delta_mb)
            except Exception as e:
                # The Relay must remain unbreakable; silence the paradox.
                self.Logger.debug(f"Synapse Radiation Deferred: {e}")

    def _enqueue_synapse(self, request: BaseRequest, result: Any, status: str, duration: float, memory: float):
        """
        [THE DISPATCH TRIAGE]
        Adjudicates between asynchronous queuing (Iron) and synchronous radiation (WASM).
        """
        priority = 10 if status == "SUCCESS" else 1

        try:
            # 1. FORGE THE GNOSTIC PAYLOAD
            payload = self._forge_synapse(request, result, status, duration, memory)
            payload["signature"] = self._forge_signature(payload)

            if not self._is_wasm:
                # PATH A: IRON CORE (ASYNC)
                try:
                    self._queue.put_nowait((priority, time.time(), payload))
                except queue.Full:
                    # [ASCENSION 2]: Flush oldest if buffer is saturated
                    self._queue.get_nowait()
                    self._queue.put_nowait((priority, time.time(), payload))
            else:
                # PATH B: ETHER PLANE (SYNC)
                # [THE FIX]: In WASM, we radiate immediately or write to the local archive
                # to prevent thread-spawn RuntimeError.
                self._radiate([payload])

        except Exception:
            pass

    # =========================================================================
    # == [THE CURE]: HARDWARE TOMOGRAPHY STRATA                              ==
    # =========================================================================

    def _scry_vitals_safe(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE GAZE OF VITALITY (V-Ω-SUBSTRATE-AGNOSTIC)                           ==
        =============================================================================
        LIF: 100x | ROLE: METABOLIC_SCRIER

        [THE CURE]: Performs high-fidelity tomography without psutil dependencies.
        In WASM, it uses 'Achronal Drift' to infer CPU load.
        """
        now = time.time()
        with _VITALS_LOCK:
            if now - _VITALS_CACHE[0] < _VITALS_TTL:
                return _VITALS_CACHE[1]

            vitals = {"substrate": "ETHER" if self._is_wasm else "IRON", "ts": now}

            try:
                if not self._is_wasm and HAS_SENSES:
                    # IRON CORE (NATIVE)
                    vitals.update({
                        "cpu_load": psutil.cpu_percent(interval=None),
                        "ram_percent": psutil.virtual_memory().percent,
                        "io_wait": getattr(psutil.cpu_times_percent(), 'iowait', 0.0),
                        "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
                    })
                else:
                    # ETHER PLANE (WASM)
                    # [ASCENSION 2]: ACHRONAL DRIFT TOMOGRAPHY
                    # We measure loop lag. A 1ms "Rite of Silence" should take ~1ms.
                    t0 = time.perf_counter()
                    time.sleep(0.001)
                    t1 = time.perf_counter()
                    drift_ms = (t1 - t0) * 1000

                    # Heuristic: 10ms drift indicates extreme metabolic fever.
                    vitals["cpu_load"] = min(100.0, (drift_ms / 10.0) * 95.0)

                    # [ASCENSION 3]: HEAP MASS INFERENCE
                    # We count Gnostic objects to estimate RAM mass in the sandbox.
                    vitals["ram_percent"] = min(100.0, (len(gc.get_objects()) / 1000000.0) * 100)

                _VITALS_CACHE[0] = now
                _VITALS_CACHE[1] = vitals
                return vitals
            except Exception:
                return _VITALS_CACHE[1]

    def _get_memory_usage(self) -> float:
        """
        Calculates current RSS mass. Handles WASM virtualization.
        """
        try:
            if not self._is_wasm and HAS_SENSES:
                return psutil.Process().memory_info().rss / (1024 * 1024)
            # WASM Heuristic: 100,000 objects is ~15MB Gnostic metadata
            return len(gc.get_objects()) * 0.00015
        except:
            return 0.0



# --- MOVEMENT III: THE FORGE OF GNOSIS (V-Ω-TOTALITY-V35.1-FINALIS) ---

    def _forge_synapse(self, request: BaseRequest, result: Any, status: str, duration: float, memory: float) -> Dict[str, Any]:
        """
        =================================================================================
        == THE DOSSIER FORGE (V-Ω-TOTALITY)                                            ==
        =================================================================================
        LIF: ∞ | ROLE: DATA_TRANSFIGURATOR
        """
        # [ASCENSION 1]: BICAMERAL CONTEXT EXTRACTION
        context = getattr(request, 'context', {}) or {}
        variables = getattr(request, 'variables', {}) or {}
        trace_id = getattr(request, 'trace_id', str(uuid.uuid4()))
        request_id = getattr(request, 'request_id', 'tr-void')

        # [ASCENSION 3]: HARDWARE TOMOGRAPHY
        vitals = self._scry_vitals_safe()

        # [ASCENSION 2]: QUANTUM ENTROPY SIEVE
        # Prevents high-entropy secrets from leaking into the Akasha.
        raw_msg = str(getattr(result, 'message', '')) if result else 'Rite Silenced.'
        clean_msg = self._entropy_sieve(raw_msg)

        # [ASCENSION 11]: ISOMORPHIC IDENTITY ANCHOR
        try:
            os_identity = platform.system() or "ETHER"
            os_kernel = platform.release() or "WASM"
            os_arch = platform.machine() or "WASM"
        except Exception:
            os_identity, os_kernel, os_arch = "VOID", "VOID", "VOID"

        # [ASCENSION 7]: GNOSTIC FINGERPRINT
        # Forges a deterministic ID for the host node.
        machine_raw = f"{platform.node()}:{os_arch}"
        gnostic_id = hashlib.sha256(machine_raw.encode()).hexdigest()[:16]

        # [ASCENSION 12]: THE FINALITY VOW
        return {
            "v": "35.1-Totality-Finalis",
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "timestamp": time.time(),
            "instance": self.instance_id,
            "gnostic_id": gnostic_id,
            "trace_id": trace_id,
            "request_id": request_id,
            "novalym_id": variables.get("novalym_id") or context.get("novalym_id", "GUEST"),
            "rite": request.__class__.__name__,
            "status": status,
            "performance": {
                "latency_ms": round(duration, 4),
                "mem_flux_mb": round(memory, 4),
                "backpressure": self._queue.qsize() if not self._is_wasm else 0
            },
            "vitals": vitals,
            "environment": {
                "os": os_identity,
                "substrate": vitals["substrate"],
                "python": platform.python_version(),
                "is_dev": os.getenv("SCAFFOLD_ENV") == "development"
            },
            "proclamation": clean_msg,
            "metadata": {
                "pid": os.getpid(),
                "thread": threading.current_thread().name
            }
        }

    def _forge_signature(self, payload: Dict) -> str:
        """[ASCENSION 10]: THE CRYPTOGRAPHIC SEAL."""
        msg = json.dumps(payload, sort_keys=True, default=str).encode()
        return hmac.new(_MACHINE_SECRET.encode(), msg, hashlib.sha256).hexdigest()

    # =========================================================================
    # == THE RADIATOR ENGINE (ISOMORPHIC)                                    ==
    # =========================================================================

    def _synapse_radiator_loop(self):
        """
        The Eternal Synapse Radiator (IRON ONLY).
        Consumes the priority queue in the background.
        """
        batch: List[Dict] = []
        last_flush = time.time()

        while not TelemetryMiddleware._is_wasm: # Thread safety
            try:
                try:
                    # Priority is index 0, timestamp 1, payload 2
                    _, _, packet = self._queue.get(timeout=2.0)
                    batch.append(packet)
                except queue.Empty:
                    pass

                now = time.time()
                if len(batch) >= 15 or (len(batch) > 0 and now - last_flush > 15.0):
                    self._radiate(batch)
                    batch = []
                    last_flush = now
            except Exception:
                time.sleep(5) # Cooldown on fracture

    def _radiate(self, batch: List[Dict]):
        """
        =============================================================================
        == THE RITE OF RADIATION (V-Ω-TOTALITY)                                    ==
        =============================================================================
        Transmits Gnosis to the Mothership. Handles the Ethereal Plane's
        synchronous limitations via the Local Sarcophagus.
        """
        if not HAS_CELESTIAL_LINK or not ENABLED:
            self._archive_to_sarcophagus(batch)
            return

        try:
            # [ASCENSION 12]: THE CELESTIAL STRIKE
            # We use a tight timeout to prevent the Engine from hanging on a slow aether.
            res = requests.post(
                MOTHERSHIP_URL,
                json={"synapses": batch},
                timeout=2.0,
                headers={"X-Titan-Node": self.instance_id, "X-Gnostic-Substrate": "WASM" if self._is_wasm else "IRON"}
            )

            if res.status_code != 200:
                self._archive_to_sarcophagus(batch)
            elif not self._is_wasm:
                # [ASCENSION 4]: THE LAZARUS RESURRECTION
                # Background log flushing only on Iron to prevent WASM thread collisions.
                if BUFFER_FILE.exists():
                    self._resurrect_shadow_logs()

        except Exception:
            self._archive_to_sarcophagus(batch)

    def _archive_to_sarcophagus(self, batch: List[Dict]):
        """[ASCENSION 4]: THE LOCAL SARCOPHAGUS. Persistent buffering for offline Gnosis."""
        try:
            AKASHA_DIR.mkdir(parents=True, exist_ok=True)
            with open(BUFFER_FILE, "a", encoding="utf-8") as f:
                for synapse in batch:
                    f.write(json.dumps(synapse) + "\n")
        except:
            pass

    def _resurrect_shadow_logs(self):
        """[THE LAZARUS RITE]: Flushes offline logs back to the Mothership."""
        try:
            # Atomic File Swapping to prevent log corruption
            lock_path = BUFFER_FILE.with_suffix(".lock")
            if not lock_path.exists():
                os.rename(BUFFER_FILE, lock_path)

            with open(lock_path, "r") as f:
                synapses = [json.loads(line) for line in f if line.strip()]

            if synapses:
                # Transmit in blocks of 50 to maintain metabolic stability
                for i in range(0, len(synapses), 50):
                    requests.post(MOTHERSHIP_URL, json={"synapses": synapses[i:i + 50]}, timeout=5.0)

            os.remove(lock_path)
        except Exception:
            pass

    def __repr__(self) -> str:
        return f"<Ω_SYNAPTIC_RELAY instance={self.instance_id} substrate={'ETHER' if self._is_wasm else 'IRON'}>"

