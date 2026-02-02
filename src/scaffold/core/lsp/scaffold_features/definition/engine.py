# Path: core/lsp/scaffold_features/definition/engine.py
# -----------------------------------------------------
from typing import Any
from ...base.features.definition.engine import DefinitionEngine
from .rules import (
    LocalVariableRule,
    FileLinkRule,
    GlobalCortexRule,
    MacroRule,
    StandardLibraryRule,
)


class ScaffoldDefinitionEngine:
    """
    =============================================================================
    == THE SCAFFOLD DEFINITION ENGINE (V-Ω-INTEGRATION-V12)                    ==
    =============================================================================
    The High Priest of Origins.
    Factory for binding Scaffold navigation logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> DefinitionEngine:
        engine = DefinitionEngine(server)

        # 1. Local Symbols (Keystroke-level speed)
        engine.register(LocalVariableRule(server))   # Priority 100
        engine.register(MacroRule(server))           # Priority 95

        # 2. Physical Reality (Filesystem)
        engine.register(FileLinkRule(server))        # Priority 90

        # 3. Deep Gnosis (Daemon/Cortex)
        engine.register(GlobalCortexRule(server))    # Priority 50

        # 4. Universal Laws (Built-ins)
        engine.register(StandardLibraryRule(server)) # Priority 10

        return engine