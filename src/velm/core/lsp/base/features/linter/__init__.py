# Path: core/lsp/base/features/linter/__init__.py
# -----------------------------------------------

"""
=================================================================================
== THE HALL OF RULES (V-Ω-LINTER-BASE)                                         ==
=================================================================================
The abstract engine for static analysis.
It defines the physics of how a Document is judged against a set of Laws.

[EXPORTS]:
- LinterEngine: The central processor that runs the rules.
- LinterRule: The abstract contract for a single unit of logic.
"""

from .engine import LinterEngine
from .contracts import LinterRule

__all__ = ["LinterEngine", "LinterRule"]