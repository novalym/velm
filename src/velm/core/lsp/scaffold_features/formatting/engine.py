# Path: core/lsp/scaffold_features/formatting/engine.py
# ------------------------------------------------------
from typing import Any
from ...base.features.formatting.engine import FormattingEngine
from .providers import ScaffoldBeautifier


class ScaffoldFormattingEngine:
    """
    =============================================================================
    == THE SCAFFOLD FORMATTING ENGINE (V-Ω-INTEGRATION-V12)                    ==
    =============================================================================
    The High Priest of Geometry.
    Factory for binding Scaffold aesthetic logic to the Agnostic Core.
    """

    @staticmethod
    def forge(server: Any) -> FormattingEngine:
        # 1. Awake the Iron Core
        engine = FormattingEngine(server)

        # 2. Consecrate and Register the Scaffold Purifier
        # Since it's the primary language, we give it high priority.
        engine.register(ScaffoldBeautifier(server))

        return engine