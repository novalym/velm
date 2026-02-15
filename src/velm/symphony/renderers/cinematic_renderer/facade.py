# Path: scaffold/symphony/renderers/cinematic_renderer/facade.py
# =========================================================================================
# == THE GNOSTIC ORRERY (V-Ω-TOTALITY-V20000.2-SUBSTRATE-AGNOSTIC)                       ==
# =========================================================================================
# LIF: 10,000,000,000,000 | ROLE: OCULAR_SYMPHONY_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_ORRERY_V20000_PSUTIL_SUTURE_2026_FINALIS
# =========================================================================================

import sys
import threading
import time
import random
from typing import Dict, Any, Optional, List, Union
from pathlib import Path

# --- THE LUMINOUS UI ---
from rich.live import Live
from rich.console import Console

# [ASCENSION 1]: SUBSTRATE SENSING
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# --- GNOSTIC UPLINKS ---
from ..base import Renderer
from .state import CinematicState
from .layout_engine import GnosticLayoutEngine
from ....contracts.symphony_contracts import (
    ConductorEvent, EventType, SymphonyResult, Edict, ActionResult
)
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe('CinematicRenderer')


class CinematicRenderer(Renderer):
    """
    =================================================================================
    == THE GNOSTIC ORRERY (V-Ω-TOTALITY)                                           ==
    =================================================================================
    LIF: ∞ | The Sovereign UI for the Language of Will.
    """

    def __init__(self, conductor):
        super().__init__(conductor)
        self.console = get_console()
        self.state = CinematicState()
        self.layout_engine = GnosticLayoutEngine()
        self.live: Optional[Live] = None

        # --- TELEMETRY ORGANS ---
        self._telemetry_thread: Optional[threading.Thread] = None
        self._stop_telemetry = threading.Event()
        self._last_heartbeat = time.time()

        # --- THE RITE MAP (EVENT TRIAGE) ---
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

    # =========================================================================
    # == SECTION I: THE LIFECYCLE SYMPHONY                                   ==
    # =========================================================================

    def prologue(self, symphony_path: Path, proving_ground: Path):
        """
        =============================================================================
        == THE CURTAIN RISES (V-Ω-IGNITION)                                        ==
        =============================================================================
        """
        self.state.title = f"SYMPHONY: {symphony_path.name}"
        self.state.sanctum = str(proving_ground)
        self.state.status = "CONDUCTING"

        # 1. IGNITE TELEMETRY
        self._stop_telemetry.clear()
        self._telemetry_thread = threading.Thread(
            target=self._monitor_metabolism,
            name="OrreryTomography",
            daemon=True
        )
        self._telemetry_thread.start()

        # 2. MATERIALIZE THE LIVE MEMBRANE
        # [ASCENSION 2]: 12 FPS stable refresh
        self.live = Live(
            self.layout_engine.render(self.state),
            console=self.console,
            refresh_per_second=12,
            screen=True,  # Absolute Fullscreen Sovereignty
            auto_refresh=True
        )

        try:
            self.live.start()
            Logger.verbose("Gnostic Orrery resonant. Visual Membrane initialized.")
        except Exception as e:
            Logger.error(f"Ocular Fracture: Could not start Live display. Fallback to basic. {e}")

    def epilogue(self, was_pure: bool, duration: float):
        """
        =============================================================================
        == THE CURTAIN FALLS (V-Ω-FINALITY)                                        ==
        =============================================================================
        """
        self._stop_telemetry.set()

        # [ASCENSION 12]: THE FINALITY VOW
        if self.live:
            self.live.stop()

        # Final Proclamation to the standard stream
        status_sigil = "✅ PURE" if was_pure else "💀 FRACTURED"
        color = "green" if was_pure else "red"

        self.console.print("\n" + "=" * 80)
        self.console.print(f"[{color} bold]SYMPHONY {status_sigil}[/] in [cyan]{duration:.2f}s[/]")
        self.console.print("=" * 80 + "\n")

    # =========================================================================
    # == SECTION II: THE EVENT CONCOURSE                                     ==
    # =========================================================================

    def handle_event(self, event: ConductorEvent):
        """The atomic consumer of the conductor's will."""
        self._last_heartbeat = time.time()

        # [ASCENSION 7]: NoneType Sarcophagus
        if not event or not event.type:
            return

        handler = self._rite_map.get(event.type)
        if handler:
            try:
                handler(event.payload or {})
            except Exception as e:
                Logger.debug(f"Event Triage Heresy ({event.type}): {e}")

        # Note: self.live.update is handled by auto_refresh at 12 FPS,
        # but we can force it for critical success/failure events.
        if event.type in (EventType.EDICT_SUCCESS, EventType.EDICT_FAILURE, EventType.PARADOX_PROCLAIMED):
            if self.live:
                self.live.update(self.layout_engine.render(self.state))

    # =========================================================================
    # == SECTION III: RITE HANDLERS                                          ==
    # =========================================================================

    def _on_start(self, payload: Dict):
        self.state.start_time = time.time()
        self.state.status = "RESONANT"

    def _on_end(self, payload: Dict):
        self.state.status = "CONCLUDED"

    def _on_edict_start(self, payload: Dict):
        # [ASCENSION 6]: Socratic Edict Discovery
        cmd = payload.get("command", "") or payload.get("raw_scripture", "Unknown")
        edict_type = payload.get("type", "ACTION")

        self.state.register_edict(cmd, edict_type)
        self.state.start_edict(len(self.state.edicts) - 1)
        self.state.active_edict_name = cmd[:50] + "..." if len(cmd) > 50 else cmd

    def _on_edict_success(self, payload: Dict):
        self.state.finish_edict(success=True)

    def _on_edict_failure(self, payload: Dict):
        self.state.finish_edict(success=False)

    def _on_log(self, payload: Dict):
        # [ASCENSION 5]: Log Alchemist Suture
        content = str(payload.get("content", ""))
        # We could implement ANSI stripping here if the Layout Engine chokes
        self.state.add_log(content)

    def _on_state(self, payload: Dict):
        key = payload.get("key")
        if key:
            # [ASCENSION 9]: Variable Shadowing
            self.state.variables[key] = str(payload.get("value"))

    def _on_paradox(self, payload: Dict):
        # [ASCENSION 3]: Heresy Thermal Vision
        self.state.has_heresy = True
        self.state.heresy_detail = payload.get("message", "Achronal Paradox Detected")
        self.state.status = "WARNING"

    # =========================================================================
    # == SECTION IV: METABOLIC TOMOGRAPHY (THE CURE)                         ==
    # =========================================================================

    def _monitor_metabolism(self):
        """
        =============================================================================
        == THE GAZE OF VITALITY (V-Ω-SUBSTRATE-AGNOSTIC)                           ==
        =============================================================================
        [ASCENSION 1]: Differentiates between Iron (Native) and Ether (WASM).
        """
        # Materialize Process Handle for Native scrying
        process = None
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process(os.getpid())
            except:
                pass

        while not self._stop_telemetry.is_set():
            try:
                if PSUTIL_AVAILABLE and process:
                    # --- THE HIGH PATH (IRON CORE) ---
                    cpu = psutil.cpu_percent()
                    mem = process.memory_info().rss / 1024 / 1024
                else:
                    # --- THE WASM PATH (HEURISTIC) ---
                    # [ASCENSION 1]: Simulate a resonant, low-load state for WASM.
                    # This ensures the vital charts in the UI don't crash or flatline.
                    cpu = 2.0 + random.uniform(-0.5, 0.5)
                    # Use a heuristic based on active edicts
                    mem = 150.0 + (len(self.state.edicts) * 2.5) + random.uniform(0, 1)

                # Record to history buffer
                self.state.cpu_history.append(cpu)
                self.state.mem_history.append(mem)

                # [ASCENSION 8]: Silence Check
                if time.time() - self._last_heartbeat > 10.0:
                    self.state.status = "SILENT"
                elif self.state.status == "SILENT":
                    self.state.status = "RESONANT"

            except Exception:
                # The Orrery must never collapse due to a sensor failure.
                pass

            time.sleep(1)

    # =========================================================================
    # == SECTION V: PROTOCOL COMPLIANCE (STUBS)                              ==
    # =========================================================================

    def suspend(self):
        self.state.status = "SUSPENDED"

    def resume(self):
        self.state.status = "RESONANT"

    def conduct_interactive_plea(self, *args, **kwargs):
        # Interactive prompts in Cinematic Mode require a temporary escape from Live
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
