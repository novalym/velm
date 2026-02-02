# Path: scaffold/artisans/distillation/ranker/factors/structural.py
# -----------------------------------------------------------------

import math
from .....core.cortex.contracts import FileGnosis


class StructuralJudge:
    """
    =============================================================================
    == THE STRUCTURAL ARCHITECT (DENSITY & FORM)                               ==
    =============================================================================
    Rewards files with high information density (API surface vs Lines of Code).
    """

    def judge(self, gnosis: FileGnosis) -> float:
        if gnosis.category != 'code': return 0.0

        func_count = gnosis.ast_metrics.get('function_count', 0)
        class_count = gnosis.ast_metrics.get('class_count', 0)

        # Base structural value
        score = (func_count * 0.2) + (class_count * 0.5)

        # Density Bonus: Value per Token
        # If a file has 10 functions but only 100 tokens, it's an Interface (High Value)
        # If it has 1 function and 1000 tokens, it's Implementation (Lower Value for context)
        if gnosis.token_cost > 0:
            density = (func_count + class_count) / math.log1p(gnosis.token_cost)
            score *= (1.0 + density)

        return score