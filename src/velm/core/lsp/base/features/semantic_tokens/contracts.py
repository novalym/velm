# Path: core/lsp/features/semantic_tokens/contracts.py
# ----------------------------------------------------

from abc import ABC, abstractmethod
from typing import List
from .encoder import RawToken
from ...document import TextDocument

class TokenProvider(ABC):
    """
    Every language-specific spectrometer must sign this contract.
    It defines how to identify tokens of meaning.
    """
    def __init__(self, server):
        self.server = server

    @abstractmethod
    def scry_tokens(self, doc: TextDocument) -> List[RawToken]:
        """
        [THE RITE OF PERCEPTION]
        Returns a list of RawTokens found in the scripture.
        """
        pass