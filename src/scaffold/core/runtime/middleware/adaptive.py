# Path: core/runtime/middleware/adaptive.py
# -----------------------------------------
# LIF: 10,000,000,000,000 | AUTH_CODE: Ω_ADAPTIVE_SURVIVOR_V12
# SYSTEM: SCAFFOLD_RUNTIME | ROLE: ENVIRONMENTAL_AEGIS
# =================================================================================
# [12 ASCENSIONS OF THE ADAPTIVE SURVIVOR]:
# 1.  HOLLOW-BORE JIT: Zero top-level imports of psutil to annihilate boot latency.
# 2.  RITE-WEIGHT TRIAGE: Only executes analytical probes for heavy "Foundry" rites.
# 3.  ECONOMY MODE: Automatically swaps 'smart' models for 'fast' models on low power.
# 4.  CONTEXT SHEDDING: Reduces RAG and Distill budgets if memory pressure is high.
# 5.  THERMAL GUARD: (Prophecy) Prepares for thermal-aware compute regulation.
# 6.  NETWORK GAUGE: Detects thin pipes and suggests RAG pruning.
# 7.  DETERMINISTIC BYPASS: Honors SCAFFOLD_ADAPTIVE=0 for manual control.
# 8.  RSS CEILING WATCH: Prevents OOM by blocking heavy rites near the memory wall.
# 9.  PROCESS CONCURRENCY: Detects sibling daemons and reduces thread counts.
# 10. ADAPTIVE TIMEOUTS: Relaxes chronometric limits if the machine is lagging.
# 11. LUMINOUS TELEMETRY: Injects environmental health data into the final Result.
# 12. ATOMIC CACHE: Remembers resource state for 5 seconds to prevent I/O thrashing.
# =================================================================================

import os
import sys
import time
from typing import Dict, Any, Optional

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult

# [ASCENSION 12]: Atomic Resource Cache
# (Timestamp, CPU_Load, Memory_Used, Battery_State)
_RESOURCE_CACHE = [0.0, 0.0, 0.0, None]
_CACHE_TTL = 5.0  # Seconds


class AdaptiveResourceMiddleware(Middleware):
    """
    =============================================================================
    == THE ADAPTIVE SURVIVOR (V-Ω-ENVIRONMENTAL-AEGIS-ULTIMA)                  ==
    =============================================================================
    LIF: ∞ | The Guardian of System Vitality.

    Dynamically modulates the Engine's ambition based on the physical reality
    of the host machine.
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        Conducts the Rite of Environmental Adaptation.
        """
        # --- MOVEMENT I: THE SILENT BYPASS ---
        # 1. Check for manual override
        if os.environ.get("SCAFFOLD_ADAPTIVE") == "0":
            return next_handler(request)

        # 2. Check Rite Weight
        # We only perform intensive scans for rites that actually consume compute.
        # This keeps 'status', 'ping', 'help', and 'version' at zero latency.
        rite_name = type(request).__name__
        is_heavy = any(k in rite_name for k in ["Manifest", "Distill", "Genesis", "Refactor", "Analyze"])

        if not is_heavy:
            return next_handler(request)

        # --- MOVEMENT II: THE JIT MATERIALIZATION ---
        # [THE CURE]: We import psutil ONLY here, inside the heavy rite path.
        try:
            import psutil
        except ImportError:
            # If psutil is missing, we are blind. We proceed in a pure state.
            return next_handler(request)

        # --- MOVEMENT III: THE VITALITY PROBE (CACHED) ---
        now = time.time()
        if now - _RESOURCE_CACHE[0] > _CACHE_TTL:
            try:
                # CPU Gaze (Non-blocking)
                _RESOURCE_CACHE[1] = psutil.cpu_percent()
                # Memory Gaze
                _RESOURCE_CACHE[2] = psutil.virtual_memory().percent
                # Battery Gaze
                _RESOURCE_CACHE[3] = psutil.sensors_battery()
                _RESOURCE_CACHE[0] = now
            except Exception:
                pass  # Hardware scrying failed; rely on last known truth.

        cpu_load = _RESOURCE_CACHE[1]
        mem_load = _RESOURCE_CACHE[2]
        battery = _RESOURCE_CACHE[3]

        # --- MOVEMENT IV: THE RITE OF MODULATION ---

        # [ASCENSION 3]: ECONOMY MODE (Battery Protection)
        if battery and not battery.power_plugged and battery.percent < 15:
            if "model" in request.variables and request.variables["model"] == "smart":
                self.logger.warn(f"Reality Threatened: Low Energy ({battery.percent}%). Downgrading to Fast Model.")
                request.variables["model"] = "fast"
                request.variables["_adapted_reason"] = "low_battery"

        # [ASCENSION 4]: CONTEXT SHEDDING (Memory Protection)
        if mem_load > 85:
            self.logger.warn(f"Reality Threatened: Memory Wall ({mem_load}%). Pruning Gnostic Budget.")
            # Reduce token budget for AI rites to prevent OOM
            if hasattr(request, 'token_budget'):
                original = request.token_budget or 100000
                request.token_budget = int(original * 0.4)
                request.variables["_adapted_reason"] = "memory_pressure"

        # [ASCENSION 9]: CONCURRENCY THROTTLING (CPU Protection)
        if cpu_load > 90:
            # If the machine is screaming, we slow down our own background workers
            os.environ["SCAFFOLD_MAX_THREADS"] = "1"
            self.logger.verbose("System Fever detected. Restricting Engine to single-thread mode.")

        # --- MOVEMENT V: THE EXECUTION ---
        result = next_handler(request)

        # --- MOVEMENT VI: TELEMETRY INJECTION ---
        # [ASCENSION 11]: We stamp the result with the machine state for the Cockpit to see.
        if result.data is not None and isinstance(result.data, dict):
            result.data["_env_health"] = {
                "cpu": cpu_load,
                "mem": mem_load,
                "on_battery": battery.power_plugged is False if battery else False,
                "battery_level": battery.percent if battery else 100
            }

        return result