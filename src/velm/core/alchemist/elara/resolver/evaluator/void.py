# Path: core/alchemist/elara/resolver/evaluator/void.py
# -----------------------------------------------------

from typing import Any

class GnosticVoid:
    """
    =============================================================================
    == THE GNOSTIC VOID (V-Ω-TOTALITY-VMAX-NULL-OBJECT-PATTERN)                ==
    =============================================================================
    LIF: ∞ | ROLE: NON_EXISTENCE_WARDEN | RANK: OMEGA

    [THE MANIFESTO]: This is a bit-perfect representation of 'Nothing'.
    It is a sovereign Null-Object that absorbs all kinetic strikes (operators)
    to prevent TypeErrors from shattering the Engine's Mind.
    """
    __slots__ = ()

    def __bool__(self): return False
    def __len__(self): return 0
    def __iter__(self): return iter([])
    def __str__(self): return ""
    def __repr__(self): return "/* 0xVOID */"

    #[ASCENSION 5]: THE BLACK HOLE OPS
    def __add__(self, _): return self
    def __sub__(self, _): return self
    def __mul__(self, _): return self
    def __truediv__(self, _): return self
    def __floordiv__(self, _): return self
    def __mod__(self, _): return self
    def __pow__(self, _): return self
    def __getitem__(self, _): return self
    def __getattr__(self, _): return self
    def __call__(self, *args, **kwargs): return self

# Initialize the Singleton Void
VOID = GnosticVoid()

class LaminarTypeRegistry:
    """
    =============================================================================
    == THE LAMINAR TYPE REGISTRY (V-Ω-TOTALITY)                                ==
    =============================================================================
    LIF: 10,000x | ROLE: ISOMORPHIC_TYPE_CASTER
    """
    @staticmethod
    def thaw_truth(value: Any) -> Any:
        """Transmutes string-bits into logical bits."""
        if not isinstance(value, str):
            return value

        v_low = value.lower().strip()
        if v_low in ("true", "yes", "on", "resonant"): return True
        if v_low in ("false", "no", "off", "fractured"): return False
        if v_low in ("null", "none", "void"): return None

        # [ASCENSION 13]: Numeric Auto-Inception
        if v_low.isdigit():
            return int(v_low)
        try:
            return float(v_low)
        except ValueError:
            return value