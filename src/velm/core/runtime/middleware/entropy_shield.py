# Path: scaffold/core/runtime/middleware/entropy_shield.py
# =========================================================================================
# == THE ENTROPY SHIELD (V-Ω-TOTALITY-V20000.12-ISOMORPHIC-INTEL)                        ==
# =========================================================================================
# LIF: ∞ | ROLE: METABOLIC_PERIMETER_GOVERNOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SHIELD_V20000_SUBSTRATE_AWARE_2026_FINALIS
# =========================================================================================

import os
import time
import threading
import gc
import sys
from dataclasses import dataclass, field
from typing import Tuple, Dict, Any, Optional, List

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


# [ASCENSION 1]: GLOBAL METABOLIC STATE
# We maintain a process-wide history of vitals to detect trends (rising vs falling load).
@dataclass
class MetabolicState:
    timestamp: float = 0.0
    cpu_history: List[float] = field(default_factory=list)
    mem_history: List[float] = field(default_factory=list)
    is_healthy: bool = True
    diagnosis: str = "System Initialized"
    lock: threading.Lock = field(default_factory=threading.Lock)
    substrate: str = "UNKNOWN"


_METABOLISM = MetabolicState()
_CACHE_TTL = 1.5  # Vitals are tightened to 1.5s for higher-order precision
_HISTORY_LEN = 10  # Expanded history for trend forecasting


class EntropyShieldMiddleware(Middleware):
    """
    =============================================================================
    == THE ENTROPY SHIELD (V-Ω-PREDICTIVE-GOVERNANCE-ULTIMA)                    ==
    =============================================================================
    LIF: ∞ | The Sovereign Protector of the Machine.
    """

    # Heavy rites that consume significant Gnostic Mass
    HEAVY_RITES = {
        'GenesisRequest', 'WeaveRequest', 'SymphonyRequest',
        'RefactorRequest', 'AnalyzeRequest', 'DistillRequest',
        'BuildRequest', 'DeployRequest', 'TrainRequest'
    }

    # Physics Thresholds (Standard Iron Core)
    MIN_RAM_MB = 384
    MAX_SWAP_PERCENT = 80.0
    MAX_CPU_PERCENT = 95.0
    MAX_IOWAIT = 40.0

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """The Rite of Defensive Interception."""

        # 1. THE GAZE OF NECESSITY
        rite_name = type(request).__name__
        if rite_name not in self.HEAVY_RITES or request.force:
            # [ASCENSION 9]: Even in bypass, we yield a microsecond to allow OS breath
            time.sleep(0)
            return next_handler(request)

        # 2. THE METABOLIC INQUEST
        is_healthy, diagnosis, severity = self._assess_system_health()

        # 3. THE RITE OF COOLING (Adaptive Yielding)
        if not is_healthy:
            # [ASCENSION 6]: Adaptive Yield Duration
            # If load is 98%, we cool for 2.5s. If 91%, we cool for 1s.
            yield_time = 1.0 if severity == "WARNING" else 2.0

            self.logger.warn(
                f"[{getattr(request, 'trace_id', 'tr-unbound')}] Entropy Detected: {diagnosis}. Cooling for {yield_time}s...")
            time.sleep(yield_time)

            # Final Gaze after cooling
            is_healthy, diagnosis, severity = self._assess_system_health(force_refresh=True)

        # 4. THE ADJUDICATION
        if not is_healthy:
            if severity == "CRITICAL":
                raise ArtisanHeresy(
                    "System Critical: The Entropy Shield has blocked the rite.",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Metabolic Failure on substrate [{_METABOLISM.substrate}]: {diagnosis}",
                    suggestion="Close high-load applications or provision a higher-strata Node."
                )
            elif severity == "WARNING":
                self.logger.warn(f"Metabolic Friction: {diagnosis}. Proceeding with backpressure.")
                # Inject a metabolic yielding sleep
                time.sleep(0.5)

        # 5. PROCEED
        return next_handler(request)

    def _assess_system_health(self, force_refresh: bool = False) -> Tuple[bool, str, str]:
        """
        [THE RITE OF VITAL UPDATE]
        Performs the physical or virtual probe of the substrate.
        Returns: (IsHealthy, Diagnosis, Severity[CRITICAL|WARNING|NONE])
        """
        now = time.monotonic()

        with _METABOLISM.lock:
            # 1. CHRONOCACHE PROBE
            if not force_refresh and (now - _METABOLISM.timestamp < _CACHE_TTL):
                sev = "NONE" if _METABOLISM.is_healthy else "CRITICAL"
                return _METABOLISM.is_healthy, _METABOLISM.diagnosis, sev

            # 2. SENSORY TRIAGE (IRON vs ETHER)
            try:
                import psutil
                _METABOLISM.substrate = "IRON"
                return self._scry_iron_core(psutil, now)
            except (ImportError, AttributeError):
                _METABOLISM.substrate = "ETHER"
                return self._scry_ether_plane(now)

    def _scry_iron_core(self, psutil, now: float) -> Tuple[bool, str, str]:
        """[STRATUM: IRON] Physical hardware scrying logic."""
        issues = []
        severity = "NONE"

        # A. Memory Tomography
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        available_mb = mem.available / (1024 * 1024)

        if available_mb < self.MIN_RAM_MB:
            issues.append(f"RAM_DEEP_VACUUM({available_mb:.0f}MB)")
            severity = "CRITICAL"

        if swap.percent > self.MAX_SWAP_PERCENT:
            issues.append(f"SWAP_THRASHING({swap.percent}%)")
            severity = "CRITICAL"

        # B. CPU Tomography
        cpu_percent = psutil.cpu_percent(interval=None) or 0.0
        _METABOLISM.cpu_history.append(cpu_percent)

        # [ASCENSION 4]: Entropy Velocity Forecasting
        if len(_METABOLISM.cpu_history) >= 3:
            # If CPU has been > 90% for the last 3 ticks
            if all(h > 90.0 for h in list(_METABOLISM.cpu_history)[-3:]):
                issues.append(f"SUSTAINED_CPU_FEVER({cpu_percent}%)")
                if severity != "CRITICAL": severity = "WARNING"

        # C. Load & IO Wait
        if hasattr(os, 'getloadavg'):
            load_1 = os.getloadavg()[0]
            if load_1 > (os.cpu_count() or 1) * 2:
                issues.append(f"LOAD_SATURATION({load_1:.1f})")
                if severity != "CRITICAL": severity = "WARNING"

        cpu_times = psutil.cpu_times_percent()
        iowait = getattr(cpu_times, 'iowait', 0.0)
        if iowait > self.MAX_IOWAIT:
            issues.append(f"DISK_IO_STALL({iowait:.1f}%)")
            if severity != "CRITICAL": severity = "WARNING"

        return self._finalize_inquest(issues, severity, now)

    def _scry_ether_plane(self, now: float) -> Tuple[bool, str, str]:
        """[STRATUM: ETHER] WASM/Browser scrying logic via Metabolic Drift."""
        issues = []
        severity = "NONE"

        # [ASCENSION 2]: Metabolic Drift Tomography
        # Measure execution jitter by timing a micro-sleep
        t0 = time.perf_counter()
        time.sleep(0.001)
        t1 = time.perf_counter()
        drift_ms = (t1 - t0) * 1000

        # [ASCENSION 3]: Heap Object Tomography
        # 500,000 objects in Pyodide is approx 75MB of metadata alone
        obj_count = len(gc.get_objects())

        # Adjudicate Drift (CPU)
        if drift_ms > 10.0:  # Significant loop lag
            issues.append(f"METABOLIC_LAG({drift_ms:.1f}ms)")
            severity = "CRITICAL"
        elif drift_ms > 5.0:
            issues.append(f"LOOP_JITTER({drift_ms:.1f}ms)")
            severity = "WARNING"

        # Adjudicate Mass (RAM)
        if obj_count > 800000:
            issues.append(f"HEAP_DENSITY_CRITICAL({obj_count})")
            severity = "CRITICAL"
        elif obj_count > 500000:
            issues.append(f"HEAP_DENSITY_HIGH({obj_count})")
            if severity != "CRITICAL": severity = "WARNING"

        return self._finalize_inquest(issues, severity, now)

    def _finalize_inquest(self, issues: List[str], severity: str, now: float) -> Tuple[bool, str, str]:
        """Commits the result to the global metabolic state."""
        if severity != "NONE":
            _METABOLISM.is_healthy = False
            _METABOLISM.diagnosis = " | ".join(issues)
        else:
            _METABOLISM.is_healthy = True
            _METABOLISM.diagnosis = "NOMINAL"

        _METABOLISM.timestamp = now
        # Keep histories clean
        if len(_METABOLISM.cpu_history) > _HISTORY_LEN: _METABOLISM.cpu_history.pop(0)

        return _METABOLISM.is_healthy, _METABOLISM.diagnosis, severity

# == SCRIPTURE SEALED: THE ENTROPY SHIELD IS OMEGA TOTALITY ==