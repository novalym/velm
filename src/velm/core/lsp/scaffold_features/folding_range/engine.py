# Path: core/lsp/scaffold_features/folding_range/engine.py
# --------------------------------------------------------

from typing import Any, List
from ...base.features.folding_range.engine import FoldingRangeEngine
from ...base.features.folding_range.models import FoldingRange, FoldingRangeParams

# --- THE COUNCIL OF COMPRESSORS ---
from .providers.gnostic_structure import GnosticStructureProvider
from .providers.content_block import ContentBlockProvider
from .providers.indentation_fallback import IndentationFallbackProvider
from .providers.commentary import CommentaryProvider


class ScaffoldFoldingEngine:
    """
    =============================================================================
    == THE SCAFFOLD FOLDING ENGINE (V-Ω-GEOMETRIC-ORCHESTRATOR)                ==
    =============================================================================
    LIF: 10,000,000 | ROLE: SPATIAL_COMPRESSOR

    Coordinates specialized providers to map the fold-lines of reality.
    """

    @staticmethod
    def forge(server: Any) -> FoldingRangeEngine:
        # 1. Awake the Iron Core
        engine = FoldingRangeEngine(server)

        # 2. Consecrate the Capability
        server.register_capability(lambda caps: setattr(caps, 'folding_range_provider', True))

        # 3. Register the Council (Priority Order)
        # Specific syntax providers run first.
        engine.register(GnosticStructureProvider(server))  # @if, %%
        engine.register(ContentBlockProvider(server))  # :: """ ... """
        engine.register(CommentaryProvider(server))  # # ...

        # Fallback to indentation for anything else (e.g. nested lists)
        engine.register(IndentationFallbackProvider(server))

        return engine