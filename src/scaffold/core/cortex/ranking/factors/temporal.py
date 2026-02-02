# Path: scaffold/artisans/distillation/ranker/factors/temporal.py
# ---------------------------------------------------------------

import math
from .....core.cortex.contracts import FileGnosis


class TemporalJudge:
    """
    =============================================================================
    == THE CHRONOMANCER (HISTORY & CHURN)                                      ==
    =============================================================================
    Rewards files that are actively evolving but stable enough to be relevant.
    """

    def judge(self, gnosis: FileGnosis) -> float:
        # Logarithmic bonus for churn (high activity = high relevance)
        churn_bonus = math.log1p(gnosis.churn_score) * 0.1

        # Recency Penalty: If it changed in the last 7 days, it might be volatile.
        # However, for debugging, recent files are often THE MOST relevant.
        # We define stability: older is more stable.

        # For Distillation (Context), we usually WANT recent changes + high churn.
        # So we actually reward recency here, unlike the Stability Score in the Historian.

        days_ago = gnosis.days_since_last_change or 999
        recency_bonus = 1.0 / (max(1, days_ago) ** 0.5)  # Decay function

        return churn_bonus + (recency_bonus * 2.0)