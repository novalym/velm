# Path: scaffold/core/maestro/handlers/base.py
# --------------------------------------------

from abc import ABC, abstractmethod
from typing import Any

from ..contracts import MaestroContext
from ...alchemist import DivineAlchemist
from ...redemption.diagnostician import AutoDiagnostician
from ....creator.registers import QuantumRegisters
from ....logger import Scribe


class BaseRiteHandler(ABC):
    """
    The sacred, abstract soul of a Rite Handler. It defines the unbreakable
    contract all specialist artisans in the Maestro's Pantheon must honor.
    """

    def __init__(self, registers: QuantumRegisters, alchemist: DivineAlchemist, context: MaestroContext):
        self.regs = registers
        self.alchemist = alchemist
        self.context = context
        self.console = registers.console
        self.diagnostician = AutoDiagnostician
        self.logger = Scribe(self.__class__.__name__)

    @abstractmethod
    def conduct(self, transmuted_command: str):
        """The one true rite. All handlers must implement this."""
        pass

    def _redact_secrets(self, text: str) -> str:
        """A shared utility for veiling secrets before proclamation."""
        import re
        for key in ['api_key', 'secret', 'token', 'password']:
            text = re.sub(f'({key}[= ]+)([\'"]?)([^\s\'"]+)', r'\1\2******', text, flags=re.IGNORECASE)
        return text