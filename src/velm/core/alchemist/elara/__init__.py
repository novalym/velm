"""
=================================================================================
== THE SOVEREIGN GNOSTIC FORGE (SGF) (V-Ω-TOTALITY-V1)                         ==
=================================================================================
LIF: ∞^∞ | ROLE: NATIVE_LOGIC_SYNTHESIS_ENGINE | RANK: OMEGA_PROGENITOR
AUTH_CODE: Ω_SGF_ENTRY_V1_AMNESTY_SHIELD_FINALIS

[THE MANIFESTO]
The Jinja era is dead. This is the Sovereign Gnostic Forge.
It does not parse text; it perceives Topography and Intent.
It grants Absolute Amnesty to alien syntax. It enforces Isomorphic Indentation.
It is mathematically warded against the "Unexpected End of Template" heresy.
=================================================================================
"""

from .engine import SGFEngine
from .constants import SGFTokens
from .contracts.atoms import GnosticToken, TokenType
from .scanner import GnosticScanner

__all__ = [
    "SGFEngine",
    "GnosticScanner",
    "GnosticToken",
    "TokenType",
    "SGFTokens"
]