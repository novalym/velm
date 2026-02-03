# Path: artisans/holocron/artisan.py
# ----------------------------------

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import HolocronRequest, DistillRequest  # Import DistillRequest
from ...help_registry import register_artisan


@register_artisan("holocron")
class HolocronArtisan(BaseArtisan[HolocronRequest]):
    """
    =================================================================================
    == THE HOLOCRON (V-Ω-GNOSTIC-ALIAS)                                            ==
    =================================================================================
    @gnosis:title The Holocron (The Gnostic Alias)
    @gnosis:summary A sacred alias for the `distill --format dossier` rite. It is the
                     one true, intuitive gateway to the Dossier of Understanding.
    """

    def execute(self, request: HolocronRequest) -> ScaffoldResult:
        self.logger.info("The Holocron alias awakens. Transmuting plea for the Distill Artisan...")

        # We transmute the HolocronRequest into a DistillRequest, setting the sacred format flag.
        distill_plea = DistillRequest.model_validate(request.model_dump())

        # The core of the alias: set the intent and the format.
        distill_plea.intent = request.entry_point  # Map entry_point to intent
        if not distill_plea.variables:
            distill_plea.variables = {}
        distill_plea.variables['format'] = 'dossier'
        distill_plea.diagnose = True  # Always run AI analysis for holocron

        # We delegate the entire rite to the true master artisan.
        return self.engine.dispatch(distill_plea)