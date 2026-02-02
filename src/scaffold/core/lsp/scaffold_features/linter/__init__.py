# Path: core/lsp/scaffold_features/linter/__init__.py
# ------------------------------------------

"""
=================================================================================
== THE HALL OF JUDGMENT (V-Ω-MODULAR-LINTER)                                   ==
=================================================================================
The judicial center of the Language Server.
It orchestrates the validation of scripture against the Gnostic Laws.

[EXPORTS]:
- LinterEngine: The sovereign controller.
- AnalysisContext: The snapshot of reality passed to rules.
"""

from .engine import LinterEngine
from .context import AnalysisContext

__all__ = ["LinterEngine", "AnalysisContext"]