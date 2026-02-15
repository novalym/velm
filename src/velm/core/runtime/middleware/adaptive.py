# Path: core/runtime/middleware/adaptive.py
# =========================================================================================
# == THE ADAPTIVE SURVIVOR (V-Ω-TOTALITY-V20.0-ISOMORPHIC-AEGIS)                         ==
# =========================================================================================
# LIF: ∞ | ROLE: ENVIRONMENTAL_GOVERNOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ADAPTIVE_V20_SUBSTRATE_AWARE_2026_FINALIS
# =========================================================================================

import os
import sys
import time
import gc
import random
from typing import Dict, Any, Optional, Tuple, List, Final

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 12]: Atomic Metabolic Cache
# (Timestamp, CPU_Load, Memory_Used, Is_WASM, Latency_Jitter)
_METABOLIC_SNAPSHOT = [0.0, 0.0, 0.0, False, 0.0]
_CACHE_TTL: Final[float] = 2.5  # Tightened for high-velocity adaptation


class AdaptiveResourceMiddleware(Middleware):
    """
    =============================================================================
    == THE ADAPTIVE SURVIVOR (V-Ω-ENVIRONMENTAL-AEGIS-ULTIMA)                  ==
    =============================================================================
    LIF: ∞ | The Sovereign Protector of the Engine's Homeostasis.

    Dynamically modulates the Engine's ambition based on the physical reality
    of the host machine, whether forged in Iron (Native) or Ether (WASM).
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """Conducts the Rite of Environmental Adaptation."""

        # --- MOVEMENT I: THE DETERMINISTIC BYPASS ---
        if os.environ.get("SCAFFOLD_ADAPTIVE") == "0":
            return next_handler(request)

        # 2. RITE-WEIGHT TRIAGE
        # We skip metabolic scrying for lightweight telemetry or status rites.
        rite_name = type(request).__name__
        is_heavy = any(k in rite_name for k in ["Manifest", "Distill", "Genesis", "Refactor", "Analyze", "Train"])

        if not is_heavy and not getattr(request, "force_adaptive", False):
            return next_handler(request)

        # --- MOVEMENT II: THE MULTIVERSAL PROBE ---
        # [ASCENSION 1 & 2]: Substrate Sensing
        vitals = self._scry_metabolism()

        # --- MOVEMENT III: THE RITE OF MODULATION ---
        self._modulate_request(request, vitals)

        # --- MOVEMENT IV: KINETIC EXECUTION ---
        # [ASCENSION 6]: Hydraulic Yielding
        # We yield a microsecond to the host OS to ensure we aren't starving sibling processes.
        time.sleep(0)

        result = next_handler(request)

        # --- MOVEMENT V: TELEMETRY INJECTION ---
        # [ASCENSION 10 & 11]: Luminous Telemetry Suture
        return self._inject_health_dossier(result, vitals)

    def _scry_metabolism(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE GAZE OF VITALITY (V-Ω-SUBSTRATE-AGNOSTIC)                           ==
        =============================================================================
        Performs a deep-tissue biopsy of the system. In WASM, it uses Chronometric
        Drift to divine CPU pressure.
        """
        now = time.time()
        if now - _METABOLIC_SNAPSHOT[0] < _CACHE_TTL:
            return self._format_vitals(_METABOLIC_SNAPSHOT)

        cpu_load = 0.0
        mem_load = 0.0
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        jitter = 0.0

        try:
            # --- PATH A: THE IRON CORE (NATIVE) ---
            if not is_wasm:
                try:
                    import psutil
                    cpu_load = psutil.cpu_percent(interval=None)
                    mem_load = psutil.virtual_memory().percent
                except ImportError:
                    is_wasm = True  # Fallback to heuristic scrying

            # --- PATH B: THE ETHER PLANE (HEURISTIC) ---
            if is_wasm:
                # [ASCENSION 2]: Achronal Drift Tomography
                # Measure loop lag: A 1ms sleep that takes 10ms means 900% saturation.
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                jitter = (t1 - t0) - 0.001

                # CPU Inference from jitter
                cpu_load = min(100.0, jitter * 50000)  # Heuristic scaling

                # [ASCENSION 8]: Heap Object Tomography
                # Count living Python objects to estimate memory pressure.
                obj_count = len(gc.get_objects())
                mem_load = min(100.0, (obj_count / 1000000) * 100)  # Assume 1M objects is 'Heavy'

        except Exception as paradox:
            self.logger.debug(f"Metabolic scrying deferred: {paradox}")

        # Update Atomic Cache
        _METABOLIC_SNAPSHOT[:] = [now, cpu_load, mem_load, is_wasm, jitter]
        return self._format_vitals(_METABOLIC_SNAPSHOT)

    def _modulate_request(self, request: BaseRequest, vitals: Dict[str, Any]):
        """
        =============================================================================
        == THE ALCHEMICAL MODULATOR (V-Ω-WILL-TRANSFIGURATION)                    ==
        =============================================================================
        Surgically alters the plea to match the system's thermal and memory state.
        """
        cpu = vitals["cpu_percent"]
        mem = vitals["mem_percent"]
        is_wasm = vitals["is_wasm"]

        # 1. ECONOMY MODE (Model Swapping)
        if cpu > 85.0 or (is_wasm and cpu > 60.0):
            if "model" in request.variables and request.variables["model"] == "smart":
                self.logger.warn("Metabolic Fever: Downgrading to 'fast' neural model.")
                request.variables["model"] = "fast"
                request.variables["_adaptation"] = "cpu_throttle"

        # 2. CONTEXT SHEDDING (Memory Protection)
        if mem > 80.0:
            if hasattr(request, 'token_budget'):
                # [ASCENSION 4]: Shear the Gnostic Budget by 40%
                original = request.token_budget or 100000
                request.token_budget = int(original * 0.6)
                self.logger.verbose(f"Memory Wall: Shearing token budget to {request.token_budget}")

        # 3. ADAPTIVE CHRONOMETRY (Timeout Scaling)
        if cpu > 70.0:
            # [ASCENSION 7]: If the machine is lagging, we give it more time to think.
            if hasattr(request, 'timeout_seconds'):
                request.timeout_seconds = int(request.timeout_seconds * 1.5)

    def _inject_health_dossier(self, result: ScaffoldResult, vitals: Dict[str, Any]) -> ScaffoldResult:
        """Grafts environmental gnosis onto the final revelation."""
        # Ensure result and data are manifest
        if result is None: return None

        # [ASCENSION 5]: NoneType Sarcophagus
        if result.data is None:
            # We initialize a safe container if none exists
            object.__setattr__(result, 'data', {})

        if isinstance(result.data, dict):
            # 1. Physical Health
            result.data["_metabolism"] = {
                "substrate": "ETHER" if vitals["is_wasm"] else "IRON",
                "cpu_load": round(vitals["cpu_percent"], 1),
                "ram_load": round(vitals["mem_percent"], 1),
                "resonant": vitals["cpu_percent"] < 90.0
            }

            # 2. Haptic Ocular Hints
            if result.ui_hints is None:
                object.__setattr__(result, 'ui_hints', {})

            # [ASCENSION 10]: Aura Radiation
            if vitals["cpu_percent"] > 90.0:
                result.ui_hints["glow"] = "#ef4444"  # Red Panic
                result.ui_hints["vfx"] = "shake"
            elif vitals["cpu_percent"] > 70.0:
                result.ui_hints["glow"] = "#f59e0b"  # Amber Fever

        return result

    def _format_vitals(self, snapshot: list) -> Dict[str, Any]:
        return {
            "ts": snapshot[0],
            "cpu_percent": snapshot[1],
            "mem_percent": snapshot[2],
            "is_wasm": snapshot[3],
            "jitter": snapshot[4]
        }

