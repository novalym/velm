# Path: core/lsp/scaffold_features/type_hierarchy/engine.py
# ---------------------------------------------------------
from typing import Any
from ...base.features.type_hierarchy.engine import TypeHierarchyEngine
from .providers.daemon_bridge import DaemonTypeHierarchyProvider


class ScaffoldTypeHierarchyEngine:
    """
    =============================================================================
    == THE GENETIC NEXUS (V-Ω-SCAFFOLD-AWARE)                                  ==
    =============================================================================
    Factory for the Genetic Tracer.
    """

    @staticmethod
    def forge(server: Any) -> TypeHierarchyEngine:
        engine = TypeHierarchyEngine(server)

        # Consecrate Capability
        server.register_capability(lambda caps: setattr(caps, 'type_hierarchy_provider', True))

        # Register the Daemon Bridge
        engine.register(DaemonTypeHierarchyProvider(server))

        return engine