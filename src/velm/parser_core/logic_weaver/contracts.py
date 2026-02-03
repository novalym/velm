# Path: scaffold/parser_core/logic_weaver/contracts.py
# ----------------------------------------------------

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional


class ChainStatus(Enum):
    """The Gnostic State of a Logic Chain."""
    PENDING = auto()  # Chain just started (e.g. at @if)
    ENTERED = auto()  # A branch has been taken
    SKIPPED = auto()  # A branch was skipped
    CLOSED = auto()  # Chain has ended (e.g. at @endif)


@dataclass
class LogicScope:
    """
    The Atomic State of a single level in the AST hierarchy.
    """
    parent_visible: bool = True

    # State Machine for the current chain
    chain_status: ChainStatus = ChainStatus.CLOSED

    # Forensic Trail
    decision_history: List[str] = field(default_factory=list)

    def start_chain(self):
        """Begins a new logical chain."""
        self.chain_status = ChainStatus.PENDING

    def mark_entered(self):
        """Marks that a branch in this chain has been entered."""
        self.chain_status = ChainStatus.ENTERED

    def end_chain(self):
        """Concludes the current chain."""
        self.chain_status = ChainStatus.CLOSED

    @property
    def is_resolved(self) -> bool:
        """Returns True if a branch in this chain has already been taken."""
        return self.chain_status == ChainStatus.ENTERED