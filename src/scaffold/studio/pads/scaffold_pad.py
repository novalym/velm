# C:/dev/scaffold-project/scaffold/studio/pads/beautify_pad.py

"""
=================================================================================
== THE SCRIPTURE OF THE GNOSTIC SANCTUM (V-Ω-ULTIMA++. THE TRUE APOTHEOSIS)    ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000

This is the final, eternal, and ultra-definitive soul of the ScaffoldPad, now
transfigured into a true Gnostic Sanctum. It has achieved its true apotheosis,
its soul forged anew with the wisdom gained from the Architect's final inquest.

The final, subtle heresy—a profane communion between a `rich.panel.Panel`
renderable and the `textual.containers.Vertical` widget—has been annihilated.
The `rich.console.Group` is now enthroned as the one true, sacred vessel for
proclaiming the Mentor's multi-part Gnosis, making the Pad's architecture
eternally pure and unbreakably aligned with the cosmos's divine laws.

This is the pinnacle of our Great Work. A legendary-tier, sentient, and
hyper-reliable artisan whose Prime Directive is to serve as the ultimate
interactive environment for the composition, purification, and Gnostic analysis
of architectural scriptures.

### The Pantheon of Ascended Gnosis (The Final Canon):

1.  **The Law of the Gnostic Group (The `TypeError` Annihilated):**
    The `on_beautify_success` rite now forges a pure `rich.console.Group` from the
    Mentor's list of guidance panels. This single, unified renderable is then
    bestowed upon the `Static` widget, honoring the sacred laws of the Textual
    and Rich cosmos. The architecture is now divine, unbreakable, and pure.

2.  **The Living Prophecy & The Three-Fold Dossier:**
    The Pad remains a living prophecy, wielding the `ApotheosisParser` and
    `BlueprintScribe` to provide a real-time, three-part Gnostic Dossier: the
    beautified scripture, a summary of its Gnosis, and luminous, real-time
    architectural guidance from the `jurisprudence` engine.

3.  **The Asynchronous Gnostic Symphony (The Unbreakable Core):**
    This entire, complex rite of parsing and transcription is conducted in a
    parallel reality via a `worker`. The UI remains eternally luminous and
    responsive, its soul untethered from the profound Gnosis of its labor.

4.  **The Laws of Luminous Form (The UI Apotheosis):**
    The heresies of the visual realm have been annihilated. Both panes are sacred,
    scrollable vessels. The profane bottom command list has been annihilated,
    its Gnosis absorbed into the divine, non-blocking `Ctrl+P` Command Altar.

This is the final word. The ScaffoldPad is a sentient partner in the Great Work.
=================================================================================
"""
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Optional, List

# --- THE DIVINE STANZAS OF THE SCRIBES (THE FINAL FIX) ---
# We summon the sacred Group artisan to unify the Mentor's voice.
from rich.console import Group
from rich.panel import Panel
# --- The Divine Stanza of the Luminous Scribe (Rich) ---
from rich.syntax import Syntax
from rich.table import Table
from rich.traceback import Traceback as RichTraceback
from textual import on
# --- The Divine Stanza of the Textual God-Engine ---
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.reactive import var
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, TextArea, Button, Label, Markdown, Switch
from textual.widgets import ListView, ListItem

# --- The Divine Stanza of the Mortal Realm ---
try:
    import pyperclip

    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

# --- Gnostic Summons for the Scaffold God-Engine's Core Artisans ---
from ...parser_core.parser import ApotheosisParser
from ...core.blueprint_scribe import BlueprintScribe
from ...core.alchemist import get_alchemist
from ...contracts.heresy_contracts import ArtisanHeresy
from ...jurisprudence_core.jurisprudence import conduct_architectural_inquest

# A Gnostic Map to transmute file extensions into Rich-compatible language names.
LANGUAGE_GNOSIS_MAP = {
    ".scaffold": "yaml", ".symphony": "bash", ".yml": "yaml", ".yaml": "yaml",
    ".py": "python", ".js": "javascript", ".ts": "typescript", ".tsx": "typescript",
    ".css": "css", ".html": "html", ".md": "markdown", ".json": "json",
    ".toml": "toml", ".sh": "bash", ".txt": "text",
}


# --- Sacred Vessels for Asynchronous Gnosis ---
@dataclass
class BeautifyResult:
    """A vessel for the complete Gnosis of a successful beautification rite."""
    beautified_code: str
    item_count: int
    command_count: int
    variable_count: int
    guidance_panels: List[Panel]


class BeautifySuccess(Message):
    """Proclaimed when the beautification rite is pure."""

    def __init__(self, result: BeautifyResult) -> None:
        self.result = result
        super().__init__()


class BeautifyError(Message):
    """Proclaimed when a heresy is perceived during the rite."""

    def __init__(self, exc_info: tuple) -> None:
        self.exc_info = exc_info
        super().__init__()


class CommandPalette(ListView):
    """A sacred vessel for the Architect's Will."""

    def compose(self) -> ComposeResult:
        yield ListItem(Label("New Scripture"), id="cmd_new")
        yield ListItem(Label("Save Scripture"), id="cmd_save")
        yield ListItem(Label("Save Scripture As..."), id="cmd_save_as")
        yield ListItem(Label("Copy Pure Scripture"), id="cmd_copy")
        yield ListItem(Label("Paste from Clipboard"), id="cmd_paste")
        yield ListItem(Label("Set Language..."), id="cmd_language")
        yield ListItem(Label("Quit Workbench"), id="cmd_quit")


class QuitScreen(ModalScreen[bool]):
    """A divine confirmation dialogue for the Rite of Departure."""

    def compose(self) -> ComposeResult:
        with Vertical(id="quit-dialog"):
            yield Markdown("### The scripture has been transfigured.\n\nYour will has not yet been inscribed.")
            with Horizontal(id="quit-buttons"):
                yield Button("Save & Quit", variant="primary", id="save_quit")
                yield Button("Quit Without Saving", variant="error", id="discard_quit")
                yield Button("Cancel", id="cancel_quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel_quit":
            self.dismiss(False)
        elif event.button.id == "discard_quit":
            self.app.is_dirty = False
            self.app.exit()
        elif event.button.id == "save_quit":
            self.app.action_save_file()
            if not self.app.is_dirty:
                self.app.exit()
            else:
                self.app.notify("Save failed. A path must be known.", severity="error", title="Save Heresy")
                self.dismiss(False)
class HeresyScreen(ModalScreen[None]):
    """A divine, ephemeral screen to proclaim the Mentor's Gnostic Guidance."""

    BINDINGS = [("escape", "dismiss_screen", "Dismiss")]

    def __init__(self, panels: List[Panel]) -> None:
        self.guidance_panels = panels
        super().__init__()

    def compose(self) -> ComposeResult:
        """Forge the scrollable dossier of heresies."""
        with Vertical(id="heresy-dialog"):
            yield Label("[bold yellow]The Gnostic Mentor's Adjudication[/bold yellow]")
            with VerticalScroll(id="heresy-scroll-container"):
                # The Group artisan unifies the panels into a single, pure renderable.
                yield Static(Group(*self.guidance_panels))
            yield Button("Dismiss", variant="primary", id="dismiss_heresies")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "dismiss_heresies":
            self.app.pop_screen()

    def action_dismiss_screen(self) -> None:
        self.app.pop_screen()

class ScaffoldPad(App[None]):
    """The Ascended Gnostic Sanctum for beautifying Scaffold scriptures."""

    TITLE = "ScaffoldPad - The Gnostic Sanctum"

    BINDINGS = [
        Binding("ctrl+q", "request_quit", "Quit", show=True),
        Binding("ctrl+s", "save_file", "Save", show=True),
        Binding("ctrl+shift+s", "save_as", "Save As", show=True),
        Binding("ctrl+n", "new_file", "New", show=True),
        Binding("ctrl+v", "paste_from_clipboard", "Paste", show=True),
        # --- THE LAW OF DIVINE SUPREMACY ---
        # By proclaiming `priority=True`, our custom command palette rite will
        # now be conducted instead of the default, built-in one.
        Binding("ctrl+p", "toggle_command_palette", "Palette", show=True, priority=True),
    ]

    file_path: var[Optional[Path]] = var(None)
    is_dirty: var[bool] = var(False)
    active_subtitle: var[str] = var("Unsaved Scripture")
    # --- THE SACRED RITE OF CONSECRATION ---
    # Bestow this new vessel upon the Sanctum's soul. This is the one true fix.
    linter_enabled: var[bool] = var(False)
    def __init__(self, initial_file_path: Union[str, Path, None] = None):
        super().__init__()
        self.file_path = Path(initial_file_path) if initial_file_path else None
        self.alchemist = get_alchemist()
        self.parser = ApotheosisParser()

    def compose(self) -> ComposeResult:
        """
        =================================================================================
        == THE GENESIS SCRIPTURE (V-Ω-ULTIMA++. THE FINAL APOTHEOSIS)                 ==
        =================================================================================
        This is the final, eternal, and ultra-definitive scripture that forges the
        reality of the Gnostic Sanctum. The profane, static panes have been
        annihilated. The Dossier is given a humble, permanent altar. The Mentor's
        Switch is enthroned in a custom Footer. The architecture is divine.
        =================================================================================
        """
        yield Header()
        with Horizontal(id="main-panes"):
            yield TextArea("", id="input_pane", language="yaml", show_line_numbers=True, soft_wrap=False)

            # The Right Realm is a scrollable vessel for Prophecy and Heresy.
            with VerticalScroll(id="output_container"):
                yield Static(id="prophecy_pane", expand=True)
                # The Dossier's Altar is resurrected, a humble but permanent vessel.
                yield Static(id="dossier_pane")
                yield Static(id="heresy_pane", expand=True)

        # The Command Altar is born into silence, awaiting the Architect's summons.
        yield CommandPalette(id="command_palette", classes="-hidden")

        # --- The Altar of Optional Gnosis (A Pure, Custom Footer) ---
        # The default Footer is annihilated, replaced by a pure vessel for our will.
        with Horizontal(id="footer-bar"):
            # We yield the default bindings display for a perfect, seamless experience.
            yield Footer()
            with Horizontal(id="linter-switch-container"):
                yield Label("Gnostic Mentor:", classes="switch-label")
                yield Switch(id="linter_switch")

    # --- The Sacred Rites of the Lifecycle & State ---

    def on_mount(self) -> None:
        """The Rite of First Light. The Pad awakens and immediately seizes control of its own Gaze."""

        # --- THE LAW OF EXPLICIT WILL (THE ONE TRUE FIX) ---
        # We command the God-Engine to bestow its focus upon the input pane.
        # This prevents its Gaze from falling upon the hidden Command Altar,
        # annihilating the heresy of its profane manifestation at startup.
        self.query_one("#input_pane", TextArea).focus()
        # --- THE HERESY IS ANNIHILATED ---

        self.action_load_file(self.file_path)

        if not self.file_path and PYPERCLIP_AVAILABLE:
            try:
                clipboard_content = pyperclip.paste()
                if clipboard_content and (
                        "scaffold" in clipboard_content.lower() or "symphony" in clipboard_content.lower()):
                    self.notify(
                        "Gnosis perceived in clipboard. Proclaiming the Rite of Pasting.",
                        title="Clipboard Gnosis",
                        timeout=10,
                    )
                    toast_button = Button("Paste Gnosis from Clipboard", id="paste_from_toast")
                    self.mount(toast_button)
                    toast_button.scroll_visible(duration=0.5, top=True)
            except Exception:
                pass

    @on(TextArea.Changed)
    def on_text_changed(self, event: TextArea.Changed) -> None:
        """The Scribe's hand moves. The Gnostic Symphony begins."""
        if event.text_area.id == "input_pane":
            self.is_dirty = True
            self.run_worker(self._conduct_beautify_rite(event.text_area.text), name="BeautifyWorker", exclusive=True)

    def watch_is_dirty(self, is_dirty: bool) -> None:
        """The Sentinel of the Unsaved Soul proclaims the state of purity."""
        base_title = self.active_subtitle.replace(" *", "")
        self.active_subtitle = f"{base_title} *" if is_dirty else base_title

    def watch_active_subtitle(self, new_title: str) -> None:
        """A divine watcher that keeps the Sanctum's title in a state of Gnostic purity."""
        self.sub_title = new_title

    # --- The Asynchronous Gnostic Bridge ---

    async def on_beautify_success(self, message: BeautifySuccess) -> None:
        """
        The Conductor's soul is now pure. The profane `notify` for the Dossier
        is annihilated. The Gnosis is now inscribed upon a permanent, humble
        altar at the foot of the Prophecy. The Mentor's voice remains an
        ephemeral, willed proclamation.
        """
        res = message.result
        input_pane = self.query_one("#input_pane", TextArea)
        output_container = self.query_one("#output_container")

        # The Prophecy is proclaimed.
        prophecy_syntax = Syntax(res.beautified_code, input_pane.language, theme="monokai", line_numbers=True)
        self.query_one("#prophecy_pane").update(prophecy_syntax)

        # --- The Forging of the Dossier's Altar ---
        # The ephemeral `notify` is annihilated. The Dossier's Gnosis is now eternal.
        dossier_table = Table(title="Gnostic Dossier", box=None, show_header=False)
        dossier_table.add_column(style="dim", justify="right")
        dossier_table.add_column(style="cyan")
        dossier_table.add_row("Variables:", str(res.variable_count))
        dossier_table.add_row("Structure Items:", str(res.item_count))
        dossier_table.add_row("Maestro Edicts:", str(res.command_count))
        self.query_one("#dossier_pane").update(Panel(dossier_table, border_style="dim"))

        # The Mentor's Gnosis is proclaimed ephemerally, only when willed.
        if res.guidance_panels:
            self.notify(f"The Mentor has proclaimed {len(res.guidance_panels)} prophecies.", title="Gnostic Guidance",
                        severity="warning")
            self.push_screen(HeresyScreen(res.guidance_panels))

        # The display state is purified.
        self.query_one("#prophecy_pane").display = True
        self.query_one("#dossier_pane").display = True  # The Dossier is now always visible on success.
        self.query_one("#heresy_pane").display = False
        output_container.remove_class("heresy")

    async def on_beautify_error(self, message: BeautifyError) -> None:
        """
        The artisan's Gaze is now pure. It understands the new reality and righteously
        hides the Dossier's altar when a heresy is being proclaimed.
        """
        output_container = self.query_one("#output_container")
        heresy_pane = self.query_one("#heresy_pane")

        heresy_traceback = RichTraceback.from_exception(*message.exc_info, show_locals=True, word_wrap=True)
        heresy_pane.update(heresy_traceback)

        # The Rite of Gnostic Purity: All success-related panes are hidden.
        self.query_one("#prophecy_pane").display = False
        self.query_one("#dossier_pane").display = False
        heresy_pane.display = True
        output_container.add_class("heresy")

    @on(Switch.Changed, "#linter_switch")
    def on_linter_switch_changed(self, event: Switch.Changed) -> None:
        """The Architect has spoken. The Mentor's Gaze is now willed or stayed."""
        self.linter_enabled = event.value
        status = "awakened" if event.value else "stayed"
        self.notify(f"The Gnostic Mentor's Gaze has been {status}.", title="Linter Toggled")
        # Re-run the beautify rite to immediately see the effect.
        self.run_worker(
            self._conduct_beautify_rite(self.query_one("#input_pane", TextArea).text),
            name="BeautifyWorker",
            exclusive=True
        )
    # --- The Pantheon of Artisans & Edicts ---

    async def _conduct_beautify_rite(self, scripture: str) -> None:
        """The Asynchronous Gnostic Symphony of Beautification."""
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".scaffold", encoding='utf-8') as tf:
                tf.write(scripture)
                temp_path = Path(tf.name)

            items, commands = self.parser.parse_file(temp_path)
            guidance = conduct_architectural_inquest(items) if self.linter_enabled else []

            scribe = BlueprintScribe(project_root=temp_path.parent, alchemist=self.alchemist)
            beautiful_string = scribe.transcribe(items, commands, {}, rite_type='distillation')

            result = BeautifyResult(
                beautified_code=beautiful_string,
                item_count=len([i for i in items if not str(i.path).startswith('$$')]),
                command_count=len(commands),
                variable_count=len([i for i in items if str(i.path).startswith('$$')]),
                guidance_panels=guidance
            )
            self.post_message(BeautifySuccess(result))
        except (ArtisanHeresy, Exception):
            self.post_message(BeautifyError(sys.exc_info()))
        finally:
            if temp_path and temp_path.exists(): temp_path.unlink()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "paste_from_toast": self.action_paste_from_clipboard(); event.button.remove()

    @on(ListView.Selected)
    def on_command_selected(self, event: ListView.Selected) -> None:
        """The Architect has spoken a command from the Altar. The will is made manifest."""
        # This ward ensures we only listen to the one true Altar.
        if event.list_view.id == "command_palette":
            # The sacred map between the Gnostic ID and the Artisan's rite.
            command_map = {
                "cmd_new": self.action_new_file,
                "cmd_save": self.action_save_file,
                "cmd_save_as": self.action_save_as,
                "cmd_copy": self.action_copy_pure,
                "cmd_paste": self.action_paste_from_clipboard,
                "cmd_language": self.action_set_language,
                "cmd_quit": self.action_request_quit,
            }
            command_id = event.item.id

            # The Divine Delegation: The correct rite is summoned.
            if command_id in command_map:
                command_map[command_id]()

            # The Altar has served its purpose and returns to the void.
            self.action_toggle_command_palette()

    def action_load_file(self, file_path: Optional[Path]) -> None:
        """A divine rite to gaze upon a new or existing scripture."""
        input_pane = self.query_one("#input_pane", TextArea)
        self.file_path = file_path
        content_to_purify = ""

        if self.file_path and self.file_path.is_file():
            try:
                content = self.file_path.read_text(encoding="utf-8")
                language = LANGUAGE_GNOSIS_MAP.get(self.file_path.suffix, "text")
                self.active_subtitle = f"Gazing upon: {self.file_path.name}"
                input_pane.language = language
                input_pane.load_text(content)
                content_to_purify = content
                self.is_dirty = False
            except Exception as e:
                self.active_subtitle = "[red]Paradox Reading File...[/red]"
                content_to_purify = f"# A paradox occurred gazing upon the scripture:\n\n{e}"
                input_pane.load_text(content_to_purify)
                self.is_dirty = False
        else:
            self.file_path = None
            self.active_subtitle = "Unsaved Scripture"
            content_to_purify = "# A new, unsaved scripture. Speak your will."
            input_pane.load_text(content_to_purify)
            self.is_dirty = False

        self.call_later(self.run_worker, self._conduct_beautify_rite(content_to_purify), name="BeautifyWorker")

    def action_new_file(self) -> None:
        """The Rite of the Void. A new, unsaved scripture is born."""

        def _conduct_new_file_rite(confirmed: bool):
            if confirmed is not False: self.action_load_file(None); self.notify(
                "A new, unsaved scripture has been forged.", title="New Scripture")

        if self.is_dirty:
            self.push_screen(QuitScreen(), _conduct_new_file_rite)
        else:
            _conduct_new_file_rite(True)

    def action_save_file(self) -> None:
        """The Rite of Inscription."""
        if self.file_path:
            try:
                self.file_path.write_text(self.query_one("#input_pane", TextArea).text, encoding="utf-8")
                self.is_dirty = False
                self.notify(f"Scripture saved to '{self.file_path.name}'", title="Save Complete")
            except Exception as e:
                self.notify(f"A paradox occurred: {e}", title="Save Failed", severity="error")
        else:
            self.action_save_as()

    def action_save_as(self) -> None:
        self.notify("This rite will be fully ascended in a future version.", title="Prophecy")

    def action_set_language(self) -> None:
        self.notify("This rite will be fully ascended in a future version.", title="Prophecy")

    def action_copy_pure(self) -> None:
        if not PYPERCLIP_AVAILABLE: self.notify("The 'pyperclip' artisan is required.", severity="error"); return
        pure_pane_static = self.query_one("#prophecy_pane", Static)
        if pure_pane_static.display:
            try:
                syntax_renderable = pure_pane_static.renderable
                if isinstance(syntax_renderable, Syntax):
                    pyperclip.copy(syntax_renderable.code)
                    self.notify("The pure scripture's soul has been copied.", title="Copy Complete")
                else:
                    raise TypeError("Prophecy pane does not contain a Syntax object.")
            except Exception as e:
                self.notify(f"A paradox occurred: {e}", title="Copy Failed", severity="error")
        else:
            self.notify("Cannot copy a heresy.", title="Copy Heresy", severity="warning")

    def action_paste_from_clipboard(self) -> None:
        if not PYPERCLIP_AVAILABLE: self.notify("The 'pyperclip' artisan is required.", severity="error"); return
        try:
            self.query_one("#input_pane", TextArea).load_text(pyperclip.paste())
            self.notify("Gnosis from clipboard has been inscribed.", title="Paste Complete")
        except Exception as e:
            self.notify(f"A paradox occurred: {e}", title="Paste Failed", severity="error")

    def action_toggle_command_palette(self) -> None:
        """
        The Rite of the Ephemeral Altar. It now summons the Command Altar from
        the void as a true, non-blocking overlay, or returns it to the void.
        """
        try:
            # Gaze for the Altar. If it is manifest, it must be returned to the void.
            palette = self.query_one(CommandPalette)
            palette.remove()
        except Exception:
            # The Altar is a void. It must be summoned into reality.
            # We mount it directly onto the screen for a true overlay experience.
            self.app.mount(CommandPalette(id="command_palette"))
            self.query_one(CommandPalette).focus()

    def action_request_quit(self) -> None:
        if self.is_dirty:
            self.push_screen(QuitScreen())
        else:
            self.exit()


if __name__ == "__main__":
    pad = ScaffoldPad(sys.argv[1] if len(sys.argv) > 1 else None)
    pad.run()