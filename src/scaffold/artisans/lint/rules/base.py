# Path: scaffold/artisans/lint/rules/base.py
# ------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Generator
from ..contracts import LintContext, LintIssue


class GnosticRule(ABC):
    """
    The Sacred Contract for a Linter Rule.
    Every rule must possess a unique ID, a category, and a Gaze (check method).
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """The unique identifier (e.g., 'graph.orphan')."""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """The domain of the rule (e.g., 'Architecture', 'Security', 'Structure')."""
        pass

    @property
    def description(self) -> str:
        """A luminous description of what this rule guards against."""
        return "A mystery of the Gnostic Mentor."

    @abstractmethod
    def check(self, context: LintContext) -> Generator[LintIssue, None, None]:
        """
        The Rite of Adjudication.
        Yields LintIssues found within the context.
        """
        pass