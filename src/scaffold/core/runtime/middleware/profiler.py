# Path: core/runtime/middleware/profiler.py
# ------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_PROFILER_SINGULARITY_V9000
# SYSTEM: GNOSTIC_SPINE | ROLE: METABOLIC_WATCHDOG
# =================================================================================

import time
import sys
import os
import threading
from typing import Any, Callable, Dict, Union, Optional
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None

from .contract import Middleware
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest


class ProfilingMiddleware(Middleware):
    """
    =============================================================================
    == THE CHRONOMETRIC SENTINEL (V-Ω-TOTALITY-FINALIS)                        ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: METABOLIC_OBSERVER

    Performs high-fidelity tomography of every rite.
    Measures temporal duration, memory flux, and logical outcome.
    """

    def handle(self, request: BaseRequest, next_handler: Callable[[BaseRequest], ScaffoldResult]) -> ScaffoldResult:
        # [ASCENSION 2]: Nanosecond Ignition
        start_ns = time.perf_counter_ns()
        start_mem = self._get_memory_mb()

        trace_id = getattr(request, 'trace_id', '0xVOID')
        rite_name = type(request).__name__.replace('Request', '')

        result = None
        status = "INCOMPLETE"

        try:
            # 1. EXECUTE THE CHAIN
            result = next_handler(request)

            # 2. [ASCENSION 1 & 5]: TYPE-AGNOSTIC ADJUDICATION
            if result is None:
                status = "VOID_RETURN"
            else:
                success = self._divine_success(result)
                status = "SUCCESS" if success else "HERESY"

            return result

        except Exception as e:
            status = "FRACTURED"
            raise e

        finally:
            # 3. [ASCENSION 2]: CALCULATE DELTAS
            end_ns = time.perf_counter_ns()
            end_mem = self._get_memory_mb()

            duration_ms = (end_ns - start_ns) / 1_000_000
            mem_delta = end_mem - start_mem

            # 4. [ASCENSION 7 & 8]: PROCLAIM TELEMETRY
            slow_marker = " [!! HEAVY_MATTER !!]" if duration_ms > 200 else ""

            telemetry_pulse = (
                f"[SPINE] +{duration_ms:8.2f}ms : {rite_name:<20} "
                f"[ [dim]{trace_id}[/] ] -> {status}{slow_marker}"
            )

            # [THE FIX]: FORENSIC ILLUMINATION
            # If Heresy is detected, dump the payload to stderr immediately.
            if status == "HERESY" and result:
                import json
                try:
                    # Try to extract the error message safely
                    if hasattr(result, 'message'):
                        err_msg = result.message
                        err_details = getattr(result, 'error', '') or getattr(result, 'details', '')
                    elif isinstance(result, dict):
                        err_msg = result.get('message', 'Unknown Error')
                        err_details = result.get('error', '')
                    else:
                        err_msg = str(result)
                        err_details = ''

                    sys.stderr.write(f"\n[FORENSIC] HERESY DETECTED IN {rite_name}:\n")
                    sys.stderr.write(f"   Message: {err_msg}\n")
                    if err_details:
                        sys.stderr.write(f"   Details: {str(err_details)[:500]}\n")  # Truncate massive traces
                    sys.stderr.flush()
                except:
                    pass

            # [ASCENSION 10]: GRAFT GNOSIS FOR COCKPIT
            self._inject_profiler_gnosis(result, duration_ms, mem_delta, status)

            # Use engine console if available, fallback to sys.stderr
            if hasattr(self.engine, 'console') and not self.engine._silent:
                self.engine.console.print(telemetry_pulse)
            else:
                import re
                clean_msg = re.sub(r'\[/?\w+\]', '', telemetry_pulse)
                sys.stderr.write(f"{clean_msg}\n")
                sys.stderr.flush()

    def _divine_success(self, result: Any) -> bool:
        """
        [ASCENSION 1]: THE ORACLE OF SUCCESS
        Intelligently determines the outcome of both Objects and Dictionaries.
        """
        # Case A: Standard Pydantic/Object Reality
        if hasattr(result, 'success'):
            return bool(result.success)

        # Case B: Legacy/Shimmed Dictionary Reality
        if isinstance(result, dict):
            # If 'success' key exists, use it.
            # Otherwise, assume success if 'error' is absent.
            if 'success' in result:
                return bool(result['success'])
            return 'error' not in result and 'heresies' not in result

        # Case C: Unknown Reality - Default to Optimism
        return True

    def _inject_profiler_gnosis(self, result: Any, duration: float, mem: float, status: str):
        """[ASCENSION 10]: METADATA GRAFTING"""
        if result is None or not isinstance(result, (dict, object)):
            return

        gnosis = {
            "duration_ms": round(duration, 3),
            "memory_delta_mb": round(mem, 4),
            "status": status,
            "thread_id": threading.get_ident(),
            "cpu_load": self._get_cpu_load()
        }

        try:
            if isinstance(result, dict):
                if 'data' not in result or result['data'] is None:
                    result['data'] = {}
                if isinstance(result['data'], dict):
                    result['data']['_profiler'] = gnosis
            elif hasattr(result, 'data'):
                if result.data is None:
                    result.data = {}
                if isinstance(result.data, dict):
                    result.data['_profiler'] = gnosis
        except:
            pass  # Never let profiling crash the result delivery

    def _get_memory_mb(self) -> float:
        """[ASCENSION 3]: MEMORY TOMOGRAPHY"""
        try:
            if psutil:
                return psutil.Process().memory_info().rss / 1024 / 1024
        except:
            pass
        return 0.0

    def _get_cpu_load(self) -> float:
        """[ASCENSION 4]: PRESSURE SENSING"""
        try:
            if psutil:
                return psutil.cpu_percent()
        except:
            pass
        return 0.0