# Path: core/lsp/features/rename/contracts.py
# -------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Union, List, Any, Dict
from .models import WorkspaceEdit, TextEdit
from ...document import TextDocument
from ...utils.text import WordInfo

@dataclass(frozen=True)
class RenameContext:
    """The Aura surrounding the rename event."""
    uri: str
    original_name: str
    new_name: str
    info: WordInfo
    workspace_root: Optional[Any] = None
    trace_id: str = "0xVOID"

class RenameMutator(ABC):
    """
    =============================================================================
    == THE COVENANT OF THE SCRIBE (MUTATOR INTERFACE)                          ==
    =============================================================================
    Every language-specific rewrite strategy must sign this contract.
    """
    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str: pass

    @property
    def priority(self) -> int: return 50

    @abstractmethod
    def provide_edits(self, doc: TextDocument, ctx: RenameContext) -> Optional[WorkspaceEdit]:
        """Calculates the necessary TextEdits for this symbol."""
        pass

class RenameValidator(ABC):
    """
    =============================================================================
    == THE COVENANT OF PRUDENCE (VALIDATOR INTERFACE)                         ==
    =============================================================================
    Defines whether a symbol is allowed to be renamed.
    """
    def __init__(self, server: Any):
        self.server = server

    @abstractmethod
    def validate(self, doc: TextDocument, info: WordInfo) -> Optional[Any]:
        """Returns the valid range if rename is permitted, else None."""
        pass