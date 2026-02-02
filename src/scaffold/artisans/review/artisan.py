# Path: artisans/review/artisan.py
# --------------------------------

import subprocess
from typing import List, Dict, Any

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ReviewRequest
from ...help_registry import register_artisan
from ...core.ai.engine import AIEngine
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.cortex.engine import GnosticCortex


@register_artisan("review")
class ReviewArtisan(BaseArtisan[ReviewRequest]):
    """
    =================================================================================
    == THE SENTINEL'S TRIBUNAL (V-Ω-AI-GATEKEEPER)                                 ==
    =================================================================================
    LIF: 10,000,000,000

    An AI-driven code review agent. It judges staged changes against the
    laws of Security, Architecture, and Performance.
    """

    def execute(self, request: ReviewRequest) -> ScaffoldResult:
        self.logger.info("The Tribunal convenes to judge the pending commit...")

        # 1. Gather Evidence (Staged Diff)
        diff = self._get_staged_diff()
        if not diff:
            return self.success("No staged changes found. The Tribunal rests.")

        # 2. Summon Context (Cortex)
        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()
        # Simple context summary
        context_summary = f"Project contains {len(memory.inventory)} files."

        # 3. Forge the Indictment (Prompt)
        prompt = self._forge_prompt(diff, context_summary, request.socratic_mode)

        # 4. The Judgment (AI Inference)
        ai = AIEngine.get_instance()
        self.console.print("[dim]The AI Sentinel is reading the diff...[/dim]")

        verdict = ai.ignite(
            user_query=prompt,
            system="You are a Senior Software Architect and Security Auditor.",
            model="smart"
        )

        # 5. The Proclamation
        from rich.markdown import Markdown
        from rich.panel import Panel

        title = "[bold green]Socratic Guidance[/bold green]" if request.socratic_mode else "[bold red]Code Tribunal Verdict[/bold red]"
        border = "green" if request.socratic_mode else "red"

        self.console.print(Panel(Markdown(verdict), title=title, border_style=border))

        return self.success("Adjudication complete.")

    def _get_staged_diff(self) -> str:
        try:
            return subprocess.check_output(
                ["git", "diff", "--staged"], cwd=self.project_root, text=True
            ).strip()
        except subprocess.CalledProcessError:
            raise ArtisanHeresy("Not a git repository.")

    def _forge_prompt(self, diff: str, context: str, socratic: bool) -> str:
        base = (
            f"Review the following git diff.\n"
            f"Context: {context}\n\n"
            f"Focus on:\n1. Security Vulnerabilities\n2. Architectural Integrity\n3. Performance bottlenecks.\n"
            f"Ignore strict linting/formatting issues.\n\n"
            f"Diff:\n```diff\n{diff}\n```\n"
        )

        if socratic:
            return base + (
                "\nProvide your review in 'Socratic Mode'. Do not just point out errors. "
                "Ask the user guiding questions that lead them to discover the flaws themselves. "
                "Be a wise mentor, not a critic."
            )
        else:
            return base + (
                "\nProvide a rigorous, bulleted list of issues. Be concise and ruthless. "
                "If the code is good, approve it explicitly."
            )