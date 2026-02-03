# Path: core/lsp/scaffold_features/workspace/engine.py
# -----------------------------------------------------
from typing import Any
from ...base.features.workspace.engine import WorkspaceEngine
from .commands import ScaffoldCommandProvider
from .watcher import ScaffoldFluxProvider


class ScaffoldWorkspaceEngine:
    """
    =============================================================================
    == THE SCAFFOLD WORKSPACE ENGINE (V-Ω-INTEGRATION-V12)                     ==
    =============================================================================
    The High Warden of the Monorepo.
    Factory for binding Scaffold macro-logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> WorkspaceEngine:
        # 1. Awake the Iron Core (Agnostic Watchers and Folders)
        engine = WorkspaceEngine(server)

        # 2. Consecrate Scaffold-specific Command Bridge
        # This registers 'scaffold.heal', 'scaffold.transmute', etc.
        commands = ScaffoldCommandProvider(server)
        commands.register_rites(engine.commands)

        # 3. Consecrate Scaffold-specific Flux Provider
        # This reacts to .scaffold and .lock changes
        watcher = ScaffoldFluxProvider(server)
        # In a full impl, the Agnostic Watcher allows external providers to subscribe
        # engine.watcher.subscribe(watcher)

        return engine