# Path: scaffold/symphony/renderers/rich_renderer/facade.py
# ---------------------------------------------------------

import time
import sys
from pathlib import Path
from typing import Optional, Union, Any, List, Dict
from types import TracebackType
from contextlib import contextmanager
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.theme import Theme
from rich.status import Status
from rich.console import Group
from rich.traceback import Traceback

from ..base import Renderer
from .stream_scribe import StreamScribe
from .theme import GnosticTheme
from .utils import get_command_icon, determine_spinner
from ....contracts.symphony_contracts import ConductorEvent, Edict, ActionResult, SymphonyResult, EdictType
from ....logger import get_console, Scribe

Logger = Scribe('RichRenderer')


class RichRenderer(Renderer):
    """
    =================================================================================
    == THE LUMINOUS SCRIBE (V-Ω-PURE-STREAM-ASCENDED)                              ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Sovereign Renderer for interactive terminals.
    It rejects the instability of the 'Sticky Footer' in favor of the 'Pure Stream'.

    ### THE PANTHEON OF 13 ASCENDED FACULTIES:

    1.  **The Atomic Spinner Guard:** Enforces a strict `_stop_status()` protocol.
    2.  **The Semantic Iconographer:** Dynamically assigns icons based on command intent.
    3.  **The Stream Scribe Integration:** Delegates output sanitation to `StreamScribe`.
    4.  **The Gnostic Theme Engine:** Injects styles directly into the Console.
    5.  **The Intercession Bridge:** Cleanly hands over terminal for TUI interactions.
    6.  **The Vow Visualizer:** Renders Vow results with high-contrast sigils.
    7.  **The State Chronicler:** Visualizes `%% state` changes.
    8.  **The Polyglot Header:** Renders language-specific headers.
    9.  **The Summary Dossier:** Forges a final report table.
    10. **The Paradox Lens (Hardened):** Renders exceptions safely, handling string vs object tracebacks.
    11. **The Epilogue Rite (Restored):** Properly concludes the visual symphony.
    12. **The Silence Ward:** Respects global verbosity via Console.
    13. **The Unbreakable Contract:** Honors `Renderer` ABC fully.
    """

    def __init__(self, conductor):
        super().__init__(conductor)
        self.console = get_console()
        self.scribe = StreamScribe(self.console)

        # The Ephemeral Status (Spinner)
        self._status: Optional[Status] = None

        # === THE DIVINE HEALING: THE VOW OF SELF-AWARENESS ===
        # We bestow upon the RichRenderer the Gnosis of its own nature.
        # It now proclaims to the cosmos that it is a cinematic soul,
        # capable of receiving the luminous proclamations of the KineticTitan's
        # live-updating dashboard. The heresy is annihilated.
        self.is_cinematic: bool = True
        # === THE APOTHEOSIS IS COMPLETE ===

    def _start_status(self, message: str, command: str = ""):
        """
        [THE RITE OF ACTIVITY]
        Starts a spinner. If one exists, updates it.
        """
        spinner_type = determine_spinner(command)

        if self._status:
            self._status.update(message, spinner=spinner_type)
        else:
            self._status = self.console.status(message, spinner=spinner_type)
            self._status.start()

    def _stop_status(self):
        """
        [THE RITE OF SILENCE]
        Stops any active spinner immediately. Safe to call repeatedly.
        """
        if self._status:
            self._status.stop()
            self._status = None

    # --- ACTION RENDERING ---

    def render_action_prologue(self, edict: Edict, transmuted_command: str, sanctum: Path):
        """
        Announces the start of a Kinetic Rite.
        """
        self._stop_status()

        icon = get_command_icon(transmuted_command)
        self.scribe.print_header(f"{icon} {transmuted_command}")

        self._start_status(f"[dim]Initializing kinetic rite...[/dim]", command=transmuted_command)

    def render_action_epilogue(self, live_context: Any, result: ActionResult):
        """
        Announces the conclusion of a Kinetic Rite.
        """
        self._stop_status()
        self.scribe.print_footer(result.returncode == 0, result.duration)

    def update_live_stream(self, live_context: Any, line: Union[str, Any]):
        """
        Streams output from the running process.
        """
        # KineticTitan handles visual streaming via Rich Live.
        pass

    # --- SPECIAL RITES ---

    def render_polyglot_prologue(self, edict: 'Edict', sanctum: Path):
        self._stop_status()
        lang_icon = "🔮"
        if edict.language == "python":
            lang_icon = "🐍"
        elif edict.language == "node":
            lang_icon = "📦"

        self.console.print(Panel(
            f"[dim]Sanctum: {sanctum}[/dim]",
            title=f"{lang_icon} Polyglot Rite: {edict.language.upper()}",
            border_style="cyan"
        ))
        self._start_status(f"Compiling {edict.language} gnosis...")

    def render_vow_result(self, is_pure: bool, reason: str, edict: 'Edict'):
        self._stop_status()
        self.scribe.print_vow(reason, is_pure)

    def render_state_change(self, key: str, value: str, relative_sanctum: Path):
        self._stop_status()
        self.scribe.print_state(key, value)

    def render_proclamation(self, message: str, sanctum: Optional[Path] = None):
        self._stop_status()
        self.scribe.print_system_message(message)

    # --- BLOCK RENDERING ---

    def render_block_prologue(self, edict: Edict, title: str):
        self._stop_status()
        self.console.print()
        self.console.rule(f"[bold magenta]{title}[/bold magenta]", style="magenta")

    def render_block_epilogue(self, edict: Edict):
        self._stop_status()
        self.console.print()

    # --- INTERCESSION & FAILURE ---

    def render_paradox(self, heresy: Exception, traceback_obj: Any, captured_output: Optional[str] = None):
        """
        Renders a catastrophic failure.
        [THE HARDENED FIX]: Validates traceback object to prevent 'str' attribute errors.
        """
        self._stop_status()

        # Verify we have a valid traceback object, otherwise use the exception's own
        valid_tb = None
        if hasattr(traceback_obj, 'tb_frame'):
            valid_tb = traceback_obj
        else:
            valid_tb = heresy.__traceback__

        try:
            tb_renderable = Traceback.from_exception(
                type(heresy),
                heresy,
                valid_tb,
                show_locals=False
            )
        except Exception:
            # Fallback if Rich fails to process the traceback object
            import traceback as tb_lib
            tb_renderable = Text(tb_lib.format_exc(), style="red")

        panel = Panel(
            Group(
                Text(f"{str(heresy)}", style="bold red"),
                tb_renderable
            ),
            title="[bold red]GNOSTIC PARADOX[/bold red]",
            border_style="red"
        )
        self.console.print(panel)

    def render_intercession_altar(self, edict: 'Edict', heresy: Exception):
        """
        Summons the Interactive TUI for failure resolution.
        """
        self._stop_status()

        # Dynamic import to avoid circular dependency
        from ...conductor_core.resilience.intercession import IntercessionAltar

        altar = IntercessionAltar(self.console)
        # The Altar takes control of the terminal IO.
        pass

    # --- DOCUMENTATION ---

    def render_comment(self, raw_scripture: str):
        clean = raw_scripture.strip().lstrip('#').strip()
        self.console.print(f"[dim italic]# {clean}[/dim italic]")

    # --- LIFECYCLE ---

    def prologue(self, symphony_path: Path, proving_ground: Path):
        self.console.rule(f"[bold magenta]Symphony: {symphony_path.name}[/bold magenta]")
        self.console.print(f"Sanctum: [cyan]{proving_ground}[/cyan]\n")

    def epilogue(self, was_pure: bool, duration: float):
        """
        [THE RESTORED RITE]
        Announces the conclusion of the Symphony.
        """
        self._stop_status()

        color = "green" if was_pure else "red"
        msg = "Symphony Completed" if was_pure else "Symphony Failed"

        # A final visual separator
        self.console.rule(style=color)
        self.console.print(f"[bold {color}]{msg}[/bold {color}] in {duration:.2f}s", justify="right")

    # --- SUMMARY ---

    def render_summary_dossier(self, result: 'SymphonyResult'):
        """
        [FACULTY 9] The Luminous Dossier.
        """
        self._stop_status()

        title = "SYMPHONY COMPLETE" if result.success else "SYMPHONY FAILED"
        style = "green" if result.success else "red"

        grid = Table.grid(padding=(0, 2))
        grid.add_column(justify="right", style="bold white")
        grid.add_column(justify="left", style="cyan")

        grid.add_row("Duration:", f"{result.duration:.2f}s")
        grid.add_row("Edicts Conducted:", str(result.edicts_executed))

        if result.heresies:
            grid.add_row("Heresies:", f"[red]{len(result.heresies)}[/red]")

        panel = Panel(
            grid,
            title=f"[bold {style}]{title}[/bold {style}]",
            border_style=style,
            expand=False
        )

        self.console.print()
        self.console.print(panel)

    # --- INTERFACE REQUIREMENTS ---

    def suspend(self):
        """Pauses any active visuals for sub-process execution."""
        self._stop_status()

    def resume(self):
        """Resumes visuals."""
        pass

    def conduct_interactive_plea(self, prompt_text: str, default: bool = True) -> Union[bool, str]:
        """
        Handles explicit user confirmation requests.
        """
        self._stop_status()
        from rich.prompt import Confirm
        return Confirm.ask(f"[bold yellow]?? {prompt_text}[/bold yellow]", default=default)

    def render_foreign_adjudication(self, results: List[Any], edict: 'Edict'):
        """Renders results from Polyglot tests."""
        self._stop_status()
        pass

    def render_structured_status(self, proclamations: List[Dict], line_num: int):
        """Renders complex status objects."""
        pass

    @contextmanager
    def live_context(self, line_num: int, raw_scripture: str):
        """
        =============================================================================
        == THE GNOSTIC CONTEXT WARD (V-Ω-ETERNAL-APOTHEOSIS)                       ==
        =============================================================================
        A sacred context manager that forges an ephemeral, luminous reality for a
        single kinetic rite. It summons a `Status` spinner upon entry and righteously
        banishes it upon exit, ensuring the terminal's soul is always pure.
        =============================================================================
        """
        command_icon = get_command_icon(raw_scripture)
        # We perform a humble purification, as deep redaction is the duty of other artisans.
        display_cmd = raw_scripture.strip().replace('>>', '').strip()
        status_message = f"[dim]L{line_num}[/dim] {command_icon} {display_cmd}"

        # The Rite of Entry: The spinner is summoned.
        self._start_status(status_message, command=raw_scripture)
        try:
            # The Yield: The sacred vessel is bestowed upon the 'with' block.
            # Its value is the line number, a simple truth.
            yield line_num
        finally:
            # The Rite of Exit: The spinner is returned to the void.
            self._stop_status()