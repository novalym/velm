# Path: core/lsp/scaffold_features/inline_completion/engine.py
# ------------------------------------------------------------

from typing import Any
from ...base.features.inline_completion.engine import InlineCompletionEngine
from .providers.muse import MuseProphet
from .providers.snippet import SnippetProphet

class ScaffoldInlineCompletionEngine:
    """
    =============================================================================
    == THE SCAFFOLD PROPHETIC ENGINE (V-Ω-CONSECRATED)                         ==
    =============================================================================
    LIF: INFINITY | ROLE: FORESIGHT_DISPATCHER
    """

    @staticmethod
    def forge(server: Any) -> InlineCompletionEngine:
        # 1. Awake the Iron Core
        engine = InlineCompletionEngine(server)

        # 2. Consecrate the Capability
        server.register_capability(lambda caps: setattr(caps, 'inline_completion_provider', True))

        # 3. Register the Prophets
        engine.register(MuseProphet(server))     # AI / Daemon
        engine.register(SnippetProphet(server))  # Local Context

        return engine