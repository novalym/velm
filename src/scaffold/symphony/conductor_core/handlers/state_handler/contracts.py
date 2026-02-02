# Path: scaffold/symphony/conductor_core/handlers/state_handler/contracts.py
# --------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .....contracts.symphony_contracts import Edict

if TYPE_CHECKING:
    from ..base import BaseHandler


class StateSpecialist(ABC):
    """
    The Sacred Contract for a State Mutation Specialist.
    """

    def __init__(self, handler: 'BaseHandler'):
        self.handler = handler
        self.logger = handler.logger
        self.console = handler.console

    @abstractmethod
    def conduct(self, edict: Edict, value: str) -> None:
        """
        Performs the specific state mutation.
        Args:
            edict: The full command vessel.
            value: The transmuted (resolved) value string from the Alchemist.
        """
        pass

