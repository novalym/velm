# Path: src/velm/core/runtime/engine/lifecycle/vitality.py
# ---------------------------------------------------------
# SYSTEM: Core Runtime / Resource Management
# COMPONENT: VitalityMonitor
# STABILITY: Stable / Production
# ---------------------------------------------------------

from __future__ import annotations
import threading
import time
import os
import sys
import gc
import json
import logging
import platform
import collections
from pathlib import Path
from typing import Optional, Dict, Any, Final, Union

from .....logger import Scribe

# Optional Dependency: PSUtil
# Provides detailed process metrics on native substrates.
# Gracefully degrades to heuristic estimation if unavailable (WASM/Restricted).
try:
    import psutil

    PS_AVAILABLE = True
except ImportError:
    psutil = None
    PS_AVAILABLE = False

from .state import LifecyclePhase

# Initialize structured logger for resource monitoring
Logger = Scribe("VitalityMonitor")


class VitalityMonitor:
    """
    Manages system resource utilization and process health.

    This component acts as the centralized governor for memory and CPU usage within the engine.
    It monitors runtime metrics and triggers corrective actions (Garbage Collection, Cache Eviction)
    based on configured thresholds to prevent Out-Of-Memory (OOM) crashes or system hangs.

    Key Responsibilities:
    1.  **Substrate Adaptation:** Detects environment capabilities (Native vs WASM) and adjusts
        concurrency models (Threading vs Polling) accordingly.
    2.  **Resource Throttling:** Implements a tiered response system for memory pressure:
        - Soft Limit (60%): Lazy GC invocation.
        - Hard Limit (85%): Aggressive cache clearing.
        - Critical Limit (95%): Emergency dump and thread suspension.
    3.  **Heartbeat Emission:** Writes periodic status updates to a pulse file for external
        health checks (e.g., by the CLI or Orchestrator).
    4.  **Trend Analysis:** Calculates the velocity of memory allocation to predict and
        preemptively handle usage spikes.
    """

    # --- Configuration Constants ---
    PULSE_INTERVAL_IDLE: Final[float] = 10.0  # Seconds between checks when idle
    PULSE_INTERVAL_ACTIVE: Final[float] = 2.0  # Seconds between checks when under load
    MEMORY_HYSTERESIS_MB: Final[float] = 50.0  # Buffer to prevent oscillating states
    WASM_DRIFT_THRESHOLD_MS: Final[float] = 15.0  # CPU contention threshold for browser environments

    def __init__(self, engine: Any):
        """
        Initializes the monitor and calibrates resource baselines based on the host environment.
        """
        import sys
        import os
        import threading
        import time
        from pathlib import Path

        self.engine = engine
        self.logger = Logger

        # Concurrency Controls
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()

        # --- Environment Detection ---
        # WASM/Emscripten environments do not support standard threading or subprocess inspection.
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        # "Blind Mode" indicates we cannot read OS-level process counters (psutil missing).
        self._is_blind = not PS_AVAILABLE
        self._pid = os.getpid()

        # --- Resource Calibration ---
        # Determine available memory ceiling.
        try:
            if not self._is_blind:
                # Native: Read total physical RAM
                total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
            else:
                # WASM/Container: Assume standard 4GB allocation limit
                total_ram_gb = 4.0
        except Exception:
            total_ram_gb = 8.0

        # --- Threshold Definitions ---
        # 1. Soft Limit (60%): Trigger opportunistic cleanup (young-gen GC).
        self.gc_threshold_mb = max(512.0, (total_ram_gb * 1024 * 0.60))

        # 2. Hard Limit (85%): Trigger aggressive cleanup (Full GC + Cache Eviction).
        self.mem_hard_limit = max(1024.0, (total_ram_gb * 1024 * 0.85))

        # 3. Critical Limit (95%): Trigger emergency measures (Pause + Dump).
        self.mem_critical_limit = max(2048.0, (total_ram_gb * 1024 * 0.95))

        # --- Metric History ---
        # Used for calculating rates of change (Velocity).
        self._last_proclaimed_mb = 0.0
        self._last_gc_ts = 0.0
        self._last_soft_gc_ts = 0.0
        self._last_cleanup_ts = 0.0
        self._entropy_velocity = 0.0
        self._last_biopsy_ts = time.monotonic()
        self._drift_ms = 0.0

        # --- Process Ancestry ---
        try:
            self._parent_pid = os.getppid() if hasattr(os, 'getppid') else 0
        except Exception:
            self._parent_pid = 0

        self.pulse_path: Optional[Path] = None

    def get_vitals(self) -> Dict[str, Any]:
        """
        Public API for retrieving current system health metrics.
        Returns a standardized dictionary for consumption by dashboards or loggers.
        """
        v = self._measure_resources()
        mb = v["rss_mb"]

        return {
            "rss_mb": mb,
            "velocity": v["velocity_mb_s"],
            "load_percent": (mb / self.mem_critical_limit) * 100 if self.mem_critical_limit else 0,
            "healthy": mb < self.mem_hard_limit,
            "platform": platform.system(),
            "blind_mode": self._is_blind
        }

    def start_vigil(self, pulse_file_path: Optional[str] = None):
        """
        Starts the monitoring process.

        In Native environments, this spawns a background daemon thread.
        In WASM environments, this performs a single synchronous check and exits,
        delegating future checks to the event loop.
        """
        if pulse_file_path:
            self.pulse_path = Path(pulse_file_path)

        # Re-verify environment in case of late-binding environment variables
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        self.logger.info(
            f"Resource Monitor initialized. [Substrate: {'ETHER/WASM' if self.is_wasm else 'IRON/NATIVE'}]"
        )

        # WASM Strategy: Passive Monitoring
        if self.is_wasm:
            self.logger.debug("WASM environment detected. Disabling background thread; switching to passive polling.")
            try:
                self.pulse()
            except Exception:
                pass
            return

        # Native Strategy: Active Background Thread
        try:
            self._thread = threading.Thread(
                target=self._monitor_loop,
                name="VitalityMonitor",
                daemon=True
            )
            self._thread.start()
        except RuntimeError as e:
            # Fallback if threading is disabled by the OS/Runtime
            self.logger.warn(f"Failed to spawn monitor thread ({e}). Switching to passive mode.")
            self.is_wasm = True

    def pulse(self):
        """
        Performs a single, synchronous health check.
        Called manually by the main loop in single-threaded environments.
        """
        vitals = self._measure_resources()
        self._enforce_limits(vitals)
        self._write_pulse_data(vitals)
        return vitals

    def stop_vigil(self):
        """
        Signals the monitoring thread to terminate and cleans up resources.
        """
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            try:
                self._thread.join(timeout=0.5)
            except:
                pass
        # Write final status to indicate termination
        self._write_pulse_data(vitals={"status": "VOID"})

    def _monitor_loop(self):
        """
        Main execution loop for the background monitoring thread.
        """
        process = None
        if not self._is_blind:
            try:
                process = psutil.Process(os.getpid())
            except:
                self._is_blind = True

        while not self._stop_event.is_set():
            loop_start = time.monotonic()
            try:
                # 1. Measurement
                vitals = self._measure_resources(process)

                # 2. Enforcement
                self._enforce_limits(vitals)

                # 3. Reporting
                self._write_pulse_data(vitals)

                # Parent Process Watchdog
                # If the parent dies, we must terminate to avoid becoming a zombie process.
                if self._parent_pid > 0 and not self.is_wasm:
                    if not psutil.pid_exists(self._parent_pid):
                        self.logger.critical("Parent process terminated. Initiating shutdown.")
                        self.engine.shutdown()
                        break
            except Exception:
                # Suppress transient errors to keep the thread alive
                pass

            # Adaptive Polling Rate
            # Increase frequency if resource usage is changing rapidly.
            current_interval = self.PULSE_INTERVAL_IDLE
            if self._entropy_velocity > 10.0:
                current_interval = self.PULSE_INTERVAL_ACTIVE

            elapsed = time.monotonic() - loop_start
            if self._stop_event.wait(max(0.1, current_interval - elapsed)):
                break

    def _measure_resources(self, process: Optional[Any] = None) -> Dict[str, Any]:
        """
        Collects raw telemetry from the system.
        """
        import gc
        import time
        import json
        from pathlib import Path

        now = time.monotonic()
        dt = now - self._last_biopsy_ts
        self._last_biopsy_ts = now

        current_mb = 0.0
        cpu_load = 0.0
        substrate = "IRON"

        try:
            if process and not self._is_blind:
                # Native: Precise measurement via OS syscalls
                mem_info = process.memory_info()
                current_mb = mem_info.rss / (1024 * 1024)
                cpu_load = process.cpu_percent()
            else:
                # WASM/Blind: Heuristic estimation
                substrate = "ETHER"
                # Estimate RAM based on Python object count
                object_count = len(gc.get_objects())
                current_mb = (object_count * 0.00015) + 100.0

                # Estimate CPU load based on time-drift
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                drift_ms = (t1 - t0) * 1000
                cpu_load = min(100.0, (drift_ms / 5.0) * 100.0)
        except Exception:
            substrate = "VOID"

        # Calculate rate of change (MB/s)
        if dt > 0:
            self._entropy_velocity = (current_mb - self._last_proclaimed_mb) / dt
        self._last_proclaimed_mb = current_mb

        # Check Logical Integrity (Project Anchor)
        anchor_status = "STABLE"
        is_resonant = True
        current_root = getattr(self.engine, 'project_root', Path.cwd())
        identity_file = current_root / ".scaffold" / "identity.json"

        if identity_file.exists():
            try:
                with open(identity_file, 'r', encoding='utf-8') as f:
                    id_data = json.load(f)

                physical_id = id_data.get("id")
                logical_id = self.engine.variables.get("project_slug") or self.engine.variables.get("project_name")

                if physical_id and logical_id and physical_id != logical_id:
                    is_resonant = False
                    anchor_status = "ANCHOR_DESYNC"
            except Exception:
                anchor_status = "IDENTITY_FRACTURED"
        else:
            if str(current_root) != ".":
                anchor_status = "UNTRACKED"

        # Determine aggregate system status
        status = "RESONANT"
        if cpu_load > 90.0 or anchor_status != "STABLE":
            status = "STRESSED"
        if cpu_load > 98.0 or anchor_status == "ANCHOR_DESYNC":
            status = "CRITICAL"

        return {
            "rss_mb": round(current_mb, 1),
            "cpu_percent": round(cpu_load, 1),
            "velocity_mb_s": round(self._entropy_velocity, 2),
            "substrate": substrate,
            "anchor": {
                "status": anchor_status,
                "root": str(current_root).replace('\\', '/'),
                "resonant": is_resonant
            },
            "timestamp": time.time(),
            "status": status,
            "trace_id": getattr(self.engine, 'trace_id', 'tr-unbound')
        }

    def _enforce_limits(self, vitals: Dict[str, Any]):
        """
        Compares current usage against configured thresholds and triggers remediation.
        Includes debounce logic to prevent thrashing.
        """
        import gc
        import time
        import threading
        from .....interfaces.requests import LibrarianRequest, LustrationIntensity

        current_mb = vitals.get("rss_mb", 0.0)
        velocity = vitals.get("velocity_mb_s", 0.0)

        # Adrenaline Mode: Allow 20% higher usage if high-performance mode is requested
        is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"
        effective_soft_limit = self.gc_threshold_mb * (1.2 if is_adrenaline else 1.0)
        effective_hard_limit = self.mem_hard_limit * (1.2 if is_adrenaline else 1.0)

        # Dampening: Only react to rapid growth (>50MB/s)
        is_surging = velocity > 50.0

        now = time.monotonic()
        time_since_last = now - self._last_cleanup_ts

        # --- Tier 1: Soft Limit (Lazy GC) ---
        if current_mb > effective_soft_limit:
            if now - getattr(self, '_last_soft_gc_ts', 0) > 15.0:
                self._clear_internal_caches()
                gc.collect(1)  # Young generation only
                self._last_soft_gc_ts = now

        # --- Tier 2: Remediation Trigger ---
        should_trigger_librarian = False
        target_intensity = LustrationIntensity.SOFT

        if current_mb > self.mem_critical_limit:
            # Critical: 95% usage.
            if time_since_last > 60.0:  # 60s cooldown to prevent locking files during a crash loop
                should_trigger_librarian = True
                target_intensity = LustrationIntensity.CRITICAL
                self.logger.critical(f"Memory Critical: {current_mb:.1f}MB. Initiating emergency cleanup.")

        elif current_mb > effective_hard_limit:
            # Hard: 85% usage.
            if time_since_last > 60.0:
                should_trigger_librarian = True
                target_intensity = LustrationIntensity.HARD
                self.logger.warn(f"Memory Pressure: {current_mb:.1f}MB. Clearing deep caches.")

        elif current_mb > effective_soft_limit and is_surging:
            # Surging: Fast growth detected.
            if time_since_last > 30.0:
                should_trigger_librarian = True
                target_intensity = LustrationIntensity.SOFT
                self.logger.warn(f"Memory Surge: +{velocity:.1f}MB/s. Pre-emptive cleanup started.")

        # --- Execution ---
        if should_trigger_librarian:
            try:
                auto_req = LibrarianRequest(
                    intensity=target_intensity,
                    is_autonomic=True,
                    project_root=self.engine.project_root,
                    trace_id=f"auto-heal-{int(time.time())}"
                )

                # Dispatch cleanup in background thread
                threading.Thread(
                    target=self.engine.dispatch,
                    args=(auto_req,),
                    name=f"AutoLibrarian-{auto_req.trace_id[:4]}",
                    daemon=True
                ).start()

                self._last_cleanup_ts = now

                if self.engine.akashic:
                    try:
                        self.engine.akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {
                                "type": "RESOURCE_EVENT",
                                "label": f"AUTO_CLEANUP_{target_intensity.value.upper()}",
                                "color": "#ef4444" if target_intensity == LustrationIntensity.CRITICAL else "#fbbf24",
                                "trace": auto_req.trace_id
                            }
                        })
                    except Exception:
                        pass

            except Exception as e:
                self.logger.error(f"Automatic cleanup failed: {e}")

        # --- Tier 3: Emergency Brake ---
        # If we exceed critical + 1GB, force a full blocking GC immediately.
        if current_mb > self.mem_critical_limit + 1024.0:
            gc.collect()

    def _write_pulse_data(self, vitals: Dict[str, Any]):
        """
        Writes current status to the pulse file using atomic operations.
        This file is read by external tools to verify the engine is running.
        """
        if not self.pulse_path: return
        import os
        import json

        payload = {
            "pid": os.getpid(),
            "status": vitals.get("status", "ALIVE"),
            "timestamp": time.time(),
            "meta": vitals
        }

        try:
            # Atomic Write: Write to temp, then rename
            temp = self.pulse_path.with_suffix('.tmp')
            with open(temp, 'w', encoding='utf-8') as f:
                json.dump(payload, f)
            os.replace(str(temp), str(self.pulse_path))
        except Exception:
            pass

    def _clear_internal_caches(self):
        """
        Commands internal subsystems to release hold on optional memory.
        """
        try:
            # Clear Template Engine cache
            if hasattr(self.engine, 'alchemist'):
                self.engine.alchemist.env.cache.clear()

            # Clear Registry Lookup cache
            if hasattr(self.engine, 'registry') and hasattr(self.engine.registry, '_l1_hot_cache'):
                self.engine.registry._l1_hot_cache.clear()
        except:
            pass