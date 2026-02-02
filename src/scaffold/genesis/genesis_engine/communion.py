# Path: scaffold/genesis/genesis_engine/communion.py
# --------------------------------------------------

import argparse
import asyncio
import getpass
import sys
from pathlib import Path
from typing import Tuple, Dict, List, Any, Optional, TYPE_CHECKING

from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.status import Status
from rich.text import Text

# --- THE DIVINE SUMMONS ---
from ..genesis_profiles import PROFILES, QUICK_START_PROFILE_NAME
from ..genesis_orchestrator import GenesisDialogueOrchestrator
from ...artisans.transfigure import TransfigureArtisan
from ...contracts.data_contracts import ScaffoldItem, GnosticDossier
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.blueprint_scribe import BlueprintScribe
from ...utils.invocation import invoke_scaffold_command
from ...logger import Scribe

if TYPE_CHECKING:
    from .engine import GenesisEngine
    from ...parser_core.parser import ApotheosisParser

Logger = Scribe("GenesisCommunion")

# The Sacred Tuple of Creation
GnosticDowry = Tuple[Dict[str, Any], List[ScaffoldItem], List[str], 'ApotheosisParser']


class CommunionMixin:
    """
    =================================================================================
    == THE VOICE OF THE GENESIS ENGINE (V-Ω-COMMUNION-LAYER-ULTIMA)                ==
    =================================================================================
    LIF: 10,000,000,000,000

    This mixin endows the `GenesisEngine` with the faculty of speech and interaction.
    It handles the Gnostic Triage between:
    1.  **The Sacred Dialogue** (Interactive Q&A).
    2.  **The Gnostic Pad** (TUI Dashboard).
    3.  **The Manual Rite** (Editor-based).
    4.  **The Force Bypass** (Silent Automation).
    """

    def _conduct_dialogue_rite(self: 'GenesisEngine') -> Optional[GnosticDowry]:
        """
        [THE WISE DIPLOMAT]
        Conducts the standard interactive Q&A flow via the Orchestrator.
        """
        Logger.info("The Gnostic Diplomat awakens its mind...")

        # 1. Gather Preliminary Gnosis (Prophecy)
        prophecy = self._gaze_upon_the_cosmos()

        # 2. Merge CLI Overrides (The Architect's Command)
        cli_vars = {}
        if hasattr(self.cli_args, 'set') and self.cli_args.set:
            cli_vars = {k: v for k, v in (s.split('=', 1) for s in self.cli_args.set)}

        # 3. Forge Initial Gnosis
        initial_gnosis = {**prophecy.defaults, **cli_vars}
        Logger.success("A preliminary Gnostic context has been forged.")

        # --- MOVEMENT I: THE GNOSTIC TRIAGE (FORCE BYPASS) ---
        # [ASCENSION 1] The Force Bypass
        if self.cli_args.force:
            Logger.info("Force Directive perceived. Bypassing Sacred Dialogue. Relying on Prophecy.")
            # We assume the initial gnosis + prophecy is sufficient.
            # We must still ensure a project type is selected.
            if 'project_type' not in initial_gnosis:
                initial_gnosis['project_type'] = 'generic'

            final_gnosis = initial_gnosis
        else:
            # --- MOVEMENT II: THE SACRED DIALOGUE ---
            # We summon the specialist Orchestrator to conduct the interview.
            orchestrator = GenesisDialogueOrchestrator(
                parent_engine=self,
                prophecy=prophecy,
                final_gnosis=initial_gnosis
            )

            is_pure, final_gnosis = orchestrator.conduct_cinematic_symphony()

            if not is_pure:
                # The Architect chose to abort during the dialogue.
                raise ArtisanHeresy(
                    "The Rite of Genesis was stayed by the Architect's will during the Sacred Dialogue.",
                    exit_code=0)

        # --- MOVEMENT III: THE SELECTION OF THE WEAVER ---
        # The Diplomat performs its Gaze upon the result to find the chosen path.
        chosen_archetype_name = final_gnosis.get('project_type', 'generic')

        # [ASCENSION 8] The Archetype Adjudicator
        archetype_info = PROFILES.get(chosen_archetype_name)
        if not archetype_info:
            # Fallback for custom/unknown types to generic
            Logger.warn(f"Archetype '{chosen_archetype_name}' unknown. Falling back to 'generic'.")
            archetype_info = PROFILES.get('generic')
            if not archetype_info:
                raise ArtisanHeresy(
                    f"A catastrophic paradox: The Grimoire holds no Gnosis for '{chosen_archetype_name}' or 'generic'.")

        Logger.info("Communion complete. Bestowing final Gnosis upon the Master Weaver...")

        # --- MOVEMENT IV: THE MASTER WEAVE ---
        # We pass the final gnosis as overrides to the archetype weaving process.
        dowry = self._conduct_master_weave(
            archetype_info,
            final_gnosis,
            overrides=final_gnosis
        )

        Logger.success("The Master Weaver's proclamation has been received. The Gnostic Dowry is whole.")
        return dowry

    def _conduct_pad_rite(self: 'GenesisEngine') -> Optional[GnosticDowry]:
        """
        [THE CONDUCTOR OF THE GNOSTIC PAD]
        Summons the TUI (`GenesisPad`) for a rich, interactive genesis.
        """
        with self.logger.indent("Rite of the Gnostic Pad"):
            try:
                # Lazy import to prevent circular dependencies at module level
                from ...studio.pads.pad_launcher import PAD_GRIMOIRE, _adjudicate_dependencies
                from ...studio.pads.genesis_pad import GenesisPad

                # [ASCENSION 11] JIT Dependency Check
                pad_gnosis = PAD_GRIMOIRE['genesis']
                _adjudicate_dependencies(pad_gnosis.get("dependencies", []))

                self.logger.info("Summoning the Altar of Genesis for a sacred, interactive communion...")

                # [ASCENSION 5] The Pad Resilience
                pad = GenesisPad()

                # We run the app and wait for it to exit with a result (the Gnosis).
                final_gnosis_from_pad = pad.run()

                if not final_gnosis_from_pad:
                    self.logger.warn("The Architect has stayed the Rite of Genesis from within the Pad.")
                    return None

                self.logger.success("Communion with the Altar of Genesis is complete. Final Gnosis has been received.")

                # Merge with CLI overrides (Pad output is the final will)
                final_unified_gnosis = final_gnosis_from_pad

                # Determine Archetype
                profile_name = final_unified_gnosis.get('project_type')
                if not profile_name:
                    raise ArtisanHeresy("The Gnostic Pad returned a void soul (no 'project_type' Gnosis).")

                archetype_info = PROFILES.get(profile_name)
                if not archetype_info:
                    archetype_info = PROFILES.get('generic')

                # Inject the Pad's gnosis as overrides
                archetype_info['gnosis_overrides'] = final_unified_gnosis

                # Delegate to the standard archetype weaver
                return self._conduct_archetype_rite(archetype_info)

            except ImportError as e:
                raise ArtisanHeresy(
                    "The Gnostic Pad requires its divine allies to be manifest.",
                    suggestion=f"Speak the sacred plea: `pip install \"scaffold-cli[studio]\"` or `pip install {e.name}`",
                    child_heresy=e
                ) from e
            except Exception as e:
                raise ArtisanHeresy("A catastrophic paradox shattered the communion with the Gnostic Pad.",
                                    child_heresy=e) from e

    def _conduct_manual_rite(self: 'GenesisEngine') -> None:
        """
        [THE GOD-ENGINE OF GUIDED CREATION]
        Allows the user to manually edit the blueprint before generation.
        This rite does not return a Dowry; it manages its own materialization cycle.
        """
        from ...constants import README_FILENAME

        blueprint_path = self.project_root / "scaffold.scaffold"
        initial_content = ""

        self.console.rule("[bold magenta]Rite of the Artisan's Hand: Manual Inscription[/bold magenta]")

        # --- MOVEMENT I: THE GAZE OF PROPHETIC INTENT (README) ---
        readme_path = self.project_root / README_FILENAME

        # [ASCENSION 9] Interactive Sentinel
        if readme_path.is_file() and not self.cli_args.non_interactive:
            if Confirm.ask(
                    f"[bold question]A `{README_FILENAME}` was perceived. Distill its soul as the initial scripture?[/bold question]"):
                distill_form_only = not Confirm.ask(
                    "[bold question]Include the full content of the README in the blueprint?[/bold question]",
                    default=True)

                with Status("[cyan]Distilling the README's soul with the One True Scribe...[/cyan]",
                            console=self.console):
                    try:
                        # [ASCENSION 10] Encoding Guard & Size Limit
                        if readme_path.stat().st_size < 1024 * 100:  # 100KB limit
                            readme_content = readme_path.read_text(encoding='utf-8',
                                                                   errors='replace') if not distill_form_only else None
                            readme_item = ScaffoldItem(path=Path(README_FILENAME), is_dir=False, content=readme_content)

                            scribe = BlueprintScribe(project_root=self.project_root, alchemist=self.alchemist)
                            initial_content = scribe.transcribe(
                                items=[readme_item],
                                commands=[],
                                gnosis={'project_name': self.project_root.name, 'author': getpass.getuser()},
                                rite_type='genesis'
                            )
                            self.logger.success("README soul distilled successfully.")
                        else:
                            self.logger.warn("README is too vast for distillation. Using empty template.")
                    except Exception as e:
                        self.logger.warn(f"A minor paradox occurred while distilling the README's soul: {e}")

        # --- MOVEMENT II: THE GAZE OF THE FORGE (TEMPLATES) ---
        if not initial_content and not self.cli_args.non_interactive:
            from ..genesis_profiles import PROFILES
            available_archetypes = list(PROFILES.keys())

            choice = Prompt.ask(
                "[bold question]Select a base archetype to start from (or 'blank')[/bold question]",
                choices=["blank"] + available_archetypes,
                default="blank"
            )

            if choice != "blank":
                # Fetch content
                archetype_info = PROFILES[choice]
                import importlib.resources as pkg_resources
                # Split path "package:resource"
                if ":" in archetype_info["archetype_path"]:
                    pkg, res = archetype_info["archetype_path"].split(":")
                    initial_content = pkg_resources.files(pkg).joinpath(res).read_text(encoding='utf-8')
                else:
                    initial_content = Path(archetype_info["archetype_path"]).read_text(encoding='utf-8')

        # [ASCENSION 3] The Celestial Fallback (Void Scripture)
        if not initial_content:
            initial_content = (
                f"# == Gnostic Blueprint for: {self.project_root.name}\n"
                f"# == Forged by: {getpass.getuser()}\n"
                f"# Speak the language of Form. The God-Engine awaits your will.\n\n"
                f"$$ project_name = \"{self.project_root.name}\"\n\n"
                f"src/main.py :: \"print('Hello World')\"\n"
            )

        # --- MOVEMENT III: THE RITE OF INTERACTIVE INSCRIPTION ---
        self.logger.info("Summoning the `transfigure` artisan for Interactive Inscription...")

        blueprint_path.write_text(initial_content, encoding='utf-8')

        from ...interfaces.requests import TransfigureRequest

        transfigure_req = TransfigureRequest(
            path_to_scripture=str(blueprint_path.relative_to(self.project_root)),
            interactive=True,
            project_root=self.project_root,
            # Default values for safety
            append=False, prepend=False, create_if_void=False, guardian=False,
            force=False, dry_run=False
        )

        try:
            transfigure_artisan = TransfigureArtisan(self.engine)
            transfigure_artisan.execute(transfigure_req)

            # Check if content changed
            final_scripture = blueprint_path.read_text(encoding='utf-8')
            if not final_scripture.strip() or final_scripture.strip() == initial_content.strip():
                self.logger.warn(
                    "The Architect's will was a void or was unchanged. The Rite of Manual Genesis is gracefully stayed.")
                if blueprint_path.exists(): blueprint_path.unlink()
                return

            self.logger.success(
                f"The Architect's will has been inscribed. Scripture forged at: [cyan]{blueprint_path.name}[/cyan]")

        except ArtisanHeresy as e:
            if blueprint_path.exists(): blueprint_path.unlink()
            raise ArtisanHeresy("The communion with the native editor failed or was stayed.", child_heresy=e,
                                exit_code=1)

        # --- MOVEMENT IV: THE GAZE OF THE GNOSTIC MENTOR (LINT) ---
        if not self.cli_args.non_interactive:
            if Confirm.ask(
                    "\n[bold question]Shall I awaken the Gnostic Mentor to adjudicate your new scripture?[/bold question]",
                    default=True):
                self.console.rule("[bold yellow]The Gnostic Mentor's Gaze[/bold yellow]")

                lint_result = invoke_scaffold_command(
                    command_args=[str(blueprint_path), '--lint', '--preview'],
                    non_interactive=True,
                    cwd=self.project_root
                )
                self.console.print(lint_result.output)

                if lint_result.exit_code != 0:
                    self.logger.error("The Mentor's Gaze perceived critical heresies. The symphony cannot proceed.")
                    if Confirm.ask("[bold red]Abort?[/bold red]", default=True):
                        return

        # --- MOVEMENT V: THE FINAL ADJUDICATION & MATERIALIZATION ---
        if not self.cli_args.non_interactive:
            if Confirm.ask(
                    "\n[bold question]This manually forged reality appears pure. Shall it be materialized now?[/bold question]",
                    default=True):
                self.console.rule("[bold magenta]Rite of Immediate Materialization[/bold magenta]")

                # Invoke Genesis on the file we just made
                result = invoke_scaffold_command(
                    command_args=[str(blueprint_path)],
                    non_interactive=True,
                    cwd=self.project_root
                )

                if result.exit_code == 0:
                    self.logger.success("The new reality has been made manifest.")
                    self.console.print(result.output)
                else:
                    self.logger.error("A paradox occurred during the final Rite of Materialization.")
                    self.console.print(result.output)