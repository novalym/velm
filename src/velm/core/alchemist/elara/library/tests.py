# Path: core/alchemist/elara/library/tests.py
# -------------------------------------------

"""
=================================================================================
== THE GNOSTIC TEST ORACLE: OMEGA POINT (V-Ω-TOTALITY-VMAX-JINJA-TESTS)        ==
=================================================================================
LIF: ∞^∞ | ROLE: BOOLEAN_IDENTITY_ADJUDICATOR | RANK: OMEGA_SOVEREIGN_PRIME

[THE MANIFESTO]
This scripture heals the "Is / Is Not Schism." In standard Python, `a is b` tests
memory identity. In Jinja, `if a is defined` tests for existence via registered
functions.

The `GnosticASTEvaluator` now intercepts the `ast.Is` operator and reroutes it
here. This provides 100% Jinja parity for conditional testing without breaking
the ELARA runtime.
=================================================================================
"""

from typing import Any, Dict, Callable


class GnosticTestRegistry:
    def __init__(self):
        self.tests: Dict[str, Callable] = {}
        self._register_default_tests()

    def _register_default_tests(self):
        # --- EXISTENCE & STATE ---
        self.tests["defined"] = lambda v: v is not None and v != "VOID"
        self.tests["undefined"] = lambda v: v is None or v == "VOID"
        self.tests["none"] = lambda v: v is None

        # --- TYPOLOGY ---
        self.tests["string"] = lambda v: isinstance(v, str)
        self.tests["number"] = lambda v: isinstance(v, (int, float))
        self.tests["integer"] = lambda v: isinstance(v, int)
        self.tests["float"] = lambda v: isinstance(v, float)
        self.tests["boolean"] = lambda v: isinstance(v, bool)
        self.tests["iterable"] = lambda v: hasattr(v, '__iter__') and not isinstance(v, str)
        self.tests["mapping"] = lambda v: isinstance(v, dict)
        self.tests["callable"] = lambda v: callable(v)

        # --- MATHEMATICS ---
        self.tests["even"] = lambda v: isinstance(v, int) and v % 2 == 0
        self.tests["odd"] = lambda v: isinstance(v, int) and v % 2 != 0
        self.tests["divisibleby"] = lambda v, n: isinstance(v, int) and isinstance(n, int) and v % n == 0

        # --- STRING PHYSICS ---
        self.tests["lower"] = lambda v: isinstance(v, str) and v.islower()
        self.tests["upper"] = lambda v: isinstance(v, str) and v.isupper()

    def evaluate(self, value: Any, test_name: str, *args) -> bool:
        """The Rite of Adjudication."""
        test_func = self.tests.get(test_name.lower())
        if not test_func:
            raise ValueError(f"Gnostic Test Fracture: '{test_name}' is unmanifest in the Oracle.")
        try:
            return test_func(value, *args)
        except Exception:
            return False


# Global Singleton
test_oracle = GnosticTestRegistry()