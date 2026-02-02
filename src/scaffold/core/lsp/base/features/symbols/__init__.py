# Path: core/lsp/features/symbols/__init__.py
# -------------------------------------------

"""
=================================================================================
== THE MAP ROOM (V-Ω-SYMBOL-CORE-V12)                                          ==
=================================================================================
The cartography engine of the Language Server.
It generates the hierarchical 'Outline' view of the document.

This is the PURE, language-agnostic foundation for structural mapping.
=================================================================================
"""

from .engine import SymbolEngine
from .contracts import SymbolProvider
from .models import DocumentSymbol, SymbolKind

__all__ = ["SymbolEngine", "SymbolProvider", "DocumentSymbol", "SymbolKind"]