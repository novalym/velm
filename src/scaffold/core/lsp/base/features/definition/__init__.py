# Path: core/lsp/features/definition/__init__.py
# ----------------------------------------------

"""
=================================================================================
== THE HALL OF ORIGINS (V-Ω-DEFINITION-CORE-V12)                               ==
=================================================================================
The navigational center of the Language Server.
It resolves the genesis point of symbols, variables, and paths.

This is the PURE, language-agnostic foundation for causal tracing.
=================================================================================
"""

from .engine import DefinitionEngine
from .contracts import DefinitionRule
from .models import Location, LocationLink, DefinitionParams

__all__ = ["DefinitionEngine", "DefinitionRule", "Location", "LocationLink", "DefinitionParams"]