# Path: artisans/lfg/artisan.py
# -----------------------------

from pathlib import Path
from rich.panel import Panel
from rich.syntax import Syntax

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import LFGRequest
from ...help_registry import register_artisan
from ...parser_core.lfg_builder.facade import LFGEngine
from ...utils import atomic_write, launch_ephemeral_server


@register_artisan("lfg")
class LFGArtisan(BaseArtisan[LFGRequest]):
    """
    =================================================================================
    == THE LOGIC VISUALIZER (V-Ω-X-RAY-VISION)                                   ==
    =================================================================================
    LIF: 10,000,000,000

    Generates Mermaid.js flowcharts from Blueprints OR Code.
    Reveals the invisible currents of logic.
    """

    def execute(self, request: LFGRequest) -> ScaffoldResult:
        target = (self.project_root / request.target).resolve()
        if not target.exists():
            return self.failure(f"Target void: {target}")

        self.logger.info(f"The Cartographer gazes upon [cyan]{target.name}[/cyan]...")

        engine = LFGEngine(self.project_root)
        mermaid_code = ""

        # Gnostic Triage
        if request.mode == "blueprint" or target.suffix in ['.scaffold', '.symphony', '.arch']:
            mermaid_code = engine.generate_blueprint_lfg(target)
        elif request.mode == "codebase" or target.suffix == '.py':
            mermaid_code = engine.generate_codebase_lfg(target)
        else:
            return self.failure("Unsupported file type for LFG generation.")

        # Proclaim
        self.console.print(Panel(
            Syntax(mermaid_code, "mermaid", theme="monokai"),
            title=f"[bold magenta]Logic Flow: {target.name}[/bold magenta]",
            border_style="magenta"
        ))

        # Inscribe (if requested)
        artifacts = []
        if request.output_path:
            out = self.project_root / request.output_path
            atomic_write(out, mermaid_code, self.logger, self.project_root)
            artifacts.append(Artifact(path=out, type="file", action="created"))

        return self.success("Logic Flow Graph generated.", artifacts=artifacts)