# Path: core/lsp/scaffold_features/references/engine.py
# ------------------------------------------------------
from typing import Any
from ...base.features.references.engine import ReferenceEngine
from .providers import (
    LocalUsageProvider,
    InclusionProvider,
    DaemonCortexProvider
)


class ScaffoldReferenceEngine:
    """
    =============================================================================
    == THE SCAFFOLD REFERENCE ENGINE (V-Ω-INTEGRATION-V12)                     ==
    =============================================================================
    The High Priest of Echoes.
    Factory for binding Scaffold relational logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> ReferenceEngine:
        # 1. Awake the Iron Core
        engine = ReferenceEngine(server)

        # 2. Consecrate and Register the Scaffold Seekers
        # Priority 100: Instant Local Usage ({{ var }})
        engine.register(LocalUsageProvider(server))

        # Priority 90: Inclusion Tracing (@include, <<)
        engine.register(InclusionProvider(server))

        # Priority 50: Global Daemon Search (Cortex)
        engine.register(DaemonCortexProvider(server))

        return engine