# Path: core/alchemist/environment/__init__.py
# --------------------------------------------

"""
=================================================================================
== THE COGNITIVE BIOSPHERE (V-Ω-ENVIRONMENT-SANCTUM-VMAX)                      ==
=================================================================================
LIF: ∞^∞ | ROLE: LEXICAL_AND_METABOLIC_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_BIOSPHERE_VMAX_JINJA_EXORCISM_2026_FINALIS

[THE MANIFESTO]
This Sanctum houses the native SGF Environment. It is the absolute replacement
for the legacy Jinja2 `.env`. It manages the global namespace, custom filters,
and metabolic caching natively, providing an isomorphic interface for all legacy
Scribes while operating entirely on the ELARA AST backend.
=================================================================================
"""

from .engine import SGFEnvironment
from .globals_vault import SGFGlobalsVault
from .filters_vault import SGFFiltersVault
from .cache_warden import SGFCacheWarden

__all__ = [
    "SGFEnvironment",
    "SGFGlobalsVault",
    "SGFFiltersVault",
    "SGFCacheWarden"
]