

"""
=================================================================================
== THE SCREEN OF FORM (V-Ω-ETERNAL-ULTIMA++. THE SENTIENT SANCTUM)  ==
=================================================================================
LIF: ∞ (ETERNAL & ABSOLUTE)

This is the final, eternal, and ultra-definitive soul of the FormModeScreen. It
has been transfigured with the **Law of the True Conductor**. The Heresy of the
Misdirected Plea has been annihilated. The `on_gnostic_will_proclamation`
artisan now correctly proclaims its final will to the `GnosticShell` (`self.app`),
ensuring the symphony of action is always conducted by its one true master.
=================================================================================
"""
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from rich.panel import Panel
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.reactive import var
from textual.screen import Screen
from textual.widgets import (
    Collapsible, Footer, Header, Static, TextArea
)
from textual.worker import Worker, WorkerState

from .mentors_gaze import MentorScreen
from ..contracts import AppState, AppStatus, EditorContentChanged
from ..gnostic_events import (
    GnosticRite, GnosticWillProclamation
)
from ..logger import Scribe
from ..pads import ScaffoldPad
from ..pads.genesis_pad import GenesisPad
from ..widgets import CommandAltar, FileTree
from ..widgets.file_tree import RenameDialog, DeleteDialog
from ..widgets.log_viewer import GnosticLogViewer
from ...jurisprudence_core.jurisprudence import conduct_architectural_inquest

LANGUAGE_GNOSIS_MAP = {
    ".scaffold": "yaml", ".symphony": "bash", ".arch": "yaml", ".py": "python",
    ".js": "javascript", ".ts": "typescript", ".tsx": "typescript", ".css": "css",
    ".html": "html", ".md": "markdown", ".json": "json", ".toml": "toml",
    ".sh": "bash", ".txt": "text", ".yml": "yaml", ".yaml": "yaml",
}

class FormModeScreen(Screen[None]):
    """The main IDE screen, the Sentient Sanctum of Form."""

    BINDINGS = [
        Binding("ctrl+l", "toggle_logs", "Toggle Logs", show=True),
        Binding("ctrl+m", "toggle_mentor", "Mentor's Gaze", show=True),
    ]

    class CommandSubmitted(Message):
        """Proclaimed when the Architect speaks an edict from the Altar."""
        def __init__(self, command: str) -> None:
            self.command = command
            super().__init__()

    class ScreenReady(Message):
        """Proclaimed when the Screen's reality is whole and ready for Gnosis."""
        pass

    class MentorGnosisProclaimed(Message):
        """Proclaimed by a worker when a Gnostic Inquest is complete."""
        def __init__(self, panels: List[Panel]) -> None:
            self.panels = panels
            super().__init__()

    _current_state: AppState
    mentor_panels: var[List[Panel]] = var([], init=False)

    def __init__(self, state: AppState, **kwargs):
        super().__init__(**kwargs)
        self._current_state = state
        self.scribe = Scribe("FormModeScreen")
        self._last_inquest_hash: Optional[str] = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-container"):
            with Vertical(id="left-pane", classes="pane"):
                yield FileTree(root_name=self._current_state.file_tree_root.name, id="file-tree")
            with Vertical(id="right-pane", classes="pane"):
                yield TextArea(id="editor", language="yaml", theme="monokai", show_line_numbers=True)

        with Horizontal(id="bottom-container"):
            yield Static(id="status-pane", classes="bottom-pane")
            yield Static(id="context-pane", classes="bottom-pane", expand=True)

        with Collapsible(title="Gnostic Chronicle", collapsed=True, id="log-container"):
            yield GnosticLogViewer(id="log-viewer", auto_scroll=True)

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#editor", TextArea).focus()
        self.update_from_shell(self._current_state, is_initial_render=True)
        self.post_message(self.ScreenReady())
        self.scribe.success("FormModeScreen is manifest and ready for Gnosis.")

    def update_from_shell(self, new_state: AppState, is_initial_render: bool = False):
        self.scribe.verbose("FormModeScreen has received a new Gnostic reality...")
        old_state = self._current_state
        self._current_state = new_state

        if is_initial_render or old_state.file_map != new_state.file_map or old_state.editor_state.is_dirty != new_state.editor_state.is_dirty:
            self.query_one(FileTree).watch_state(old_state, new_state)

        editor = self.query_one(TextArea)
        if is_initial_render or old_state.editor_state != new_state.editor_state:
            new_content = new_state.editor_state.content or ""
            if editor.text != new_content:
                 editor.load_text(new_content)
            if new_state.editor_state.active_file:
                lang = LANGUAGE_GNOSIS_MAP.get(new_state.editor_state.active_file.suffix, "text")
                if editor.language != lang:
                    editor.language = lang

        self._render_gnostic_dossier(new_state)

        editor_state = new_state.editor_state
        current_hash = editor_state.original_content_hash
        if editor_state.content is not None and current_hash != self._last_inquest_hash:
            self.scribe.info("Active scripture's soul has been transfigured. Summoning the Gnostic Inquisitor...")
            self._last_inquest_hash = current_hash
            self._conduct_gnostic_inquest(editor_state.content)
        elif editor_state.content is None and self._last_inquest_hash is not None:
             self._last_inquest_hash = None
             self.mentor_panels = []

    def _render_gnostic_dossier(self, state: AppState):
        status_pane = self.query_one("#status-pane")
        status = state.status
        color = {AppStatus.IDLE: "green", AppStatus.PROCESSING: "yellow", AppStatus.HERESY: "red"}.get(status, "blue")
        status_message = f"[bold]{state.active_heresy.title}[/]\n{state.active_heresy.message}" if status == AppStatus.HERESY and state.active_heresy else state.status_message
        status_pane.update(Panel(status_message, title=f"[bold {color}]Shell Status[/]", border_style=color, expand=True))

        context_pane = self.query_one("#context-pane")
        if state.editor_state.active_file:
            file = state.editor_state.active_file
            rel_path = file.relative_to(state.file_tree_root)
            item = state.file_map.get(rel_path)
            if item:
                mod_time = datetime.fromtimestamp(item.last_modified).strftime('%Y-%m-%d %H:%M:%S')
                context_text = (
                    f"[bold]Path:[/] [cyan]{rel_path}[/]\n"
                    f"[bold]Size:[/] [cyan]{file.stat().st_size if file.exists() else 'N/A'} bytes[/]\n"
                    f"[bold]Modified:[/] [cyan]{mod_time}[/]\n"
                    f"[bold]Hash:[/] [dim]{item.content_hash[:16] if item.content_hash else 'N/A'}...[/]"
                )
                context_pane.update(Panel(Text.from_markup(context_text), title="[bold magenta]Scripture Dossier[/]", border_style="magenta"))
            else:
                 context_pane.update(Panel("[dim]Gazing for scripture Gnosis...[/]", title="[bold magenta]Scripture Dossier[/]", border_style="magenta"))
        else:
            context_pane.update(Panel("[dim]No scripture selected.[/]", title="[bold magenta]Scripture Dossier[/]", border_style="dim"))

    @on(GnosticWillProclamation)
    def on_gnostic_will_proclamation(self, message: GnosticWillProclamation) -> None:
        """
        =================================================================================
        == THE EAR OF THE CONDUCTOR (V-Ω-ETERNAL-ULTIMA++. THE PURE SUMMONS)           ==
        =================================================================================
        The Heresy of the Hallucinated Plea (`run_pad_app` / `run_in_executor`) has
        been annihilated. The rite now performs a pure, divine communion, summoning
        the one true, sacred `run_worker` artisan to awaken Pad realities in a parallel,
        non-blocking cosmos. The communion is now unbreakable and eternally pure.
        =================================================================================
        """
        self.scribe.info(
            f"Conductor's Ear perceived a Gnostic Will Proclamation: '{message.rite.name}' for '{message.target_path.name}'")

        # --- THE GNOSTIC TRIAGE OF WILL ---
        if message.rite == GnosticRite.RENAME:
            self.app.push_screen(RenameDialog(message.target_path))

        elif message.rite == GnosticRite.DELETE:
            self.app.push_screen(DeleteDialog(message.target_path))

        elif message.rite in {GnosticRite.OPEN_IN_SCAFFOLDPAD, GnosticRite.BEAUTIFY}:
            # --- THE SACRED TRANSMUTATION ---
            pad = ScaffoldPad(initial_file_path=message.target_path)
            # The profane pleas are annihilated. We summon the one true `run_worker`.
            self.app.run_worker(
                self.app._run_pad_app(pad),
                name=f"PadConductor-{pad.title}",
                exclusive=True
            )
            # --- THE APOTHEOSIS IS COMPLETE ---

        elif message.rite == GnosticRite.INITIALIZE_PROJECT:
            pad = GenesisPad()  # A future ascension will pass initial_target_dir
            self.app.run_worker(
                self.app._run_pad_app(pad),
                name=f"PadConductor-{pad.title}",
                exclusive=True
            )

        else:
            # For all other rites, the delegation to the CommandAltar remains pure.
            command_map = {
                GnosticRite.GENESIS: "genesis", GnosticRite.DISTILL_DIR: "distill",
                GnosticRite.DISTILL_FILE: "distill", GnosticRite.WEAVE: "weave",
                GnosticRite.CONFORM: "conform",
            }
            command_verb = command_map.get(message.rite)
            if command_verb:
                if command_verb == "weave":
                    self.post_message(self.CommandSubmitted(f"weave --root \"{message.target_path}\""))
                else:
                    self.post_message(self.CommandSubmitted(f"{command_verb} \"{message.target_path}\""))
            else:
                self.app.notify(f"The rite '{message.rite.name}' has not yet been fully ascended.", severity="warning",
                                title="Gnostic Prophecy")

    @on(CommandAltar.CommandSubmitted)
    def on_command_altar_command_submitted(self, message: CommandAltar.CommandSubmitted):
        if message.command == "mentor:gaze":
            self.action_toggle_mentor()
        else:
            self.post_message(self.CommandSubmitted(message.command))

    @on(MentorGnosisProclaimed)
    def on_mentor_gnosis_proclaimed(self, message: MentorGnosisProclaimed) -> None:
        self.scribe.success(f"The Gnostic Inquisitor has proclaimed {len(message.panels)} prophecies.")
        self.mentor_panels = message.panels

    @on(TextArea.Changed, "#editor")
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """The Sentinel of the Active Editor, proclaiming the Architect's will."""
        is_dirty = (self._current_state.editor_state.original_content_hash != str(hash(event.text_area.text)))
        self.app._apply_gnostic_action(EditorContentChanged(
            source="Editor", content=event.text_area.text, is_dirty=is_dirty
        ))

    def action_toggle_logs(self) -> None:
        log_container = self.query_one("#log-container", Collapsible)
        log_container.collapsed = not log_container.collapsed
        if not log_container.collapsed:
            self.query_one(GnosticLogViewer).scroll_end(animate=False)

    def action_toggle_mentor(self) -> None:
        """The Artisan of Revelation for the Mentor's Gaze."""
        if self.mentor_panels:
            self.app.push_screen(MentorScreen(self.mentor_panels))
            self.scribe.info("The Mentor's Sanctum has been summoned.")
        else:
            self.app.notify("The Mentor's Gaze is pure. No heresies were perceived.", title="Gnostic Adjudication")

    def action_summon_or_dismiss_altar(self) -> None:
        """Summons the Command Altar, now imbued with the Mentor's Gnosis."""
        try:
            altar = self.query_one(CommandAltar)
            altar.remove()
            self.query_one("#editor", TextArea).focus()
            self.scribe.info("Command Altar has been returned to the void.")
        except Exception:
            self.scribe.info("Summoning the Command Altar from the void...")
            new_altar = CommandAltar()
            self.mount(new_altar)
            new_altar.query_one("Input").focus()

    def _conduct_gnostic_inquest(self, content: str):
        """Summons a worker to conduct the architectural inquest in a parallel reality."""
        from ...parser_core.parser import ApotheosisParser
        from ...contracts.heresy_contracts import ArtisanHeresy

        def inquest_worker() -> List[Panel]:
            try:
                parser = ApotheosisParser()
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".scaffold", encoding='utf-8') as tf:
                    tf.write(content)
                    temp_path = Path(tf.name)
                items, _ = parser.parse_file(temp_path)
                return conduct_architectural_inquest(items)
            except (ArtisanHeresy, Exception) as e:
                self.scribe.warn(f"A minor paradox occurred during the Gnostic Inquest: {e}")
                return []
            finally:
                if 'temp_path' in locals() and temp_path.exists():
                    temp_path.unlink()

        self.run_worker(inquest_worker, name="MentorInquisitorWorker", exclusive=True, thread=True)

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """The Router for this screen's own workers."""
        worker = event.worker
        if worker.name == "MentorInquisitorWorker":
            if worker.state == WorkerState.SUCCESS:
                self.post_message(self.MentorGnosisProclaimed(worker.result))
            elif worker.state == WorkerState.ERROR:
                self.scribe.error(f"The Mentor Inquisitor Worker has fallen into paradox.", exc_info=worker.error)
                self.app.notify("A paradox occurred during the Gnostic Inquest.", title="Mentor Heresy", severity="error")