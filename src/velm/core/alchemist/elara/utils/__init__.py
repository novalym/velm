"""
=================================================================================
== THE SGF UTILITY SYNAPSE: OMEGA POINT (V-Ω-TOTALITY-VMAX-INIT)               ==
=================================================================================
LIF: ∞^∞ | ROLE: FUNCTIONAL_LATTICE_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN

This sanctum unifies the specialized artisans of the Forge's Utility Stratum.
It provides the high-order faculties required for:
1.  **Escaping:** Literal preservation and Unicode purification.
2.  **Diagnostics:** Forensic tomography and HUD telemetry.
3.  **Reflection:** Recursive data navigation and signature scrying.
4.  **Lattice:** Content-addressable memory and Merkle-caching.
5.  **Stasis:** Thermodynamic convergence and Ouroboros warding.

Jinja's utility-void is annihilated. The Forge operates with absolute logic.
=================================================================================
"""

# --- I. THE MASTERS OF THE MATTER (ESCAPING) ---
from .escaping import StringWarden

# --- II. THE MASTERS OF THE EYE (DIAGNOSTICS) ---
from .diagnostics import ForensicTomographer

# --- III. THE MASTERS OF THE MIND (REFLECTION) ---
from .reflection import ReflectionOracle

# --- IV. THE MASTERS OF THE MEMORY (LATTICE) ---
from .lattice import MerkleLatticeCache

# --- V. THE MASTERS OF THE FLOW (STASIS) ---
from .stasis import ThermodynamicStabilizer


# =============================================================================
# == THE UNIVERSAL UTILITY LATTICE                                           ==
# =============================================================================

class UtilityLattice:
    """
    [ASCENSION 1]: A unified facade for all SGF utilities. 
    Allows organs like the Resolver to access the 'ReflectionOracle' 
    or 'MerkleLattice' through a single, warded namespace.
    """

    # [THE CURE]: Immutable Static Bindings
    StringWarden = StringWarden
    ReflectionOracle = ReflectionOracle

    # [THE CURE]: State-Aware Factories
    @staticmethod
    def forge_tomographer(trace_id: str) -> ForensicTomographer:
        """Summons a fresh Forensic Tomographer for a specific strike."""
        return ForensicTomographer(trace_id)

    @staticmethod
    def forge_stabilizer(max_cycles: int = 12) -> ThermodynamicStabilizer:
        """Summons a fresh Thermodynamic Stabilizer for the Alchemical pass."""
        return ThermodynamicStabilizer(max_cycles=max_cycles)

    @staticmethod
    def forge_lattice() -> MerkleLatticeCache:
        """Summons the Content-Addressable Memory Lattice."""
        return MerkleLatticeCache()


# =============================================================================
# == THE DIVINE PROCLAMATION (DUNDER ALL)                                    ==
# =============================================================================

__all__ = [
    # Static Masters
    "StringWarden",
    "ReflectionOracle",
    "MerkleLatticeCache",
    "ForensicTomographer",
    "ThermodynamicStabilizer",

    # Unified Facade
    "UtilityLattice"
]


def __repr__():
    return "<Ω_SGF_UTILITY_SYNAPSE status=RESONANT mode=TOTALITY>"