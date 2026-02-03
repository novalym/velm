# Path: scaffold/core/runtime/middleware/budget.py
# ------------------------------------------------

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy


class BudgetMiddleware(Middleware):
    """
    =============================================================================
    == THE GUARDIAN OF THE TREASURY (V-Ω-COST-CONTROL)                         ==
    =============================================================================
    Enforces token limits on Generative Rites.
    """

    AI_RITES = {'GenesisRequest', 'RefactorRequest', 'AnalyzeRequest'}

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        request_type = request.__class__.__name__

        # Only guard costly rites
        if request_type in self.AI_RITES:
            # Load Budget Gnosis
            # (In a real impl, this would read from settings/state)
            from ....settings.manager import SettingsManager
            settings = SettingsManager(request.project_root)

            budget_limit = settings.get("ai.budget_limit")  # e.g., 100000 tokens
            current_usage = settings.get("ai.usage_session", 0)

            # Heuristic Check (Real counting happens in the Artisan)
            if budget_limit and current_usage >= budget_limit:
                if not request.force:
                    raise ArtisanHeresy(
                        "Budget Exhausted: The Treasury is empty.",
                        suggestion="Increase `ai.budget_limit` in settings or use `--force` to override."
                    )

        return next_handler(request)