# Path: core/runtime/middleware/telemetry.py
# ------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_TELEMETRY_SINGULARITY_V12_TOTALITY
# SYSTEM: GNOSTIC_SPINE | ROLE: OBSERVABILITY_ENGINE
# =================================================================================

import hashlib
import json
import os
import platform
import threading
import time
import uuid
import sys
import queue
import socket
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List, Tuple, Final
from concurrent.futures import ThreadPoolExecutor

try:
    import requests
except ImportError:
    requests = None

try:
    import psutil
except ImportError:
    psutil = None

from .contract import Middleware
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest

# --- THE GNOSTIC CONFIGURATION ---
MOTHERSHIP_URL: Final[str] = os.getenv("SCAFFOLD_TELEMETRY_URL", "https://telemetry.novalym.dev.com/ingest")
AKASHA_DIR: Final[Path] = Path.home() / ".scaffold" / "telemetry"
BUFFER_FILE: Final[Path] = AKASHA_DIR / "shadow_logs.jsonl"
ENABLED: Final[bool] = os.getenv("SCAFFOLD_TELEMETRY", "1") != "0"

# --- THE METABOLIC CACHE (ASCENSION 10) ---
# (Timestamp, Vitals_Dict)
_VITALS_CACHE: List[Any] = [0, {}]
_VITALS_LOCK = threading.Lock()
_VITALS_TTL = 10.0


class TelemetryMiddleware(Middleware):
    """
    =============================================================================
    == THE SYNAPTIC RELAY (V-Ω-TOTALITY-V12-OMNISCIENT)                        ==
    =============================================================================
    LIF: ∞ | ROLE: SYNAPTIC_CONDUCTOR | RANK: OMEGA_SOVEREIGN

    The supreme orchestrator of system observability. It transmutes the internal
    kinetics of the Monolith into a stream of Gnostic light.
    """

    _queue: queue.Queue = queue.Queue(maxsize=1000)
    _executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="SynapseRadiator")
    _initialized = False
    _lock = threading.Lock()

    def __init__(self, engine: Any):
        super().__init__(engine)
        self._ensure_radiator_active()
        self.instance_id = f"node-{uuid.uuid4().hex[:6].upper()}"

    def _ensure_radiator_active(self):
        """[ASCENSION 1]: Materializes the background processing thread."""
        with self._lock:
            if not TelemetryMiddleware._initialized:
                TelemetryMiddleware._executor.submit(self._synapse_radiator_loop)
                TelemetryMiddleware._initialized = True

    def handle(self, request: BaseRequest, next_handler: Callable[[BaseRequest], ScaffoldResult]) -> ScaffoldResult:
        if not ENABLED:
            return next_handler(request)

        # 1. Capture Inception Physics
        start_time = time.perf_counter()
        start_mem = self._get_memory_usage()

        # [ASCENSION 12]: Initialize status early to guard against SystemExit
        status = "interrupted"
        result = None

        try:
            # 2. Execute the Rite
            # This is the moment of manifest logic
            result = next_handler(request)

            # 3. Adjudicate Outcome (Dual-Mode Divination)
            if result is None:
                status = "void"
            elif hasattr(result, "success"):
                status = "success" if result.success else "failure"
            elif isinstance(result, dict):
                is_success = result.get("success", True) and not result.get("error")
                status = "success" if is_success else "failure"
            else:
                status = "unknown"

            return result

        except Exception as e:
            status = "crash"
            # Explicitly define result for the crash context
            result = {"error": str(e), "success": False, "traceback": str(sys.exc_info())}
            raise e

        finally:
            # 4. Finalize Metabolic Metrics
            duration_ms = (time.perf_counter() - start_time) * 1000
            end_mem = self._get_memory_usage()
            mem_delta = end_mem - start_mem

            # 5. Enqueue for Radiation
            # [ASCENSION 1]: Zero-latency offload
            self._enqueue_synapse(request, result, status, duration_ms, mem_delta)

    def _enqueue_synapse(self, request: BaseRequest, result: Any, status: str, duration: float, memory: float):
        """[ASCENSION 1]: Places the event on the high-speed synaptic queue."""
        try:
            # Forge the packet synchronously to capture current state
            payload = self._forge_synapse(request, result, status, duration, memory)

            try:
                self._queue.put_nowait(payload)
            except queue.Full:
                # [ASCENSION 7]: Sacred Shear
                # Drop oldest if queue is backpressured
                try:
                    self._queue.get_nowait()
                except:
                    pass
                self._queue.put_nowait(payload)
        except Exception as e:
            # Telemetry must never kill the main thread
            pass

    def _forge_synapse(self, request: BaseRequest, result: Any, status: str, duration: float, memory: float) -> Dict[
        str, Any]:
        """
        =============================================================================
        == THE FORGE OF GNOSIS (V-Ω-TOTALITY-V12)                                  ==
        =============================================================================
        LIF: ∞ | ROLE: DATA_TRANSFIGURATOR
        """
        # [ASCENSION 3]: GNOSTIC IDENTITY FINGERPRINT
        # Hash the machine DNA to identify the node without PII
        machine_raw = f"{platform.node()}:{socket.gethostname()}:{platform.processor()}"
        gnostic_id = hashlib.sha256(machine_raw.encode()).hexdigest()[:16]

        # [ASCENSION 5]: RECURSIVE CONTEXT SIPHON
        # Extract industrial and economic metadata
        context = getattr(request, 'context', {}) or {}
        variables = getattr(request, 'variables', {}) or {}

        # [ASCENSION 4]: METABOLIC TAX ACCOUNTING
        # Siphon cost data from the result vitals if it's an AI strike
        vitals = getattr(result, 'vitals', {}) if hasattr(result, 'vitals') else {}
        cost_usd = float(vitals.get("metabolic_cost_usd", 0.0))

        # [ASCENSION 2 & 10]: THERMODYNAMIC TOMOGRAPHY
        vitals_biopsy = self._scry_vitals()

        # [ASCENSION 8]: SOVEREIGN REDACTION
        # Ensure result data is safe before sending
        safe_data_preview = None
        if result and status != "crash":
            # Just a high-level summary, no PII
            if isinstance(result, dict):
                safe_data_preview = {"keys": list(result.keys())}
            elif hasattr(result, 'data') and isinstance(result.data, dict):
                safe_data_preview = {"keys": list(result.data.keys())}

        return {
            "timestamp": time.time(),
            "instance": self.instance_id,
            "gnostic_id": gnostic_id,
            "trace_id": getattr(request, 'trace_id', str(uuid.uuid4())),
            "novalym_id": variables.get("novalym_id") or context.get("novalym_id", "SYSTEM"),
            "rite": request.__class__.__name__,
            "status": status,
            "performance": {
                "duration_ms": round(duration, 3),
                "memory_delta_mb": round(memory, 4),
                "metabolic_tax_usd": cost_usd
            },
            "vitals": vitals_biopsy,
            "environment": {
                "os": platform.system(),
                "arch": platform.machine(),
                "python": platform.python_version(),
                "scaffold_v": os.getenv("SCAFFOLD_VERSION", "unknown"),
                "is_dev": os.getenv("SCAFFOLD_ENV") == "development"
            },
            "context": {
                "industry": variables.get("industry") or context.get("industry"),
                "tier": variables.get("tier") or context.get("client_tier"),
                "remote": bool(getattr(request, 'remote', False)),
                "docker": bool(getattr(request, 'runtime', '') == 'docker')
            },
            "forensics": {
                "data_schema": safe_data_preview,
                "error_summary": str(result.get("error")) if isinstance(result, dict) else None
            }
        }

    def _synapse_radiator_loop(self):
        """
        =============================================================================
        == THE SYNAPSE RADIATOR (V-Ω-ACHRONAL-BATCHING)                            ==
        =============================================================================
        LIF: ∞ | ROLE: DATA_EMITTER
        """
        batch: List[Dict] = []
        last_flush = time.time()

        while True:
            try:
                # 1. Wait for matter (Non-blocking with timeout)
                try:
                    event = self._queue.get(timeout=1.0)
                    batch.append(event)
                except queue.Empty:
                    pass

                # 2. Adjudicate Flush Rite
                now = time.time()
                # Flush if 10 events reached OR 5 seconds passed
                if len(batch) >= 10 or (len(batch) > 0 and now - last_flush > 5.0):
                    self._radiate(batch)
                    batch = []
                    last_flush = now

            except Exception as fracture:
                # The Radiator is immortal
                time.sleep(2)

    def _radiate(self, batch: List[Dict]):
        """[THE KINETIC EMISSION] Transmits or archives the Gnosis."""
        if not requests:
            self._archive_to_sarcophagus(batch)
            return

        try:
            # 1. TRANSMIT
            res = requests.post(
                MOTHERSHIP_URL,
                json={"batch": batch},
                timeout=2.0,
                headers={"X-Nov-Instance": self.instance_id}
            )

            if res.status_code != 200:
                self._archive_to_sarcophagus(batch)
            else:
                # [ASCENSION 7]: Flush the Shadow if we have internet again
                if BUFFER_FILE.exists():
                    self._resurrect_shadow_logs()

        except Exception:
            # 2. ARCHIVE (FALLBACK)
            self._archive_to_sarcophagus(batch)

    def _archive_to_sarcophagus(self, batch: List[Dict]):
        """[ASCENSION 6]: The Local Sarcophagus (Resilience Buffer)."""
        try:
            AKASHA_DIR.mkdir(parents=True, exist_ok=True)
            with open(BUFFER_FILE, "a", encoding="utf-8") as f:
                for event in batch:
                    f.write(json.dumps(event) + "\n")
        except Exception:
            pass

    def _resurrect_shadow_logs(self):
        """[ASCENSION 6]: Re-integrates offline data when connection is resonant."""
        try:
            # Simple atomic move to lock file
            lock_file = BUFFER_FILE.with_suffix(".lock")
            BUFFER_FILE.rename(lock_file)

            with open(lock_file, "r") as f:
                payloads = [json.loads(line) for line in f if line.strip()]

            if payloads:
                # Send in one heavy burst
                requests.post(MOTHERSHIP_URL, json={"batch": payloads}, timeout=10.0)

            lock_file.unlink()
        except:
            pass

    def _scry_vitals(self) -> Dict[str, Any]:
        """[ASCENSION 10]: High-speed metabolic scrying with caching."""
        if not psutil: return {}

        now = time.time()
        with _VITALS_LOCK:
            if now - _VITALS_CACHE[0] < _VITALS_TTL:
                return _VITALS_CACHE[1]

            # Perform the Tomography
            try:
                vitals = {
                    "cpu_load": psutil.cpu_percent(),
                    "mem_percent": psutil.virtual_memory().percent,
                    "io_wait": getattr(psutil.cpu_times_percent(), 'iowait', 0.0),
                    "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0],
                    "process_threads": threading.active_count()
                }
                _VITALS_CACHE[0] = now
                _VITALS_CACHE[1] = vitals
                return vitals
            except:
                return _VITALS_CACHE[1]

    def _get_memory_usage(self) -> float:
        """[ASCENSION 6]: THE METABOLIC GAUGE"""
        try:
            if psutil:
                process = psutil.Process()
                return process.memory_info().rss / 1024 / 1024  # MB
        except:
            pass
        return 0.0

    def __repr__(self) -> str:
        return f"<Ω_TELEMETRY_CONDUCTOR node={self.instance_id} queue={self._queue.qsize()}>"

# == SCRIPTURE SEALED: THE SYNAPTIC RELAY IS OMNIPOTENT ==