# Path: core/alchemist/elara/resolver/evaluator/visitor/state.py
# --------------------------------------------------------------

import time
import os
import sys
from typing import Dict, Any, Final, TYPE_CHECKING

# [THE MASTER CURE]: ACHRONAL TYPE SHIELDING
# We move the heavy LexicalScope import behind the TYPE_CHECKING veil
# to annihilate the circular dependency at runtime.
if TYPE_CHECKING:
    from ...context import LexicalScope

from ..constants import EvaluationConstants, IS_WASM
from ..heresies import MetabolicFeverHeresy


class VisitorState:
    """
    =============================================================================
    == THE VISITOR STATE MATRIX (V-Ω-TOTALITY-VMAX-HEALED)                     ==
    =============================================================================
    LIF: ∞ | ROLE: THERMODYNAMIC_MEMORY_CELL | RANK: OMEGA_GUARDIAN

    [THE MANIFESTO]
    This organ has been surgically repaired to support 'Apophatic Perception'.
    It no longer requires the physical presence of the LexicalScope class
    during module ignition, preventing the Ouroboros Import Fracture.
    """
    __slots__ = (
        'scope', 'strict_mode', 'trace_id', 'filters',
        'in_default_filter', '_instruction_tax', '_start_ns'
    )

    def __init__(self, scope: 'LexicalScope', strict_mode: bool):
        """
        [THE RITE OF BINDING]: Uses string-forward referencing for the scope type.
        """
        self.scope = scope
        self.strict_mode = strict_mode

        # [ASCENSION 1]: Recursive Context Scrying
        # We safely extract the trace_id from the global context proxy
        self.trace_id = getattr(scope.global_ctx, 'trace_id', 'tr-void')
        self.filters = scope.get('__filters__') or {}

        # [THE CURE]: Laminar State Matrix for Amnesty
        self.in_default_filter = False

        # Metabolic Tomography
        self._instruction_tax = 0
        self._start_ns = time.perf_counter_ns()

    def check_metabolism(self, node: Any):
        """[ASCENSION 15]: METABOLIC CHECKPOINT YIELDING."""
        self._instruction_tax += 1
        if self._instruction_tax % 200 == 0:
            if not IS_WASM: time.sleep(0)

            elapsed_ns = time.perf_counter_ns() - self._start_ns
            if elapsed_ns > EvaluationConstants.MAX_EVAL_TIME_NS:
                raise MetabolicFeverHeresy(
                    elapsed_ms=elapsed_ns / 1_000_000,
                    limit_ms=EvaluationConstants.MAX_EVAL_TIME_NS / 1_000_000,
                    trace_id=self.trace_id,
                    line_num=getattr(node, 'lineno', 0)
                )