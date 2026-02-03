# Path: core/lsp/features/workspace/engine.py
# -------------------------------------------
import logging
import time
from typing import List, Any, Dict, Optional
from .models import WorkspaceFolder, FileEvent, ExecuteCommandParams, WorkspaceSymbolParams
from .folders.manager import FolderManager
from .watcher.core import FluxWatcher
from .commands.router import CommandRouter
from .symbols.scryer import LocalScryer

Logger = logging.getLogger("WorkspaceEngine")

class WorkspaceEngine:
    """
    =============================================================================
    == THE HIGH WARDEN (V-Ω-TOTALITY-ORCHESTRATOR-V12)                         ==
    =============================================================================
    The supreme coordinator of project-wide awareness.
    """
    def __init__(self, server: Any):
        self.server = server
        self.folders = FolderManager(server)
        self.watcher = FluxWatcher(server)
        self.commands = CommandRouter(server)
        self.symbols = LocalScryer(server)

    def handle_folders_changed(self, params: Any):
        added = [WorkspaceFolder(**f) for f in params.get('added', [])]
        removed = [WorkspaceFolder(**f) for f in params.get('removed', [])]
        self.folders.update(added, removed)
        self.watcher.realign_boundaries(added, removed)

    def handle_watched_files(self, params: Any):
        events = [FileEvent(**e) for e in params.get('changes', [])]
        self.watcher.ingest_flux(events)

    def handle_execute_command(self, params: ExecuteCommandParams) -> Any:
        return self.commands.dispatch(params.command, params.arguments or [])

    def handle_workspace_symbols(self, params: WorkspaceSymbolParams) -> List[Dict]:
        return self.symbols.scry(params.query)