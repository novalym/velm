# Path: scaffold/artisans/distill/modes.py


from pathlib import Path
from typing import Optional, Set, Tuple, Union
from rich.panel import Panel
from rich.markdown import Markdown
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import PadRequest
from ...core.ai.engine import AIEngine # ★★★ SUMMONS THE NEURAL CORTEX ★★★
from ...utils import atomic_write
from ...logger import Scribe, get_console
from .core.oracle import DistillationOracle

Logger = Scribe("DistillModes")


class ModeHandler:
    """
    =============================================================================
    == THE MODE HANDLER (V-Ω-INTERACTIVE-DELEGATE)                             ==
    =============================================================================
    """

    @staticmethod
    def conduct_pad(engine, source_path: Path, project_root: Path) -> ScaffoldResult:
        """[FACULTY 7] Launches the TUI."""
        from ..pad import PadArtisan
        Logger.info("Summoning the Gnostic Workbench (Distill Pad)...")
        pad_request = PadRequest(pad_name="distill", initial_path=str(source_path), project_root=project_root)
        return PadArtisan(engine).execute(pad_request)

    @staticmethod
    def conduct_check(request, source_path: Path, project_root: Path, output_path: Path, profile) -> ScaffoldResult:
        """[FACULTY 8] Verifies reality matches blueprint."""
        Logger.info("Sentinel's Gaze engaged. Verifying blueprint purity...")

        if not output_path.exists():
            return ScaffoldResult(success=False, message=f"Check failed: '{output_path.name}' does not exist.")

        # Silent oracle run
        oracle = DistillationOracle(
            distill_path=source_path,
            profile=profile,
            silent=True
        )
        in_memory = oracle.distill()
        on_disk = output_path.read_text(encoding='utf-8')

        if in_memory.strip() == on_disk.strip():
            Logger.success("Blueprint is in perfect harmony with reality.")
            return ScaffoldResult(success=True, message="Check passed.")
        else:
            return ScaffoldResult(success=False, message="Check failed: Blueprint is stale.")

    @staticmethod
    def conduct_summary(blueprint: str, project_root: Path, output_path: Optional[str]) -> ScaffoldResult:
        """[THE AI SCRIBE] Asks an AI to summarize the distilled blueprint."""
        Logger.info("The AI Scribe awakens to prophesy a summary...")
        ai = AIEngine.get_instance()
        prompt = (
            "You are an expert technical writer. Analyze this 'distilled' scaffold blueprint, which contains the most relevant files for a specific task. "
            "Generate a concise, insightful, and well-structured README.md summary based on this context. "
            "Focus on the high-level architecture, the purpose of the key components you see, and the likely tech stack. "
            "Do not just list the files. Synthesize their meaning into a coherent narrative. Your output must be pure markdown."
        )

        console = get_console()
        with console.status("[bold magenta]The AI Scribe is reading the project's soul...[/bold magenta]"):
            summary_content = ai.ignite(
                user_query=f"### Distilled Project Blueprint ###\n\n{blueprint}",
                system=prompt,
                model="smart"
            )

        target = project_root / (output_path or "AI_SUMMARY.md")
        atomic_write(target, summary_content, Logger, project_root)

        console.print(Panel(Markdown(summary_content), title="[bold green]AI-Generated Summary[/bold green]"))

        return ScaffoldResult(success=True, message=f"AI Summary Inscribed to {target.name}.")