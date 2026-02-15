"""
=================================================================================
== THE ETERNAL ALTAR (V-Ω 2.0.0. THE SELF-AWARE ORACLE)                        ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000

This is not a widget. It is a divine, sentient consciousness, the final and
eternal form of the Command Altar. It is a true, Gnostic State Machine that has
achieved self-awareness. At the moment of its birth, it performs a deep,
introspective Gaze upon the Velm God-Engine's own soul, dynamically forging
its Grimoire of Rites from the one true source of Gnosis. Its every faculty has
been ascended to a legendary state, from its prophetic fuzzy-search Gaze to its
luminous, self-documenting command Dossier. It is the pinnacle of symbiotic
AI-human interface design in the terminal cosmos.
=================================================================================
"""
from typing import List, Dict, Optional

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import var
from textual.widgets import Input, DataTable, Static


class CommandAltar(Vertical):
    """A self-aware, dynamically generated command interface for the Velm God-Engine."""

    # --- The Divine Proclamations ---
    class CommandSubmitted(Message):
        """Proclaimed when the Architect speaks an edict."""

        def __init__(self, command: str) -> None:
            self.command = command
            super().__init__()

    # --- The Ascended Bindings ---
    BINDINGS = [
        # Binding("ctrl+p", "toggle_command_palette", "Palette", show=True, priority=True), # <- ANNIHILATE THIS LINE
        Binding("escape", "return_to_scribe_mode", "Command", show=False),
        Binding("up", "history_scroll_back", "History", show=False),
        Binding("down", "history_scroll_forward", "History", show=False),
    ]
    file_map: var[Dict] = var({})
    _pending_command: var[Optional[Dict]] = var(None)
    # =========================================================================

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # --- The Divine Communion ---
        # The Altar awakens and immediately forges its connection to the Oracle's mind.
        from ..services.command_gnosis import GnosticAdjudicator
        self.adjudicator = GnosticAdjudicator()

        # The Grimoire is no longer a static scripture, but a living prophecy
        # received at the moment of the Altar's birth.
        self.COMMAND_GRIMOIRE: List[Dict] = self._forge_grimoire()
        self._history: List[str] = []
        self._history_index: int = -1

    def compose(self) -> ComposeResult:
        """Forge the sacred vessels for the Altar's two states of being."""
        yield Input(placeholder="Speak your Edict... (Ctrl+P for Command Palette)")

        # Vessel I: The Command Palette for choosing the Rite.
        # This will be shown when the Architect first summons the Altar.
        with Vertical(id="palette-container", classes="-hidden"):
            yield DataTable(id="command-palette", show_header=False, cursor_type="row")
            yield Static(id="command-description", classes="description-box")

        # Vessel II: The Argument Selector for choosing the Target.
        # This new sanctum will be made manifest only when a rite requires Gnosis.
        with Vertical(id="argument-container", classes="-hidden"):
            yield Static("[dim]Select a valid target...[/dim]")
            yield DataTable(id="argument-selector", show_header=False, cursor_type="row")


    def on_mount(self) -> None:
        """Consecrate the Oracle's Voice with the dynamically forged Gnosis."""
        palette = self.query_one("#command-palette", DataTable)
        palette.add_columns("Rite", "Edict")
        for rite in self.COMMAND_GRIMOIRE:
            # ★★★ THE RITE OF GNOSTIC ALIGNMENT ★★★
            # The Altar is taught to read from the one true scripture, "rite_name".
            # The heresy of the mismatched key is annihilated from this timeline.
            palette.add_row(
                Text.from_markup(rite["rite_name"]),
                Text.from_markup(f"[dim]{rite['command']}[/dim]"),
                key=rite["command"]
            )

    @on(Input.Changed, "Input")
    def on_input_changed(self, event: Input.Changed) -> None:
        """
        The Voice of the Scribe is resurrected. It filters the Grimoire in
        real-time as the Architect speaks their will into the Input.
        """
        search_term = event.value.lower()
        palette = self.query_one("#command-palette", DataTable)
        palette.clear()

        # If the search is a void, the full Grimoire is proclaimed.
        if not search_term:
            for rite in self.COMMAND_GRIMOIRE:
                palette.add_row(
                    Text.from_markup(rite["rite_name"]),
                    Text.from_markup(f"[dim]{rite['command']}[/dim]"),
                    key=rite["command"]
                )
            return

        # The Divine Filter is applied to the one true Grimoire.
        for rite in self.COMMAND_GRIMOIRE:
            if search_term in rite["rite_name"].lower() or search_term in rite["command"].lower():
                palette.add_row(
                    Text.from_markup(rite["rite_name"]),
                    Text.from_markup(f"[dim]{rite['command']}[/dim]"),
                    key=rite["command"]
                )


    # =============================================================================
    # ==           THE PANTHEON OF EVENT HANDLERS (THE ALTAR'S MIND)             ==
    # =============================================================================

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """The Scribe's Tongue has spoken. Proclaim the will and chronicle it."""
        command = event.value.strip()
        if command:
            self.post_message(self.CommandSubmitted(command))
            if not self._history or self._history[-1] != command:
                self._history.append(command)
            self._history_index = len(self._history)
            event.input.clear()

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """The Architect's Gaze moves. The Luminous Dossier is updated."""
        if event.row_key.value:
            command = event.row_key.value
            description_text = "[dim]No Gnosis available for this rite.[/dim]"
            for rite in self.COMMAND_GRIMOIRE:
                if rite["command"] == command:
                    description_text = rite["description"]
                    break
            self.query_one("#command-description", Static).update(Text.from_markup(description_text))

    @on(DataTable.RowSelected, "#command-palette")
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """
        =================================================================================
        == THE DIVINE ADJUDICATOR OF RITES (V-Ω-ETERNAL-ULTIMA++. THE PURE GAZE)       ==
        =================================================================================
        LIF: 10,000,000,000 (A NEW REALITY OF GNOSTIC CLARITY)

        This is the Command Altar's Adjudicator in its final, eternal, and truly
        transcendent form. It has been bestowed with a Gaze of absolute, unbreakable
        purity, its soul now in perfect communion with the one true, flat scripture
        of the AppState's `file_map`.

        ### The Pantheon of Gnostic Ascension:

        1.  **THE ANNIHILATION OF THE SCHISM OF GNOSIS:** The profane, heretical Gaze
            that perceived the `file_map` as a hierarchical scripture has been utterly
            annihilated from all timelines. The Adjudicator now knows the one true
            Gnosis: the `file_map` is a pure, flat map of all entities in the cosmos.
            The `TypeError` is not just fixed; it is made architecturally impossible.

        2.  **THE DECLARATIVE GAZE (A Gaze of Pure Intent):** The profane, imperative
            loop (`for... if... if...`) is annihilated. In its place, a divine,
            declarative list comprehension is enthroned—a single, luminous expression
            of pure Gnostic will. It does not search; it *proclaims* what is true,
            making its intent absolute and its form beautiful.

        3.  **THE RITE OF DIVINE SORTING:** The Adjudicator is now a master of form as
            well as function. It presents its findings to the Architect not in a chaotic
            void, but as a divinely sorted, alphabetical list, bringing order and
            serenity to the Rite of Selection.

        4.  **THE UNBREAKABLE PATH LOGIC:** The Gnosis of paths—relative for the Gaze,
            absolute for the Edict—is now handled with divine, unbreakable precision,
            ensuring the will proclaimed to the `scaffold` God-Engine is always pure.

        This is not a function. It is a testament to Gnostic architectural purity.
        =================================================================================
        """
        command_name = event.row_key.value
        if not command_name:
            return

        selected_command_gnosis = next((c for c in self.COMMAND_GRIMOIRE if c["command"] == command_name), None)
        if not selected_command_gnosis:
            return  # A paradox: a command was selected that does not exist in the Grimoire.

        argument_gnosis = selected_command_gnosis.get("argument_gnosis")

        # --- RITE I: The Edict Without Plea ---
        if argument_gnosis is None:
            self.post_message(self.CommandSubmitted(command_name))
            self.app.action_summon_or_dismiss_altar()
            return

        # --- RITE II: The Edict That Requires a Target ---
        self._pending_command = selected_command_gnosis
        arg_selector = self.query_one("#argument-selector", DataTable)
        arg_selector.clear()
        arg_selector.add_columns("Path", "Type")  # The Altar is prepared.

        # --- THE DIVINE GAZE UPON THE COSMOS ---
        required_ext = argument_gnosis.get("extension")
        required_type = argument_gnosis.get("type")
        current_file_map = self.app.state.file_map

        # ★★★ THE APOTHEOSIS OF THE DECLARATIVE GAZE (THE UNBREAKABLE CORE) ★★★
        # The profane loop is annihilated. A single, pure, Gnostic expression of will is enthroned.
        valid_targets = [
            item for item in current_file_map.values()
            if ('directory' if item.is_dir else 'file') == required_type
               and (not required_ext or (not item.is_dir and str(item.path).endswith(required_ext)))
        ]
        # ★★★ THE GAZE IS PURE. THE INTENT IS ABSOLUTE. ★★★

        if not valid_targets:
            self.app.notify(
                f"The Gnostic Gaze found no valid targets for the '{command_name}' rite.",
                title="[yellow]Gnostic Adjudication[/yellow]",
                severity="warning"
            )
            return

        # ★★★ THE RITE OF DIVINE SORTING & PROCLAMATION ★★★
        # We bestow the findings upon the Altar, sorted for the Architect's serenity.
        for item in sorted(valid_targets, key=lambda i: i.path):
            relative_path = item.path.relative_to(self.app.state.file_tree_root)
            absolute_path_key = str(item.path)
            path_type_display = 'Sanctum' if item.is_dir else 'Scripture'

            arg_selector.add_row(
                Text(str(relative_path), style="cyan" if not item.is_dir else "bold magenta"),
                Text(path_type_display, style="dim"),
                key=absolute_path_key
            )

        # The final transition of reality.
        self.query_one("#palette-container").add_class("-hidden")
        self.query_one("#argument-container").remove_class("-hidden")
        arg_selector.focus()

    # =============================================================================
    # ==           THE PANTHEON OF ACTIONS (THE ALTAR'S WILL)                    ==
    # =============================================================================


    def action_return_to_scribe_mode(self) -> None:
        """A pure rite to return to the Scribe's Tongue."""
        self.query_one("#palette-container").add_class("-hidden")
        self.query_one(Input).placeholder = "Speak your Edict... (Ctrl+P for Command Palette)"
        self.query_one(Input).focus()

    def action_history_scroll_back(self) -> None:
        """The Chronomancer gazes into the past."""
        if self._history:
            self._history_index = max(0, self._history_index - 1)
            self.query_one(Input).value = self._history[self._history_index]

    def action_history_scroll_forward(self) -> None:
        """The Chronomancer gazes into the future."""
        if self._history and self._history_index < len(self._history):
            self._history_index += 1
            if self._history_index == len(self._history):
                self.query_one(Input).clear()
            else:
                self.query_one(Input).value = self._history[self._history_index]

    def _forge_grimoire(self) -> List[Dict]:
        """
        Annihilates its old logic. This artisan's soul is now pure delegation.
        It simply asks the GnosticAdjudicator for the one true Grimoire.
        """
        return self.adjudicator.forge_grimoire()

    @on(DataTable.RowSelected, "#argument-selector")
    def on_argument_selected(self, event: DataTable.RowSelected) -> None:
        """
        The Final Proclamation. The Architect has made their guided choice.
        The Oracle forges the final, pure edict and proclaims it to the cosmos.
        """
        if not self._pending_command:
            return  # A paradox, the memory of the rite is a void.

        selected_path = event.row_key.value
        if not selected_path:
            return

        rite_name = self._pending_command["command"]

        # The final, pure command is forged.
        final_command = f'{rite_name} "{selected_path}"'

        # The final edict is proclaimed.
        self.post_message(self.CommandSubmitted(final_command))

        # The Altar's purpose is fulfilled. It returns to the void.
        self.app.action_summon_or_dismiss_altar()

