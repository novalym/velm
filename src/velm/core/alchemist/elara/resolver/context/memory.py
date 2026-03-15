# Path: core/alchemist/elara/resolver/context/memory.py
# -----------------------------------------------------

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .engine import LexicalScope

class MemorySuture:
    """
    =============================================================================
    == THE MEMORY SUTURE (V-Ω-LAMINAR-REFERENCE)                               ==
    =============================================================================
    LIF: ∞ | ROLE: PHYSICAL_POINTER_PRESERVER
    Mathematically guarantees that internal Engine pointers are shared by physical
    REFERENCE across all scopes, annihilating Anomaly 236 (Ghost Projects).
    """

    RESERVOIRS = (
        '__woven_matter__', '__woven_commands__', '__engine__',
        '__alchemist__', '__trace_id__', '__current_file__', '__current_dir__'
    )

    @classmethod
    def bind_reservoirs(cls, scope: 'LexicalScope'):
        """Surgically copies the memory address (id) of Prime Reservoirs."""
        for key in cls.RESERVOIRS:
            prime_val = scope.global_ctx.variables.get(key)
            if prime_val is None and scope.parent:
                prime_val = scope.parent.get(key)

            if prime_val is not None:
                # Use dict.__setitem__ to bypass GnosticSovereignDict's auto-wrapping,
                # ensuring the physical pointer is never severed or shadowed.
                dict.__setitem__(scope.local_vars, key, prime_val)