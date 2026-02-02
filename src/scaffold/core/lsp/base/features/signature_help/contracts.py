# Path: core/lsp/features/signature_help/contracts.py
# ---------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Any, Dict
from .models import SignatureInformation
from ...document import TextDocument

@dataclass(frozen=True)
class InvocationContext:
    """The aura surrounding a callable summons."""
    uri: str
    symbol_name: str
    active_parameter: int
    full_line: str
    prefix: str
    trace_id: str = "0xVOID"

class SignatureProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF THE SUMMONS (INTERFACE)                                 ==
    =============================================================================
    Every language-specific oracle must sign this contract to provide help
    for their specific callable archetypes.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str: pass

    @property
    def priority(self) -> int: return 50

    @abstractmethod
    def provide_signatures(self, ctx: InvocationContext) -> List[SignatureInformation]:
        """
        [THE RITE OF REVELATION]
        Returns potential signatures for the identified symbol.
        """
        pass