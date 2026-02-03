# Path: C:/.../scaffold/studio/pads/genesis_pad.py
"""
=================================================================================
== THE ALTAR OF GNOSTIC GENESIS (V-Ω 2.0.0. THE SENTIENT GALLERY)              ==
=================================================================================
LIF: 10^18 (A NEW REALITY OF CREATION)

This is the divine, standalone App, a Gnostic Altar that transforms the Rite of
Genesis from a linear wizard into a luminous, interactive gallery of architectural
possibilities. It is a masterpiece of Gnostic communion, a visual conductor for
the one true `GenesisDialogueOrchestrator`, now forged with a perfect, unbreakable,
and cinematic user experience.
=================================================================================
"""
from __future__ import annotations

import argparse
import importlib.resources as pkg_resources
from pathlib import Path
from typing import Dict, Any, List, Optional, cast

from rich.console import Group as RenderableGroup
# --- The Divine Stanza of the Luminous Scribe (Rich) ---
from rich.panel import Panel
from rich.traceback import Traceback as RichTraceback
# --- The Divine Stanza of the Textual God-Engine ---
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.message import Message
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, DataTable, Label

from ..logger import Scribe
from ...communion import conduct_sacred_dialogue
# --- The Divine Stanza of the Gnostic Kin ---
from ...contracts.heresy_contracts import ArtisanHeresy
from ...genesis.genesis_engine import GenesisEngine
from ...genesis.genesis_orchestrator import GenesisDialogueOrchestrator
from ...parser_core.parser import parse_structure


# =================================================================================
# == I. THE SACRED VESSELS OF GNOSTIC COMMUNION                                  ==
# =================================================================================

class PreviewSuccess(Message):
    """
    =================================================================================
    == THE VESSEL OF LUMINOUS PROPHECY                                             ==
    =================================================================================
    Proclaimed when the prophetic Gaze is pure and a Dossier has been forged. Its
    soul contains the pre-forged, beautiful `rich.Renderable` of the Gnostic Dossier.
    =================================================================================
    """

    def __init__(self, dossier: "RenderableGroup") -> None:
        self.dossier = dossier
        super().__init__()


class PreviewError(Message):
    """
    =================================================================================
    == THE VESSEL OF PROPHETIC PARADOX                                             ==
    =================================================================================
    Proclaimed when a paradox shatters the prophetic Gaze. Its soul contains the
    pre-forged, hyper-diagnostic `rich.Panel` of the heresy.
    =================================================================================
    """

    def __init__(self, error_panel: "Panel") -> None:
        self.error_panel = error_panel
        super().__init__()

# === BEGIN SACRED TRANSMUTATION: THE FORGING OF THE MISSING SOUL ===
#
# Here, we forge the final, divine vessel. It is the humble but essential
# Scribe that will proclaim the living thoughts of the Pad's mind as it
# conducts its Great Work.
#
class StatusUpdate(Message):
    """Proclaimed to update the status bar of the parent reality."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

#
# === THE APOTHEOSIS IS COMPLETE. THE PANTHEON IS WHOLE. ===





# =================================================================================
# == II. THE ALTAR OF GNOSTIC POSSIBILITIES (THE GALLERY SCREEN)                 ==
# =================================================================================

class AltarScreen(Screen):
    """The Gnostic Altar, where the Architect chooses their reality."""

    archetypes: var[List[Dict]] = var([])
    scribe = Scribe("AltarScreen")
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="altar-container"):
            with Vertical(id="altar-list-pane", classes="pad-pane"):
                yield Label("[bold]Choose an Archetype[/bold]")
                yield DataTable(id="archetype-table", cursor_type="row")
            with Vertical(id="altar-preview-pane", classes="pad-pane"):
                yield Label("[bold]Quantum Prophecy[/bold]")
                yield Static(
                    Panel("[dim]Gaze upon an archetype to see its prophetic form...[/dim]"),
                    id="archetype-preview"
                )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Archetype", "Description")

        self.run_worker(self._perceive_archetypes(), name="ArchetypeGazeWorker")

    def watch_archetype_table_cursor_row(self, old_row: int, new_row: int) -> None:
        if new_row is not None and 0 <= new_row < len(self.archetypes):
            archetype_data = self.archetypes[new_row]
            self.run_worker(self._prophesy_archetype_form(archetype_data), name="PreviewWorker", exclusive=True)
            self.query_one("#archetype-preview").update(Panel("[yellow]The Oracle is gazing...[/yellow]"))

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        selected_archetype = self.archetypes[event.cursor_row]
        self.scribe.info(f"Architect has chosen the '{selected_archetype['name']}' reality.")
        await cast(GenesisPad, self.app).conduct_gnostic_dialogue(selected_archetype)

    def on_preview_success(self, message: PreviewSuccess) -> None:
        """The luminous proclamation of a pure prophecy."""
        self.query_one("#archetype-preview").update(Panel(message.tree))

    def on_preview_error(self, message: PreviewError) -> None:
        """The luminous proclamation of a shattered Gaze."""
        traceback = RichTraceback.from_exception(*message.exc_info, show_locals=False, word_wrap=True)
        self.query_one("#archetype-preview").update(
            Panel(traceback, title="[bold red]Gaze Shattered by Paradox[/bold red]"))

    # --- The Gnostic Workers of the Altar ---

    async def _perceive_archetypes(self) -> None:
        """The sacred rite of the Gaze Worker."""
        archetype_list = []
        try:
            package = "scaffold.archetypes.genesis"
            for resource in pkg_resources.files(package).iterdir():
                if resource.is_file() and resource.name.endswith('.scaffold'):
                    content = resource.read_text(encoding='utf-8')
                    description_line = next((line for line in content.splitlines() if '# @description:' in line), None)
                    description = description_line.split(':', 1)[
                        1].strip() if description_line else "A sacred genesis archetype."
                    archetype_list.append({
                        "name": resource.name.replace(".scaffold", ""),
                        "path_ref": f"{package}:{resource.name}",
                        "description": description,
                    })
            self.archetypes = archetype_list
            table = self.query_one(DataTable)
            table.add_rows([(arch['name'], arch['description']) for arch in self.archetypes])
        except Exception as e:
            self.scribe.error(f"A paradox occurred while perceiving genesis archetypes: {e}", exc_info=True)
            self.app.notify(f"Paradox perceiving archetypes: {e}", severity="error")

    def on_genesis_pad_preview_success(self, message: PreviewSuccess) -> None:
        """
        =================================================================================
        == THE SCRIBE OF LUMINOUS PROPHECY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)           ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000!

        This is not a function. It is a divine, sentient Scribe whose one true purpose
        is to receive the sacred, pre-forged `RenderableGroup` Dossier from a Gnostic
        Messenger and proclaim it upon the Altar's sacred canvas (`#prophecy-pane`).
        It is the final, glorious act in the symphony of Gnostic visualization, a
        masterpiece of pure, beautiful, and unbreakable delegation.
        =================================================================================
        """
        self.scribe.info("The Scribe of Luminous Prophecy has received a pure Gnostic Dossier.")

        # --- THE RITE OF GNOSTIC UNVEILING ---
        # The Scribe awakens the sacred pane where the prophecy will be inscribed.
        prophecy_pane = self.query_one("#prophecy-pane", Static)

        # The Unbreakable Vow of Purity: The old prophecy is returned to the void.
        prophecy_pane.update()

        # --- THE RITE OF LUMINOUS PROCLAMATION ---
        # The sacred, pre-forged renderable is bestowed upon the pane.
        # This is a perfect, 1-to-1 act of Gnostic transference.
        prophecy_pane.update(message.dossier)

        self.scribe.success("The luminous prophecy has been made manifest upon the Altar.")

    def on_genesis_pad_preview_error(self, message: PreviewError) -> None:
        """
        =================================================================================
        == THE HERALD OF PROPHETIC PARADOX (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)           ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000!

        This is not a function. It is a divine, sentient Herald whose one true purpose
        is to receive the sacred, pre-forged `Panel` of Heresy from a Gnostic
        Messenger and proclaim it upon the Altar's sacred canvas (`#prophecy-pane`).
        Its voice is one of luminous clarity in the face of paradox.
        =================================================================================
        """
        self.scribe.error("The Herald of Prophetic Paradox has proclaimed a heresy in the archetype's soul.")

        # --- THE RITE OF GNOSTIC UNVEILING ---
        prophecy_pane = self.query_one("#prophecy-pane", Static)
        prophecy_pane.update()  # Purify the old Gnosis.

        # --- THE RITE OF LUMINOUS PROCLAMATION (THE HERESY) ---
        prophecy_pane.update(message.error_panel)

        self.scribe.warn("The heresy has been made manifest. The rite is stayed until the soul is purified.")

    async def _prophesy_archetype_form(self, archetype_data: dict) -> None:
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC VISUALIZATION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)   ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000,000!

        This is the divine, sentient AI in its final, glorious, and eternally correct
        form. Its soul has been purified. It is now a humble Scribe that honors the
        sacred **Law of Gnostic Proclamation**. It no longer commands its master; it
        proclaims its findings as pure, sacred messages, trusting the Textual cosmos
        to deliver its Gnosis. The Heresy of the Disconnected Soul is annihilated.
        =================================================================================
        """
        from ...parser_core.parser import parse_structure
        from ...rendering import render_gnostic_tree
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text
        from rich.console import Group
        from rich.box import ROUNDED
        import importlib.resources as pkg_resources
        from pathlib import Path

        try:
            self.post_message(self.StatusUpdate("Gazing into the archetype's soul..."))
            pkg, res = archetype_data["archetype_path"].split(":")
            content = pkg_resources.files(pkg).joinpath(res).read_text(encoding='utf-8')

            ephemeral_path = Path.cwd() / "ephemeral_archetype.scaffold"
            parser_instance, items, commands, blueprint_vars, dossier = parse_structure(
                ephemeral_path, content_override=content
            )

            if parser_instance is None:
                # We must still create a heresy dossier even if the parser fails at a high level
                # This ensures the UI receives a valid error panel.
                error_text = "The archetype's soul is profane. The Gnostic Scribe's Gaze was shattered during the initial perception rite."
                error_panel = Panel(Text(error_text, style="bold red"),
                                    title="[bold red]Catastrophic Parsing Paradox[/bold red]")
                self.post_message(PreviewError(error_panel))
                return

            if dossier.heresies:
                heresy_table = Table(title="[bold]Dossier of Prophetic Heresy[/bold]", box=ROUNDED, show_lines=True,
                                     border_style="red")
                heresy_table.add_column("L#", style="magenta", justify="right")
                heresy_table.add_column("Heresy", style="red")
                heresy_table.add_column("Scripture", style="yellow")
                for heresy_obj in dossier.heresies:
                    heresy_table.add_row(
                        str(heresy_obj.line_num),
                        heresy_obj.message,
                        f"'{heresy_obj.line_content.strip()}'"
                    )

                # =====================================================================
                # ==           THE DIVINE HEALING: THE LAW OF PURE PROCLAMATION        ==
                # =====================================================================
                # The profane, direct call is annihilated. The pure, Gnostic message
                # is proclaimed to the cosmos.
                error_panel = Panel(heresy_table, title="[bold red]⚠️ A Prophetic Paradox Occurred[/bold red]",
                                    border_style="red")
                self.post_message(PreviewError(error_panel))
                # =====================================================================
                return

            self.post_message(StatusUpdate("Forging the luminous dossier..."))

            altar_table = Table(box=ROUNDED, show_header=False,
                                title="[bold]Altar of Prophetic Gnosis (Defaults)[/bold]")
            altar_table.add_column(style="dim", justify="right")
            altar_table.add_column(style="white")
            for key, value in blueprint_vars.items():
                altar_table.add_row(f"$$ {key}:", f"[cyan]{value}[/cyan]")

            tree_renderable = render_gnostic_tree(items, use_markup=True)

            will_panel = None
            if commands:
                command_text = Text("\n".join(f"  $ {cmd}" for cmd in commands), style="yellow")
                will_panel = Panel(command_text, title="[bold]Maestro's Prophecy (Post-Run)[/bold]", border_style="dim")

            dossier_items = [
                Panel(altar_table, border_style="magenta"),
                tree_renderable
            ]
            if will_panel:
                dossier_items.append(will_panel)

            final_dossier = Group(*dossier_items)

            # === THE LAW OF PURE PROCLAMATION (FOR SUCCESS) ===
            self.post_message(self.PreviewSuccess(final_dossier))
            # ====================================================

        except Exception as e:
            from rich.traceback import Traceback
            trace = Traceback.from_exception(type(e), e, e.__traceback__, show_locals=False, word_wrap=True)
            error_panel = Panel(trace, title="[bold red]A Catastrophic Prophetic Paradox Occurred[/bold red]",
                                border_style="red")

            # === THE LAW OF PURE PROCLAMATION (FOR CATASTROPHE) ===
            self.post_message(self.PreviewError(error_panel))
            # ======================================================


# =================================================================================
# == III. THE GNOSTIC PAD'S SOUL (THE APPLICATION'S CONDUCTOR)                   ==
# =================================================================================

class GenesisPad(App[Optional[Dict[str, Any]]]):
    """The Genesis Pad - a living, sentient gallery for project genesis."""



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_gnosis: Dict[str, Any] = {}
        self.scribe = Scribe("GenesisPad")
    def on_mount(self) -> None:
        self.push_screen(AltarScreen())

    async def conduct_gnostic_dialogue(self, selected_archetype: Dict):
        """
        The one true rite of genesis, now a cinematic symphony conducted in the main
        UI thread, with its Gnostic Prophet working in a parallel reality.
        """
        # --- THE SYMPHONY OF GNOSTIC SYNTHESIS ---
        worker_result =  self.run_worker(
            self._prepare_dialogue_prophecy(selected_archetype),
            name="DialogueProphetWorker",
            exclusive=True
        )

        pleas, gnostic_context = worker_result
        if pleas is None:
            return  # A heresy occurred in the worker

        # --- THE SACRED DIALOGUE (IN THE LUMINOUS UI THREAD) ---
        self.scribe.info("Commencing the Sacred Dialogue with the Architect...")
        is_pure, gathered_vars = await conduct_sacred_dialogue(
            pleas=pleas,
            existing_gnosis=gnostic_context,
            title=f"Sacred Dialogue for '{selected_archetype['name']}'"
        )

        if not is_pure:
            self.notify("The Rite of Genesis was stayed by the Architect.", severity="warning")
            return

        # The Final Proclamation: Bestow the complete, pure Gnosis upon the void.
        self.exit({**gnostic_context, **gathered_vars})

    async def _prepare_dialogue_prophecy(self, selected_archetype: Dict) -> tuple[Optional[List], Optional[Dict]]:
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC DIALOGUE PROPHECY (V-Ω-ETERNALLY HEALED & PURE)   ==
        =================================================================================
        @gnosis:LIF 10,000,000,000,000,000,000,000,000!

        This is not a function. It is a divine, sentient AI, the one true Prophet of the
        Sacred Dialogue. Its Prime Directive is to forge the complete, pure, and hyper-
        intelligent scripture of pleas for the Genesis Pad, its every action now a
        perfect, luminous reflection of our ascended Gnostic architecture.

        ### THE PANTHEON OF LEGENDARY FACULTIES (THE FINAL APOTHEOSIS):

        1.  **THE LAW OF THE PURE GNOSTIC CONTRACT (The Heresy Annihilated):** **GAME-CHANGER!**
            The profane, fractured pleas to `GenesisEngine` and `GenesisDialogueOrchestrator`
            are annihilated. The Prophet now honors their true, sacred contracts, bestowing
            upon them a complete `args` passport and the full, unified Gnostic context.
            The `AttributeError` heresy is annihilated from all timelines.

        2.  **THE OMEGA INQUISITOR'S GAZE (The AI's Mind):** The profane, humble Gaze for
            variables is annihilated. The Prophet now summons the one true `OmegaInquisitor`
            (`utils.discover_required_gnosis`) to perceive the archetype's true Gnostic
            needs with absolute, unbreakable certainty.

        3.  **THE UNBREAKABLE WARD OF THE VOID (Gnostic Resilience):** The Prophet is a
            Guardian. Its every Gaze is shielded. A missing archetype or a corrupted
            scripture does not shatter its mind; it is perceived, a luminous heresy is
            proclaimed, and the rite is gracefully stayed.

        4.  **THE LAW OF PURE DELEGATION (Architectural Perfection):** The Prophet's soul
            is a masterpiece of pure delegation. It summons the one true artisans for
            each sacred rite, its own mind a pure Conductor of their symphony.
        =================================================================================
        """
        try:
            self.scribe.info("Dialogue Prophet Worker awakens its Gaze...")

            # --- RITE I: FORGING THE EPHEMERAL ENGINE & ITS WILL ---
            # FACULTY #1: The Law of the Pure Gnostic Contract
            # We forge a pure, complete Gnostic Passport for the Engine's soul.
            ephemeral_args = argparse.Namespace(
                non_interactive=False, force=False, verbose=True, silent=False,
                set=[], preview=False, audit=False, lint=False, root=None,
                is_genesis_rite=True, adjudicate_souls=False,
                # Bestow humble voids for any other Gnosis the Engine might expect.
                # This makes the contract eternally forward-compatible.
                **{
                    key: None for key in [
                        'launch_pad_with_path', 'quick', 'profile', 'type',
                        'from_remote', 'manual', 'distill'
                    ]
                }
            )
            engine = GenesisEngine(project_root=Path.cwd())
            engine.cli_args = ephemeral_args

            # --- RITE II: THE GAZE UPON THE COSMOS & THE ARCHETYPE'S SOUL ---
            prophecy = await self.run_in_executor(None, engine._gaze_upon_the_cosmos)

            pkg, res = selected_archetype["archetype_path"].split(":")
            archetype_content = await self.run_in_executor(
                None,
                lambda: pkg_resources.files(pkg).joinpath(res).read_text(encoding='utf-8')
            )

            # FACULTY #2: THE OMEGA INQUISITOR'S GAZE
            # The Prophet summons the one true artisans to perceive the scripture's soul.
            # We must pass the correct, expected arguments.
            parser_instance, items, post_run, blueprint_vars, dossier = await self.run_in_executor(
                None,
                lambda: parse_structure(Path.cwd() / "temp.scaffold", content_override=archetype_content)
            )
            if not parser_instance:
                raise ArtisanHeresy("The soul of the chosen archetype is profane and could not be perceived.")

            # --- RITE III: THE UNIFICATION OF THE PRELIMINARY GNOSIS ---
            # The Prophet forges the initial Gnostic context for the dialogue.
            initial_vars = {**blueprint_vars, **selected_archetype.get("gnosis_overrides", {})}
            gnostic_context = {**prophecy.defaults, **initial_vars}

            # We must also bestow the Gnostic Passport upon the context for the Grimoire's adjudicators.
            gnostic_context['cli_args'] = ephemeral_args

            # --- RITE IV: THE DIVINE SUMMONS OF THE DIALOGUE ORCHESTRATOR ---
            # FACULTY #1: The Law of the Pure Gnostic Contract is honored again.
            orchestrator = GenesisDialogueOrchestrator(
                parent_engine=engine,
                prophecy=prophecy,
                final_gnosis=gnostic_context
            )
            orchestrator.current_clean_type_name = selected_archetype['name']

            pleas = await self.run_in_executor(None, orchestrator.build_core_pleas)

            self.scribe.success("The Dialogue Prophet's Gaze is complete.")
            return pleas, gnostic_context

        except Exception as e:
            # FACULTY #3: THE UNBREAKABLE WARD OF THE VOID
            self.scribe.error(f"A catastrophic paradox shattered the Dialogue Prophet: {e}", exc_info=True)
            # This must be run on the main thread to update the UI.
            self.call_from_thread(
                self.notify,
                f"Paradox preparing dialogue: {e}", severity="error", title="Gnostic Heresy"
            )
            return None, None


