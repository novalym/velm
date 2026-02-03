# scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/base_strategy.py

from abc import ABC
from ..contracts import StructureStrategy
from ....logger import Scribe

class BaseStrategy(ABC, StructureStrategy):
    """
    =============================================================================
    == THE ANCESTRAL SOUL OF THE GUARDIANS                                     ==
    =============================================================================
    The abstract ancestor for all specialist structural guardians. It provides a
    common Gnostic root and a luminous voice (Logger).
    """
    def __init__(self, language_name: str):
        self.language_name = language_name
        self.logger = Scribe(f"{language_name.title()}StructureGuardian")