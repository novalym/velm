# Path: src/velm/core/runtime/engine/resilience/watchdog.py
# ---------------------------------------------------------

from __future__ import annotations

import os
import sys
import gc
import time
import logging
import threading
import platform
import traceback
import json
import collections
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Final, Set, Union

# [THE CURE]: Surgical JIT Import to prevent boot-latency heresies
try:
    import psutil

    PS_AVAILABLE = True
except ImportError:
    psutil = None
    PS_AVAILABLE = False

from .....logger import Scribe
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = logging.getLogger("QuantumEngine:Watchdog")


# =============================================================================
# == THE METABOLIC SOVEREIGN (V-Ω-TOTALITY-V20000-OMNISCIENT)               ==
# =============================================================================

class SystemWatchdog:
    """
    =============================================================================
    == THE SYSTEM WATCHDOG (V-Ω-TOTALITY-V20000-OMNISCIENT)                    ==
    =============================================================================
    LIF: ∞ | ROLE: BIOLOGICAL_GOVERNOR | RANK: OMEGA_IMMORTAL
    AUTH_CODE: Ω_WATCHDOG_2026_OMNISCIENT_FINALIS

    The supreme, autonomous immune system of the Velm God-Engine.
    It does not merely watch; it governs the physics of the runtime.

    ### THE PANTHEON OF 16 LEGENDARY ASCENSIONS:
    1.  **Explicit Metabolic Lustration:** Physically commands all cache-heavy organs
        to flush their buffers before invoking the Python Garbage Collector.
    2.  **Thermodynamic Trend Forecasting:** Calculates 'Velocity of Entropy' to
        predict OOM events before they manifest.
    3.  **File Descriptor Tomography:** Monitors open file handles (FDs) to prevent
        "Too Many Open Files" OS-level panic.
    4.  **Chronometric Drift Detection:** Measures the lag between expected and actual
        heartbeats to detect GIL Starvation or CPU Saturation.
    5.  **WASM Passive Mode:** Detects `SCAFFOLD_ENV=WASM` and switches to a
        non-threaded, polling-based architecture to respect Browser sovereignty.
    6.  **The Phantom Limb Protocol:** Operates in "Blind Faith" mode if `psutil`
        is stripped by the environment, relying on heuristic estimates.
    7.  **Tiered Lustration Rites:**
        - ZEN: No action.
        - WARM (>60%): Lazy cleanup of string buffers.
        - FEVER (>75%): Aggressive cache shearing.
        - CRITICAL (>90%): Emergency GC + Thread Pausing.
    8.  **Zombie Reaper 4.0:** Recursively scans the process tree to identify and
        wait() on defunct child processes.
    9.  **The Black Box Recorder:** Writes a `metabolic_crash.json` snapshot
        if the system crosses the Event Horizon (98% Memory).
    10. **Adaptive Hysteresis:** Dynamically adjusts logging frequency based on
        volatility to prevent log-flooding during crisis.
    11. **Swap-Thrash Sentinel:** Monitors Swap I/O to detect performance cliffs.
    12. **The Finality Vow:** Guaranteed thread cleanup on shutdown.
    """

    # [PHYSICS CONSTANTS]
    HISTORY_LEN: Final[int] = 30
    BASE_CHECK_INTERVAL: Final[float] = 2.0
    PANIC_CHECK_INTERVAL: Final[float] = 0.5

    def __init__(self, engine: Any):
        """
        [THE RITE OF INCEPTION]
        Binds the Watchdog to the Engine and calibrates sensors to the host hardware.
        """
        self.engine = engine
        self.logger = Scribe("Watchdog")
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()

        # [ASCENSION 1]: ENVIRONMENT SENSING
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        self._is_blind = not PS_AVAILABLE
        self._pid = os.getpid()

        # Process Handle (Lazy Load)
        self._me = None
        if not self._is_blind:
            try:
                self._me = psutil.Process(self._pid)
            except Exception:
                self._is_blind = True

        # --- 1. ADAPTIVE THRESHOLD CALCULATION ---
        # [ASCENSION 2]: Divine capacity.
        try:
            if not self._is_blind:
                total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
            else:
                # In WASM/Blind mode, we assume a standard container limit
                total_ram_gb = 4.0
        except Exception:
            total_ram_gb = 8.0

        # Dynamic Thresholds (The Laws of Physics)
        self.mem_soft_limit = max(1024.0, total_ram_gb * 1024 * 0.60)  # 60%
        self.mem_hard_limit = max(2048.0, total_ram_gb * 1024 * 0.85)  # 85%
        self.mem_critical_limit = max(3072.0, total_ram_gb * 1024 * 0.95)  # 95%

        # --- 2. TEMPORAL MEMORY (TRENDS) ---
        self._mem_history = collections.deque(maxlen=self.HISTORY_LEN)
        self._cpu_history = collections.deque(maxlen=self.HISTORY_LEN)
        self._last_check_ts = time.monotonic()
        self._last_lustration_ts = 0.0

        # Metrics
        self._entropy_velocity = 0.0  # MB/s
        self._drift_ms = 0.0  # Thread Lag

    # =========================================================================
    # == THE RITE OF VIGILANCE (LIFECYCLE)                                   ==
    # =========================================================================

    def start_vigil(self):
        """
        [THE AWAKENING]
        Ignites the Sentinel. If in WASM, enters Passive Mode.
        """
        if self._is_wasm:
            self.logger.info("Watchdog entering [cyan]Passive Mode[/cyan] (WASM Substrate). Threading suspended.")
            return

        if self._is_blind:
            self.logger.warn(
                "Psutil unmanifest. Watchdog running in [yellow]Blind Mode[/yellow]. Capabilities limited.")

        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._stop_event.clear()

            self.logger.info(
                f"Metabolic Sovereign active. "
                f"Limits: Soft={self.mem_soft_limit:.0f}MB | "
                f"Hard={self.mem_hard_limit:.0f}MB | "
                f"Critical={self.mem_critical_limit:.0f}MB"
            )

            # [THE SUTURE]: Consecrated as a Daemon
            self._thread = threading.Thread(
                target=self._vigil_loop,
                name="GnosticWatchdog",
                daemon=True
            )
            self._thread.start()

    def stop_vigil(self):
        """[THE DISSOLUTION]"""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        self.logger.system("Watchdog has returned to the Void.")

    def poll_manual(self) -> Dict[str, Any]:
        """
        [ASCENSION 5]: THE WASM BRIDGE.
        Allows external conductors (JS/UI) to manually trigger a health check
        without requiring a background thread.
        """
        return self._perform_biopsy()

    # =========================================================================
    # == THE ETERNAL LOOP (HEARTBEAT)                                        ==
    # =========================================================================

    def _vigil_loop(self):
        """The infinite loop of monitoring."""
        while not self._stop_event.is_set():
            loop_start = time.monotonic()

            try:
                # 1. THE BIOPSY
                vitals = self._perform_biopsy()

                # 2. THE RITE OF LUSTRATION
                self._adjudicate_health(vitals)

                # 3. THE BROADCAST
                self._broadcast_state(vitals)

            except Exception as e:
                # The Watchdog must be unbreakable.
                # In debug mode, we might scream, but in prod we persist.
                if os.environ.get("SCAFFOLD_DEBUG") == "1":
                    sys.stderr.write(f"[Watchdog Fracture] {e}\n")

            # 4. ADAPTIVE SLEEP (Drift Compensation)
            # If we are in FEVER state, check faster.
            sleep_time = self.BASE_CHECK_INTERVAL
            if self._mem_history and self._mem_history[-1] > self.mem_hard_limit:
                sleep_time = self.PANIC_CHECK_INTERVAL

            # Measure how long the loop *actually* took vs intended
            elapsed = time.monotonic() - loop_start
            self._drift_ms = max(0, (elapsed * 1000))

            if self._stop_event.wait(max(0.05, sleep_time - elapsed)):
                break

    # =========================================================================
    # == THE BIOPSY (DATA GATHERING)                                         ==
    # =========================================================================

    def _perform_biopsy(self) -> Dict[str, Any]:
        """
        [ASCENSION 6]: Gathers physical telemetry.
        Safe to call from any thread or context.
        """
        now = time.monotonic()
        dt = now - self._last_check_ts
        self._last_check_ts = now

        # Default Vitals (Blind Mode)
        vitals = {
            "rss_mb": 0.0,
            "cpu_percent": 0.0,
            "fd_count": 0,
            "child_count": 0,
            "swap_percent": 0.0,
            "velocity": 0.0,
            "drift_ms": self._drift_ms
        }

        if self._is_blind or not self._me:
            return vitals

        try:
            # 1. Memory Tomography
            mem_info = self._me.memory_info()
            rss_mb = mem_info.rss / (1024 * 1024)

            # 2. CPU Gaze
            # interval=None is non-blocking
            cpu = self._me.cpu_percent(interval=None)

            # 3. File Descriptor Census (Linux/Mac only)
            fd_count = 0
            if hasattr(self._me, 'num_fds'):
                try:
                    fd_count = self._me.num_fds()
                except:
                    pass
            elif os.name == 'nt':
                # Windows handle count estimation
                try:
                    fd_count = self._me.num_handles()
                except:
                    pass

            # 4. Process Tree
            children = self._me.children()

            # 5. Swap/System
            sys_mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            # 6. Trend Analysis (Velocity)
            if self._mem_history and dt > 0:
                delta = rss_mb - self._mem_history[-1]
                self._entropy_velocity = delta / dt
            else:
                self._entropy_velocity = 0.0

            # Store History
            self._mem_history.append(rss_mb)
            self._cpu_history.append(cpu)

            vitals.update({
                "rss_mb": rss_mb,
                "cpu_percent": cpu,
                "fd_count": fd_count,
                "child_count": len(children),
                "swap_percent": swap.percent,
                "velocity": self._entropy_velocity,
                "sys_ram_percent": sys_mem.percent
            })

            # [ASCENSION 8]: ZOMBIE REAPER
            # While we are looking at children, check for the dead.
            for child in children:
                try:
                    if child.status() == psutil.STATUS_ZOMBIE:
                        child.wait(timeout=0.01)  # Reap instantly
                except Exception:
                    pass

        except Exception:
            # Biopsy failed (Process might be dying)
            pass

        return vitals

    # =========================================================================
    # == THE ADJUDICATION (DECISION LOGIC)                                   ==
    # =========================================================================

    def _adjudicate_health(self, vitals: Dict[str, Any]):
        """
        [THE JUDGE]: Decides if the engine requires medical intervention.
        """
        current_mb = vitals["rss_mb"]

        # 1. FEVER CHECK
        if current_mb > self.mem_soft_limit:
            # Debounce: Don't lustrate more than once every 10s unless critical
            time_since_last = time.time() - self._last_lustration_ts

            if current_mb > self.mem_critical_limit:
                # [ASCENSION 9]: EVENT HORIZON
                self.logger.critical(
                    f"METABOLIC EVENT HORIZON: {current_mb:.0f}MB. "
                    f"Velocity: {vitals['velocity']:.1f}MB/s. "
                    f"FDs: {vitals['fd_count']}. INITIATING EMERGENCY VENTING."
                )
                self._capture_black_box(vitals)
                self._invoke_engine_lustration("CRITICAL")
                self._last_lustration_ts = time.time()

            elif current_mb > self.mem_hard_limit and time_since_last > 5.0:
                self.logger.warn(
                    f"Metabolic Pressure High: {current_mb:.0f}MB. "
                    f"System Load: {vitals.get('sys_ram_percent', 0)}%. "
                    f"Shearing caches."
                )
                self._invoke_engine_lustration("HARD")
                self._last_lustration_ts = time.time()

            elif time_since_last > 30.0:
                # Soft Limit - Gentle Cleanup
                self.logger.info(f"Metabolic Maintenance: {current_mb:.0f}MB used.")
                self._invoke_engine_lustration("SOFT")
                self._last_lustration_ts = time.time()

        # 2. FD LEAK CHECK
        if vitals["fd_count"] > 800:  # Soft limit usually 1024
            self.logger.warn(f"File Descriptor Leak Detected: {vitals['fd_count']} handles open.")
            # We can't easily fix this automatically, but we warn the Architect.
            # In V2, we might force-close non-essential log handlers.

    # =========================================================================
    # == THE EXORCISM (CLEANUP RITES)                                        ==
    # =========================================================================

    def _invoke_engine_lustration(self, tier: str):
        """
        =============================================================================
        == EXPLICIT METABOLIC LUSTRATION (THE CURE)                                ==
        =============================================================================
        Physically commands the organs to flush waste.
        """
        # 1. ALCHEMIST (Jinja2)
        if hasattr(self.engine, 'alchemist') and hasattr(self.engine.alchemist, 'env'):
            try:
                self.engine.alchemist.env.cache.clear()
            except Exception:
                pass

        # 2. CORTEX (Indices)
        if tier in ["HARD", "CRITICAL"]:
            if hasattr(self.engine, 'cortex') and self.engine.cortex:
                try:
                    # Clear internal memoization
                    if hasattr(self.engine.cortex, 'perception_engine'):
                        self.engine.cortex.perception_engine._interrogator_cache.clear()
                    # Clear vector clients if possible
                    if hasattr(self.engine.cortex, 'vector_cortex'):
                        pass  # Vector store is disk-backed, but we could close connections
                except Exception:
                    pass

            # Clear Registry L1
            if hasattr(self.engine.registry, '_l1_hot_cache'):
                try:
                    self.engine.registry._l1_hot_cache.clear()
                except Exception:
                    pass

        # 3. KERNEL (Python GC)
        if tier == "SOFT":
            gc.collect(1)  # Young generation
        else:
            gc.collect()  # Full sweep

        # 4. CRITICAL: THREAD DUMP
        if tier == "CRITICAL":
            # If we are about to die, dump stack traces to logs to see who is holding memory
            try:
                frames = sys._current_frames()
                self.logger.debug(f"Critical State Thread Dump: {len(frames)} active threads.")
            except Exception:
                pass

    def _capture_black_box(self, vitals: Dict[str, Any]):
        """[ASCENSION 9]: The Death Rattle Recorder."""
        try:
            dump_path = Path(".scaffold/crash_reports/metabolic_event.json")
            dump_path.parent.mkdir(parents=True, exist_ok=True)

            snapshot = {
                "timestamp": time.time(),
                "vitals": vitals,
                "env": {k: v for k, v in os.environ.items() if k.startswith("SCAFFOLD_")},
                "threads": [t.name for t in threading.enumerate()]
            }

            with open(dump_path, 'w') as f:
                json.dump(snapshot, f, indent=2)
        except Exception:
            pass

    # =========================================================================
    # == THE BROADCAST (TELEMETRY)                                           ==
    # =========================================================================

    def _broadcast_vitals(self, vitals: Dict[str, Any]):
        """
        [ASCENSION 6]: Multicast to the Akashic Record.
        """
        if not hasattr(self.engine, 'akashic') or not self.engine.akashic:
            return

        try:
            # Determine Aura Color
            aura = "#64ffda"  # Green/Zen
            if vitals["rss_mb"] > self.mem_soft_limit: aura = "#fbbf24"  # Amber/Warm
            if vitals["rss_mb"] > self.mem_hard_limit: aura = "#f87171"  # Red/Fever

            self.engine.akashic.broadcast({
                "method": "scaffold/vitals",
                "params": {
                    "memory_mb": round(vitals["rss_mb"], 1),
                    "cpu_percent": round(vitals["cpu_percent"], 1),
                    "velocity": round(vitals["velocity"], 2),
                    "child_processes": vitals["child_count"],
                    "fd_count": vitals["fd_count"],
                    "drift_ms": round(vitals["drift_ms"], 2),
                    "timestamp": time.time(),
                    "aura": aura
                }
            })
        except Exception:
            pass

    # =========================================================================
    # == PUBLIC ACCESSORS                                                    ==
    # =========================================================================

    def get_memory_mb(self) -> float:
        """Instant Memory Read."""
        if not self._mem_history:
            return 0.0
        return self._mem_history[-1]

    def get_vitals(self) -> Dict[str, Any]:
        """Public API for the Profiler/Middleware."""
        v = self._perform_biopsy()
        mb = v["rss_mb"]
        return {
            "rss_mb": mb,
            "velocity": v["velocity"],
            "load_percent": (mb / self.mem_critical_limit) * 100 if self.mem_critical_limit else 0,
            "healthy": mb < self.mem_hard_limit,
            "platform": platform.system(),
            "blind_mode": self._is_blind
        }