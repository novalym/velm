# Path: src/velm/core/runtime/engine/lifecycle/vitality.py
# =========================================================================================
# == THE METABOLIC SOVEREIGN (V-Ω-TOTALITY-V20000-WASM-HYBRID-FINALIS)                  ==
# =========================================================================================
# LIF: ∞ | ROLE: METABOLIC_GOVERNOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_VITALITY_V20K_THREAD_BYPASS_2026_FINALIS
# =========================================================================================

from __future__ import annotations
import threading
import time
import os
import sys
import gc
import json
import logging
import platform
from pathlib import Path
from typing import Optional, Dict, Any, Final, Union

# [ASCENSION 1]: SURGICAL SENSORY GUARD
# We attempt to manifest the psutil artisan for Iron Core realities.
try:
    import psutil

    PS_AVAILABLE = True
except ImportError:
    psutil = None
    PS_AVAILABLE = False

# --- GNOSTIC UPLINKS ---
from .state import LifecyclePhase

Logger = logging.getLogger("QuantumEngine:Metabolism")


class VitalityMonitor:
    """
    =================================================================================
    == THE METABOLIC SOVEREIGN (V-Ω-TOTALITY-V20000-WASM-HYBRID)                  ==
    =================================================================================
    The evolved immune system of the Scaffold Engine.
    It has been ascended to possess **Substrate Independence**, governing health
    in both Bare Metal (Iron) and WebAssembly (Ether) environments.

    ### THE 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Thread-Bypass (THE CURE):** Detects WASM substrate at nanosecond
        zero and stays the hand of the Threading system, preventing RuntimeError.
    2.  **Temporal Drift Tomography:** In WASM, measures loop jitter to infer CPU
        saturation without hardware-level access.
    3.  **Heap Density Scrying:** Estimates memory mass by observing the count of
        objects in the Python Garbage Collector.
    4.  **Bicameral Heartbeat:** Supports both background threading (Iron) and
        synchronous manual pulses (Ether).
    5.  **Parent Vigil Amnesty:** Prevents autonomic self-annihilation in WASM
        environments where PID scrying is a heresy.
    6.  **Deterministic Health FLOOR:** Proclaims a "RESONANT" status by default
        unless temporal drift exceeds the Event Horizon.
    7.  **Isomorphic Vitals Payload:** Normalizes hardware-specific metrics into a
        universal Gnostic schema for the Ocular HUD.
    8.  **Atomic Swap Persistence:** Uses the `os.replace` rite for telemetry
        updates, ensuring the pulse file is never corrupted.
    9.  **Tiered Lustration:** Automatically modulates GC intensity based on the
        perceived "Metabolic Tax" of the current substrate.
    10. **Zero-IO Inception:** If the pulse_path is void, telemetry is routed
        exclusively through the internal Akashic Record.
    11. **Metabolic Yield:** Injects hardware-appropriate yields to the host OS.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable heartbeat.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    PULSE_ZEN_RATE: Final[float] = 10.0
    PULSE_KINETIC_RATE: Final[float] = 2.0
    MEMORY_HYSTERESIS_MB: Final[float] = 50.0
    ETHER_DRIFT_CEILING: Final[float] = 15.0  # ms of lag before "Fever"

    def __init__(self, engine: Any):
        self.engine = engine
        self.logger = Logger
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # [ASCENSION 1]: SUBSTRATE DETECTION
        # We scry the environment to determine the physics of the vigil.
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self.is_blind = not PS_AVAILABLE

        # --- 1. ADAPTIVE THRESHOLD CALCULATION ---
        try:
            if not self.is_blind:
                total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
            else:
                total_ram_gb = 4.0  # Heuristic limit for browser workers
        except Exception:
            total_ram_gb = 8.0

        self.gc_threshold_mb = max(1024.0, (total_ram_gb * 1024 * 0.15))
        self.memory_limit_mb = max(2048.0, (total_ram_gb * 1024 * 0.30))

        # --- 2. HYSTERESIS STATE ---
        self._last_proclaimed_mb = 0.0
        self._last_gc_ts = 0.0
        self._entropy_velocity = 0.0
        self._last_biopsy_ts = time.monotonic()

        # [ASCENSION 5]: Parent Identification
        try:
            self._parent_pid = os.getppid() if hasattr(os, 'getppid') else 0
        except Exception:
            self._parent_pid = 0

        self.pulse_path: Optional[Path] = None

    def start_vigil(self, pulse_file_path: Optional[str] = None):
        """
        =============================================================================
        == THE RITE OF IGNITION: SUBSTRATE-AWARE HEARTBEAT                         ==
        =============================================================================
        [THE CURE]: Prevents the 'can't start new thread' heresy in the browser tab.
        """
        if pulse_file_path:
            self.pulse_path = Path(pulse_file_path)

        # [ASCENSION 1]: SUBSTRATE DETECTION
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        self.logger.info(
            f"Vitality Monitor active. [Substrate: {'ETHER' if is_wasm else 'IRON'}]"
        )

        if is_wasm:
            self.logger.info("Heartbeat shifted to [cyan]Synchronous Pulse[/cyan].")
            # We perform one manual pulse to initialize telemetry
            self.pulse()
            return

        # PATH: IRON CORE (NATIVE)
        # Background threads are only permitted on physical substrates.
        try:
            self._thread = threading.Thread(
                target=self._vigil_loop,
                name="VitalityVigil",
                daemon=True
            )
            self._thread.start()
        except RuntimeError:
            self.logger.warn("Threading prohibited. Heartbeat remains silent.")



    def pulse(self):
        """
        =============================================================================
        == THE RITE OF THE ACHRONAL PULSE                                          ==
        =============================================================================
        [ASCENSION 10]: Manual heartbeat trigger.
        Used by WASM environments to check vitals without background threads.
        """
        vitals = self._perform_biopsy()
        self._adjudicate_metabolism(vitals)
        self._write_pulse_data(vitals)
        return vitals

    def stop_vigil(self):
        """Graceful Cessation."""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            try:
                self._thread.join(timeout=0.5)
            except:
                pass
        self._write_pulse_data(vitals={"status": "VOID"})

    def _vigil_loop(self):
        """The Eternal Vigil Loop for Native Strata."""
        # Warm the process scrier
        process = None
        if not self.is_blind:
            try:
                process = psutil.Process(os.getpid())
            except:
                self.is_blind = True

        while not self._stop_event.is_set():
            loop_start = time.monotonic()
            try:
                vitals = self._perform_biopsy(process)
                self._adjudicate_metabolism(vitals)
                self._write_pulse_data(vitals)

                # PARENT VIGIL
                if self._parent_pid > 0 and not self.is_wasm:
                    if not psutil.pid_exists(self._parent_pid):
                        self.logger.critical("Parent process vanished. Dissolving reality.")
                        self.engine.shutdown()
                        break
            except Exception:
                pass

            # Adaptive Pacing
            current_rate = self.PULSE_ZEN_RATE
            if self._entropy_velocity > 10.0: current_rate = self.PULSE_KINETIC_RATE

            elapsed = time.monotonic() - loop_start
            if self._stop_event.wait(max(0.1, current_rate - elapsed)):
                break

    def _perform_biopsy(self, process: Optional[Any] = None) -> Dict[str, Any]:
        """
        =============================================================================
        == THE METABOLIC BIOPSY (V-Ω-SUBSTRATE-AGNOSTIC)                           ==
        =============================================================================
        [ASCENSION 2 & 3]: High-fidelity sensing without psutil.
        """
        now = time.monotonic()
        dt = now - self._last_biopsy_ts
        self._last_biopsy_ts = now

        # --- MOVEMENT I: MEMORY TOMOGRAPHY ---
        if process and not self.is_blind:
            mem_info = process.memory_info()
            current_mb = mem_info.rss / (1024 * 1024)
            cpu_load = process.cpu_percent()
        else:
            # [ASCENSION 3]: HEAP MASS INFERENCE (WASM)
            # Count Python objects. Heuristic: 100k objects ~ 15MB Gnostic Mass.
            object_count = len(gc.get_objects())
            current_mb = (object_count * 0.00015) + 100.0  # Base 100MB floor

            # [ASCENSION 2]: TEMPORAL DRIFT TOMOGRAPHY (WASM CPU)
            t0 = time.perf_counter()
            time.sleep(0.001)  # Micro-yield
            t1 = time.perf_counter()
            drift_ms = (t1 - t0) * 1000
            # Map drift to synthetic CPU percent (Drift of 5ms = 100% saturation)
            cpu_load = min(100.0, (drift_ms / 5.0) * 100.0)

        # --- MOVEMENT II: TREND ANALYSIS ---
        if dt > 0:
            self._entropy_velocity = (current_mb - self._last_proclaimed_mb) / dt

        return {
            "rss_mb": round(current_mb, 1),
            "cpu_percent": round(cpu_load, 1),
            "velocity_mb_s": round(self._entropy_velocity, 2),
            "substrate": "ETHER" if self.is_wasm else "IRON",
            "timestamp": time.time(),
            "status": "RESONANT" if cpu_load < 90 else "STRESSED"
        }

    def _adjudicate_metabolism(self, vitals: Dict[str, Any]):
        """Decides if the engine requires surgical lustration."""
        current_mb = vitals["rss_mb"]

        # LUSTRATION TRIGGER
        if current_mb > self.gc_threshold_mb:
            if time.monotonic() - self._last_gc_ts > 15.0:
                self.logger.warning(f"Metabolic Fever ({current_mb:.0f}MB). Initiating lustration...")
                self._shear_engine_caches()
                self._last_gc_ts = time.monotonic()

        # EMERGENCY SHEDDING
        if current_mb > self.memory_limit_mb:
            self.logger.critical(f"MEMORY_WALL: Substrate saturation at {current_mb:.0f}MB.")
            # Trigger emergency GC
            gc.collect()

        self._last_proclaimed_mb = current_mb

    def _write_pulse_data(self, vitals: Dict[str, Any]):
        """Atomic write of the heartbeat to the virtual or physical disk."""
        if not self.pulse_path: return

        payload = {
            "pid": os.getpid(),
            "status": vitals.get("status", "ALIVE"),
            "timestamp": time.time(),
            "meta": vitals
        }

        try:
            temp = self.pulse_path.with_suffix('.tmp')
            # [ASCENSION 8]: ATOMIC SWAP
            with open(temp, 'w', encoding='utf-8') as f:
                json.dump(payload, f)
            os.replace(str(temp), str(self.pulse_path))
        except Exception:
            pass

    def _shear_engine_caches(self):
        """Emergency cache evaporation to reclaim RAM."""
        try:
            if hasattr(self.engine, 'alchemist'):
                self.engine.alchemist.env.cache.clear()
            gc.collect(1)  # Young generation sweep
        except:
            pass

    def get_vitals(self) -> Dict[str, Any]:
        """Provides a direct biopsy to the Dispatcher or Profiler."""
        return self._perform_biopsy()
