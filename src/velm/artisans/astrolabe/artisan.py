# Path: scaffold/artisans/astrolabe/artisan.py
# --------------------------------------------
from pathlib import Path
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import AstrolabeRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy

try:
    from .tui import AstrolabeApp

    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False


@register_artisan("ast-lab")
class AstrolabeArtisan(BaseArtisan[AstrolabeRequest]):
    """
    =============================================================================
    == THE ASTROLABE (V-Ω-AST-EXPLORER)                                        ==
    =============================================================================
    LIF: 10,000,000,000

    Launches an interactive TUI to explore the Abstract Syntax Tree (AST) of a
    scripture using Tree-sitter queries.
    """

    def execute(self, request: AstrolabeRequest) -> ScaffoldResult:
        if not TEXTUAL_AVAILABLE:
            return self.failure("The Astrolabe requires 'textual'. pip install textual")

        target_path = (self.project_root / request.target_file).resolve()
        if not target_path.exists():
            return self.failure(f"Target scripture not found: {target_path}")

        self.logger.info(f"Awakening the Astrolabe for [cyan]{target_path.name}[/cyan]...")

        app = AstrolabeApp(target_path, self.project_root)
        app.run()

        return self.success("Astrolabe session concluded.")


