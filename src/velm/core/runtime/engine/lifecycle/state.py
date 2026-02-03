# Path: core/runtime/engine/lifecycle/state.py
# --------------------------------------------

from enum import Enum, auto


class LifecyclePhase(Enum):
    """The Phases of the God-Engine's Existence."""
    VOID = auto()  # Pre-init
    BOOTING = auto()  # Bootstrap active
    AWAKE = auto()  # Fully operational
    DRAINING = auto()  # Shutting down, finishing tasks
    FRACTURED = auto()  # Critical failure state


class EngineState:
    """
    Thread-safe state container.
    """

    def __init__(self):
        self._phase = LifecyclePhase.VOID

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, new_phase: LifecyclePhase):
        # Allow transitions? (Validation logic could go here)
        self._phase = new_phase