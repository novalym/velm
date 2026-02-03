# Path: scaffold/symphony/renderers/stream_renderer/facade.py
# -----------------------------------------------------------

import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from ..base import Renderer
from .emitter import LinearEmitter
from ....contracts.symphony_contracts import (
    ConductorEvent, EventType, SymphonyResult, Edict, ActionResult
)
from ....logger import Scribe

Logger = Scribe('StreamRenderer')


class StreamRenderer(Renderer):
    """
    =================================================================================
    == THE LINEAR PROPHET (V-Ω-MODULAR-ASCENSION-STREAMING)                        ==
    =================================================================================
    LIF: 10,000,000,000,000 (THE RAW TRUTH)

    The Ascended Stream Renderer. A robust, linear renderer that proclaims events
    as they happen with zero latency. It is the perfect choice for debugging complex
    command chains where the Cinematic Dashboard might obscure race conditions.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Modular Architecture:** Split into Facade, Emitter, and Codex.
    2.  **The Event-Driven Core:** Fully reactive to the `ConductorEvent` stream.
    3.  **The Zero-Latency Pipe:** Passes subprocess output directly to the user.
    4.  **The Visual Segregator:** Distinctly marks the difference between Scaffold
        overhead and script output using visual pipes (`│`).
    5.  **The ANSI Preserver:** Respects colors emitted by child processes.
    6.  **The Vow Visualizer:** Renders Vow results with high-contrast sigils.
    7.  **The State Chronicler:** Logs metaphysical state changes in real-time.
    8.  **The Luminous Prologue:** Clearly announces the start of every kinetic rite.
    9.  **The Paradox Illuminator:** Renders full tracebacks without truncation.
    10. **The Interactive Proxy:** Falls back to simple input prompts when needed.
    11. **The Epilogue Rite:** Summarizes the run without clearing the history.
    12. **The Unbreakable Contract:** Honors `Renderer` ABC fully.
    """

    def __init__(self, conductor):
        super().__init__(conductor)
        self.emitter = LinearEmitter()

        # The Map of Rites
        self._rite_map = {
            EventType.SYMPHONY_START: self._on_symphony_start,
            EventType.SYMPHONY_END: self._on_symphony_end,
            EventType.ACTION_PROLOGUE: self._on_action_prologue,
            EventType.ACTION_EPILOGUE: self._on_action_epilogue,
            EventType.LOG: self._on_log,
            EventType.PARADOX_PROCLAIMED: self._on_paradox,
            EventType.STATE_CHANGE: self._on_state_change,
            EventType.VOW_RESULT: self._on_vow_result,
            # Block events are noise in stream mode, we skip them or log minimally
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
        self.emitter.emit_block(f"BEGIN SYMPHONY: {path}")

    def _on_symphony_end(self, payload: Dict):
        success = payload.get("success", False)
        duration = payload.get("duration", 0.0)

        style = "success" if success else "failure"
        msg = f"SYMPHONY COMPLETED in {duration:.2f}s"

        self.emitter.emit_block(f"[{style}]{msg}[/{style}]")

    def _on_action_prologue(self, payload: Dict):
        """Announce the kinetic intent."""
        command = payload.get("command", "")
        # Uses '>> Executing: cmd'
        self.emitter.emit_meta(f"Executing: {command}", style_key="prologue", icon_key="action")

    def _on_action_epilogue(self, payload: Dict):
        """Announce the kinetic result."""
        result = payload.get("result", {})
        rc = result.returncode
        duration = result.duration

        style = "success" if rc == 0 else "failure"
        icon = "success" if rc == 0 else "failure"
        msg = f"Process Exited (Code {rc}) [{duration:.2f}s]"

        self.emitter.emit_meta(msg, style_key=style, icon_key=icon)

    def _on_log(self, payload: Dict):
        """Stream raw output."""
        content = payload.get("content", "")
        # Stream renderer prints everything, unlike Basic which might filter.
        self.emitter.emit_raw_stream(content)

    def _on_state_change(self, payload: Dict):
        key = payload.get("key")
        value = payload.get("value")
        self.emitter.emit_meta(f"State Mutation: {key} = {value}", style_key="meta", icon_key="state")

    def _on_vow_result(self, payload: Dict):
        success = payload.get("success")
        reason = payload.get("reason")
        style = "success" if success else "failure"
        self.emitter.emit_meta(f"Vow: {reason}", style_key=style, icon_key="vow")

    def _on_paradox(self, payload: Dict):
        error_msg = payload.get("message", "Unknown Paradox")
        trace = payload.get("traceback", "")
        self.emitter.emit_meta(f"PARADOX: {error_msg}", style_key="failure", icon_key="error")
        if trace:
            # We print the traceback raw for maximum clarity in stream mode
            print(trace)

    # --- INTERFACE IMPLEMENTATION ---

    def render_summary_dossier(self, result: SymphonyResult):
        # Stream renderer doesn't do a big table at the end, just a final status line
        pass

    def conduct_interactive_plea(self, prompt_text: str, default: bool = True) -> bool:
        """Proxies to simple input."""
        from rich.prompt import Confirm
        return Confirm.ask(prompt_text, default=default)

    # --- REQUIRED ABSTRACT METHODS (Stubs) ---
    # These are handled by the event bus now, but kept for interface compliance

    def prologue(self, symphony_path: Path, proving_ground: Path):
        pass

    def epilogue(self, was_pure: bool, duration: float):
        pass

    def render_paradox(self, heresy: Exception, traceback_obj: Any, captured_output: Optional[str] = None):
        pass

    def render_action_prologue(self, edict: Edict, transmuted_command: str, sanctum: Path):
        """
        [THE ASCENSION] This is no longer a stub.
        It proclaims the meta-event that a kinetic rite is about to begin.
        """
        # We use the emitter to ensure the [meta] tag and timestamp are applied.
        self.emitter.emit_meta(
            f"Executing: {transmuted_command}",
            style_key="prologue",
            icon_key="action"  # This will resolve to ">>" in the codex
        )

    def render_action_epilogue(self, live_context: Any, result: ActionResult):
        """
        [THE ASCENSION] This is no longer a stub.
        It proclaims the final verdict of the kinetic rite.
        """
        style = "success" if result.returncode == 0 else "failure"
        icon = "success" if result.returncode == 0 else "failure"
        msg = f"Process Exited (Code {result.returncode}) [{result.duration:.2f}s]"

        self.emitter.emit_meta(msg, style_key=style, icon_key=icon)

    def update_live_stream(self, live_context: Any, line: Union[str, Any]):
        """
        [THE FIX] The Raw Pipe.
        Passes the line directly to the emitter's raw stream.
        """
        content = str(line).rstrip()
        if content:
            self.emitter.emit_raw_stream(content)

    def render_polyglot_prologue(self, edict: 'Edict', sanctum: Path):
        pass

    def render_vow_result(self, is_pure: bool, reason: str, edict: 'Edict'):
        pass

    def render_state_change(self, key: str, value: str, relative_sanctum: Path):
        pass

    def render_proclamation(self, message: str, sanctum: Optional[Path] = None):
        pass

    def render_block_prologue(self, edict: Edict, title: str):
        pass

    def render_block_epilogue(self, edict: Edict):
        pass

    def render_intercession_altar(self, edict: 'Edict', heresy: Exception):
        pass

    def render_comment(self, raw_scripture: str):
        pass

    def render_foreign_adjudication(self, results: List[Any], edict: 'Edict'):
        pass

    def render_structured_status(self, proclamations: List[Dict], line_num: int):
        pass

    def suspend(self):
        pass

    def resume(self):
        pass