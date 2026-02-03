# Path: core/lsp/features/rename/contracts.py
# -------------------------------------------

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

# --- GNOSTIC UPLINKS ---
from ...types import WorkspaceEdit
from ...document import TextDocument
from ...utils.text import WordInfo

if TYPE_CHECKING:
    from ....server import GnosticLSPServer

class BaseRenameProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF TRANSMUTATION (ABSTRACT)                                ==
    =============================================================================
    The Template for all Reality-Shifting Artisans.
    """

    def __init__(self, server: 'GnosticLSPServer'):
        self.server = server

    @abstractmethod
    def supports(self, info: WordInfo) -> bool:
        """
        [THE GAZE OF FEASIBILITY]
        Determines if this provider can handle the symbol under the cursor.
        """
        pass

    @abstractmethod
    def provide(self, doc: TextDocument, info: WordInfo, new_name: str) -> Optional[WorkspaceEdit]:
        """
        [THE RITE OF REWRITING]
        Calculates the edits required to rename the symbol across the cosmos.
        Must return a WorkspaceEdit object mapping URIs to TextEdits.
        """
        pass