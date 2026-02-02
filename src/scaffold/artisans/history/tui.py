# Path: scaffold/artisans/history/tui.py

from __future__ import annotations
import time
import tempfile
from pathlib import Path
from typing import List, Optional

from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.reactive import var
from textual.widgets import Header, Footer, Static, DataTable, Button

from .contracts import RiteGnosis
from .scribe import HistoryScribe
from .differ import TemporalDiffer  # ASCENSION: The Differ is now a core artisan
from ....core.kernel.hologram import HolographicEngine
from ....interfaces.requests import UndoRequest, PatchRequest  # ASCENSION: We now speak the tongue of Patch
from ....logger import Scribe, get_console

Logger = Scribe("HistoryAltar")


class HistoryAltarApp(App[None]):
    """The Altar of Time - The Interactive Gnostic Timeline."""

    TITLE = "Scaffold - Gnostic Timeline"
    CSS = """
    Screen { layout: vertical; }
    #timeline_container { height: 1fr; border-bottom: solid $accent; }
    #detail_pane { height: 12; border-bottom: solid $accent; padding: 1; }
    #chronoslider_container { height: 3; align: center middle; padding: 1; }
    #actions_container { height: 3; align: center middle; }
    DataTable { height: 100%; }
    DataTable:focus .datatable--cursor { background: $accent; color: $text; }
    #chronoslider_label { margin-right: 2; }
    #slider_text { width: 1fr; }
    Button { margin: 0 1; }
    """

    BINDINGS = [
        Binding("u", "undo_selected", "Undo", show=True),
        # === THE ASCENSION OF WILL ===
        Binding("r", "revert_selected", "Revert (Patch)", show=True),
        Binding("p", "pick_selected", "Cherry-Pick", show=True),
        # =============================
        Binding("q", "quit", "Quit", show=True),
        Binding("up,k", "cursor_up", "Up", show=False),
        Binding("down,j", "cursor_down", "Down", show=False),
        Binding("left,h", "slider_left", "Time--", show=False),
        Binding("right,l", "slider_right", "Time++", show=False),
    ]

    history: var[List[RiteGnosis]] = var([])
    selected_rite: var[Optional[RiteGnosis]] = var(None)
    is_hologram_active: var[bool] = var(False)

    def __init__(self, history: List[RiteGnosis], project_root: Path, engine: "ScaffoldEngine"):
        super().__init__()
        self.history = history
        self.project_root = project_root
        self.engine = engine
        self.scribe = HistoryScribe(get_console())
        self.hologram_engine = HolographicEngine(project_root)
        self.differ = TemporalDiffer(self.console)  # ASCENSION: The Differ is now an artisan of this Altar

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="timeline_container"):
            yield DataTable(id="history_table", cursor_type="row")
        yield Static("Select a rite to inspect its Gnosis.", id="detail_pane")
        with Horizontal(id="chronoslider_container"):
            yield Static("⏪", id="slider_left_arrow")
            yield Static("─" * 50, id="slider_text")
            yield Static("⏩", id="slider_right_arrow")
        with Horizontal(id="actions_container"):
            yield Button("Undo Back to Here", id="btn_undo", variant="error")
            yield Button("Revert This Rite", id="btn_revert", variant="warning")  # ASCENSION
            yield Button("Toggle Hologram", id="btn_hologram", variant="primary")
        yield Footer()

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns("ID", "Age", "Rite Name", "Impact")
        for rite in self.history:
            table.add_row(
                rite.rite_id[:8],
                self.scribe._format_age(rite.timestamp) if not rite.is_head else "[b]HEAD[/b]",
                rite.rite_name,
                self._format_impact(rite),
                key=rite.rite_id
            )
        if self.history:
            self.query_one(DataTable).cursor_coordinate = (0, 0)

    def watch_selected_rite(self, rite: Optional[RiteGnosis]):
        details = self.query_one("#detail_pane")
        if not rite:
            details.update("Select a rite.")
            return

        detail_text = Text.assemble(
            ("Rite: ", "bold"), (f"{rite.rite_name}\n", "cyan"),
            ("ID:   ", "bold"), (f"{rite.rite_id}\n", "dim"),
            ("Date: ", "bold"), (f"{rite.timestamp.strftime('%Y-%m-%d %H:%M:%S')}", "dim")
        )
        details.update(detail_text)
        self._update_chronoslider()

    # ... (on_row_selected, _format_impact, _update_chronoslider, update_hologram, action_toggle_hologram, slider actions remain pure)
    @on(DataTable.RowSelected)
    def on_row_selected(self, event: DataTable.RowSelected):
        rite_id = event.row_key.value
        self.selected_rite = next((r for r in self.history if r.rite_id == rite_id), None)

    def _format_impact(self, rite: RiteGnosis) -> str:
        stats = rite.provenance.rite_stats
        c, u, d, m = stats.get('create', 0), stats.get('update', 0), stats.get('delete', 0), stats.get('move', 0)
        parts = []
        if c > 0: parts.append(f"[green]+{c}[/green]")
        if u > 0: parts.append(f"[yellow]~{u}[/yellow]")
        if d > 0: parts.append(f"[red]-{d}[/red]")
        if m > 0: parts.append(f"[cyan]>>{m}[/cyan]")
        return " ".join(parts) or f"{len(rite.manifest)} files"

    def _update_chronoslider(self):
        if not self.selected_rite or len(self.history) <= 1:
            return
        idx = self.history.index(self.selected_rite)
        total = len(self.history) - 1
        pos = total - idx
        width = 50
        filled_width = int((pos / total) * width) if total > 0 else width
        slider_bar = "█" * filled_width + "─" * (width - filled_width)
        self.query_one("#slider_text").update(f"[{slider_bar}]")
        self.run_worker(self.update_hologram(), exclusive=True, group="hologram")

    @work(thread=True)
    def update_hologram(self):
        if not self.is_hologram_active or not self.selected_rite:
            return
        self.hologram_engine.materialize(self.selected_rite.rite_id)

    @on(Button.Pressed, "#btn_hologram")
    def action_toggle_hologram(self):
        self.is_hologram_active = not self.is_hologram_active
        btn = self.query_one("#btn_hologram")
        if self.is_hologram_active:
            btn.label = "Deactivate Hologram"
            btn.variant = "warning"
            self.notify("Holographic Repository ACTIVE. Filesystem is now a projection of the past.",
                        severity="warning")
            self._update_chronoslider()
        else:
            self.hologram_engine.dematerialize()
            btn.label = "Activate Hologram"
            btn.variant = "primary"
            self.notify("Holographic Repository deactivated. Reality restored to the present.")

    def action_slider_left(self):
        if not self.selected_rite or not self.history: return
        idx = self.history.index(self.selected_rite)
        if idx < len(self.history) - 1:
            self.query_one(DataTable).action_cursor_down()

    def action_slider_right(self):
        if not self.selected_rite or not self.history: return
        idx = self.history.index(self.selected_rite)
        if idx > 0:
            self.query_one(DataTable).action_cursor_up()

    @on(Button.Pressed, "#btn_undo")
    def action_undo_selected(self):
        if not self.selected_rite or self.selected_rite.is_head:
            self.notify("Cannot undo the present (HEAD).", severity="error")
            return
        steps_to_undo = self.history.index(self.selected_rite)

        async def conduct_undo():
            await self.suspend_process()
            try:
                self.engine.dispatch(UndoRequest(steps=steps_to_undo, project_root=self.project_root, force=True))
            finally:
                self.exit(f"Undo complete. Timeline reverted by {steps_to_undo} step(s).")

        self.run_worker(conduct_undo)

    # === THE ASCENDED RITES OF TEMPORAL ACTION ===

    @on(Button.Pressed, "#btn_revert")
    def action_revert_selected(self):
        """[ASCENSION 1] The Temporal Schism."""
        if not self.selected_rite or self.selected_rite.is_head:
            self.notify("Cannot revert the present (HEAD).", severity="error")
            return

        target_rite = self.selected_rite
        current_rite = self.history[0]  # HEAD

        async def conduct_revert():
            await self.suspend_process()
            try:
                # The Differ forges the reverse patch scripture
                patch_content = self.differ.forge_revert_patch(
                    rite_to_revert=target_rite,
                    current_reality=current_rite,
                    project_root=self.project_root
                )

                # We materialize the patch to an ephemeral file
                with tempfile.NamedTemporaryFile(mode='w+', suffix=".patch.scaffold", delete=False,
                                                 encoding='utf-8') as tmp:
                    tmp.write(patch_content)
                    tmp_path = Path(tmp.name)

                # We summon the PatchArtisan to apply it
                self.engine.dispatch(PatchRequest(patch_path=str(tmp_path), project_root=self.project_root, force=True))
                os.unlink(tmp_path)
            finally:
                self.exit(f"Reverted changes from rite {target_rite.rite_id[:8]}.")

        self.run_worker(conduct_revert)

    def action_pick_selected(self):
        """[ASCENSION 2] The Cherry-Pick Rite."""
        if not self.selected_rite: return

        rite = self.selected_rite
        self.notify(f"Attempting to cherry-pick rite: {rite.rite_name}...")

        async def conduct_pick():
            # This is a complex rite. We reconstruct the original command.
            # A full implementation requires mapping rite_name back to an Artisan and its Request.
            # For this ascension, we demonstrate the principle.

            # Example: If rite_name was 'Weave component', we'd forge a WeaveRequest.
            # The variables would come from rite.gnosis_delta.

            # This is a prophecy. We will simply log the intent.
            await self.suspend_process()
            try:
                self.engine.logger.info(f"Cherry-Pick Gnosis for '{rite.rite_name}':")
                self.engine.logger.info(f"  -> Variables: {rite.gnosis_delta}")
                self.engine.logger.info(f"  -> Edicts: {rite.edicts}")
                time.sleep(2)  # Simulate work
            finally:
                self.exit(
                    f"Cherry-Pick rite simulated for {rite.rite_id[:8]}. A future artisan will make this manifest.")

        self.run_worker(conduct_pick)

    def on_unmount(self):
        self.hologram_engine.dematerialize()