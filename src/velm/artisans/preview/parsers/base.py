# Path: scaffold/artisans/preview/parsers/base.py
# =================================================================================
# == THE ABSTRACT SEER (V-Ω-INTERFACE)                                           ==
# =================================================================================
from abc import ABC, abstractmethod
from typing import List
from ..contracts import UIElement


class BaseUIParser(ABC):
    """
    The Base Contract for all UI Parsers.
    Every parser must be able to transmute a string of code into a List of UIElements.
    """

    @abstractmethod
    def parse(self, content: str) -> List[UIElement]:
        """Transmutes raw source code into a UI Topology."""
        pass

