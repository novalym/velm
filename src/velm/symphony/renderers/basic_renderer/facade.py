# Path: scaffold/symphony/renderers/basic_renderer/facade.py
# ----------------------------------------------------------

import traceback
from pathlib import Path
from typing import Dict, Any, Union, Optional, List

from rich.panel import Panel
from rich.text import Text
from rich.traceback import Traceback as RichTraceback
from rich.table import Table

from ..base import Renderer
from .emitter import BasicEmitter
from ....contracts.symphony_contracts import (
    ConductorEvent, EventType, SymphonyResult, Edict, ActionResult
)
from ....logger import Scribe

Logger = Scribe('BasicRendererFacade')


class BasicRenderer(Renderer):
    """
    =================================================================================
    == THE FORENSIC SCRIBE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                         ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000 (ABSOLUTE FIDELITY)

    The divine Scribe for non-interactive realms (CI/CD, logs). It speaks plainly
    but with deep Gnostic awareness. It has been ascended to a pure, event-driven
    artisan, its mind whole and its voice perfectly synchronized with the Conductor's
    will. It annihilates the "Staircase Heresy" by enforcing a strictly linear,
    non-indented proclamation of truth.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Event-Driven Soul:** The profane, stateful rendering loop is annihilated.
        Its mind is now a pure, event-driven `handle_event` rite, making its logic
        stateless and perfectly synchronized.

    2.  **The Atomic Emitter:** It delegates the physical act of writing to the
        `BasicEmitter`, a specialist artisan that ensures every line is timestamped,
        prefixed with a Gnostic sigil, and flushed instantly.

    3.  **The Gnostic Triage (`_rite_map`):** It wields a declarative dispatch table,
        a sacred map that teaches it the one true way to render every `EventType`,
        making its consciousness infinitely extensible.

    4.  **The Heresy Chronicler:** `PARADOX_PROCLAIMED` events are transmuted into
        luminous, detailed error reports with full, unabridged tracebacks.

    5.  **The Telemetry Scribe:** It perceives `ACTION_EPILOGUE` events,
        chronicling the duration and outcome of each kinetic rite with precision.

    6.  **The Luminous Prologue:** It proclaims the intent of every Action before it
        begins, creating a clear, readable narrative of the Symphony's will.

    7.  **The Unbreakable Stream (THE FIX):** The `update_live_stream` rite is now
        divine. It correctly bridges the raw output from the Kinetic Titan to the
        `BasicEmitter`, ensuring the voice of the child process is never lost.

    8.  **The Vow Adjudicator's Voice:** Renders the outcome of Vows (`??`) with a clear
        `Vow Upheld` or `Vow Broken` proclamation, including the Gnostic reason.

    9.  **The State Weaver's Voice:** Chronicles every metaphysical change (`%% let`, `%% sanctum`)
        to the Symphony's context with clarity.

    10. **The Unbreakable Contract:** It flawlessly honors every vow of the abstract `Renderer`
        contract, its soul pure and its purpose absolute.

    11. **The Interactive Guardian:** Its `conduct_interactive_plea` provides a safe,
        blocking prompt for `?? confirm` rites, respecting the Architect's will.

    12. **The Final Dossier:** Its `render_summary_dossier` provides a complete,
        forensic summary of the Symphony's entire journey, a final word of truth.
    """

    def __init__(self, conductor):
        super().__init__(conductor)
        self.emitter = BasicEmitter()

        # [FACULTY 3] The Gnostic Triage Map
        self._rite_map = {
            EventType.SYMPHONY_START: self._on_symphony_start,
            EventType.SYMPHONY_END: self._on_symphony_end,

            # This is the specific, high-level event we want to handle.
            EventType.ACTION_PROLOGUE: self._on_action_prologue,

            EventType.ACTION_EPILOGUE: self._on_action_epilogue,
            # LOG events are handled by update_live_stream.
            EventType.PARADOX_PROCLAIMED: self._on_paradox,
            EventType.STATE_CHANGE: self._on_state_change,
            EventType.VOW_RESULT: self._on_vow_result,

            # We explicitly ignore the low-level events that cause the echo.
            EventType.EDICT_START: lambda p: None,
            EventType.EDICT_SUCCESS: lambda p: None,
            EventType.EDICT_FAILURE: lambda p: None,
        }

    def handle_event(self, event: ConductorEvent):
        """The Grand Router of Events."""
        handler = self._rite_map.get(event.type)
        if handler:
            handler(event.payload)

    # --- EVENT HANDLERS ---

    def _on_symphony_start(self, payload: Dict):
        path = payload.get("symphony_path", "Unknown")
        sanctum = payload.get("sanctum", "Unknown")
        self.emitter.emit_block(f"Symphony: {path}")
        self.emitter.emit_meta(f"Sanctum: {sanctum}", icon_key="info")

    def _on_symphony_end(self, payload: Dict):
        success = payload.get("success", False)
        duration = payload.get("duration", 0.0)

        style = "success" if success else "failure"
        msg = f"SYMPHONY {'COMPLETED' if success else 'FAILED'} in {duration:.2f}s"

        self.emitter.emit_block(f"[{style}]{msg}[/{style}]")

    def _on_action_prologue(self, payload: Dict):
        self.emitter.emit_prologue(payload.get("command", "Unknown Command"))

    def _on_action_epilogue(self, payload: Dict):
        self.emitter.emit_epilogue(payload.get("result", {}))

    def _on_state_change(self, payload: Dict):
        key = payload.get("key", "?")
        value = str(payload.get("value", "?"))
        # Redact secrets before they are even passed to the emitter
        if "secret" in key.lower() or "token" in key.lower() or "key" in key.lower():
            value = "***"
        self.emitter.emit_state(key, value)

    def _on_vow_result(self, payload: Dict):
        self.emitter.emit_vow(payload.get("reason", ""), payload.get("success", False))

    def _on_paradox(self, payload: Dict):
        self.emitter.emit_heresy(payload.get("message", "Unknown Paradox"), payload.get("traceback", ""))

    # --- DIRECT INTERFACE IMPLEMENTATIONS ---

    def render_action_prologue(self, edict: Edict, transmuted_command: str, sanctum: Path):
        """
        The Luminous Prologue. Announces the start of a kinetic rite.
        """
        self.emitter.emit_prologue(transmuted_command)

    def render_action_epilogue(self, live_context: Any, result: ActionResult):
        """
        The Final Verdict. Announces the conclusion of the rite.
        """
        self.emitter.emit_epilogue(result.model_dump())

    def update_live_stream(self, live_context: Any, line: Union[str, Any]):
        """
        [THE UNBREAKABLE STREAM]
        The divine rite that inscribes the living soul of a child process into the chronicle.
        This is the definitive fix for the "Silent Output" heresy.
        """
        content = str(line).rstrip()
        if content:
            self.emitter.emit_stream(content)

    def render_vow_result(self, is_pure: bool, reason: str, edict: 'Edict'):
        self.emitter.emit_vow(reason, is_pure)

    def render_state_change(self, key: str, value: str, relative_sanctum: Path):
        self.emitter.emit_state(key, value)

    def render_paradox(self, heresy: Exception, traceback_obj: Any, captured_output: Optional[str] = None):
        """Renders catastrophic failures."""
        if isinstance(heresy, ArtisanHeresy):
            self.emitter.emit_heresy(heresy.message, heresy.details or "")
        else:
            tb_str = "".join(traceback.format_exception(type(heresy), heresy, traceback_obj))
            self.emitter.emit_heresy(str(heresy), tb_str)

    def conduct_interactive_plea(self, prompt_text: str, default: bool = True) -> bool:
        """Proxies to simple input."""
        from rich.prompt import Confirm
        return Confirm.ask(prompt_text, default=default)

    def render_summary_dossier(self, result: SymphonyResult):
        """Renders the final report."""
        if self.conductor and self.conductor.is_simulation: return
        self.emitter.console.print()

        table = Table(title="[bold]Symphony Dossier[/bold]", box=None, show_header=False)
        table.add_column(style="dim", justify="right")
        table.add_column(style="bold")

        table.add_row("Duration:", f"{result.duration:.2f}s")
        table.add_row("Edicts Conducted:", str(result.edicts_executed))

        final_panel = Panel(
            table,
            title="[bold green]SYMPHONY COMPLETE[/bold green]" if result.success else "[bold red]SYMPHONY FAILED[/bold red]",
            border_style="green" if result.success else "red",
            expand=False
        )
        self.emitter.console.print(final_panel)

    # --- STUBS FOR UNUSED/DEPRECATED RITES ---
    def prologue(self, *args, **kwargs):
        pass

    def epilogue(self, *args, **kwargs):
        pass

    def render_polyglot_prologue(self, *args, **kwargs):
        pass

    def render_proclamation(self, message: str, *args, **kwargs):
        self.emitter.emit_meta(message, style_key="info", icon_key="info")

    def render_block_prologue(self, *args, **kwargs):
        pass

    def render_block_epilogue(self, *args, **kwargs):
        pass

    def render_intercession_altar(self, *args, **kwargs):
        pass

    def render_comment(self, raw_scripture: str):
        self.emitter.emit_meta(raw_scripture, style_key="meta")

    def render_foreign_adjudication(self, *args, **kwargs):
        pass

    def render_structured_status(self, *args, **kwargs):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass