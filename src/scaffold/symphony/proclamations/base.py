# Path: scaffold/symphony/proclamations/base.py
# ---------------------------------------------

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from ....core.alchemist import DivineAlchemist
    from ....creator.registers import QuantumRegisters
    from ....symphony.conductor_core.engine import SymphonyEngine
    from rich.console import Console

class ProclamationHandler(ABC):
    """
    The abstract soul of a Proclamation Scribe.
    Defines the unbreakable contract for rendering Gnostic truths.
    """
    def __init__(
        self,
        alchemist: "DivineAlchemist",
        console: "Console",
        engine: "SymphonyEngine",
        registers: "QuantumRegisters"
    ):
        self.alchemist = alchemist
        self.console = console
        self.engine = engine
        self.regs = registers

    @property
    @abstractmethod
    def key(self) -> str:
        """The sacred keyword that summons this Scribe (e.g., 'table', 'file')."""
        pass

    @abstractmethod
    def execute(self, gnostic_arguments: str):
        """The one true rite of proclamation."""
        pass