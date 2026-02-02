# Path: core/lsp/scaffold_features/symbols/providers/base.py
# ----------------------------------------------------------

from abc import ABC
from ....base.features.symbols.contracts import SymbolProvider


class BaseSymbolProvider(SymbolProvider, ABC):
    """
    =============================================================================
    == THE SCAFFOLD SYMBOL BRIDGE                                              ==
    =============================================================================
    Inherits from the Iron Core's `SymbolProvider`.

    It remains Abstract (ABC) because it does not implement `extract`.
    Specific providers (VariableProvider, LogicProvider) will inherit from this
    and implement the `extract` rite.

    [ANCESTRY]:
    SymbolProvider (Core) -> BaseSymbolProvider (Scaffold) -> ConcreteProvider
    """
    pass