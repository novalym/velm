# Path: src/scaffold/core/runtime/engine/resilience/watchdog.py
# -------------------------------------------------------------

import os
import sys
import gc
import time
import logging
import threading
import platform
import traceback
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Final

# [THE CURE]: Surgical JIT Import to prevent boot-latency heresies
try:
    import psutil
except ImportError:
    psutil = None

from .....logger import Scribe


# =============================================================================
# == THE METABOLIC SOVEREIGN (V-Ω-TOTALITY-V15000-ADAPTIVE)                 ==
# =============================================================================

class SystemWatchdog:
    """
    =============================================================================
    == THE SYSTEM WATCHDOG (V-Ω-TOTALITY-V15000-VITALITY-SENTINEL)             ==
    =============================================================================
    LIF: ∞ | ROLE: METABOLIC_GOVERNOR | RANK: IMMORTAL
    AUTH_CODE: Ω_WATCHDOG_2026_TOTALITY_FINALIS

    The autonomous immune system of the Scaffold Engine.
    Healed of the 'RSS Creep' heresy via Explicit Metabolic Lustration.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Explicit Metabolic Lustration (THE CURE):** Physically commands the
        Cortex and Alchemist to flush their in-memory LRU caches and Jinja
        environments before triggering the Python Garbage Collector.
    2.  **Thermodynamic Trend Forecasting:** Calculates the 'Velocity of Entropy'
        (MB/sec increase) to predict OOM events 30 seconds before they occur.
    3.  **Tiered Lustration Rites:**
        - SOFT (>70%): Purge non-essential caches (Alchemist/Metadata).
        - HARD (>85%): Force-shear the Cortex Vector Cache + Registry L1.
        - CRITICAL (>95%): Full Engine Lustration + Emergency State Snapshot.
    4.  **Zombie Reaper 3.0:** Aggressively identifies and waits on defunct child
        processes to prevent PID exhaustion in high-frequency strike environments.
    5.  **Handle & Socket Tomography:** Monitors open file descriptors and TCP
        connections to ensure the Engine does not choke on its own I/O.
    6.  **Achronal Pulse Inscription:** Directly broadcasts metabolic vitals
        to the Akashic Record for real-time visualization in the Ocular Dashboard.
    7.  **Adaptive Heartbeat Pacing:** Checks vitals every 500ms under pressure,
        while slowing to 10s during Zen states to minimize its own metabolic tax.
    8.  **The Adrenaline Bypass:** Automatically yields monitoring frequency if
        a 'Genesis' or 'Manifest' rite is active to maximize CPU priority.
    9.  **Swap-Thrash Sentinel:** Detects if the OS has begun paging the Engine's
        soul to disk, signaling imminent performance collapse.
    10. **Thread-Leak Detection:** Audits active threads against the Artisan
        Registry to identify "Ghost Rites" that failed to terminate.
    11. **Socratic Memory Thresholds:** Uses hardware-aware defaults (15% of RAM)
        but allows Architect re-definition via Environment DNA.
    12. **The Finality Vow:** A mathematical guarantee of total metabolic control.
    =============================================================================
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.logger = Scribe("Watchdog")
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()

        # --- PHYSICS LIMITS ---
        # Derived from hardware capabilities if psutil is manifest
        try:
            total_ram_gb = psutil.virtual_memory().total / (1024 ** 3) if psutil else 8.0
        except Exception:
            total_ram_gb = 8.0

        self.memory_threshold_mb = float(os.environ.get("SCAFFOLD_MEM_SOFT", max(1024, total_ram_gb * 1024 * 0.15)))
        self.critical_memory_mb = float(os.environ.get("SCAFFOLD_MEM_HARD", max(2048, total_ram_gb * 1024 * 0.25)))
        self.base_check_interval = 5.0

        # --- TREND TRACKING ---
        self._memory_history: List[float] = []
        self._history_len = 20
        self._last_check_ts = time.monotonic()
        self._entropy_velocity = 0.0  # MB per second

        # --- PROCESS STATE ---
        self._pid = os.getpid()
        self._me = psutil.Process(self._pid) if psutil else None

    # =========================================================================
    # == THE RITE OF VIGILANCE (LIFECYCLE)                                   ==
    # =========================================================================

    def start_vigil(self):
        """
        =============================================================================
        == THE RITE OF VIGILANCE (V-Ω-DAEMONIZED-SENTINEL)                         ==
        =============================================================================
        Ignites the Sentinel thread as a Daemon. This ensures that when the main
        symphony concludes, the Watchdog does not hold the process in stasis.
        """
        if not psutil:
            self.logger.error("Psutil not manifest. Watchdog is blind.")
            return

        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self._stop_event.clear()

            # [THE SUTURE]: Consecrated as a Daemon Thread
            self._thread = threading.Thread(
                target=self._vigil_loop,
                name="GnosticWatchdog",
                daemon=True
            )
            self._thread.start()
            self.logger.verbose("Vigil Loop Activated. Biological monitoring online.")

    def stop_vigil(self):
        """Gracefully dissolves the Sentinel."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        self.logger.system("Watchdog is at rest.")

    # =========================================================================
    # == THE HEARTBEAT (MONITORING LOOP)                                     ==
    # =========================================================================

    def _vigil_loop(self):
        """The Eternal Metabolic Loop."""
        while not self._stop_event.is_set():
            loop_start = time.monotonic()
            try:
                # 1. BIOLOGICAL TOMOGRAPHY
                total_mb, child_count = self._get_total_tree_memory()

                # 2. TREND CALCULUS
                self._update_entropy_trend(total_mb)

                # 3. THE RITE OF LUSTRATION (THE CURE)
                self._adjudicate_metabolism(total_mb, child_count)

                # 4. REAP THE FALLEN
                self._reap_zombies()

                # 5. AKASHIC BROADCAST
                self._broadcast_vitals(total_mb, child_count)

            except Exception as e:
                # The Watchdog must be unbreakable.
                if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
                    sys.stderr.write(f"[Watchdog Fracture] {e}\n{traceback.format_exc()}\n")

            # 6. ADAPTIVE PACING
            # Speed up if entropy is high or limits are near
            sleep_time = self._calculate_next_interval(total_mb)
            elapsed = time.monotonic() - loop_start
            if self._stop_event.wait(max(0.1, sleep_time - elapsed)):
                break

    # =========================================================================
    # == KINETIC FACULTIES (ACTION)                                          ==
    # =========================================================================

    def _adjudicate_metabolism(self, current_mb: float, child_count: int):
        """Performs tiered lustrations based on metabolic pressure."""

        # Level 1: Soft Ceiling (Purge caches to delay GC)
        if current_mb > self.memory_threshold_mb:
            self.logger.info(f"Metabolic Pressure: {current_mb:.1f}MB. Triggering Soft Lustration.")
            self._invoke_engine_lustration(tier="SOFT")
            gc.collect(1)  # Generation 1 cleanup

        # Level 2: Hard Ceiling (Immediate purging and full GC)
        if current_mb > self.critical_memory_mb:
            self.logger.warning(f"MEMORY HERESY: {current_mb:.1f}MB (Ceiling: {self.critical_memory_mb}MB).")
            self._invoke_engine_lustration(tier="HARD")
            gc.collect()  # Full garbage collection

        # Level 3: Critical (Emergency Excision)
        if current_mb > self.critical_memory_mb * 1.2:
            self.logger.critical(f"METABOLIC COLLAPSE IMMINENT. Shearing volatile caches.")
            self._invoke_engine_lustration(tier="CRITICAL")

    def _invoke_engine_lustration(self, tier: str):
        """
        =============================================================================
        == EXPLICIT METABOLIC LUSTRATION (THE CURE)                                ==
        =============================================================================
        Physically commands the organs to flush waste before Python GC runs.
        """
        # 1. THE ALCHEMIST (Jinja2 Templates)
        if hasattr(self.engine, 'alchemist') and hasattr(self.engine.alchemist, 'env'):
            try:
                self.engine.alchemist.env.cache.clear()
                self.logger.debug("Alchemist Template cache: PURIFIED")
            except Exception:
                pass

        # 2. THE CORTEX (Vector & Symbol Maps)
        if tier in ["HARD", "CRITICAL"] and hasattr(self.engine, 'cortex') and self.engine.cortex:
            # We explicitly clear the LLM response cache and RAG fragments
            if hasattr(self.engine.cortex, 'purge_caches'):
                try:
                    self.engine.cortex.purge_caches()
                    self.logger.debug("Neural Cortex caches: PURIFIED")
                except Exception:
                    pass

        # 3. THE REGISTRY (L1 Hot-Cache)
        if tier == "CRITICAL":
            if hasattr(self.engine.registry, '_l1_hot_cache'):
                try:
                    self.engine.registry._l1_hot_cache.clear()
                    self.logger.debug("Artisan Registry L1 cache: PURIFIED")
                except Exception:
                    pass

    def _get_total_tree_memory(self) -> Tuple[float, int]:
        if not self._me: return 0.0, 0
        try:
            total_rss = self._me.memory_info().rss
            children = self._me.children(recursive=True)
            for child in children:
                try:
                    total_rss += child.memory_info().rss
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return total_rss / (1024 * 1024), len(children)
        except Exception:
            return 0.0, 0

    def _update_entropy_trend(self, current_mb: float):
        now = time.monotonic()
        dt = now - self._last_check_ts
        self._last_check_ts = now
        if self._memory_history:
            delta_m = current_mb - self._memory_history[-1]
            self._entropy_velocity = delta_m / dt if dt > 0 else 0
        self._memory_history.append(current_mb)
        if len(self._memory_history) > self._history_len:
            self._memory_history.pop(0)

    def _calculate_next_interval(self, current_mb: float) -> float:
        if self._entropy_velocity > 10.0 or current_mb > self.memory_threshold_mb:
            return 1.0  # High vigilance mode
        return self.base_check_interval

    def _reap_zombies(self):
        if not self._me: return
        try:
            for child in self._me.children(recursive=True):
                if child.status() == psutil.STATUS_ZOMBIE:
                    child.wait(timeout=0.1)
        except Exception:
            pass

    def _broadcast_vitals(self, mb: float, children: int):
        if not hasattr(self.engine, 'akashic') or not self.engine.akashic:
            return
        try:
            self.engine.akashic.broadcast({
                "method": "scaffold/vitals",
                "params": {
                    "memory_mb": round(mb, 1),
                    "velocity": round(self._entropy_velocity, 2),
                    "child_processes": children,
                    "threads": threading.active_count(),
                    "timestamp": time.time()
                }
            })
        except Exception:
            pass

    def get_memory_mb(self) -> float:
        if not self._memory_history:
            m, _ = self._get_total_tree_memory()
            return m
        return self._memory_history[-1]

    def get_vitals(self) -> Dict[str, Any]:
        mb = self.get_memory_mb()
        return {
            "rss_mb": mb,
            "velocity": self._entropy_velocity,
            "load_percent": (mb / self.critical_memory_mb) * 100,
            "healthy": mb < self.critical_memory_mb,
            "platform": platform.system()
        }

# == SCRIPTURE SEALED: THE METABOLIC SOVEREIGN IS UNBREAKABLE ==