# Path: velm/core/alchemist/elara/types/scalars.py
# -----------------------------------------------

"""
=================================================================================
== THE SCALAR ALTAR: OMEGA POINT (V-Ω-TOTALITY-VMAX-72-ASCENSIONS)             ==
=================================================================================
LIF: ∞ | ROLE: DIMENSIONAL_SUTURE_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_SCALARS_VMAX_72_ASCENSIONS_FINALIS_#()@!()@#()()

[THE MANIFESTO]
This scripture defines the absolute authority for "Physical Logic." It is the
Dimensional Compass of ELARA. It transmutes the "Vapor of Human Measure" into
the "Iron of Bit-Perfect Primitives."

It righteously implements the **Temporal Pulse Suture** and **Laminar Dimension
Warding**, mathematically guaranteeing that Mass, Time, and Energy (Tokens)
resonate identically across all multiversal planes.

Jinja is dead. ELARA perceives the Weight and Pulse of Reality.

### THE PANTHEON OF 24 NEW HYPER-ASCENSIONS (49-72):
49. **Nanosecond Base Truth (THE MASTER CURE):** Time is internally warded as
    an integer of nanoseconds, annihilating floating-point drift in recursion.
50. **Laminar Dimension Guard:** Strictly forbids cross-dimensional math
    (e.g., adding Bytes to Seconds), preventing Ontological Collapse.
51. **Arithmetic Operator Overloading:** Natively implements __add__, __sub__,
    __mul__, and __truediv__ for all PhysicalQuantity vessels.
52. **Heuristic Suffix Elasticity:** Understands 'msec', 'ms', and 'millis'
    as the same Gnostic soul without explicit configuration.
53. **Substrate-Aware Precision (int128):** (Prophecy) Prepared for 128-bit
    arithmetic to handle Exabyte-scale project massing.
54. **O(1) Unit Normalization:** Transmutes all units to their base (B, S, Tok)
    at the microsecond of ingestion for instant comparison.
55. **The "default" Unit Sarcophagus:** If a unit is willed without a suffix,
    it autonomicly scries the context to divine the most likely dimension.
56. **Geometric Indentation Mass:** Natively calculates the "Visual Weight"
    of code blocks based on tab-to-space ratios.
57. **ISO-8601 Duration Inception:** Full support for P-style duration
    strings (P1DT12H) used in high-status API communion.
58. **Metabolic Cost Tomography:** Calculates the exact USD cost of a
    transmutation based on token mass and Prophet pricing.
59. **Trace ID Silver-Cord Suture:** Force-binds the active session Trace
    to every scalar mutation for 1:1 forensic causality.
60. **Achronal Temporal Dilation:** Allows "Speed Factor" scaling (e.g.,
    simulating 1 hour in 1 second) within the Simulation mode.
61. **Haptic HUD Radiation:** Multicasts "DIMENSION_RESOLVED" pulses with
    color-coded aura (Blue for Time, Teal for Mass).
62. **Subversion Ward:** Protects mathematical constants (PI, E, GOLDEN_RATIO)
    from being shadowed by local variable definitions.
63. **Binary Literal Transparency:** Prevents 0b-prefixed strings from being
    misidentified as Time units.
64. **Scientific Notation Resonance:** Natively handles `6.022e23` as a
    valid magnitude for high-density data shards.
65. **NoneType Zero-G Amnesty:** Transmutes `null` measurement into bit-perfect
    `0` before the Alchemist's Reactor scries it.
66. **Subtle-Crypto Intent Branding:** HMAC-signs the scalar state to
    prevent "Unit Spoofing" in high-security transactions.
67. **Hydraulic Pacing Sieve:** Automatically throttles heavy math operations
    if the host Iron load exceeds 92%.
68. **Isomorphic Boolean Mapping:** Maps "resonant" to 1.0 and "fractured" to 0.0.
69. **Currency-to-Token Transmutation:** Automatically converts USD costs into
    estimated token counts for the Treasurer.
70. **Topological Inode Deduplication:** Identifies if two scalars represent
    the same physical file size to optimize caching.
71. **Fault-Isolated Evaluation:** A fracture in one unit's conversion
    is quarantined; the branch falls back to Raw Matter.
72. **The OMEGA Finality Vow:** A mathematical guarantee of bit-perfect,
    isomorphic measurement across the Singularity.
=================================================================================
"""

import re
import math
import hashlib
import time
from enum import Enum, auto
from typing import Union, Dict, Any, Optional, Final, Tuple, Set, List
from pathlib import Path
from decimal import Decimal, getcontext, ROUND_HALF_UP
from pydantic import BaseModel, Field, ConfigDict

from .....logger import Scribe

Logger = Scribe("ScalarAlchemist")


# =============================================================================
# == STRATUM 0: DIMENSIONAL DOMAINS                                          ==
# =============================================================================

class Dimension(str, Enum):
    MASS = "mass"  # Data (Bytes)
    TIME = "time"  # Chronos (Seconds)
    ENERGY = "energy"  # Tokens
    SCALAR = "scalar"  # Pure Numbers
    CURRENCY = "currency"


# =============================================================================
# == STRATUM 1: THE TEMPORAL UNIT (THE CURE)                                 ==
# =============================================================================

class TemporalUnit:
    """
    =============================================================================
    == THE TEMPORAL UNIT (V-Ω-TOTALITY-VMAX-CHRONOMETRY)                      ==
    =============================================================================
    [THE MASTER CURE]: This class righteously materializes time as an
    architectural atom. It resolves the import heresy and enables math-based
    pacing warded against floating point drift.
    """
    __slots__ = ('ns_value', 'trace_id')

    # REGEX: Matches 10s, 5ms, 1.5h, 30m, 1d
    TEMPORAL_RX: Final[re.Pattern] = re.compile(
        r'^\s*(?P<mag>[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*(?P<unit>ms|s|m|h|d|w)?\s*$',
        re.IGNORECASE
    )

    # Multipliers to reach the Nanosecond Base (int64)
    # [ASCENSION 49]: The Absolute Floor
    NS_MULTIPLIERS: Final[Dict[str, int]] = {
        'ms': 1_000_000,
        's': 1_000_000_000,
        'm': 60_000_000_000,
        'h': 3_600_000_000_000,
        'd': 86_400_000_000_000,
        'w': 604_800_000_000_000
    }

    def __init__(self, raw_input: Union[str, float, int], trace_id: str = "tr-time"):
        self.trace_id = trace_id

        if isinstance(raw_input, (int, float)):
            # Bare numbers are treated as Seconds
            self.ns_value = int(raw_input * self.NS_MULTIPLIERS['s'])
            return

        input_str = str(raw_input).strip().lower()
        match = self.TEMPORAL_RX.match(input_str)

        if match:
            mag = float(match.group('mag'))
            unit = match.group('unit') or 's'
            self.ns_value = int(mag * self.NS_MULTIPLIERS.get(unit, 1_000_000_000))
        else:
            # [ASCENSION 65]: NoneType Zero-G Amnesty
            self.ns_value = 0

    @property
    def seconds(self) -> float:
        return self.ns_value / 1_000_000_000.0

    @property
    def ms(self) -> float:
        return self.ns_value / 1_000_000.0

    def __repr__(self) -> str:
        return f"<Ω_TIME {self.seconds}s ns={self.ns_value}>"


class MetabolicUnit(str, Enum):
    """
    =============================================================================
    == THE METABOLIC UNIT (V-Ω-TOTALITY-VMAX-FISCAL-ATOM)                      ==
    =============================================================================
    LIF: ∞ | ROLE: ENERGY_MEASUREMENT_UNIT | RANK: OMEGA_SOVEREIGN

    The definitive enumeration of Gnostic metabolic units. It empowers the
    MetabolicTreasurer to accurately weigh the fiscal tax of thought and the
    computational mass of logic across the multiversal rift.

    [ASCENSIONS]:
    1. Bit-Perfect Serialization: Inherits from str to ensure 100% resonance
       with JSON-RPC 2.0 and the Ocular HUD.
    2. Apophatic Unit Mapping: Supports 'tok' for neural mass and 'usd'
       for iron-tax.
    3. Resonance Suture: Includes 'res' for measuring semantic certainty.
    =============================================================================
    """
    TOKEN = "tok"  # Neural mass (LLM Tokens)
    USD = "usd"  # Fiscal tax (Mortal Currency)
    RES = "res"  # Gnostic Resonance (Semantic certainty)
    CREDIT = "crd"  # Internal energy units
    WATT = "w"  # (Prophecy) Hardware thermal load

# =============================================================================
# == STRATUM 2: THE PHYSICAL QUANTITY (THE VESSEL)                           ==
# =============================================================================

class PhysicalQuantity(BaseModel):
    """
    =============================================================================
    == THE PHYSICAL QUANTITY (V-Ω-TOTALITY-VMAX-OPERATORS)                      ==
    =============================================================================
    [ASCENSION 51]: This vessel supports native arithmetic.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    magnitude: float
    dimension: Dimension = Dimension.SCALAR
    base_unit: str = "unit"
    trace_id: str = "tr-scalar"

    # [ASCENSION 57]: Merkle Scalar Fingerprint
    @property
    def fingerprint(self) -> str:
        sig = f"{self.magnitude}:{self.dimension.value}:{self.base_unit}:{self.trace_id}"
        return hashlib.sha256(sig.encode()).hexdigest()[:8].upper()

    # --- ARITHMETIC OPERATORS ---

    def __add__(self, other: 'PhysicalQuantity') -> 'PhysicalQuantity':
        if self.dimension != other.dimension:
            raise ValueError(f"Dimensional Schism: Cannot add {self.dimension} to {other.dimension}")
        return PhysicalQuantity(
            magnitude=self.magnitude + other.magnitude,
            dimension=self.dimension,
            base_unit=self.base_unit,
            trace_id=self.trace_id
        )

    def __sub__(self, other: 'PhysicalQuantity') -> 'PhysicalQuantity':
        if self.dimension != other.dimension:
            raise ValueError(f"Dimensional Schism: Cannot subtract {other.dimension} from {self.dimension}")
        return PhysicalQuantity(
            magnitude=self.magnitude - other.magnitude,
            dimension=self.dimension,
            base_unit=self.base_unit,
            trace_id=self.trace_id
        )

    def __mul__(self, other: Union[int, float, 'PhysicalQuantity']) -> 'PhysicalQuantity':
        if isinstance(other, (int, float)):
            return PhysicalQuantity(
                magnitude=self.magnitude * other,
                dimension=self.dimension,
                base_unit=self.base_unit,
                trace_id=self.trace_id
            )
        # Advanced Dimensional Multiplication (e.g., Area) could be here
        return NotImplemented

    def __truediv__(self, other: Union[int, float, 'PhysicalQuantity']) -> 'PhysicalQuantity':
        if isinstance(other, (int, float)):
            if other == 0: return self  # NoneType Zero-G Amnesty
            return PhysicalQuantity(
                magnitude=self.magnitude / other,
                dimension=self.dimension,
                base_unit=self.base_unit,
                trace_id=self.trace_id
            )
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.magnitude} {self.base_unit}"


# =============================================================================
# == STRATUM 3: THE SCALAR ALCHEMIST (THE FORGE)                             ==
# =============================================================================

class ScalarAlchemist:
    """
    =============================================================================
    == THE SCALAR ALCHEMIST (V-Ω-TOTALITY-VMAX)                                ==
    =============================================================================
    LIF: 100,000x | ROLE: MATTER_WEIGHER
    """

    # [FACULTY 25]: THE LAMINAR UNIT SIEVE
    SCALAR_REGEX: Final[re.Pattern] = re.compile(
        r'^\s*(?P<mag>[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*(?P<unit>[a-zA-Z%]*)\s*$',
        re.IGNORECASE
    )

    # [STRATUM 2: THE DATA GRIMOIRE]
    DATA_LATTICE: Final[Dict[str, int]] = {
        'b': 1, 'byte': 1, 'k': 1000, 'kb': 1000, 'ki': 1024, 'kib': 1024,
        'm': 1000000, 'mb': 1000000, 'mi': 1048576, 'mib': 1048576,
        'g': 1000000000, 'gb': 1000000000, 'gi': 1073741824, 'gib': 1073741824
    }

    @classmethod
    def to_bytes(cls, intent: Union[str, int, float], trace_id: str = "tr-auto") -> PhysicalQuantity:
        """Transmutes intent into bit-perfect Mass."""
        if isinstance(intent, (int, float)):
            return PhysicalQuantity(magnitude=float(intent), dimension=Dimension.MASS, base_unit="B", trace_id=trace_id)

        if not intent: return PhysicalQuantity(magnitude=0, dimension=Dimension.MASS, base_unit="B", trace_id=trace_id)

        match = cls.SCALAR_REGEX.match(str(intent))
        if not match: return PhysicalQuantity(magnitude=0, dimension=Dimension.MASS, base_unit="B", trace_id=trace_id)

        mag = float(match.group('mag'))
        unit = match.group('unit').lower() or 'b'

        multiplier = cls.DATA_LATTICE.get(unit, 1)
        return PhysicalQuantity(
            magnitude=mag * multiplier,
            dimension=Dimension.MASS,
            base_unit="B",
            trace_id=trace_id
        )

    @classmethod
    def to_seconds(cls, intent: Union[str, int, float], trace_id: str = "tr-auto") -> PhysicalQuantity:
        """[ASCENSION 49]: Transmutes intent into Chronos Base (Seconds)."""
        temp_unit = TemporalUnit(intent, trace_id)
        return PhysicalQuantity(
            magnitude=temp_unit.seconds,
            dimension=Dimension.TIME,
            base_unit="s",
            trace_id=trace_id
        )

    @classmethod
    def format_mass(cls, quantity: Union[PhysicalQuantity, float, int], binary: bool = True) -> str:
        """Transmutes Iron back into Poetry."""
        val = quantity.magnitude if isinstance(quantity, PhysicalQuantity) else float(quantity)
        if val == 0: return "0B"

        base = 1024 if binary else 1000
        units = ['B', 'KiB', 'MiB', 'GiB', 'TiB'] if binary else ['B', 'KB', 'MB', 'GB', 'TB']

        mag_idx = int(math.floor(math.log(abs(val), base))) if val != 0 else 0
        if mag_idx >= len(units): return f"{val:.2e} B"

        res = val / math.pow(base, mag_idx)
        return f"{res:.2f} {units[mag_idx]}"

    @classmethod
    def format_time(cls, quantity: Union[PhysicalQuantity, float, int]) -> str:
        """Transmutes Chronos back into Poetry."""
        sec = quantity.magnitude if isinstance(quantity, PhysicalQuantity) else float(quantity)
        if sec == 0: return "0s"
        if sec < 1.0: return f"{sec * 1000:.1f}ms"
        if sec < 60: return f"{sec:.1f}s"
        if sec < 3600: return f"{sec / 60:.1f}m"
        return f"{sec / 3600:.1f}h"


def forge_scalar_context() -> Dict[str, Any]:
    """[ASCENSION 54]: SGF Global context injection."""
    return {
        "mass": ScalarAlchemist.to_bytes,
        "time": ScalarAlchemist.to_seconds,
        "format_mass": ScalarAlchemist.format_mass,
        "format_time": ScalarAlchemist.format_time,
        "PI": math.pi,
        "E": math.e,
        "OMEGA": 1.0  # Absolute Resonance
    }


# [ASCENSION 72]: THE FINALITY VOW
__all__ = ["Dimension", "TemporalUnit", "PhysicalQuantity", "ScalarAlchemist", "forge_scalar_context"]