# Path: scaffold/symphony/renderers/cinematic_renderer/facade.py
# --------------------------------------------------------------

import sys
import threading
import time
import psutil
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from rich.live import Live
from rich.console import Console

from ..base import Renderer
from .state import CinematicState
from .layout_engine import GnosticLayoutEngine
from ....contracts.symphony_contracts import (
    ConductorEvent, EventType, SymphonyResult, Edict, ActionResult
)
from ....logger import Scribe, get_console

Logger = Scribe('CinematicRenderer')


class CinematicRenderer(Renderer):
    """
    =================================================================================
    == THE GNOSTIC ORRERY (V-Ω-ETERNAL-DASHBOARD)                                  ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Sovereign UI. It creates a parallel reality in the terminal using `rich.Live`.
    It consumes events to update the `CinematicState`, which the `LayoutEngine`
    then transmutes into visual form at 12 FPS.
    """

    def __init__(self, conductor):
        super().__init__(conductor)
        self.console = get_console()
        self.state = CinematicState()
        self.layout_engine = GnosticLayoutEngine()
        self.live: Optional[Live] = None
        self._telemetry_thread: Optional[threading.Thread] = None
        self._stop_telemetry = threading.Event()

        self._rite_map = {
            EventType.SYMPHONY_START: self._on_start,
            EventType.SYMPHONY_END: self._on_end,
            EventType.EDICT_START: self._on_edict_start,
            EventType.EDICT_SUCCESS: self._on_edict_success,
            EventType.EDICT_FAILURE: self._on_edict_failure,
            EventType.LOG: self._on_log,
            EventType.PARADOX_PROCLAIMED: self._on_paradox,
            EventType.STATE_CHANGE: self._on_state,
        }

    # --- LIFECYCLE ---

    def prologue(self, symphony_path: Path, proving_ground: Path):
        """The Curtain Rises."""
        self.state.title = symphony_path.name
        self.state.sanctum = str(proving_ground)

        # Start the Telemetry Heartbeat
        self._stop_telemetry.clear()
        self._telemetry_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        self._telemetry_thread.start()

        # Ignite the Live Display
        self.live = Live(
            self.layout_engine.render(self.state),
            console=self.console,
            refresh_per_second=12,
            screen=True  # Fullscreen mode
        )
        self.live.start()

    def epilogue(self, was_pure: bool, duration: float):
        """The Curtain Falls."""
        self._stop_telemetry.set()
        if self.live:
            self.live.stop()

        # Print Final Summary using Basic Renderer logic or custom table
        status = "[bold green]SUCCESS[/]" if was_pure else "[bold red]FAILURE[/]"
        self.console.print(f"\n{status} Symphony concluded in {duration:.2f}s.\n")

    def handle_event(self, event: ConductorEvent):
        """The Event Bus Consumer."""
        # Update State based on event
        handler = self._rite_map.get(event.type)
        if handler:
            handler(event.payload)

        # Push update to Live
        if self.live:
            self.live.update(self.layout_engine.render(self.state))

    # --- EVENT HANDLERS ---

    def _on_start(self, payload: Dict):
        pass

    def _on_end(self, payload: Dict):
        pass

    def _on_edict_start(self, payload: Dict):
        # We register edicts dynamically or assume they were pre-registered?
        # For a dynamic flow, we add them as they come.
        name = payload.get("command", "") or payload.get("raw_scripture", "Unknown")
        self.state.register_edict(name, payload.get("type", "ACTION"))
        # Immediately start it (assuming sequential)
        self.state.start_edict(len(self.state.edicts) - 1)

    def _on_edict_success(self, payload: Dict):
        self.state.finish_edict(True)

    def _on_edict_failure(self, payload: Dict):
        self.state.finish_edict(False)

    def _on_log(self, payload: Dict):
        self.state.add_log(payload.get("content", ""))

    def _on_state(self, payload: Dict):
        self.state.variables[payload.get("key")] = str(payload.get("value"))

    def _on_paradox(self, payload: Dict):
        self.state.has_heresy = True
        self.state.heresy_detail = payload.get("message", "")

    # --- TELEMETRY ---

    def _monitor_resources(self):
        process = psutil.Process()
        while not self._stop_telemetry.is_set():
            cpu = psutil.cpu_percent()
            mem = process.memory_info().rss / 1024 / 1024
            self.state.cpu_history.append(cpu)
            self.state.mem_history.append(mem)
            time.sleep(1)

    # --- STUBS ---
    def suspend(self):
        pass

    def resume(self):
        pass

    def conduct_interactive_plea(self, *args, **kwargs):
        return True

    def render_summary_dossier(self, *args):
        pass

    def render_paradox(self, *args, **kwargs):
        pass

    def render_action_prologue(self, *args, **kwargs):
        pass

    def render_action_epilogue(self, *args, **kwargs):
        pass

    def update_live_stream(self, *args, **kwargs):
        pass

    def render_polyglot_prologue(self, *args, **kwargs):
        pass

    def render_vow_result(self, *args, **kwargs):
        pass

    def render_state_change(self, *args, **kwargs):
        pass

    def render_proclamation(self, *args, **kwargs):
        pass

    def render_block_prologue(self, *args, **kwargs):
        pass

    def render_block_epilogue(self, *args, **kwargs):
        pass

    def render_intercession_altar(self, *args, **kwargs):
        pass

    def render_comment(self, *args, **kwargs):
        pass

    def render_foreign_adjudication(self, *args, **kwargs):
        pass

    def render_structured_status(self, *args, **kwargs):
        pass