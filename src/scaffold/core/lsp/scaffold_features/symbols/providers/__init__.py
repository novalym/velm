# Path: core/lsp/scaffold_features/symbols/providers/__init__.py
# ------------------------------------------------------------

"""
=================================================================================
== THE COUNCIL OF GEOMETERS (V-Ω-SYMBOL-PROVIDERS)                             ==
=================================================================================
The assembly of specialized scanners that perceive structure in chaos.

[EXPORTS]:
- VariableProvider: $$ var
- LogicProvider: @if, @for
- MatterProvider: file.ext :: "content"
- MaestroProvider: %% post-run
- PolyglotProvider: python:
"""

from .variables import VariableProvider
from .logic import LogicProvider
from .matter import MatterProvider
from .maestro import MaestroProvider
from .polyglot import PolyglotProvider

__all__ = [
    "VariableProvider",
    "LogicProvider",
    "MatterProvider",
    "MaestroProvider",
    "PolyglotProvider"
]