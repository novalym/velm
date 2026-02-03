# Path: scaffold/symphony/conductor_core/handlers/state_handler/facade.py
# -----------------------------------------------------------------------
from ..base import BaseHandler
from .....contracts.symphony_contracts import Edict
from .dispatcher import StateDispatcher


class StateHandler(BaseHandler):
    """
    =================================================================================
    == THE KEEPER OF CONTEXT (V-Ω-MODULAR-FACADE-HEALED)                           ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The Facade for the new modular State Engine.
    It initializes the Dispatcher and delegates execution.

    ### HEALING (V-Ω):
    - **Context Property Access:** Removed profane parentheses from `self.engine.context`.
      It is a property, not a method.
    - **Preserved Complexity:** Fully delegates to `StateDispatcher`, maintaining the
      full pantheon of specialist artisans (Sanctum, Environment, Variables, etc.).
    """

    def __init__(self, conductor, engine, performer, resilience_manager, context_manager):
        super().__init__(conductor, engine, performer, resilience_manager, context_manager)
        self.dispatcher = StateDispatcher(self)

    @property
    def is_dry_run(self) -> bool:
        """
        [THE FIX] Access context as property, do not call it.
        self.engine.context -> GnosticContextManager (dict-like)
        """
        # We access the property .context, which returns the manager.
        # Then we call .get() on the manager (which is a MutableMapping).
        return self.engine.context.get('is_simulation', False)

    @property
    def regs(self):
        """
        Bridge to old 'regs' access if needed by specialists via handler.regs.
        The conductor usually has regs.
        """
        return self.conductor.regs

    def execute(self, edict: Edict):
        """Delegates the Rite to the Gnostic Router."""
        self.dispatcher.dispatch(edict)