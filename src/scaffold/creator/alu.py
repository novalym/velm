# Path: scaffold/creator/alu.py
# -----------------------------
from typing import Any, Dict

from .registers import QuantumRegisters
from ..core.alchemist import get_alchemist
from ..logger import Scribe

Logger = Scribe("ALU")


class AlchemicalLogicUnit:
    """
    The Brain of Transmutation.
    Handles variable resolution, template rendering, and logic evaluation.
    """

    def __init__(self, registers: QuantumRegisters):
        self.regs = registers
        self.alchemist = get_alchemist()

    def transmute(self, content: str, context_override: Dict[str, Any] = None) -> str:
        """
        Performs Gnostic Transmutation on a string using the Registers' Gnosis.
        Supports temporary context injection for specific operations.
        """
        if not content: return ""

        # Merge global gnosis with local override
        context = self.regs.gnosis.copy()
        if context_override:
            context.update(context_override)

        try:
            return self.alchemist.transmute(content, context)
        except Exception as e:
            # The ALU is resilient; it warns but does not halt the machine for render errors
            Logger.warn(f"ALU Paradox during transmutation: {e}")
            return content

    def evaluate_condition(self, condition: str) -> bool:
        """
        [FUTURE FACULTY] Evaluates a boolean expression (e.g., for @if directives).
        """
        # Placeholder for future integration with the LogicWeaver's adjudicator
        return True