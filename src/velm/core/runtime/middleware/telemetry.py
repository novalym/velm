# Path: src/velm/core/runtime/middleware/telemetry.py
# ---------------------------------------------------

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List, Tuple, Final
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
_MACHINE_SECRET: Final[str] = os.getenv("SCAFFOLD_INTERNAL_KEY", uuid.getnode())

# [ASCENSION 11]: METABOLIC CACHE
_VITALS_CACHE: List[Any] = [0, {}]  # [Timestamp, Vitals_Dict]
_VITALS_LOCK = threading.Lock()
_VITALS_TTL = 1.5  # Seconds of freshness for hardware scrying


class TelemetryMiddleware(Middleware):
    """
    =============================================================================
    == THE SYNAPTIC RELAY (V-Ω-TOTALITY-V20.0-LEGENDARY-FINALIS)               ==
    =============================================================================
    LIF: ∞ | ROLE: SYNAPTIC_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_TELEMETRY_V20_TOTALITY

    The supreme orchestrator of system observability. It transmutes the internal
    kinetics of the God-Engine into a stream of Gnostic light for the Akasha.
    """

    # [ASCENSION 9]: Prioritized Synaptic Queue
    _queue: queue.PriorityQueue = queue.PriorityQueue(maxsize=1000)
    _executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="SynapseRadiator")
    _initialized = False
    _lock = threading.Lock()

    def __init__(self, engine: Any):
        """[THE RITE OF INCEPTION]"""
        super().__init__(engine)
        self._ensure_radiator_active()
        self.instance_id = f"node-{uuid.uuid4().hex[:6].upper()}"
        self.Logger = Scribe("SynapticRelay")

    def _ensure_radiator_active(self):
        """Materializes the background processing thread."""
        with self._lock:
            if not TelemetryMiddleware._initialized:
                TelemetryMiddleware._executor.submit(self._synapse_radiator_loop)
                TelemetryMiddleware._initialized = True

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF PERCEPTION (HANDLE)                                         ==
        =============================================================================
        Intercepts the plea, times the transmutation, and radiates the result.
        """
        if not ENABLED:
            return next_handler(request)

        # [ASCENSION 1]: Nanosecond Precision
        start_ns = time.perf_counter_ns()
        start_mem = self._get_memory_usage()

        status = "INTERRUPTED"
        result = None

        try:
            # --- THE EXECUTION (THE CORE WORK) ---
            result = next_handler(request)

            # --- ADJUDICATE OUTCOME ---
            if result is None:
                status = "VOID_REVELATION"
            elif hasattr(result, "success"):
                status = "SUCCESS" if result.success else "HERESY"
            elif isinstance(result, dict):
                is_success = result.get("success", True) and not result.get("error")
                status = "SUCCESS" if is_success else "HERESY"
            else:
                status = "UNKNOWN_REALITY"

            return result

        except Exception as fracture:
            status = "CATASTROPHIC_COLLAPSE"
            # Return original result or forge a crash-result for the pipeline
            raise fracture

        finally:
            # --- METABOLIC FINALITY ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            end_mem = self._get_memory_usage()
            mem_delta_mb = end_mem - start_mem

            # [ASCENSION 2 & 9]: ENQUEUE FOR RADIATION
            try:
                self._enqueue_synapse(request, result, status, duration_ms, mem_delta_mb)
            except Exception as telemetry_paradox:
                # The Relay must NEVER crash the Engine.
                self.Logger.verbose(f"Synapse failed to radiate: {telemetry_paradox}")

    def _enqueue_synapse(self, request: BaseRequest, result: Any, status: str, duration: float, memory: float):
        """Wraps the data in a priority packet and places it on the synaptic bus."""
        priority = 10  # Normal
        if status in ("HERESY", "CATASTROPHIC_COLLAPSE"):
            priority = 1  # High Priority

        try:
            # Pre-forge the payload to capture current state context
            payload = self._forge_synapse(request, result, status, duration, memory)

            # [ASCENSION 10]: CRYPTOGRAPHIC SEALING
            payload["signature"] = self._forge_signature(payload)

            try:
                # (Priority, Timestamp, Payload)
                self._queue.put_nowait((priority, time.time(), payload))
            except queue.Full:
                # [ASCENSION 2]: Hydraulic Shield - Drop oldest to prevent OOM
                try:
                    self._queue.get_nowait()
                    self._queue.put_nowait((priority, time.time(), payload))
                except:
                    pass
        except Exception:
            pass

    def _forge_synapse(self, request: BaseRequest, result: Any, status: str, duration: float, memory: float) -> Dict[
        str, Any]:
        """
        =================================================================================
        == THE FORGE OF GNOSIS (V-Ω-TOTALITY-V20.1-TITANIUM-FINALIS)                   ==
        =================================================================================
        LIF: ∞ | ROLE: DATA_TRANSFIGURATOR | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: @!#()#()@)#(!@)#(
        """
        # [ASCENSION 1]: NONETYPE SARCOPHAGUS
        # Defensive extraction of intent context to prevent AttributeErrors on ghost requests.
        context = getattr(request, 'context', {}) or {}
        variables = getattr(request, 'variables', {}) or {}
        trace_id = getattr(request, 'trace_id', str(uuid.uuid4()))
        request_id = getattr(request, 'request_id', 'tr-void')

        # [ASCENSION 3 & 9]: BICAMERAL MEMORY & HARDWARE LATTICE SCRYING
        # Warded against hardware failures and OS-level permission heresies.
        vitals_tomography = self._scry_vitals_safe()

        # [ASCENSION 4]: METABOLIC TAX & ENGINE FRICTION
        # Siphons the economic cost from the result, if manifest.
        result_vitals = getattr(result, 'vitals', {}) if result else {}
        cost_usd = float(result_vitals.get("metabolic_cost_usd", 0.0))

        # [ASCENSION 2]: QUANTUM ENTROPY SIEVE
        # Redacts high-information-density matter (Secrets) from the proclamation.
        raw_msg = str(getattr(result, 'message', '')) if result else 'Rite Concluded in Silence.'
        clean_msg = self._entropy_sieve(raw_msg)

        # [ASCENSION 11]: PLATFORM PURITY WARD (THE FIX)
        # Replacing the heretical os.platform with the righteous platform module.
        try:
            os_identity = platform.system()  # e.g., 'Linux', 'Windows'
            os_kernel = platform.release()  # e.g., '5.15.0-generic'
            os_arch = platform.machine()  # e.g., 'x86_64'
        except Exception:
            os_identity = "VOID_OS"
            os_kernel = "VOID_KERNEL"
            os_arch = "VOID_ARCH"

        # [ASCENSION 7]: ISOMORPHIC IDENTITY
        machine_raw = f"{platform.node()}:{socket.gethostname()}:{os_arch}"
        gnostic_id = hashlib.sha256(machine_raw.encode()).hexdigest()[:16]

        # [ASCENSION 5]: INDUSTRIAL SOUL DIVINATION
        # Divines the project's purpose from the variables.
        industry_intent = self._divine_industry(variables)

        # [ASCENSION 6]: MERKLE CONTEXT SEAL
        # Fingerprints the willed state for integrity verification.
        context_fingerprint = hashlib.sha256(json.dumps(variables, sort_keys=True, default=str).encode()).hexdigest()[
                              :12]

        # [ASCENSION 12]: THE FINALITY VOW
        # Constructing the definitive Gnostic Dossier.
        return {
            "v": "20.1-Totality-Finalis",
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "timestamp": time.time(),
            "instance": self.instance_id,
            "gnostic_id": gnostic_id,
            "trace_id": trace_id,
            "request_id": request_id,
            "novalym_id": variables.get("novalym_id") or context.get("novalym_id", "SYSTEM"),
            "rite": request.__class__.__name__,
            "status": status,
            "performance": {
                "latency_ms": round(duration, 4),
                "mem_flux_mb": round(memory, 4),
                "tax_usd": cost_usd,
                "backpressure_depth": self._queue.qsize()  # [ASCENSION 8]
            },
            "vitals": vitals_tomography,
            "environment": {
                "os": os_identity,
                "kernel": os_kernel,
                "arch": os_arch,
                "python": platform.python_version(),
                "machine_id": self._machine_id,
                "is_dev": os.getenv("SCAFFOLD_ENV") == "development"
            },
            "intent": {
                "industry": industry_intent,
                "tier": variables.get("tier", "standard"),
                "is_remote": bool(getattr(request, 'remote', False)),
                "is_container": bool(getattr(request, 'runtime', '') == 'docker'),
                "context_hash": context_fingerprint
            },
            "proclamation": clean_msg,
            "metadata": {
                "source_file": os.path.basename(sys.argv[0]),
                "pid": os.getpid(),
                "thread": threading.current_thread().name
            }
        }

    # =========================================================================
    # == PRIVATE FACULTIES (THE INTERNAL ORGANS)                             ==
    # =========================================================================

    def _scry_vitals_safe(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE GAZE OF VITALITY (V-Ω-WARDED-SCRIER)                                ==
        =============================================================================
        [THE CURE]: Total try/except protection of hardware scrying.
        """
        if not HAS_SENSES:
            return {"senses": "blind"}

        now = time.time()
        with _VITALS_LOCK:
            if now - _VITALS_CACHE[0] < _VITALS_TTL:
                return _VITALS_CACHE[1]

            try:
                # Perform the biological tomography
                # Note: interval=None makes psutil.cpu_percent non-blocking
                vitals = {
                    "cpu_load": psutil.cpu_percent(interval=None),
                    "ram_percent": psutil.virtual_memory().percent,
                    "swap_percent": psutil.swap_memory().percent,
                    "io_wait": getattr(psutil.cpu_times_percent(), 'iowait', 0.0),
                    "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
                    "process_threads": threading.active_count(),
                    "handle_count": len(psutil.Process().open_files()) if hasattr(psutil.Process(), 'open_files') else 0
                }

                # [ASCENSION 11]: Cache the scry result
                _VITALS_CACHE[0] = now
                _VITALS_CACHE[1] = vitals
                return vitals
            except Exception:
                # If hardware is uncooperative, return the previous state or empty
                return _VITALS_CACHE[1]

    def _entropy_sieve(self, text: str) -> str:
        """
        [ASCENSION 3]: SHANNON ENTROPY ADJUDICATOR.
        Redacts high-information-density strings (secrets/keys).
        """
        if not text or len(text) < 12:
            return text

        # Heuristic: Find continuous non-space sequences
        words = text.split()
        sanitized_words = []

        for word in words:
            if len(word) > 24:
                # Calculate basic entropy
                prob = [float(word.count(c)) / len(word) for c in dict.fromkeys(list(word))]
                entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])

                # Keys (Stripe/JWT/API) typically have entropy > 4.0
                if entropy > 3.9 and not any(c in word for c in ('/', '.', '\\')):
                    sanitized_words.append("[REDACTED_HIGH_ENTROPY_MATTER]")
                    continue
            sanitized_words.append(word)

        return " ".join(sanitized_words)

    def _divine_industry(self, vars: Dict) -> str:
        """[ASCENSION 5]: INTENT DIVINATION."""
        # Simple heuristic based on common project variables
        keys = vars.keys()
        if any(k in keys for k in ("stripe", "billing", "invoice", "wallet")): return "FINTECH"
        if any(k in keys for k in ("model", "openai", "training", "weights")): return "NEURAL_AI"
        if any(k in keys for k in ("vpc", "cluster", "terraform", "s3")): return "INFRASTRUCTURE"
        return "GENERAL_COMPUTE"

    def _forge_signature(self, payload: Dict) -> str:
        """[ASCENSION 10]: CRYPTOGRAPHIC SEAL."""
        # Canonicalize JSON for consistent hashing
        msg = json.dumps(payload, sort_keys=True).encode()
        return hmac.new(str(_MACHINE_SECRET).encode(), msg, hashlib.sha256).hexdigest()

    def _get_memory_usage(self) -> float:
        """Standard RSS TOMOGRAPHY."""
        try:
            if HAS_SENSES:
                return psutil.Process().memory_info().rss / 1024 / 1024
        except:
            pass
        return 0.0

    # =========================================================================
    # == THE RADIATOR ENGINE (BACKGROUND)                                    ==
    # =========================================================================

    def _synapse_radiator_loop(self):
        """The Eternal Synapse Radiator."""
        batch: List[Dict] = []
        last_flush = time.time()

        while True:
            try:
                # 1. Fetch from Priority Queue (Blocking)
                try:
                    # priority is index 0, payload is index 2
                    _, _, packet = self._queue.get(timeout=2.0)
                    batch.append(packet)
                except queue.Empty:
                    pass

                # 2. Adjudicate Radiation Rite
                now = time.time()
                # Radiation occurs every 10 packets OR 10 seconds of latency
                if len(batch) >= 10 or (len(batch) > 0 and now - last_flush > 10.0):
                    self._radiate(batch)
                    batch = []
                    last_flush = now

            except Exception:
                # Radiator is immortal; retry in 5s if logic fractures
                time.sleep(5)

    def _radiate(self, batch: List[Dict]):
        """Transmits the Gnosis across the celestial link."""
        if not HAS_CELESTIAL_LINK:
            self._archive_to_sarcophagus(batch)
            return

        try:
            # 1. ATTEMPT CELESTIAL EMISSION
            res = requests.post(
                MOTHERSHIP_URL,
                json={"synapses": batch},
                timeout=3.0,
                headers={"X-Titan-Instance": self.instance_id}
            )

            if res.status_code != 200:
                self._archive_to_sarcophagus(batch)
            else:
                # [ASCENSION 4]: LAZARUS RESURRECTION
                # If we were previously offline, check if shadow logs need flushing
                if BUFFER_FILE.exists():
                    self._resurrect_shadow_logs()

        except Exception:
            # 2. ARCHIVE ON FAILURE
            self._archive_to_sarcophagus(batch)

    def _archive_to_sarcophagus(self, batch: List[Dict]):
        """[ASCENSION 4]: THE LOCAL SARCOPHAGUS."""
        try:
            AKASHA_DIR.mkdir(parents=True, exist_ok=True)
            with open(BUFFER_FILE, "a", encoding="utf-8") as f:
                for synapse in batch:
                    f.write(json.dumps(synapse) + "\n")
        except:
            pass

    def _resurrect_shadow_logs(self):
        """[ASCENSION 4]: FLUSH THE SHADOWS."""
        try:
            # Attempt to move the file to a lock-state for reading
            lock_path = BUFFER_FILE.with_suffix(".lock")
            if not lock_path.exists():
                BUFFER_FILE.rename(lock_path)

            with open(lock_path, "r") as f:
                synapses = [json.loads(line) for line in f if line.strip()]

            if synapses:
                # Emit in bulk (max 50 at a time to prevent timeout)
                for i in range(0, len(synapses), 50):
                    requests.post(MOTHERSHIP_URL, json={"synapses": synapses[i:i + 50]}, timeout=10.0)

            lock_path.unlink()
        except:
            pass

    def __repr__(self) -> str:
        return f"<Ω_SYNAPTIC_RELAY instance={self.instance_id} queue={self._queue.qsize()}>"

# == SCRIPTURE SEALED: THE AKASHIC PERCEPTION IS NOW OMEGA TOTALITY ==