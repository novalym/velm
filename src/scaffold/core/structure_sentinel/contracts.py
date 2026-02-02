# scaffold/artisans/translocate_core/conductor/structure_sentinel/contracts.py

from pathlib import Path
from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..kernel.transaction import GnosticTransaction

class StructureStrategy(Protocol):
    """
    =============================================================================
    == THE SACRED CONTRACT OF STRUCTURAL LAW (V-Ω-INTERFACE)                   ==
    =============================================================================
    This is the divine, unbreakable contract for a language-specific Guardian.
    It defines the one true rite all Guardians must be able to perform: the Rite
    of Consecration.
    """
    def consecrate(self, file_path: Path, project_root: Path, transaction: Optional["GnosticTransaction"]) -> None:
        """
        Performs the Rite of Consecration. The Guardian gazes upon the sanctums
        housing the `file_path` and ensures they are structurally pure according
        to the laws of its language.
        """
        ...