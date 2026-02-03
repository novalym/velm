# Path: scaffold/parser_core/parser/parser_scribes/base_scribe.py
# ---------------------------------------------------------------

from abc import ABC, abstractmethod
import re
from typing import List, TYPE_CHECKING, Optional

from ....contracts.data_contracts import GnosticVessel
from ....logger import Scribe

if TYPE_CHECKING:
    from ....parser_core.parser import ApotheosisParser


class FormScribe(ABC):
    """
    The abstract soul of all Scribes, now a self-aware entity.
    """

    def __init__(self, parser: 'ApotheosisParser', scribe_name: Optional[str] = None):
        """
        A Scribe is born. It is bestowed with an unbreakable bond to its master
        Conductor.

        [THE DIVINE HEALING]
        If the `scribe_name` is not spoken (None), the Scribe performs the
        Rite of Self-Awareness, deriving its name from its own class identity.
        This allows Scribes like `OnUndoScribe` to exist without defining a
        redundant `__init__`.
        """
        self.parser = parser

        # The Rite of Self-Awareness
        final_name = scribe_name or self.__class__.__name__

        self.Logger = Scribe(final_name)

    @abstractmethod
    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The One True, Sacred Rite.
        """
        pass

