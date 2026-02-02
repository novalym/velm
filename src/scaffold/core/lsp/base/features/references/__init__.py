# Path: core/lsp/features/references/__init__.py
# -----------------------------------------------

"""
=================================================================================
== THE ECHO CHAMBER (V-Ω-REFERENCE-CORE-V12)                                   ==
=================================================================================
The relational center of the Language Server.
It resolves all usages and echoes of a symbol across the project constellation.

This is the PURE, language-agnostic foundation.
=================================================================================
"""

from .engine import ReferenceEngine
from .contracts import ReferenceProvider
from .models import ReferenceParams, Location, ReferenceContext

__all__ = ["ReferenceEngine", "ReferenceProvider", "ReferenceParams", "Location", "ReferenceContext"]