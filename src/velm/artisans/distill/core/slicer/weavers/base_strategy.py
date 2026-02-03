# Path: scaffold/artisans/distill/core/slicer/weavers/base_strategy.py
# --------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import List
from .contracts import WeaveContext


class BaseWeaveStrategy(ABC):
    """
    The Sacred Contract for all Weaving Strategies.
    It defines the one true rite: `weave_segments`.
    """

    @abstractmethod
    def weave_segments(self, context: WeaveContext) -> str:
        """
        Receives the full Gnostic context and must return the final,
        surgically reconstructed scripture as a single string.
        """
        pass

    def _detect_indent(self, line: str) -> str:
        """A shared Gaze to perceive the indentation of a line."""
        import re
        match = re.match(r"^(\s*)", line)
        return match.group(1) if match else ""

