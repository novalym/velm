# Path: core/runtime/middleware/reflective.py
# -------------------------------------------

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest, RunRequest
from ....interfaces.base import ScaffoldResult
from ....core.ai.engine import AIEngine
from ....contracts.heresy_contracts import ArtisanHeresy


class ReflectiveCritiqueMiddleware(Middleware):
    """
    =============================================================================
    == THE REFLECTIVE CRITIC (V-Ω-AUTOMATED-REVIEW)                            ==
    =============================================================================
    LIF: 50,000,000,000

    Intercepts successful AI generation results.
    Before returning to the user, it asks a lightweight AI model:
    "Did the previous output actually satisfy the user's intent?"

    If the score is low, it triggers an internal retry (Self-Correction).
    """

    CRITIQUE_THRESHOLD = 0.8
    # Only critique these high-value rites
    TARGET_RITES = {'ManifestRequest', 'RefactorRequest', 'ArchitectRequest'}# should we add AgentRequest here?

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        result = next_handler(request)

        # Only critique successful AI operations
        if not result.success or type(request).__name__ not in self.TARGET_RITES:
            return result

        # Skip if explicitly disabled or dry-run
        if request.dry_run or request.variables.get('no_critique'):
            return result

        # Retrieve intent and output
        # This assumes the result.data contains the generated content or path
        # For V1, we simply log the intent to critique.

        intent = getattr(request, 'prompt', 'Unknown Intent')

        # In a real impl, we would extract the generated code string from result.artifacts
        # and send it to the AI.

        self.logger.verbose(f"Reflective Critic is pondering the result of '{intent[:30]}...'")

        # Mock Logic for V1:
        # ai = AIEngine.get_instance()
        # score = ai.ignite(f"Rate this code against intent: {intent}", model="fast")
        # if score < self.CRITIQUE_THRESHOLD:
        #    logger.warn("Critic is unsatisfied. Triggering regeneration...")
        #    return next_handler(request) # Retry logic would go here

        return result