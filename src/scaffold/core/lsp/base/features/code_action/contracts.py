# Path: core/lsp/features/code_action/contracts.py
# -----------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Union
from .models import CodeAction, CodeActionParams, Diagnostic
from ...document import TextDocument
from ...types.primitives import Range

class CodeActionProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF THE PHYSICIAN (INTERFACE)                               ==
    =============================================================================
    Every specialized healer must sign this contract.
    It defines how to scry for potential cures based on diagnostics or cursor position.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of the action source."""
        pass

    @property
    def priority(self) -> int:
        """Determines the sort order (0-100)."""
        return 50

    @abstractmethod
    def provide_actions(self, doc: TextDocument, range: Range, diagnostics: List[Diagnostic]) -> List[CodeAction]:
        """
        [THE RITE OF DIAGNOSIS]
        Scans the context and returns potential CodeActions.
        """
        pass

    @abstractmethod
    def resolve_action(self, action: CodeAction) -> CodeAction:
        """
        [THE RITE OF SPLICING]
        Populates the 'edit' or 'command' field if it was deferred.
        """
        return action