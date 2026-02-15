# Path: src/velm/core/structure_sentinel/strategies/python_strategy/contracts.py
# ------------------------------------------------------------------------------

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .....core.kernel.transaction import GnosticTransaction
    from .....creator.io_controller import IOConductor
    from .....logger import Scribe

@dataclass(frozen=True)
class SharedContext:
    """
    The Gnostic Vessel of Shared Consciousness.
    Passed to every faculty in the Python Hive-Mind.
    """
    project_root: Path
    transaction: Optional["GnosticTransaction"]
    logger: "Scribe"
    io_conductor: Optional["IOConductor"] = None # [ASCENSION]: The Hand of God