# Path: core/lsp/base/features/linter/contracts.py
# ------------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Any
from ...types import Diagnostic


class LinterRule(ABC):
    """
    =============================================================================
    == THE COVENANT OF LAW (INTERFACE)                                         ==
    =============================================================================
    The abstract contract that every Static Analysis Rule must sign.

    Whether the rule checks for syntax errors, security leaks, or stylistic drift,
    it must adhere to this shape to be accepted by the LinterEngine.
    """

    @property
    @abstractmethod
    def code(self) -> str:
        """
        [THE SIGNATURE]
        The machine-readable heresy code (e.g., LINT_001, SECURITY_RISK).
        Used for suppression tracking and UI filtering.
        """
        pass

    @property
    def priority(self) -> int:
        """
        [THE WEIGHT]
        Determines the order of execution (0-100).
        Higher priority rules run first. Default is 50.
        """
        return 50

    @abstractmethod
    def validate(self, ctx: Any) -> List[Diagnostic]:
        """
        [THE RITE OF JUDGMENT]
        Performs the forensic scan on the provided context.

        Args:
            ctx (Any): The AnalysisContext object. It contains the document,
                       pre-computed symbol tables, and configuration.
                       (Defined concretely in the implementing feature layer).

        Returns:
            List[Diagnostic]: A list of heresies found. Empty list if pure.
        """
        pass