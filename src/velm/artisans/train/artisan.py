# scaffold/artisans/train/artisan.py

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import TrainRequest
from ...help_registry import register_artisan
from ...forge.conductor import ForgeConductor


@register_artisan("train")
class TrainArtisan(BaseArtisan[TrainRequest]):
    """
    =============================================================================
    == THE GNOSTIC FORGE (V-Ω-SELF-IMPROVEMENT)                                ==
    =============================================================================
    Conducts the Ouroboros Protocol. Trains a custom AI model on the current
    project's codebase, documentation, and architectural patterns.
    """

    def execute(self, request: TrainRequest) -> ScaffoldResult:
        conductor = ForgeConductor(self.project_root)

        try:
            conductor.conduct_training_rite(request)
            return self.success(f"Model '{request.output_model_name}' training process concluded.")
        except Exception as e:
            return self.failure(f"The Forge faltered: {e}")