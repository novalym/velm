# Path: core/lsp/scaffold_features/selection_range/engine.py
# --------------------------------------------------------
from typing import Any
from ...base.features.selection_range.engine import SelectionRangeEngine
from .providers.semantic_expander import SemanticExpanderProvider


class ScaffoldSelectionRangeEngine:
    """
    =============================================================================
    == THE GEOMETRIC EXPANDER (V-Ω-SCAFFOLD-AWARE)                             ==
    =============================================================================
    Factory for the Smart Selection capability.
    """

    @staticmethod
    def forge(server: Any) -> SelectionRangeEngine:
        engine = SelectionRangeEngine(server)

        # Consecrate Capability
        server.register_capability(lambda caps: setattr(caps, 'selection_range_provider', True))

        # Register the Semantic Expander
        engine.register(SemanticExpanderProvider(server))

        return engine