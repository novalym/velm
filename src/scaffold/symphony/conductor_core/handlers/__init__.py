# Path: scaffold/symphony/conductor_core/handlers/__init__.py
# -----------------------------------------------------------

import threading
import time
from typing import TYPE_CHECKING, List, Optional, Dict, Iterable

from .action_handler import ActionHandler
from .logic_handler import LogicHandler
from .state_handler import StateHandler
from .vow_handler import VowHandler
from .meta_handler import MetaHandler
from .parallel_handler import ParallelHandler
from ....contracts.symphony_contracts import Edict, EdictType, ActionResult
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

if TYPE_CHECKING:
    from ...conductor.orchestrator import SymphonyConductor
    from ..engine import SymphonyEngine
    from ...execution import KineticInterface
    from ..resilience import SymphonyResilienceManager
    from ..context import GnosticContextManager

Logger = Scribe('SymphonyHandlers')


class SymphonyHandlers:
    """
    =================================================================================
    == THE GRAND FACADE (V-Ω-GNOSTIC-PROPAGATION-ENGINE)                           ==
    =================================================================================
    The Sovereign Hub for all Edict Handlers. It performs Gnostic Triage and now
    ensures all its children are eternally bound to the soul of the Symphony Engine.
    """

    def __init__(
            self,
            conductor: 'SymphonyConductor',
            engine: Optional['SymphonyEngine'],
            performer: 'KineticInterface',
            resilience_manager: 'SymphonyResilienceManager',
            context_manager: 'GnosticContextManager'
    ):
        self._engine_ref = engine

        # --- THE FORGING OF THE PANTHEON ---
        self.action = ActionHandler(conductor, engine, performer, resilience_manager, context_manager)
        self.logic = LogicHandler(conductor, engine, performer, resilience_manager, context_manager)
        self.state = StateHandler(conductor, engine, performer, resilience_manager, context_manager)
        self.vow = VowHandler(conductor, engine, performer, resilience_manager, context_manager)
        self.meta = MetaHandler(conductor, engine, performer, resilience_manager, context_manager)
        self.parallel = ParallelHandler(conductor, engine, performer, resilience_manager, context_manager)

        # --- THE SACRED LIST OF SOULS ---
        # This list ensures the Gnostic Propagation reaches every artisan.
        self.HANDLERS = [self.action, self.logic, self.state, self.vow, self.meta, self.parallel]

    @property
    def engine(self) -> 'SymphonyEngine':
        """
        [THE GAZE OF THE VOID]
        Ensures the engine is manifest before it is summoned.
        """
        if self._engine_ref is None:
            raise ArtisanHeresy(
                "A Gnostic Schism occurred: The Handlers' connection to the Engine's soul was never forged.")
        return self._engine_ref

    @engine.setter
    def engine(self, new_engine: 'SymphonyEngine'):
        """
        [THE RITE OF GNOSTIC PROPAGATION]
        Bestows the soul of the Engine upon all child handlers.
        """
        self._engine_ref = new_engine
        Logger.verbose("Gnostic Propagation: Bestowing Engine's soul upon the Handler Pantheon...")
        for handler in self.HANDLERS:
            handler.engine = new_engine
            # We also ensure the handler's internal reference is updated
            if hasattr(handler, '_engine_ref'):
                handler._engine_ref = new_engine

    def dispatch(self, edict: Edict):
        """
        The Grand Triage.
        """
        if edict.type in (EdictType.ACTION, EdictType.POLYGLOT_ACTION):
            # The result of the action is captured and passed to the engine.
            action_result = self.action.execute(edict)
            self.engine.update_last_reality(action_result)
        elif edict.type == EdictType.VOW:
            self.vow.execute(edict)
        elif edict.type == EdictType.STATE:
            self.state.execute(edict)
        elif edict.type == EdictType.CONDITIONAL:
            self.logic.execute_conditional(edict)
        elif edict.type == EdictType.LOOP:
            self.logic.execute_loop(edict)
        elif edict.type == EdictType.FILTER:
            self.logic.execute_filter(edict)
        elif edict.type == EdictType.DIRECTIVE:
            self.meta.execute_directive(edict)
        elif edict.type == EdictType.PARALLEL_RITE:
            self.parallel.execute(edict)
        else:
            # Comments, Breakpoints, etc. are handled by the renderer/engine directly
            pass

    def activate_runtime_vows(self, vow_edicts: List[Edict]):
        """Injects runtime vows into the VowHandler."""
        self.meta.activate_runtime_vows(vow_edicts)