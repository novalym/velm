# Path: core/alchemist/elara/library/architectural/jurisprudence/metabolism.py
# ----------------------------------------------------------------------------

import time
from typing import Any, Optional
from ...registry import register_rite


class MetabolicFeverHeresy(Exception): pass


@register_rite("budget")
def metabolic_budget(value: Any, limit_ms: float, start_time_ns: Optional[int] = None, **kwargs) -> Any:
    """
    =============================================================================
    == THE METABOLIC BUDGET WARD (V-Ω-TOTALITY)                                ==
    =============================================================================
    [ASCENSION 48]: Predictive Metabolism. Throttles heavy intent.
    If the template takes longer than `limit_ms` to generate, it fractures to
    save the OS from hanging.
    """
    ctx_start_ns = kwargs.get('start_time_ns', start_time_ns)
    if ctx_start_ns is None: return value

    elapsed = (time.perf_counter_ns() - ctx_start_ns) / 1_000_000
    if elapsed > limit_ms:
        raise MetabolicFeverHeresy(f"Metabolic Budget Breached: {elapsed:.2f}ms > {limit_ms}ms")
    return value