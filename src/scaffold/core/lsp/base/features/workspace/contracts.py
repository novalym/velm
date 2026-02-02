# Path: core/lsp/features/workspace/contracts.py
# ----------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Any, Optional, Dict
from .models import FileEvent, WorkspaceFolder

class WorkspaceProvider(ABC):
    """
    =============================================================================
    == THE COVENANT OF THE OBSERVATORY (INTERFACE)                             ==
    =============================================================================
    """
    def __init__(self, server: Any):
        self.server = server

    @abstractmethod
    def on_file_events(self, events: List[FileEvent]): pass

    @abstractmethod
    def on_folders_changed(self, added: List[WorkspaceFolder], removed: List[WorkspaceFolder]): pass