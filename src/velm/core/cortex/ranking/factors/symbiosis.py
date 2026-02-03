# Path: scaffold/artisans/distillation/ranker/factors/symbiosis.py
# ----------------------------------------------------------------

from typing import List
from .....core.cortex.contracts import FileGnosis


class SymbiosisJudge:
    """
    =============================================================================
    == THE SYMBIOTIC LINKER (TEST & IMPLEMENTATION)                            ==
    =============================================================================
    Determines the value of a test file based on the rank of its parent.
    """

    def judge(self, test_gnosis: FileGnosis, ranked_impls: List[FileGnosis]) -> float:
        # Heuristic: test_stem should match stem
        test_stem = test_gnosis.path.stem.replace('test_', '').replace('_test', '')

        # Find the implementation file in the ALREADY RANKED list
        parent = next((f for f in ranked_impls if f.path.stem == test_stem), None)

        if parent:
            # A test is worth 50% of its implementation
            return parent.centrality_score * 0.5

        return 0.1  # Orphaned test

