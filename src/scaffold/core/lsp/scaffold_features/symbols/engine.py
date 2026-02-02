# Path: core/lsp/scaffold_features/symbols/engine.py
# --------------------------------------------------

from typing import Any
from ...base.features.symbols.engine import SymbolEngine
from .providers import (
    VariableProvider,
    LogicProvider,
    MatterProvider,
    MaestroProvider,
    PolyglotProvider
)

class ScaffoldSymbolEngine:
    """
    =============================================================================
    == THE SCAFFOLD SYMBOL ENGINE (V-Ω-CONSECRATED)                            ==
    =============================================================================
    LIF: INFINITY | ROLE: TOPOLOGICAL_NAVIGATOR
    """

    @staticmethod
    def forge(server: Any) -> SymbolEngine:
        engine = SymbolEngine(server)

        # [ASCENSION: CONSECRATION]
        # Informs the Kernel that we provide the 'Outline' view.
        server.register_capability(lambda caps: setattr(caps, 'document_symbol_provider', True))

        # Register the Geometers
        engine.register(VariableProvider(server))
        engine.register(LogicProvider(server))
        engine.register(PolyglotProvider(server))
        engine.register(MaestroProvider(server))
        engine.register(MatterProvider(server))

        return engine