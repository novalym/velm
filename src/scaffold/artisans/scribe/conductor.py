# Path: artisans/scribe/conductor.py
# ----------------------------------

import re
from pathlib import Path
from typing import Dict, Type

from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Confirm

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import ScribeRequest, DistillRequest, TransmuteRequest, ArchRequest
from ...help_registry import register_artisan
from ...core.ai.engine import AIEngine
from ...utils import atomic_write
from ...contracts.heresy_contracts import ArtisanHeresy

# --- THE DIVINE SUMMONS OF THE PANTHEON ---
from .base_scribe import BaseScribe
from .form_scribe import FormScribe
from .will_scribe import WillScribe
from .monad_scribe import MonadScribe


# ------------------------------------------

@register_artisan("scribe")
class ScribeConductor(BaseArtisan[ScribeRequest]):
    """
    =================================================================================
    == THE HIGH CONDUCTOR OF PROPHECY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)              ==
    =================================================================================
    @gnosis:title The Gnostic Scribe (`scribe`)
    @gnosis:summary The divine conductor that transmutes a high-level architectural plea
                     into a pure, executable Gnostic scripture (`.scaffold`, `.symphony`, or `.arch`).
    @gnosis:LIF 100,000,000,000,000

    This is the High Priest of Prophecy. It is a divine Gnostic Triage that gazes
    upon the Architect's plea, discerns the required tongue, and summons the correct
    specialist Scribe from its Pantheon to forge the scripture. It is the one true
    gateway between your pure intent and executable architectural law.
    """

    def __init__(self, engine):
        super().__init__(engine)
        # --- THE PANTHEON OF SCRIBES ---
        self.pantheon: Dict[str, Type[BaseScribe]] = {
            "scaffold": FormScribe,
            "symphony": WillScribe,
            "arch": MonadScribe,
        }
        # -------------------------------

    def execute(self, request: ScribeRequest) -> ScaffoldResult:
        self.console.rule(f"[bold magenta]The Scribe Pantheon Awakens[/bold magenta]")

        # --- MOVEMENT I: THE GNOSTIC TRIAGE OF TONGUES ---
        language = request.language.lower()
        ScribeClass = self.pantheon.get(language)
        if not ScribeClass:
            raise ArtisanHeresy(f"The Scribe Pantheon knows not the tongue of '{language}'.",
                                suggestion=f"Known tongues are: {list(self.pantheon.keys())}")

        scribe = ScribeClass(self.engine)
        self.logger.info(
            f"Summoning the [cyan]{scribe.name}[/cyan] to forge a [yellow]'{language}'[/yellow] scripture...")

        # --- MOVEMENT II: THE CONTEXTUAL GAZE ---
        with self.console.status("[dim]Perceiving current reality...[/dim]"):
            distill_req = DistillRequest(source_path=".", strategy="structure", silent=True, non_interactive=True)
            distill_result = self.engine.dispatch(distill_req)
            reality_context = distill_result.data.get("blueprint_content",
                                                      "") if distill_result.success else "<!-- Gaze Averted -->"

        # --- MOVEMENT III: THE COMMUNION WITH THE CORTEX ---
        with self.console.status(
                "[bold magenta]The Scribe is communing with the Cortex... Prophecy is being forged...[/bold magenta]"):
            scripture_content = scribe.prophesy(request.plea, reality_context)
            scripture_content = self._purify_scripture(scripture_content, language)

        # --- MOVEMENT IV: THE LUMINOUS PROCLAMATION & ADJUDICATION ---
        self.console.print(Panel(
            Syntax(scripture_content, language, theme="monokai", line_numbers=True),
            title=f"[bold green]The {scribe.name}'s Prophecy[/bold green]",
            border_style="green"
        ))

        # --- MOVEMENT V: THE INTERACTIVE ALTAR ---
        if request.interactive:
            choices = ["s", "m", "d"]
            prompt = "\n[bold]Your Will?[/] ([green]s[/]ave, [yellow]m[/]aterialize, [red]d[/]iscard): "
            if language == "symphony":
                prompt = "\n[bold]Your Will?[/] ([green]s[/]ave, [yellow]c[/]onduct, [red]d[/]iscard): "
                choices = ["s", "c", "d"]

            action = self.console.input(prompt).lower().strip()

            if action == 's' or action == '':
                return self._save_scripture(request, scripture_content)
            elif action == 'm' or action == 'c':
                return self._materialize_scripture(request, scripture_content)
            else:
                return self.success("The prophecy was returned to the void.")

        return self._save_scripture(request, scripture_content)

    def _purify_scripture(self, raw_content: str, language: str) -> str:
        match = re.search(fr'```(?:{language})?\n(.*?)\n```', raw_content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return raw_content.strip()

    def _save_scripture(self, request: ScribeRequest, content: str) -> ScaffoldResult:
        lang_ext = request.language if request.language != "form" else "scaffold"
        output_path_str = request.output_path or f"{request.plea[:30].replace(' ', '_')}.{lang_ext}"
        target_path = self.project_root / output_path_str

        write_result = atomic_write(target_path, content, self.logger, self.project_root)
        return self.success(
            f"Prophecy inscribed to [cyan]{target_path.name}[/cyan].",
            artifacts=[Artifact(path=target_path, type="file", action=write_result.action_taken.value)]
        )

    def _materialize_scripture(self, request: ScribeRequest, content: str) -> ScaffoldResult:
        import tempfile

        lang_ext = request.language if request.language != "form" else "scaffold"
        with tempfile.NamedTemporaryFile(mode='w+', suffix=f".{lang_ext}", delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(content)
            tmp_path = Path(tmp_file.name)

        try:
            RequestModel = TransmuteRequest if request.language in ["scaffold", "form"] else ArchRequest
            req_key = "path_to_scripture" if request.language in ["scaffold", "form"] else "arch_path"

            self.logger.info(
                f"The Scribe summons the [cyan]{RequestModel.__name__.replace('Request', '')}Artisan[/cyan] to make the prophecy manifest...")

            req_data = {
                req_key: str(tmp_path),
                "project_root": self.project_root,
                "force": False,
                "non_interactive": False,
                "preview": False
            }

            req = RequestModel(**req_data)
            return self.engine.dispatch(req)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()