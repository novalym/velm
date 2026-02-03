# Path: core/lsp/base/features/type_hierarchy/contracts.py
# --------------------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Any
from .models import TypeHierarchyItem
from ...document import TextDocument
from ...types.primitives import Position

class TypeHierarchyProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF GENETICS (INTERFACE)                                    ==
    =============================================================================
    Every lineage tracer must sign this contract.
    It defines how to resolve the ancestors (Supertypes) and descendants (Subtypes).
    """

    def __init__(self, server: Any = None):
        self.server = server

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def prepare(self, doc: TextDocument, position: Position) -> List[TypeHierarchyItem]:
        """
        [THE RITE OF IDENTIFICATION]
        Identifies the type at the cursor to start the hierarchy.
        """
        pass

    def supertypes(self, item: TypeHierarchyItem) -> List[TypeHierarchyItem]:
        """[THE RITE OF ASCENSION] Who are the parents?"""
        return []

    def subtypes(self, item: TypeHierarchyItem) -> List[TypeHierarchyItem]:
        """[THE RITE OF DESCENSION] Who are the children?"""
        return []