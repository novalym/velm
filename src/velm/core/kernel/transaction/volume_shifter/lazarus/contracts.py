# Path: src/velm/core/kernel/transaction/volume_shifter/lazarus/contracts.py
# --------------------------------------------------------------------------

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import List, Dict, Any, Optional


class OrphanState(Enum):
    """The ontological diagnosis of a fractured reality shard."""
    BLUE_OLD_STRANDED = auto()  # The legacy matter was preserved, but the transaction died.
    GREEN_ABANDONED = auto()  # The shadow forge completed, but the flip never occurred.
    JOURNAL_DEADLOCK = auto()  # A commit.journal exists with unfulfilled intent.
    UNKNOWN_ENTROPY = auto()  # Unrecognized temporal artifact.


@dataclass
class RecoveryPlan:
    """
    =============================================================================
    == THE GNOSTIC RECOVERY PLAN (V-Ω-CAUSAL-REVERSAL)                         ==
    =============================================================================
    The definitive blueprint for resurrecting a specific transaction.
    """
    tx_id: str
    state: OrphanState
    volume_dir: Path

    # Maps the stranded legacy path (blue_old/src) to its rightful home in reality (src)
    resurrection_targets: List[Dict[str, Path]] = field(default_factory=list)

    timestamp: float = 0.0
    is_executable: bool = True

