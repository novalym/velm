# Path: scaffold/artisans/distillation/ranker/factors/semantic.py
# ---------------------------------------------------------------

from typing import List
from .....core.cortex.contracts import FileGnosis


class SemanticJudge:
    """
    =============================================================================
    == THE INTENT READER (FOCUS MATCHING)                                      ==
    =============================================================================
    Rewards files that match the User's stated focus keywords.
    """

    def __init__(self, keywords: List[str]):
        self.keywords = [k.lower() for k in keywords]

    def judge(self, gnosis: FileGnosis) -> float:
        if not self.keywords: return 0.0

        score = 0.0
        path_text = str(gnosis.path).lower().replace('_', ' ').replace('-', ' ')

        for k in self.keywords:
            # High reward for path match
            if k in path_text:
                score += 8.0

            # Medium reward for internal tags (if available from Cortex)
            if k in gnosis.semantic_tags:
                score += 4.0

        return score