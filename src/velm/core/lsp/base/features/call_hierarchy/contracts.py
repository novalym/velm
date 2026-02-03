# Path: core/lsp/base/features/call_hierarchy/contracts.py
# --------------------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Any
from .models import (
    CallHierarchyItem, CallHierarchyIncomingCall, CallHierarchyOutgoingCall
)
from ...document import TextDocument
from ...types.primitives import Position

class CallHierarchyProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF LINEAGE (INTERFACE)                                     ==
    =============================================================================
    Every graph tracer must sign this contract.
    It defines how to resolve the ancestry and descendants of a symbol.
    """

    def __init__(self, server: Any = None):
        self.server = server

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def prepare(self, doc: TextDocument, position: Position) -> List[CallHierarchyItem]:
        """
        [THE RITE OF IDENTIFICATION]
        Identifies the symbol at the cursor to start the hierarchy.
        """
        pass

    def incoming_calls(self, item: CallHierarchyItem) -> List[CallHierarchyIncomingCall]:
        """[THE RITE OF ANCESTRY] Who calls this?"""
        return []

    def outgoing_calls(self, item: CallHierarchyItem) -> List[CallHierarchyOutgoingCall]:
        """[THE RITE OF DESCENDANTS] Who does this call?"""
        return []