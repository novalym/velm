# Path: src/velm/core/runtime/middleware/profiler.py
# --------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_PROFILER_SINGULARITY_V100K
# SYSTEM: GNOSTIC_SPINE | ROLE: METABOLIC_OBSERVER
# =================================================================================

import time
import sys
import os
import threading
import json
import traceback
from typing import Any, Callable, Dict, Union, Optional, Final
from dataclasses import dataclass, field

try:
    import psutil

    HAS_SENSES = True
except ImportError:
    psutil = None
    HAS_SENSES = False

# --- CORE UPLINKS ---
from .contract import Middleware
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest


@dataclass
class MetricSnapshot:
    """The Atomic State of the Machine at a single point in spacetime."""
    timestamp_ns: int
    memory_mb: float
    cpu_percent: float
    thread_count: int
    fd_count: int


class ProfilingMiddleware(Middleware):
    """
    =============================================================================
    == THE CHRONOMETRIC SENTINEL (V-Ω-TOTALITY-V100K-SILENT-GUARDIAN)          ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: METABOLIC_OBSERVER | RANK: OMEGA_SOVEREIGN

    Performs high-fidelity tomography of every kinetic rite.

    ### THE PANTHEON OF ASCENSIONS:
    1.  **Nanosecond Chronometry:** Measures execution time with `perf_counter_ns`.
    2.  **Entropy Drift Detection:** Calculates memory delta (Start vs End) to spot leaks.
    3.  **The Silence Vow (THE CURE):** Strictly gates console output. [SPINE] logs only
        appear if `SCAFFOLD_VERBOSE=1`. Normal operations are silent.
    4.  **Forensic Autopsy:** If a rite fails, it dumps the raw exception payload
        to stderr immediately for debugging, bypassing UI buffers.
    5.  **Akashic Radiation:** Multicasts telemetry to the `akashic` event bus for
        real-time graph rendering in the Frontend.
    6.  **Slow-Path Markers:** Automatically flags operations > 200ms as `HEAVY_MATTER`.
    7.  **Metabolic Injection:** Grafts the profile data into `result.data._profiler`.
    8.  **Thread-Safety:** Uses thread-local snapshots to handle concurrent swarms.
    """

    # Threshold for "Heavy" operations (ms)
    HEAVY_THRESHOLD: Final[float] = 200.0

    def handle(self, request: BaseRequest, next_handler: Callable[[BaseRequest], ScaffoldResult]) -> ScaffoldResult:
        # [ASCENSION 1]: PRE-FLIGHT SNAPSHOT
        start_metrics = self._scry_metabolism()

        trace_id = getattr(request, 'trace_id', '0xVOID')
        rite_name = type(request).__name__.replace('Request', '')

        # Determine strictness of silence
        is_verbose = os.environ.get("SCAFFOLD_VERBOSE") == "1"
        is_json_mode = getattr(request, 'json_mode', False)

        result = None
        status = "INCOMPLETE"
        error_context = None

        try:
            # --- THE KINETIC STRIKE ---
            result = next_handler(request)

            # [ASCENSION 2]: TYPE-AGNOSTIC ADJUDICATION
            if result is None:
                status = "VOID_RETURN"
            else:
                success = self._divine_success(result)
                status = "SUCCESS" if success else "HERESY"

            return result

        except Exception as e:
            status = "FRACTURED"
            error_context = e
            raise e

        finally:
            # [ASCENSION 3]: POST-FLIGHT SNAPSHOT & DELTA CALC
            end_metrics = self._scry_metabolism()

            duration_ms = (end_metrics.timestamp_ns - start_metrics.timestamp_ns) / 1_000_000
            mem_delta = end_metrics.memory_mb - start_metrics.memory_mb

            # [ASCENSION 4]: THE SILENCE VOW (LOGGING GATE)
            # We ONLY print to the console if:
            # A) The user explicitly asked for VERBOSE logs.
            # B) The system FRACTURED (Crashed).
            # C) The result was a HERESY (Logic Failure) AND we are not in JSON mode.

            should_proclaim = is_verbose or status == "FRACTURED" or (status == "HERESY" and not is_json_mode)

            if should_proclaim:
                slow_marker = " [!! HEAVY_MATTER !!]" if duration_ms > self.HEAVY_THRESHOLD else ""
                color_code = "92" if status == "SUCCESS" else "91" if status == "FRACTURED" else "93"

                # Format: [SPINE] +120ms : RiteName [TraceID] -> STATUS
                telemetry_pulse = (
                    f"\x1b[{color_code}m[SPINE] +{duration_ms:8.2f}ms : {rite_name:<20} "
                    f"[ [dim]{trace_id[:8]}[/] ] -> {status}{slow_marker}\x1b[0m"
                )

                # Write to stderr to bypass any stdout captures (VisualCortexStream usually allows stderr)
                sys.stderr.write(f"{telemetry_pulse}\n")

                # [ASCENSION 5]: FORENSIC ILLUMINATION
                if status in ("HERESY", "FRACTURED"):
                    self._proclaim_heresy(result, error_context, rite_name)

            # [ASCENSION 6]: DATA GRAFTING & RADIATION
            # We always inject the data into the result object so the UI can render it.
            self._inject_profiler_gnosis(result, duration_ms, mem_delta, status, start_metrics, end_metrics)

            # [ASCENSION 7]: AKASHIC MULTICAST
            self._radiate_to_akasha(rite_name, trace_id, duration_ms, status)

    def _scry_metabolism(self) -> MetricSnapshot:
        """Captures atomic hardware state."""
        mem = 0.0
        cpu = 0.0
        fds = 0
        threads = 1

        try:
            # Native Iron Logic
            if HAS_SENSES:
                p = psutil.Process()
                with p.oneshot():
                    mem = p.memory_info().rss / 1024 / 1024
                    cpu = p.cpu_percent()
                    threads = p.num_threads()
                    if os.name != 'nt':
                        fds = p.num_fds()
        except:
            # WASM Ether Logic (Heuristic)
            try:
                import gc
                # 100k objects ~ 15MB Gnostic Mass
                mem = len(gc.get_objects()) * 0.00015
            except:
                pass

        return MetricSnapshot(
            timestamp_ns=time.perf_counter_ns(),
            memory_mb=mem,
            cpu_percent=cpu,
            thread_count=threads,
            fd_count=fds
        )

    def _divine_success(self, result: Any) -> bool:
        """Checks Pydantic models, dicts, and objects for success flags."""
        if hasattr(result, 'success'): return bool(result.success)
        if isinstance(result, dict):
            return bool(result.get('success', True)) and not result.get('error')
        return True

    def _proclaim_heresy(self, result: Any, error: Optional[Exception], rite: str):
        """Dumps forensic data to stderr on failure."""
        try:
            sys.stderr.write(f"\n\x1b[41;1m[FORENSIC] HERESY DETECTED IN {rite}:\x1b[0m\n")

            if error:
                sys.stderr.write(f"   Exception: {type(error).__name__}: {str(error)}\n")
                traceback.print_tb(error.__traceback__, file=sys.stderr)

            if result:
                msg = getattr(result, 'message', '') or (result.get('message') if isinstance(result, dict) else '')
                details = getattr(result, 'error', '') or getattr(result, 'details', '')
                if msg: sys.stderr.write(f"   Message: {msg}\n")
                if details: sys.stderr.write(f"   Details: {str(details)[:500]}\n")

            sys.stderr.flush()
        except:
            pass

    def _inject_profiler_gnosis(
            self,
            result: Any,
            duration: float,
            mem_delta: float,
            status: str,
            start: MetricSnapshot,
            end: MetricSnapshot
    ):
        """Grafts telemetry onto the result vessel."""
        if result is None or not isinstance(result, (dict, object)):
            return

        gnosis = {
            "duration_ms": round(duration, 3),
            "memory_delta_mb": round(mem_delta, 4),
            "status": status,
            "thread_id": threading.get_ident(),
            "cpu_load_start": start.cpu_percent,
            "cpu_load_end": end.cpu_percent,
            "timestamp": time.time()
        }

        try:
            if isinstance(result, dict):
                result.setdefault('data', {})
                if isinstance(result['data'], dict):
                    result['data']['_profiler'] = gnosis
            elif hasattr(result, 'data'):
                if result.data is None:
                    # Handle Pydantic immutability via setattr bypass if needed,
                    # though 'data' field is usually mutable or a Dict.
                    try:
                        result.data = {}
                    except:
                        pass  # Immutable model
                if isinstance(result.data, dict):
                    result.data['_profiler'] = gnosis
        except:
            pass

    def _radiate_to_akasha(self, rite: str, trace: str, duration: float, status: str):
        """
        Multicasts the event to the React UI via the Akashic Record.
        This allows the Frontend to show a 'Toast' or 'Pulse' without console logs.
        """
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "KINETIC_PROFILE",
                        "label": f"{rite.upper()}_{status}",
                        "color": "#ef4444" if status != "SUCCESS" else "#64ffda",
                        "duration": duration,
                        "trace": trace
                    }
                })
            except:
                pass