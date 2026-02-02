# Path: core/lsp/features/definition/contracts.py
# -----------------------------------------------

from abc import ABC, abstractmethod
from typing import Optional, Union, List, Any, Dict
from .models import Location, LocationLink
from ...document import TextDocument
from ...utils.text import WordInfo

class DefinitionRule(ABC):
    """
    =============================================================================
    == THE COVENANT OF ORIGIN (INTERFACE)                                      ==
    =============================================================================
    Every language-specific navigation strategy must sign this contract.
    It defines how to resolve a symbol's birthplace.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the navigation rule."""
        pass

    @property
    def priority(self) -> int:
        """Determines the order of rule execution (0-100)."""
        return 50

    @abstractmethod
    def matches(self, info: WordInfo) -> bool:
        """
        [THE GAZE OF RELEVANCE]
        Does this rule have the Gnosis to handle this specific symbol?
        """
        pass

    @abstractmethod
    def resolve(self, doc: TextDocument, info: WordInfo) -> Optional[Union[Location, List[Location], List[LocationLink]]]:
        """
        [THE RITE OF LOCATION]
        Calculates the physical coordinates of the definition.
        """
        pass