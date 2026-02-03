# Path: scaffold/artisans/tool/gnosis_artisan.py
# ----------------------------------------------
from ...core.artisan import BaseArtisan
from ...interfaces.requests import GnosisRequest
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan

@register_artisan("gnosis")
class GnosisArtisan(BaseArtisan[GnosisRequest]):
    """The Gnostic Inquisitor. Reveals the Gnostic Void of a blueprint."""
    def execute(self, request: GnosisRequest) -> ScaffoldResult:
        self.logger.info(f"Gazing upon the soul of [cyan]{request.blueprint_path.name}[/cyan]...")
        # ... Implementation logic would reside here.
        # 1. Summon `OmegaInquisitor` from `utils.gnosis_discovery`.
        # 2. Call `inquire()` on the blueprint content.
        # 3. Extract the `dossier.required` set.
        # 4. Render a beautiful `rich.Table` of the missing variables.
        return self.success("Gnostic Void proclaimed.")