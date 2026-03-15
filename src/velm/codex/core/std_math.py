# Path: src/velm/codex/core/std_math.py
# -------------------------------------

"""
=================================================================================
== THE ARITHMETIC ENGINE (V-Ω-MATH-DOMAIN)                                     ==
=================================================================================
LIF: 10,000,000,000

Exposes the C-optimized `math` and `random` libraries to the blueprint.
Allows for dynamic port generation, resource allocation ratios, and crypto-math.
=================================================================================
"""
import math
import random
from typing import Dict, Any, Union

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain


@domain("math")
class MathDomain(BaseDirectiveDomain):
    """The Sovereign Calculator."""

    @property
    def namespace(self) -> str:
        return "math"

    def help(self) -> str:
        return "Native mathematical calculations (ceil, floor, round, random, pow)."

    # --- 1. BASIC ARITHMETIC ---

    def _directive_ceil(self, context: Dict[str, Any], value: float, *args, **kwargs) -> int:
        """@math/ceil(10.5) -> 11"""
        return math.ceil(value)

    def _directive_floor(self, context: Dict[str, Any], value: float, *args, **kwargs) -> int:
        """@math/floor(10.5) -> 10"""
        return math.floor(value)

    def _directive_round(self, context: Dict[str, Any], value: float, digits: int = 0, *args, **kwargs) -> float:
        """@math/round(10.555, digits=2) -> 10.56"""
        return round(value, digits)

    def _directive_abs(self, context: Dict[str, Any], value: float, *args, **kwargs) -> float:
        """@math/abs(-10.5) -> 10.5"""
        return abs(value)

    # --- 2. ADVANCED ALGEBRA ---

    def _directive_pow(self, context: Dict[str, Any], base: float, exp: float, *args, **kwargs) -> float:
        """@math/pow(base=2, exp=8) -> 256.0"""
        return math.pow(base, exp)

    def _directive_sqrt(self, context: Dict[str, Any], value: float, *args, **kwargs) -> float:
        """@math/sqrt(16) -> 4.0"""
        if value < 0:
            raise CodexHeresy("Mathematical Paradox: Cannot calculate square root of a negative number.")
        return math.sqrt(value)

    def _directive_log(self, context: Dict[str, Any], value: float, base: float = math.e, *args, **kwargs) -> float:
        """@math/log(100, base=10) -> 2.0"""
        if value <= 0:
            raise CodexHeresy("Mathematical Paradox: Logarithm domain error.")
        return math.log(value, base)

    # --- 3. ENTROPY & RANDOMNESS ---

    def _directive_randint(self, context: Dict[str, Any], min_val: int = 0, max_val: int = 100, *args, **kwargs) -> int:
        """@math/randint(min_val=1000, max_val=9999) -> 4821"""
        if min_val > max_val:
            raise CodexHeresy(f"Entropy Inversion: min_val ({min_val}) cannot be greater than max_val ({max_val}).")
        return random.randint(min_val, max_val)

    def _directive_choice(self, context: Dict[str, Any], options: list, *args, **kwargs) -> Any:
        """@math/choice(["a", "b", "c"]) -> "b" """
        if not options:
            raise CodexHeresy("Entropy Void: Cannot make a choice from an empty list.")
        return random.choice(options)

    def _directive_uuid(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """@math/uuid -> 550e8400-e29b-41d4-a716-446655440000"""
        import uuid
        return str(uuid.uuid4())