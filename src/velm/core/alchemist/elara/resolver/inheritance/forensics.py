# Path: core/alchemist/elara/resolver/inheritance/forensics.py
# -----------------------------------------------------------

import time
from typing import Dict, Any


class LineageTomographer:
    """
    =============================================================================
    == THE LINEAGE TOMOGRAPHER (V-Ω-TOTALITY)                                  ==
    =============================================================================
    LIF: ∞ | ROLE: METABOLIC_AUDITOR
    Tracks the tax of hierarchical convergence.
    """

    @classmethod
    def record_tax(cls, start_ns: int) -> float:
        """Returns nanosecond tax converted to ms."""
        return (time.perf_counter_ns() - start_ns) / 1_000_000

    @classmethod
    def log_lineage(cls, child_name: str, parent_name: str, duration: float):
        """Proclaims the success of the Morphogenesis to the Scribe."""
        from ......logger import Scribe
        Scribe("Inheritance:Forensics").success(
            f"Lineage Converged: {child_name} << {parent_name} in {duration:.2f}ms."
        )