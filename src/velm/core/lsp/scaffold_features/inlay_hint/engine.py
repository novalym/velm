# Path: core/lsp/scaffold_features/inlay_hint/engine.py
# -----------------------------------------------------
from typing import Any
from ...base.features.inlay_hint.engine import InlayHintEngine
from .providers import (
    VariableTypeProvider,
    MacroParamProvider,
    ShadowTruthProvider
)


class ScaffoldInlayHintEngine:
    """
    =============================================================================
    == THE SCAFFOLD INLAY HINT ENGINE (V-Ω-INTEGRATION-V12)                    ==
    =============================================================================
    The High Priest of Spectral Annotation.
    Factory for binding Scaffold ghost-writing logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> InlayHintEngine:
        # 1. Awake the Agnostic Iron Core
        engine = InlayHintEngine(server)

        # 2. Consecrate and Register the Scaffold Prophets
        # Order determines the order of appearance in the visual line
        engine.register(VariableTypeProvider(server))  # $$ var : type
        engine.register(MacroParamProvider(server))  # @call macro(name: val)
        engine.register(ShadowTruthProvider(server))  # {{ var }} = "actual_val"

        return engine