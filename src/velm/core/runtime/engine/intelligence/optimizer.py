# Path: core/runtime/engine/intelligence/optimizer.py
# =========================================================================================
# == THE NEURO-OPTIMIZER (V-Ω-TOTALITY-V20000.12-ADAPTIVE-MATTER)                       ==
# =========================================================================================
# LIF: 10,000,000,000,000 | ROLE: METABOLIC_GOVERNOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_OPTIMIZER_V20000_SUBSTRATE_RESONANCE_2026_FINALIS
# =========================================================================================

import os
import sys
import time
import gc
import threading
from typing import Any, Dict, Optional, Tuple, Final

# [ASCENSION 1]: SURGICAL SENSORY GUARD
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from .....logger import Scribe
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("NeuroOptimizer")


class NeuroOptimizer:
    """
    =================================================================================
    == THE NEURO-OPTIMIZER (V-Ω-TOTALITY)                                         ==
    =================================================================================
    The Sovereign Governor of the Engine's physical reality. It dynamically tunes
    the physics of the runtime to match the metabolic capacity of the substrate.
    """

    # [PHYSICS CONSTANTS]
    MEM_PANIC_THRESHOLD: Final[float] = 92.0
    CPU_FEVER_THRESHOLD: Final[float] = 85.0
    ETHER_DRIFT_CEILING: Final[float] = 8.0  # ms

    def __init__(self, engine: Any):
        """
        [THE RITE OF ANCHORING]
        Calibrates the optimizer to the host substrate.
        """
        self.engine = engine
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

        # --- CALIBRATE SENSES ---
        try:
            self.cpu_count = os.cpu_count() or 1
            if PSUTIL_AVAILABLE:
                self.total_ram = psutil.virtual_memory().total
            else:
                self.total_ram = 0  # Ethereal memory is unmeasured
        except Exception:
            self.cpu_count = 1
            self.total_ram = 0

        # Tuning History
        self._last_tuning_ts = 0.0
        self._fever_level = 0.0

    def pre_dispatch_tuning(self, heavy_mode: bool = False):
        """
        =============================================================================
        == THE RITE OF METABOLIC ALIGNMENT                                         ==
        =============================================================================
        Surgically tunes the environment before a Rite is conducted.
        """
        now = time.monotonic()
        # Debounce the scry to prevent telemetry from becoming the tax
        if now - self._last_tuning_ts < 0.5:
            return
        self._last_tuning_ts = now

        try:
            # --- MOVEMENT I: SENSORY TOMOGRAPHY ---
            vitals = self._scry_substrate()
            self._fever_level = vitals.get("cpu", 0.0)

            # --- MOVEMENT II: THE ADRENALINE INJECTION ---
            # [ASCENSION 12]: If the rite is heavy, we prioritize throughput.
            if heavy_mode and self._fever_level < self.CPU_FEVER_THRESHOLD:
                self._engage_adrenaline_mode()
            else:
                self._disengage_adrenaline_mode()

            # --- MOVEMENT III: SUBSTRATE-SPECIFIC TUNING ---
            if self.is_wasm:
                self._tune_ether(vitals)
            else:
                self._tune_iron(vitals)

            # --- MOVEMENT IV: THE CONCURRENCY GOVERNOR ---
            self._modulate_concurrency(vitals)

        except Exception as fracture:
            # [ASCENSION 5]: The Shield of Silence
            pass

    # =========================================================================
    # == INTERNAL FACULTIES (SCRYING)                                        ==
    # =========================================================================

    def _scry_substrate(self) -> Dict[str, Any]:
        """Perceives the metabolic vitals across the Iron/Ether divide."""
        if PSUTIL_AVAILABLE and not self.is_wasm:
            return {
                "cpu": psutil.cpu_percent(interval=None) or 0.0,
                "mem": psutil.virtual_memory().percent,
                "load": os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0.0
            }
        else:
            # [ASCENSION 2]: Achronal Drift Tomography (WASM Heuristics)
            t0 = time.perf_counter()
            time.sleep(0.001)
            t1 = time.perf_counter()
            drift_ms = (t1 - t0) * 1000

            # Map drift to a synthetic CPU load
            synthetic_cpu = min(100.0, (drift_ms / self.ETHER_DRIFT_CEILING) * 90.0)

            return {
                "cpu": synthetic_cpu,
                "mem": (len(gc.get_objects()) / 1000000.0) * 100,  # Heuristic RAM mass
                "load": synthetic_cpu / 100.0
            }

    # =========================================================================
    # == KINETIC TUNING RITES                                                ==
    # =========================================================================

    def _tune_iron(self, vitals: Dict[str, Any]):
        """Rites of optimization for Physical Metal (Azure/Local)."""
        # 1. Adjust Priority
        if vitals["cpu"] > self.CPU_FEVER_THRESHOLD:
            os.environ["SCAFFOLD_LOW_PRIORITY"] = "1"
            if hasattr(os, 'nice'):
                try:
                    os.nice(1)
                except:
                    pass
        else:
            os.environ.pop("SCAFFOLD_LOW_PRIORITY", None)

        # 2. Memory Wall Protection
        if vitals["mem"] > self.MEM_PANIC_THRESHOLD:
            os.environ["SCAFFOLD_DISABLE_CACHE"] = "1"
            self._lustrate_caches()
        else:
            os.environ.pop("SCAFFOLD_DISABLE_CACHE", None)

    def _tune_ether(self, vitals: Dict[str, Any]):
        """Rites of optimization for the Browser (WASM)."""
        # [ASCENSION 10]: Hydraulic Yielding
        # In WASM, high CPU means we must yield more frequently to the UI thread.
        if vitals["cpu"] > 60.0:
            os.environ["SCAFFOLD_WASM_THROTTLE"] = "1"
            # Command Pyodide to be lazy with GC to save cycles
            gc.set_threshold(50000)
        else:
            os.environ.pop("SCAFFOLD_WASM_THROTTLE", None)
            gc.set_threshold(700, 10, 10)  # Restore default

    def _engage_adrenaline_mode(self):
        """Forces the Engine into a state of high-velocity creation."""
        os.environ["SCAFFOLD_ADRENALINE"] = "1"
        # Disable lazy GC during heavy strikes to prevent stutter
        gc.disable()

    def _disengage_adrenaline_mode(self):
        """Returns the Engine to a state of calm perception."""
        if os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            os.environ.pop("SCAFFOLD_ADRENALINE", None)
            gc.enable()
            gc.collect(1)  # Immediate soft lustration

    def _modulate_concurrency(self, vitals: Dict[str, Any]):
        """Adjudicates the task-density of the worker pools."""
        if vitals["cpu"] > 80.0:
            # Command the Dispatcher to shed secondary tasks
            os.environ["SCAFFOLD_MAX_THREADS"] = "1"
        else:
            os.environ.pop("SCAFFOLD_MAX_THREADS", None)

    def _lustrate_caches(self):
        """Evaporates metabolic waste to reclaim the RAM sanctum."""
        if hasattr(self.engine, 'alchemist'):
            try:
                self.engine.alchemist.env.cache.clear()
            except:
                pass
        gc.collect()

    def __repr__(self) -> str:
        status = "FEVERISH" if self._fever_level > 70 else "RESONANT"
        return f"<NeuroOptimizer substrate={'WASM' if self.is_wasm else 'IRON'} status={status}>"