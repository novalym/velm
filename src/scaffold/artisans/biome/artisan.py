# Path: scaffold/artisans/biome/artisan.py
# ---------------------------------------

import webbrowser
from pathlib import Path

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import BiomeRequest
from ...help_registry import register_artisan
from ...utils.ephemeral_server import launch_ephemeral_server
from .analyst import BiomeAnalyst
from .template import forge_biome_html


@register_artisan("biome")
class BiomeArtisan(BaseArtisan[BiomeRequest]):
    """
    =================================================================================
    == THE BIOME CONDUCTOR (V-Ω-VISUAL-REALITY)                                    ==
    =================================================================================
    Conducts the Rite of Topography.
    1. Summons the BiomeAnalyst to perceive the project's soul.
    2. Summons the HTML Forge to create the Prismatic Lens.
    3. Summons the Ephemeral Server to project the reality into the Architect's browser.
    """

    def execute(self, request: BiomeRequest) -> ScaffoldResult:
        self.logger.info("The Biome Conductor awakens. Preparing to materialize the Codebase Terrain...")

        # 1. The Gnostic Analysis
        with self.console.status("[bold green]Scanning Complexity & Churn...[/bold green]"):
            analyst = BiomeAnalyst(self.project_root)
            gnosis = analyst.analyze()

        if not gnosis['cells']:
            return self.failure("The Gnostic Gaze found only a void. No code to visualize.")

        # 2. The Forging of the Lens
        html_content = forge_biome_html(gnosis)

        # 3. The Projection
        if request.serve:
            self.logger.info("Launching the Ephemeral Holodeck...")
            launch_ephemeral_server(html_content, content_type="text/html")
            return self.success("The Biome has been projected.")

        # Static Output (Optional)
        output_path = self.project_root / "biome.html"
        output_path.write_text(html_content, encoding="utf-8")

        return self.success(
            f"Biome materialized at: {output_path}",
            data={"stats": gnosis['stats']}
        )