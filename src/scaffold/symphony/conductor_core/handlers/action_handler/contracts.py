# Path: scaffold/symphony/conductor_core/handlers/action_handler/contracts.py
# ---------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .....contracts.symphony_contracts import Edict

if TYPE_CHECKING:
    from .facade import ActionHandler


class ActionSpecialist(ABC):
    """
    The Sacred Contract for a Kinetic Specialist.

    HEALED (V-Ω): Uses properties for dependencies to avoid "NoneType" heresies
    during early initialization.
    """

    def __init__(self, handler: 'ActionHandler'):
        self.handler = handler
        # We do not cache dynamic dependencies here.

    @property
    def logger(self):
        return self.handler.logger

    @property
    def console(self):
        return self.handler.console

    @property
    def alchemist(self):
        return self.handler.alchemist

    @property
    def renderer(self):
        """
        Dynamically accesses the Renderer.
        Ensures we get the living instance, not the None value from __init__ time.
        """
        return self.handler.renderer

    @property
    def context(self):
        return self.handler.context_manager

    @abstractmethod
    def conduct(self, edict: Edict, command: str) -> None:
        """
        Performs the specific kinetic rite.
        Args:
            edict: The full command vessel.
            command: The transmuted (resolved) command string from the Alchemist.
        """
        pass

