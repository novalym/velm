# Path: scaffold/artisans/holographic/artisan.py
# ----------------------------------------------

from pathlib import Path
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import HolographicBlueprintRequest
from ...artisans.distill.core.oracle import DistillationOracle
from ...core.cortex.contracts import DistillationProfile
from ...utils import atomic_write
from ...help_registry import register_artisan


@register_artisan("holograph")
class HolographicBlueprintArtisan(BaseArtisan[HolographicBlueprintRequest]):
    """
    =============================================================================
    == THE REALITY SCANNER (V-Ω-DIGITIZER)                                     ==
    =============================================================================
    LIF: 10,000,000,000

    Transmutes a physical directory into a single, portable .scaffold scripture.
    This is the ultimate backup and migration tool.
    """

    def execute(self, request: HolographicBlueprintRequest) -> ScaffoldResult:
        target = (self.project_root / request.target_dir).resolve()
        if not target.exists():
            return self.failure(f"Target sanctum '{target}' is a void.")

        self.logger.info(f"Initiating Holographic Scan of [cyan]{target.name}[/cyan]...")

        # 1. Configure the Oracle for Perfect Recall
        # We use 'faithful' strategy to include all content.
        profile = DistillationProfile(
            strategy="faithful" if request.full_fidelity else "structure",
            token_budget=100_000_000,  # Virtually infinite
            strip_comments=False,  # Preserve original intent
            redact_secrets=False,  # We want a perfect copy, even the dangerous parts (User warned via logs)
            ignore=[".git", ".scaffold", "__pycache__", "node_modules", "*.pyc"]
        )

        # 2. The Gaze of the Oracle
        oracle = DistillationOracle(
            distill_path=target,
            profile=profile,
            verbose=self.engine.logger.is_verbose
        )

        blueprint_content = oracle.distill()

        # 3. The Rite of Inscription
        output_path = self.project_root / request.output_file
        atomic_write(output_path, blueprint_content, self.logger, self.project_root)

        return self.success(
            f"Reality digitized into [bold green]{output_path.name}[/bold green].",
            artifacts=[Artifact(path=output_path, type="file", action="created")]
        )