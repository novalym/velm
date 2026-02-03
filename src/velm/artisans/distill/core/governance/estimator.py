# Path: scaffold/artisans/distill/core/governance/estimator.py
# ------------------------------------------------------------

import math
from typing import Dict
from .....core.cortex.contracts import FileGnosis
from .....core.cortex.tokenomics import TokenEconomist
from .contracts import RepresentationTier


class CostEstimator:
    """
    =============================================================================
    == THE QUANTUM ESTIMATOR (V-Ω-ADAPTIVE-PRICING)                            ==
    =============================================================================
    LIF: 10,000,000,000

    A predictive engine that estimates the token cost of a file in various forms
    without actually rendering it.

    It uses **Compression Heuristics** derived from the file's AST metrics to
    guess the size of a Skeleton or Summary.
    """

    # Baseline Overheads (Headers, formatting chars)
    OVERHEAD_TOKENS = 15

    def __init__(self):
        self.economist = TokenEconomist()

    def estimate(self, file: FileGnosis, tier: RepresentationTier) -> int:
        """The Rite of Estimation."""

        base_cost = file.token_cost

        if tier == RepresentationTier.FULL:
            return base_cost + self.OVERHEAD_TOKENS

        elif tier == RepresentationTier.SKELETON:
            return self._estimate_skeleton(file) + self.OVERHEAD_TOKENS

        elif tier == RepresentationTier.INTERFACE:
            # Interface is stricter than skeleton (no private members)
            return int(self._estimate_skeleton(file) * 0.7) + self.OVERHEAD_TOKENS

        elif tier == RepresentationTier.SUMMARY:
            return 150 + self.OVERHEAD_TOKENS  # Fixed average for summaries

        elif tier == RepresentationTier.PATH_ONLY:
            return self.OVERHEAD_TOKENS

        return 0

    def _estimate_skeleton(self, file: FileGnosis) -> int:
        """
        [THE ADAPTIVE HEURISTIC]
        Calculates cost based on AST density rather than a flat ratio.
        """
        if not file.ast_metrics:
            # Fallback to flat ratio for non-parsed files
            return int(file.token_cost * 0.25)

        # 1. Calculate structural weight
        # Functions/Classes cost tokens for definition + docstrings
        func_count = file.ast_metrics.get('function_count', 0)
        class_count = file.ast_metrics.get('class_count', 0)

        # Approximate tokens per signature (def name(args):)
        # Average ~15 tokens per signature line + ~20 for docstring summary
        structure_cost = (func_count + class_count) * 35

        # Add imports cost (usually preserved in skeleton)
        # Heuristic: 10% of file is imports?
        imports_cost = int(file.token_cost * 0.05)

        return structure_cost + imports_cost