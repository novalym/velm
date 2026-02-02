# Path: scaffold/core/runtime/middleware/entropy_shield.py
# --------------------------------------------------------


import os
import time
import threading
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


_METABOLISM = MetabolicState()
_CACHE_TTL = 2.0  # Vitals are fresh for 2 seconds
_HISTORY_LEN = 5  # Keep last 5 measurements for trend analysis


class EntropyShieldMiddleware(Middleware):
    """
    =============================================================================
    == THE ENTROPY SHIELD (V-Ω-PREDICTIVE-GOVERNANCE-ULTIMA)                    ==
    =============================================================================
    LIF: ∞ | The Sovereign Protector of the Machine.

    This is not a simple gate; it is a **Metabolic Governor**. It perceives the
    pressure of the mortal realm (CPU, RAM, Swap, I/O) and adjudicates whether
    adding a new rite will cause a catastrophic collapse (OOM/Freeze).

    [ASCENDED FACULTIES]:
    1.  **The Cooling Rite:** If heat is detected, it pauses to verify if the spike
        is transient. It rejects only sustained entropy.
    2.  **The Thrashing Gaze:** Monitors Swap usage. High CPU is fine; high Swap
        is death.
    3.  **The Load Balancer:** Checks System Load Average against Core Count.
    4.  **The I/O Sentinel:** Detects disk saturation (iowait) on Linux.
    5.  **The Yield Protocol:** If load is high but not critical, it injects a
        micro-sleep to "nice" the process before proceeding.
    """

    # Heavy rites that consume significant Gnostic Mass
    HEAVY_RITES = {
        'GenesisRequest', 'WeaveRequest', 'SymphonyRequest',
        'RefactorRequest', 'AnalyzeRequest', 'DistillRequest',
        'BuildRequest', 'DeployRequest', 'TrainRequest'
    }

    # Physics Thresholds
    MIN_RAM_MB = 256  # Absolute floor
    MAX_SWAP_PERCENT = 80.0  # Danger zone for thrashing
    MAX_CPU_PERCENT = 95.0  # Saturation point
    MAX_IOWAIT = 40.0  # Disk saturation (Linux only)

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """The Rite of Defensive Interception."""

        # 1. THE GAZE OF NECESSITY
        # Skip for lightweight rites or explicit Force overrides.
        rite_name = type(request).__name__
        if rite_name not in self.HEAVY_RITES or request.force:
            return next_handler(request)

        # 2. THE METABOLIC INQUEST
        is_healthy, diagnosis, severity = self._assess_system_health()

        # 3. THE RITE OF COOLING (Self-Correction)
        if not is_healthy:
            # If the system is hot, we do not reject immediately.
            # We wait 1 second and gaze again to filter transient spikes.
            self.logger.verbose(f"Entropy Spike Detected ({diagnosis}). Initiating Cooling Rite...")
            time.sleep(1.0)
            is_healthy, diagnosis, severity = self._assess_system_health(force_refresh=True)

        # 4. THE ADJUDICATION
        if not is_healthy:
            # If critical (OOM Risk), we block.
            if severity == "CRITICAL":
                raise ArtisanHeresy(
                    "System Critical: The Entropy Shield has blocked the rite.",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Machine vitals are unstable: {diagnosis}",
                    suggestion="Close heavy background applications or use --force to risk a hardware crash."
                )

            # If just High Load ("WARNING"), we warn and yield (throttle), but proceed.
            elif severity == "WARNING":
                self.logger.warn(f"System Load High: {diagnosis}. Throttling execution speed.")
                time.sleep(2.0)  # The Yield Protocol

        # 5. PROCEED
        return next_handler(request)

    def _assess_system_health(self, force_refresh: bool = False) -> Tuple[bool, str, str]:
        """
        [THE RITE OF VITAL UPDATE]
        Performs the physical probe of the hardware.
        Returns: (IsHealthy, Diagnosis, Severity[CRITICAL|WARNING|NONE])
        """
        # [ASCENSION 3]: HOLLOW-BORE JIT IMPORT
        try:
            import psutil
        except ImportError:
            return True, "Psutil Artisan Missing (Blind Mode)", "NONE"

        now = time.monotonic()

        with _METABOLISM.lock:
            # Return cached truth if fresh
            if not force_refresh and (now - _METABOLISM.timestamp < _CACHE_TTL):
                return _METABOLISM.is_healthy, _METABOLISM.diagnosis, "NONE" if _METABOLISM.is_healthy else "CRITICAL"

            try:
                issues = []
                severity = "NONE"

                # A. MEMORY GAZE (The OOM Guard)
                mem = psutil.virtual_memory()
                swap = psutil.swap_memory()
                available_mb = mem.available / (1024 * 1024)

                if available_mb < self.MIN_RAM_MB:
                    issues.append(f"Memory Starvation ({available_mb:.0f}MB free)")
                    severity = "CRITICAL"

                # [ASCENSION 2]: THRASHING CHECK
                if swap.percent > self.MAX_SWAP_PERCENT:
                    issues.append(f"Swap Thrashing ({swap.percent}% used)")
                    severity = "CRITICAL"

                # B. CPU GAZE (Non-Blocking)
                cpu_percent = psutil.cpu_percent(interval=None)

                # [ASCENSION 1]: TREND ANALYSIS
                _METABOLISM.cpu_history.append(cpu_percent)
                if len(_METABOLISM.cpu_history) > _HISTORY_LEN:
                    _METABOLISM.cpu_history.pop(0)

                # C. LOAD AVERAGE GAZE (Unix Only)
                # Calculates if the queue is deeper than the number of cores
                if hasattr(os, 'getloadavg'):
                    load_1, _, _ = os.getloadavg()
                    cpu_count = os.cpu_count() or 1
                    if load_1 > (cpu_count * 1.5):
                        issues.append(f"Load Saturation ({load_1:.2f} / {cpu_count} cores)")
                        if severity != "CRITICAL": severity = "WARNING"

                # D. I/O WAIT GAZE (Linux Only)
                # High CPU is fine if it's user space (compiling).
                # High CPU due to iowait means the disk is dead.
                cpu_times = psutil.cpu_times_percent()
                iowait = getattr(cpu_times, 'iowait', 0.0)
                if iowait > self.MAX_IOWAIT:
                    issues.append(f"Disk I/O Lock ({iowait:.1f}% wait)")
                    if severity != "CRITICAL": severity = "WARNING"

                # E. RAW CPU SPIKE
                # Only critical if we are truly maxed out
                if cpu_percent > self.MAX_CPU_PERCENT:
                    # Check trend - is it rising or falling?
                    avg_load = sum(_METABOLISM.cpu_history) / len(_METABOLISM.cpu_history)
                    if avg_load > 90.0:
                        issues.append(f"Sustained CPU Exhaustion ({cpu_percent}%)")
                        if severity != "CRITICAL": severity = "WARNING"

                # F. UPDATE STATE
                if severity == "CRITICAL":
                    _METABOLISM.is_healthy = False
                    _METABOLISM.diagnosis = "; ".join(issues)
                elif severity == "WARNING":
                    # Warning allows passage but triggers throttling
                    _METABOLISM.is_healthy = False
                    _METABOLISM.diagnosis = "; ".join(issues)
                else:
                    _METABOLISM.is_healthy = True
                    _METABOLISM.diagnosis = "System Vitality Nominal"

                _METABOLISM.timestamp = now

                return not (severity == "CRITICAL"), _METABOLISM.diagnosis, severity

            except Exception as paradox:
                # [ASCENSION 10]: Fail-Safe
                # A monitoring failure should not halt the Great Work.
                _METABOLISM.is_healthy = True
                _METABOLISM.diagnosis = f"Gaze Clouded: {paradox}"
                _METABOLISM.timestamp = now
                return True, _METABOLISM.diagnosis, "NONE"