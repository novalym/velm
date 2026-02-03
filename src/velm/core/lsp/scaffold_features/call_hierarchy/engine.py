# Path: core/lsp/scaffold_features/call_hierarchy/engine.py
# ---------------------------------------------------------
from typing import Any
from ...base.features.call_hierarchy.engine import CallHierarchyEngine
from .providers.daemon_bridge import DaemonCallHierarchyProvider


class ScaffoldCallHierarchyEngine:
    """
    =============================================================================
    == THE HIERARCHY NEXUS (V-Ω-SCAFFOLD-AWARE)                                ==
    =============================================================================
    Factory for the Graph Tracer.
    """

    @staticmethod
    def forge(server: Any) -> CallHierarchyEngine:
        engine = CallHierarchyEngine(server)

        # Consecrate Capability
        server.register_capability(lambda caps: setattr(caps, 'call_hierarchy_provider', True))

        # Register the Daemon Bridge
        engine.register(DaemonCallHierarchyProvider(server))

        return engine