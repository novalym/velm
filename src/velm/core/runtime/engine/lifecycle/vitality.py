# Path: core/runtime/engine/lifecycle/vitality.py
# ------------------------------------------------------------

from __future__ import annotations
import threading
import time
import os
import psutil
import gc
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Final

# --- GNOSTIC UPLINKS ---
from .state import LifecyclePhase

Logger = logging.getLogger("QuantumEngine:Metabolism")


# =============================================================================
# == THE METABOLIC SOVEREIGN (V-Ω-TOTALITY-V15000-ADAPTIVE)                 ==
# =============================================================================

class VitalityMonitor:
    """
    =============================================================================
    == THE METABOLIC SOVEREIGN (V-Ω-TOTALITY-V15000-ADAPTIVE)                 ==
    =============================================================================
    LIF: ∞ | ROLE: METABOLIC_GOVERNOR | RANK: SOVEREIGN
    AUTH_CODE: !)(#()#()

    The evolved immune system of the Scaffold Engine. It adjudicates health
    based on the physical reality of the host hardware.
    """

    # [PHYSICS CONSTANTS]
    PULSE_ZEN_RATE: Final[float] = 10.0  # Idle check frequency
    PULSE_KINETIC_RATE: Final[float] = 2.0  # Active check frequency
    MEMORY_HYSTERESIS_MB: Final[float] = 50.0  # Log muzzle threshold

    def __init__(self, engine: Any):
        self.engine = engine
        self.logger = Logger
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # --- 1. ADAPTIVE THRESHOLD CALCULATION ---
        # [ASCENSION 1]: We divine the machine's capacity to set rational limits.
        try:
            total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        except Exception:
            total_ram_gb = 8.0  # Fallback to standard 8GB

        # Soft Cap: 15% of total RAM or 1.5GB (Whichever is higher)
        self.gc_threshold_mb = max(1536.0, (total_ram_gb * 1024 * 0.15))
        # Hard Cap: 25% of total RAM or 2.5GB
        self.memory_limit_mb = max(2560.0, (total_ram_gb * 1024 * 0.25))

        # --- 2. HYSTERESIS STATE ---
        self._last_proclaimed_mb = 0.0
        self._last_gc_time = 0.0
        self._entropy_velocity = 0.0  # MB/second
        self._parent_pid = os.getppid()

        self.pulse_path: Optional[Path] = None

    def start_vigil(self, pulse_file_path: Optional[str] = None):
        """
        =============================================================================
        == THE RITE OF METABOLIC HEARTBEAT (V-Ω-DAEMONIZED-PULSE)                  ==
        =============================================================================
        Ignites the Heartbeat with Adaptive Awareness. Consecrated as a Daemon to
        prevent the "Lingering Soul" heresy during CLI shutdown.
        """
        if pulse_file_path:
            self.pulse_path = Path(pulse_file_path)

        self.logger.info(
            f"Metabolic Sovereign active. "
            f"GC_Threshold: {self.gc_threshold_mb:.0f}MB | "
            f"Ceiling: {self.memory_limit_mb:.0f}MB"
        )

        # [THE SUTURE]: Consecrated as a Daemon Thread
        self._thread = threading.Thread(
            target=self._vigil_loop,
            name="VitalityVigil",
            daemon=True
        )
        self._thread.start()


    def stop_vigil(self):
        """The Rite of Graceful Cessation."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        self._write_pulse(status="VOID")

    def _vigil_loop(self):
        """The Eternal Vigil Loop."""
        process = psutil.Process(os.getpid())

        while not self._stop_event.is_set():
            loop_start = time.monotonic()

            try:
                # 1. BIOLOGICAL TOMOGRAPHY
                mem_info = process.memory_info()
                current_mb = mem_info.rss / (1024 * 1024)
                sys_mem = psutil.virtual_memory()

                # 2. ENTROPY TREND ANALYSIS (Ascension 3)
                delta_m = current_mb - self._last_proclaimed_mb
                self._entropy_velocity = delta_m / self.PULSE_KINETIC_RATE

                # 3. PARENT VIGIL (Ascension 6)
                # If we were spawned by a process that has since vanished, we dissolve.
                if not psutil.pid_exists(self._parent_pid):
                    self.logger.critical("Parent process vanished. Initiating autonomic shutdown.")
                    self.engine.shutdown()
                    break

                # 4. ADJUDICATE METABOLISM (Ascension 2)
                state = "ZEN"
                should_log = abs(current_mb - self._last_proclaimed_mb) > self.MEMORY_HYSTERESIS_MB

                if current_mb > self.gc_threshold_mb:
                    state = "FEVER"
                    # [ASCENSION 5]: Tiered Lustration
                    # Only trigger heavy GC if it's been 30s since last attempt
                    if time.time() - self._last_gc_time > 30:
                        if should_log:
                            self.logger.warning(
                                f"Metabolic Fever ({current_mb:.0f}MB). "
                                f"Machine_Load: {sys_mem.percent}%. Triggering Lustration Rite."
                            )

                        # Full Purgation
                        gc.collect()
                        self._last_gc_time = time.time()
                        self._last_proclaimed_mb = current_mb

                # 5. CRITICAL ANNIHILATION SHIELD (Ascension 9)
                if current_mb > self.memory_limit_mb:
                    self.logger.critical(f"FATAL_METABOLIC_TAX: Usage at {current_mb:.0f}MB. Shearing volatile caches.")
                    self._shear_engine_caches()

                # 6. AKASHIC HEARTBEAT (Ascension 8)
                self._write_pulse(
                    status="RESONANT" if state == "ZEN" else "STRESSED",
                    metadata={
                        "rss_mb": round(current_mb, 1),
                        "sys_percent": sys_mem.percent,
                        "velocity_mb_s": round(self._entropy_velocity, 2),
                        "state": state,
                        "aura": "#64ffda" if state == "ZEN" else "#fbbf24"
                    }
                )

                # Update baseline if significant shift or log occurred
                if should_log:
                    self._last_proclaimed_mb = current_mb

            except Exception as paradox:
                # The Vigil must be unbreakable.
                pass

                # 7. ADAPTIVE PACING (Ascension 4)
            # Adjust sleep duration based on load. Faster checks during Fever.
            target_rate = self.PULSE_KINETIC_RATE if state == "FEVER" else self.PULSE_ZEN_RATE
            elapsed = time.monotonic() - loop_start

            if self._stop_event.wait(max(0.1, target_rate - elapsed)):
                break

    def _write_pulse(self, status: str = "ALIVE", metadata: Dict = None):
        """Atomic write of the pulse telemetry."""
        if not self.pulse_path: return

        payload = {
            "pid": os.getpid(),
            "timestamp": time.time(),
            "status": status,
            "meta": metadata or {}
        }

        try:
            # [ASCENSION 7]: Atomic swap
            temp = self.pulse_path.with_suffix('.tmp')
            with open(temp, 'w', encoding='utf-8') as f:
                json.dump(payload, f)

            # Use os.replace for atomic replacement (Bulletproof)
            os.replace(str(temp), str(self.pulse_path))
        except Exception:
            pass

    def _shear_engine_caches(self):
        """[ASCENSION 9]: Emergency cache evaporation."""
        try:
            # 1. Clear Alchemist Jinja templates
            if hasattr(self.engine, 'alchemist'):
                self.engine.alchemist.env.cache.clear()

            # 2. Clear Cortex Symbol Maps
            if hasattr(self.engine, 'cortex') and self.engine.cortex:
                # Future logic for clearing AST indices
                pass

            gc.collect(2)  # Deepest possible collection
        except Exception:
            pass

    def _adjust_metabolism(self):
        """Deprecated: Replaced by Adaptive Pacing logic in loop."""
        pass

# == SCRIPTURE SEALED: THE METABOLIC SOVEREIGN IS UNBREAKABLE ==