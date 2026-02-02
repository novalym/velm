# Path: core/lsp/scaffold_features/semantic_tokens/engine.py
# ----------------------------------------------------------
from typing import Any
from ...base.features.semantic_tokens.engine import SemanticTokensEngine
from .providers import GnosticTokenProvider


class ScaffoldSemanticEngine:
    """
    =============================================================================
    == THE SCAFFOLD SEMANTIC ENGINE (V-Ω-INTEGRATION-V12)                      ==
    =============================================================================
    The High Priest of Illumination.
    Factory for binding Scaffold spectral logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> SemanticTokensEngine:
        # 1. Awake the Iron Core
        engine = SemanticTokensEngine(server)

        # 2. Consecrate and Register the Gnostic Prophet
        # This provider handles the entire Scaffold/Symphony grammar
        engine.register(GnosticTokenProvider(server))

        return engine