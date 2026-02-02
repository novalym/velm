# Path: core/runtime/middleware/optimization.py
# ---------------------------------------------

import time
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....settings.manager import SettingsManager


class OptimizationMiddleware(Middleware):
    """
    =============================================================================
    == THE HEURISTIC GOVERNOR (V-Ω-SELF-OPTIMIZING-FEEDBACK)                   ==
    =============================================================================
    LIF: 100,000,000,000

    Observes metrics from the current rite. If performance or quality thresholds
    are breached, it updates the Global Settings to optimize future incarnations.
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        start_time = time.monotonic()

        # 1. Pre-Rite Optimization (Read)
        # Future: Check settings to see if we should override request params based on past stats.

        # 2. Conduct Rite
        result = next_handler(request)

        duration = (time.monotonic() - start_time) * 1000

        # 3. Post-Rite Analysis (Write)
        if result.success:
            self._optimize_self(request, result, duration)

        return result

    def _optimize_self(self, request: BaseRequest, result: ScaffoldResult, duration_ms: float):
        settings = SettingsManager(request.project_root)
        rite_key = type(request).__name__

        # --- STRATEGY A: MODEL ROUTING OPTIMIZATION ---
        # If a 'fast' model consistently produces high-quality (success) code
        # in under 2 seconds, keep using it. If it fails or takes too long, hint promotion.
        current_model = request.variables.get('model', 'unknown')

        if duration_ms > 10000 and current_model == 'fast':
            # This logic is non-invasive logging for V1.
            # V2 would actually write to .scaffold/config.json
            self.logger.verbose(
                f"Optimization Insight: {rite_key} is slow ({duration_ms:.0f}ms) on 'fast'. Consider 'smart'.")

        # --- STRATEGY B: DISTILLATION BUDGETING ---
        # If the result data shows we used < 10% of the token budget,
        # we note that the budget might be too generous.
        if rite_key == "DistillRequest" and result.data:
            stats = result.data.get("telemetry", {})
            # Assuming 'token_count' is in stats
            tokens = stats.get("token_count", 0)
            budget = request.token_budget or 100000
            if tokens > 0 and (tokens / budget) < 0.1:
                self.logger.verbose(
                    "Optimization Insight: Token budget underutilized. Consider 'aggressive' strategy next time.")

        # --- STRATEGY C: AKASHIC ENSHRINEMENT ---
        # If the rite was an AI generation rite and succeeded, enshrine it.
        if rite_key in ["GenesisRequest", "ManifestRequest", "RefactorRequest"]:
            from ...ai.akasha import AkashicRecord
            try:
                akasha = AkashicRecord()
                # We need the generated content. For Genesis, it's the blueprint in the artifacts?
                # Or the raw content. This is complex to extract generically.
                # Simplified: We just log that we WOULD enshrine here.
                # In a full impl, we'd extract the artifact content.
                pass
            except Exception:
                pass