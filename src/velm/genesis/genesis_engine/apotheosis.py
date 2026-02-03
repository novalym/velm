# Path: genesis/genesis_engine/apotheosis.py
# ------------------------------------------
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from rich.panel import Panel
from rich.prompt import Confirm
from rich.status import Status
from rich.text import Text

from ...contracts.heresy_contracts import ArtisanHeresy
from ...interfaces.requests import DistillRequest
from ...logger import Scribe
from ...utils.invocation import invoke_scaffold_command

if TYPE_CHECKING:
    from .engine import GenesisEngine

Logger = Scribe("GenesisApotheosis")


class ApotheosisMixin:
    """
    =================================================================================
    == THE APOTHEOSIS LAYER (V-Ω-REVERSE-GENESIS)                                  ==
    =================================================================================
    Handles rites of existing realities: Distillation and Celestial (Remote) Genesis.
    """

    def _conduct_celestial_rite(self: 'GenesisEngine', url: str):
        """
        [THE CELESTIAL HERALD]
        Summons a remote blueprint (Gist/URL) and materializes it.
        """
        blueprint_path = self.project_root / "scaffold.scaffold"
        gist_match = re.search(r'([a-f0-9]{32,})', url)
        gist_id = gist_match.group(1) if gist_match else None

        with Status("[bold green]Communing with the celestial void...[/bold green]", console=self.console):
            try:
                if gist_id:
                    api_url = f"https://api.github.com/gists/{gist_id}"
                    manifest = requests.get(api_url, timeout=10).json()
                    blueprint_file = next(
                        (f for f in manifest.get('files', {}).values() if f['filename'].endswith('.scaffold')), None)
                    if not blueprint_file:
                        raise ArtisanHeresy("The Gist is a void. No `.scaffold` scripture was found within.")
                    content = requests.get(blueprint_file['raw_url'], timeout=10).text
                    source_name = blueprint_file['filename']
                else:
                    content = requests.get(url, timeout=10).text
                    source_name = url.split('/')[-1]
            except requests.RequestException as e:
                raise ArtisanHeresy(f"Celestial Communion Failed: {e}")

        blueprint_path.write_text(content, encoding='utf-8')

        proclamation = Text.assemble(
            ("The celestial blueprint ", "white"),
            (f"'{source_name}'", "cyan"),
            (" has been made manifest at ", "white"),
            (f"'{blueprint_path.name}'.", "cyan")
        )
        self.console.print(
            Panel(proclamation, title="[bold green]Celestial Weaving Complete[/bold green]", border_style="green"))

        if not self.cli_args.non_interactive:
            if Confirm.ask("\n[bold question]Shall this celestial reality be materialized now?[/bold question]",
                           default=True):
                self.console.rule("[bold magenta]Rite of Immediate Materialization[/bold magenta]")
                result = invoke_scaffold_command(
                    command_args=['.'],
                    non_interactive=True,
                    cwd=str(self.project_root)
                )
                self.console.print(result.output)

    def _conduct_apotheosis_rite(self: 'GenesisEngine'):
        """
        [THE GOD-ENGINE OF REVERSE GENESIS]
        Transmutes an existing directory structure back into a Blueprint.
        """
        from ...artisans.distill import DistillArtisan

        # 1. The Gnostic Warning
        if (self.project_root / "scaffold.scaffold").exists() and not self.cli_args.force:
            self.console.print(Panel(
                Text.assemble(
                    ("A `scaffold.scaffold` scripture already exists in this reality.\n\n", "yellow"),
                    ("Proceeding with distillation will ", "white"),
                    ("transfigure (overwrite)", "bold red"), (" its current soul.", "white")
                ), title="[yellow]Prophecy of Transfiguration[/yellow]"
            ))

        # 2. The Vow of Silence Check
        # We assume the Architect intends to distill if they passed --distill or if they are interactive.
        # If they are running --quick in a dirty dir, we might skip this (handled in _offer_distillation_or_genesis)
        # But if we are HERE, we are committed to the attempt.

        if not self.cli_args.force and not self.cli_args.distill:
            self.console.print(Panel(Text.assemble(
                ("This reality is not a void. A Great Work is already in progress.\n\n", "white"),
                ("The ", "white"), ("Oracle of Perception", "bold magenta"),
                (" can be summoned to transcribe this project's existing soul...", "white")),
                title="[magenta]The Path of Apotheosis[/magenta]", border_style="magenta"))

            if not Confirm.ask("[bold question]Shall the Rite of Distillation begin?[/bold question]", default=True):
                raise ArtisanHeresy("The Rite of Apotheosis was stayed by the Architect's will.", exit_code=0)

        Logger.info("Summoning the DistillArtisan for the Rite of Apotheosis...")

        # 3. The Forging of the Plea
        distill_plea = DistillRequest(
            source_path=str(self.project_root),
            output="scaffold.scaffold",
            llm_optimized=False,
            form_only=False,
            force=self.cli_args.force,
            verbosity=1 if self.cli_args.verbose else (-1 if self.cli_args.silent else 0),
            silent=self.cli_args.silent,
            non_interactive=self.cli_args.non_interactive,
            ignore=getattr(self.cli_args, 'ignore', []),
            project_root=self.project_root
        )

        # 4. The Divine Delegation
        distill_result = self.engine.dispatch(distill_plea)

        if not distill_result.success:
            raise ArtisanHeresy(
                "The Rite of Apotheosis failed during the final distillation.",
                child_heresy=distill_result.heresies[0] if distill_result.heresies else None
            )

    def _offer_distillation_or_genesis(self: 'GenesisEngine'):
        """
        [THE PATH OF APOTHEOSIS - HEALED]
        The internal check called by conduct() to see if we should distill.
        """
        Logger.info("Path of Apotheosis perceived. A reality is already manifest.")

        # The Vow of Silence (The Fix)
        # If automating, we assume the user knows what they are doing (e.g. adding scaffold to existing project)
        # and we skip distillation to avoid blocking.
        if self.cli_args.non_interactive or self.cli_args.quick:
            Logger.verbose("Non-interactive mode. Bypassing Distillation offer. Proceeding with Genesis.")
            return

        # Delegate to the main apotheosis logic
        self._conduct_apotheosis_rite()
        # If apotheosis succeeds, we exit.
        sys.exit(0)