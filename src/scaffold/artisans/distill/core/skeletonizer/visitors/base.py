# Path: scaffold/artisans/distill/core/skeletonizer/visitors/base.py
# ------------------------------------------------------------------

from abc import ABC, abstractmethod
from ..contracts import SurgicalContext


class BaseAnatomist(ABC):
    """The Abstract Soul of a Language Specialist."""

    @abstractmethod
    def operate(self, ctx: SurgicalContext) -> str:
        """Performs the surgery."""
        pass

