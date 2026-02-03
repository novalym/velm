# Path: core/lsp/scaffold_features/code_lens/engine.py
# -----------------------------------------------------
from typing import Any
from ...base.features.code_lens.engine import CodeLensEngine
from .providers import (
    KineticActionProvider,
    BlueprintHealerProvider,
    IntelligenceProvider
)


class ScaffoldCodeLensEngine:
    """
    =============================================================================
    == THE SCAFFOLD CODE LENS ENGINE (V-Ω-INTEGRATION-V12)                     ==
    =============================================================================
    The High Priest of Action.
    Factory for binding Scaffold kinetic logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> CodeLensEngine:
        # 1. Awake the Iron Core
        engine = CodeLensEngine(server)

        # 2. Consecrate and Register the Scaffold Prophets
        # Priority determines vertical stack order in the gutter
        engine.register(BlueprintHealerProvider(server))  # Priority 100: Fixes first
        engine.register(KineticActionProvider(server))  # Priority 90:  Execution
        engine.register(IntelligenceProvider(server))  # Priority 50:  Insight

        return engine