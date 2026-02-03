# Path: scaffold/symphony/conductor_core/engine.py
# ------------------------------------------------

import queue
import sys
import time
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from typing import List, Optional, Any, Dict, TYPE_CHECKING, Union

from ...contracts.symphony_contracts import Edict, ActionResult, ConductorEvent, SymphonyResult, EventType
from ...contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity
from ...logger import Scribe

if TYPE_CHECKING:
    from ..conductor import SymphonyConductor
    from ..execution import KineticInterface
    from .resilience import SymphonyResilienceManager
    from .handlers import SymphonyHandlers
    from .context import GnosticContextManager

Logger = Scribe('SymphonyEngine')


class SymphonyEngine:
    """
    =================================================================================
    == THE ENGINE OF WILL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS++)                ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The central execution loop of the Symphony. It receives Edicts, dispatches them
    to the Handlers, and maintains the integrity of the Gnostic State. It has been
    healed with the Gnostic Bridge to the Context Manager, making its mind whole.
    """

    def __init__(
            self,
            conductor: 'SymphonyConductor',
            performer: 'KineticInterface',
            resilience_manager: 'SymphonyResilienceManager',
            handlers: 'SymphonyHandlers',
            event_bus: queue.Queue,
            context_manager: 'GnosticContextManager'
    ):
        self._lock = threading.RLock()
        self.conductor = conductor
        self.performer = performer
        self.resilience_manager = resilience_manager
        self.handlers = handlers
        self.event_bus = event_bus
        self.context_manager = context_manager

        self._is_running = False
        self._edicts_conducted = 0
        self._last_reality: Optional[ActionResult] = None
        self.event_timeline: List[ConductorEvent] = []

    @property
    def context(self) -> 'GnosticContextManager':
        return self.context_manager

    @property
    def last_reality(self) -> Optional[ActionResult]:
        with self._lock:
            return self._last_reality

    def update_last_reality(self, result: ActionResult):
        """[FACULTY 1] The Gnostic Bridge."""
        with self._lock:
            self._last_reality = result
            # We bestow the memory upon the Context Manager for the Vow Adjudicator
            self.context_manager.last_process_result = result
            Logger.verbose(f"Last Reality updated. Exit: {result.returncode}, Duration: {result.duration:.2f}s")

    def execute_symphony(self, edicts_to_conduct: List[Edict], runtime_vows: List[Edict]) -> SymphonyResult:
        """The Grand Rite of Symphony Execution."""
        start_time = time.monotonic()
        was_pure = False

        with self._lock:
            self._is_running = True
            self._edicts_conducted = 0
            self.event_timeline.clear()

        try:
            self._proclaim_event(EventType.SYMPHONY_START, {})
            if runtime_vows:
                self.handlers.activate_runtime_vows(runtime_vows)

            self.conduct_block(edicts_to_conduct)
            was_pure = True

        except Exception as e:
            # The Resilience Manager handles the final exception logging and UI.
            # We just need to mark the symphony as failed.
            was_pure = False
            # Ensure the exception is re-raised if not handled by intercession altar
            if not isinstance(e, ArtisanHeresy) or e.exit_code != 0:
                # Re-raise to be caught by the orchestrator's top-level try/except
                raise e

        finally:
            duration = time.monotonic() - start_time
            result = self.forge_result(was_pure, duration)
            self._proclaim_event(EventType.SYMPHONY_END, {"result": result})
            with self._lock:
                self._is_running = False

        return result

    def conduct_block(self, edicts: List[Edict]):
        """[FACULTY 5 & 6] The Resilient, Interactive Loop."""
        i = 0
        while i < len(edicts):
            edict = edicts[i]

            with self.resilience_manager.rite_boundary(edict) as outcome:
                self._dispatch_edict(edict)

            # [FACULTY 6] The Interactive Loop of Redemption
            if outcome.choice:
                from .resilience.contracts import IntercessionChoice
                if outcome.choice == IntercessionChoice.RETRY:
                    continue  # Re-run the current edict
                elif outcome.choice == IntercessionChoice.SKIP:
                    i += 1  # Move to the next edict
                    continue

            # If no intercession, or intercession failed, exception is re-raised by context manager
            i += 1

    def _dispatch_edict(self, edict: Edict):
        """[FACULTY 8] The Sovereign Dispatcher."""
        with self._lock:
            if not self._is_running: return

        self._edicts_conducted += 1
        self._proclaim_event(EventType.EDICT_START, {"edict": edict})

        try:
            # The Grand Triage
            self.handlers.dispatch(edict)

            # If no exception, it's a success
            self._proclaim_event(EventType.EDICT_SUCCESS, {
                "edict": edict,
                "last_reality": self.last_reality
            })
        except Exception as heresy:
            # Let the resilience manager handle the failure event proclamation
            self._proclaim_event(EventType.EDICT_FAILURE, {
                "edict": edict,
                "heresy": heresy,
                "last_reality": self.last_reality
            })
            raise heresy  # Re-raise for the resilience boundary to catch

    def _proclaim_event(self, event_type: EventType, payload: Dict):
        """[FACULTY 2] The Event-Driven Soul."""
        event = ConductorEvent(type=event_type, payload=payload)
        self.event_timeline.append(event)
        try:
            self.event_bus.put_nowait(event)
        except queue.Full:
            Logger.warn("Event bus is full. A proclamation was lost to the void.")

    def forge_result(self, was_pure: bool, duration: float) -> SymphonyResult:
        """[FACULTY 9] The Telemetric Heartbeat."""
        return SymphonyResult(
            success=was_pure,
            duration=duration,
            edicts_executed=self._edicts_conducted,
            heresies=[],  # Heresies are now handled by the Resilience Manager
            event_timeline=self.event_timeline
        )