# Path: core/lsp/base/features/document_link/contracts.py
# -------------------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Any, Optional
from .models import DocumentLink
from ...document import TextDocument

class DocumentLinkProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF CONNECTION (INTERFACE)                                  ==
    =============================================================================
    Every link weaver must sign this contract.
    It defines how to scan scripture for portals and where they lead.
    """

    def __init__(self, server: Any = None):
        self.server = server

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def provide_links(self, doc: TextDocument) -> List[DocumentLink]:
        """
        [THE RITE OF WEAVING]
        Scans the scripture and returns a list of potential wormholes.
        """
        pass

    def resolve_link(self, link: DocumentLink) -> Optional[DocumentLink]:
        """
        [THE RITE OF RESOLUTION]
        Lazy-loads the target or tooltip for a link.
        """
        return link