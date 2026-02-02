# Path: scaffold/artisans/muse/artisan.py
# -------------------------------------

from pathlib import Path
from rich.panel import Panel
from rich.table import Table
from typing import Optional, Tuple, Union
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import MuseRequest
from ...help_registry import register_artisan
from ...utils import atomic_write
from .analyst import BehavioralAnalyst


@register_artisan("muse")
class MuseArtisan(BaseArtisan[MuseRequest]):
    """
    =============================================================================
    == THE PRESCIENT MUSE (V-Ω-PREDICTIVE-SCAFFOLDING)                         ==
    =============================================================================
    Calculates the probability of your next move and offers to perform it.
    """

    def execute(self, request: MuseRequest) -> ScaffoldResult:
        context_file = request.context_file

        # If no context provided, find the most recently modified file in reality
        if not context_file:
            context_file = self._find_latest_file()
            if not context_file:
                return self.failure("The Muse cannot see. No recent files found.")
            self.logger.info(f"The Muse perceives you last touched: [cyan]{context_file}[/cyan]")

        analyst = BehavioralAnalyst(self.project_root)
        prophecies = analyst.prophesy_next(str(context_file), request.threshold)

        if not prophecies:
            return self.success("The Muse is silent. No clear patterns detected yet.")

        # Display Prophecies
        table = Table(title="[bold purple]Prophecies of the Next Step[/bold purple]")
        table.add_column("Predicted Artifact", style="cyan")
        table.add_column("Probability", style="magenta")
        table.add_column("Basis", style="dim")

        for p in prophecies:
            table.add_row(p['pattern'], f"{p['probability']:.1%}", p['reason'])

        self.console.print(table)

        # Auto-Drafting Logic (The Ghost Writer)
        # If we have a very high confidence prediction, we can propose a file.
        # Constructing the *path* from the pattern requires context awareness (mirroring the source).

        best_prediction = prophecies[0]
        if request.auto_draft or best_prediction['probability'] > 0.8:
            draft_path = self._infer_path(context_file, best_prediction['pattern'])
            if draft_path and not draft_path.exists():
                self.console.print(f"\n[bold green]✨ Ghost-Writing Draft:[/bold green] {draft_path}")
                # We create an empty file or basic template
                content = f"# Draft: {best_prediction['pattern']}\n# Auto-suggested by Scaffold Muse\n"
                atomic_write(draft_path, content, self.logger, self.project_root)
                return self.success(f"Drafted {draft_path.name}",
                                    artifacts=[Artifact(path=draft_path, type='file', action='created')])

        return self.success("Prophecy proclaimed.")

    def _find_latest_file(self) -> Optional[Path]:
        """Finds the most recently modified source file."""
        try:
            # Exclude .git and hidden dirs
            files = [
                p for p in self.project_root.rglob("*")
                if p.is_file() and not any(part.startswith(".") for part in p.parts)
            ]
            if not files: return None
            return max(files, key=lambda f: f.stat().st_mtime).relative_to(self.project_root)
        except:
            return None

    def _infer_path(self, context_path: Union[str, Path], pattern: str) -> Optional[Path]:
        """
        Infers the concrete path for a pattern based on the context file.
        E.g. src/auth/user_model.py + *service.py -> src/auth/user_service.py
        """
        ctx = Path(context_path)
        parent = ctx.parent
        stem = ctx.stem

        # Remove the 'type' from the stem if possible (user_model -> user)
        clean_stem = stem.replace("_model", "").replace("_controller", "").replace("Model", "")

        target_suffix = pattern.replace("*", "")  # e.g. _service.py
        new_filename = f"{clean_stem}{target_suffix}"

        return self.project_root / parent / new_filename