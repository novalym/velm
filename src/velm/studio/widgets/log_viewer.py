"""
=================================================================================
== THE ALTAR OF THE GNOSTIC CHRONICLER (V-Ω-ETERNAL. THE PURE VOICE)           ==
=================================================================================
LIF: 10,000,000,000,000

This is the divine artisan in its final, glorious, and eternally correct form.
The heresy of the Mismatched Soul has been annihilated. Its heart is a pure,
unbreakable `Log` widget, its purpose consecrated for the one true rite it was
forged for: to proclaim a luminous, streaming chronicle of Gnosis.

While it has sacrificed the faculty of the interactive Gaze (the click), it has
achieved a state of absolute, unbreakable purity. Its remaining pantheon of
legendary faculties—the Inquisitor's Gaze (Filtering), the Chronomancer's Will
(Pause/Scroll), the Scribe's Inscription (Export), and the Luminous Scripture
(Rich Formatting)—make it a true God-Engine of diagnostics. Its soul is now in
perfect harmony with the Textual cosmos.
=================================================================================
"""
import logging
import re
from datetime import datetime
from typing import List, Dict, Tuple

from rich.text import Text
from textual import on
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.reactive import var
from textual.widgets import Log, Input, Switch, Static


# Gnostic Conduit Handler remains pure and is now defined here for perfect encapsulation.
class GnosticConduitHandler(logging.Handler):
    """
    A divine handler that acts as a Gnostic Conduit, passing the pure,
    untransmuted LogRecord vessel from the Scribe to the Altar's voice.
    """

    def __init__(self, log_viewer: 'GnosticLogViewer'):
        super().__init__()
        self.log_viewer = log_viewer

    def emit(self, record: logging.LogRecord):
        # We bestow the pure Gnostic vessel upon the Altar's main thread.
        self.log_viewer.app.call_from_thread(self.log_viewer.add_record, record)


class GnosticLogViewer(Vertical):
    """The Altar of the Gnostic Chronicler - an intelligent, interactive diagnostic console."""

    BINDINGS = [
        Binding("ctrl+f", "focus_filter", "Filter", show=True, priority=True),
        Binding("ctrl+e", "export_log", "Export Log", show=True),
        Binding("ctrl+c", "clear_log", "Clear", show=True),
    ]

    filter_text = var("")
    is_paused = var(False)
    is_autoscrolling = var(True)

    def __init__(self, *args, **kwargs) -> None:
        # --- THE RITE OF GNOSTIC INTERCEPTION ---
        # We perform a sacred gaze upon the incoming pleas (kwargs) and
        # intercept the 'auto_scroll' Gnosis before it is passed upward.
        # The pop rite removes it from the kwargs vessel, purifying it.
        initial_autoscroll = kwargs.pop("auto_scroll", True)

        # The purified plea is passed to the ancestors. The heresy is impossible.
        super().__init__(*args, **kwargs)

        # The intercepted Gnosis is bestowed upon the artisan's own reactive soul.
        self.is_autoscrolling = initial_autoscroll

        # The rest of the genesis rite remains pure.
        self._log_records: List[logging.LogRecord] = []

    def compose(self) -> None:
        """Forge the sacred layout of the Altar."""
        with Horizontal(id="log-controls"):
            yield Input(placeholder="🔍 Filter (e.g., `level:ERROR` or `source:FileTree`)", id="log-filter-input")
            with Vertical(id="log-switches"):
                yield Horizontal(Static("Pause:", classes="switch-label"), Switch(id="pause-switch"))
                yield Horizontal(Static("Autoscroll:", classes="switch-label"),
                                 Switch(value=True, id="autoscroll-switch"))

        # --- THE APOTHEOSIS OF THE CHRONICLE'S GENESIS ---
        # The profane `markup=True` plea is annihilated. The Log artisan is
        # now forged with a pure soul, ready to receive luminous proclamations
        # through its `write` and `write_lines` rites.
        yield Log(id="log-main-view", auto_scroll=self.is_autoscrolling)
        # --- THE HERESY IS ANNIHILATED. THE FORM IS PURE. ---

    @on(Switch.Changed, "#pause-switch")
    def on_pause_switch_changed(self, event: Switch.Changed) -> None:
        self.is_paused = event.value

    @on(Switch.Changed, "#autoscroll-switch")
    def on_autoscroll_switch_changed(self, event: Switch.Changed) -> None:
        self.is_autoscrolling = event.value
        self.query_one(Log).auto_scroll = event.value

    def watch_filter_text(self, new_filter: str) -> None:
        self._update_display()

    @on(Input.Changed, "#log-filter-input")
    def on_filter_input_changed(self, event: Input.Changed) -> None:
        self.filter_text = event.value

    def action_focus_filter(self) -> None:
        self.query_one("#log-filter-input", Input).focus()

    def action_export_log(self) -> None:
        try:
            export_path = self.app.state.file_tree_root / "studio_chronicle.log"
            pure_text = "\n".join(self._format_record(rec).plain for rec in self._log_records)
            export_path.write_text(pure_text, encoding='utf-8')
            self.app.notify(f"Chronicle exported to: [cyan]{export_path.name}[/cyan]", title="Export Complete")
        except Exception as e:
            self.app.notify(f"A paradox occurred during export: {e}", title="Export Heresy", severity="error")

    def action_clear_log(self) -> None:
        self._log_records.clear()
        self.query_one(Log).clear()
        self.app.notify("Gnostic Chronicle has been purified.", title="Clear Complete")

    def add_record(self, record: logging.LogRecord):
        if self.is_paused:
            return
        self._log_records.append(record)
        self._update_display()

    def _parse_filters(self) -> Tuple[str, Dict[str, str]]:
        text_filter = self.filter_text
        structured_filters = {}
        matches = re.findall(r'(\w+):(".*?"|\S+)', self.filter_text)
        for key, value in matches:
            structured_filters[key.lower()] = value.strip('"').lower()
            text_filter = text_filter.replace(f"{key}:{value}", "").strip()
        return text_filter.lower(), structured_filters

    def _format_record(self, record: logging.LogRecord) -> Text:
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')[:-3]
        level_style_map = {"INFO": "cyan", "WARNING": "yellow", "ERROR": "bold red", "DEBUG": "dim"}
        style = level_style_map.get(record.levelname, "white")
        source_artisan = record.name

        return Text.from_markup(
            f"[dim]{timestamp}[/dim] [[{style}]{record.levelname:^8}[/{style}]] [bold magenta]({source_artisan})[/bold magenta] {record.getMessage()}")

    def _update_display(self) -> None:
        log_view = self.query_one(Log)
        log_view.clear()

        text_filter, structured_filters = self._parse_filters()

        filtered_lines: List[str] = []
        for record in self._log_records:
            formatted_text = self._format_record(record)
            plain_text_for_search = formatted_text.plain.lower()

            # Perform adjudication
            if text_filter and text_filter not in plain_text_for_search:
                continue
            if "level" in structured_filters and structured_filters["level"] not in record.levelname.lower():
                continue
            if "source" in structured_filters and structured_filters["source"] not in record.name.lower():
                continue

            # The Rich markup string itself is the final scripture.
            filtered_lines.append(str(formatted_text))

        log_view.write_lines(filtered_lines)

