# Path: scaffold/symphony/conductor_core/handlers/vow_handler/contracts.py
# ------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .....core.jurisprudence.contracts import AdjudicationContext

class VowSpecialist(ABC):
    """
    The Sacred Contract for a Vow Specialist.
    Each specialist is a master of a specific domain of truth (Filesystem, Process, etc.).
    """
    def __init__(self, context: 'AdjudicationContext'):
        self.context = context

    @abstractmethod
    def adjudicate(self, *args) -> Tuple[bool, str]:
        """
        Performs the rite of judgment.
        Returns (is_truth, reason_for_judgment).
        """
        pass