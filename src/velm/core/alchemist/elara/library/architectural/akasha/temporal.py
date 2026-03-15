# Path: core/alchemist/elara/library/architectural/akasha/temporal.py
# -------------------------------------------------------------------

import time
from pathlib import Path

class TemporalOracle:
    """
    =============================================================================
    == THE TEMPORAL ORACLE (V-Ω-TOTALITY)                                      ==
    =============================================================================
    [ASCENSIONS 21-24]:
    21. Substrate-agnostic file age calculation.
    22. Stagnation detection (TTL thresholding).
    23. Achronal caching overrides.
    """
    def age(self, path_str: str) -> float:
        """[ASCENSION 21]: Returns the age of a file in seconds."""
        p = Path(path_str)
        if not p.exists(): return 0.0
        return time.time() - p.stat().st_mtime

    def is_stagnant(self, path_str: str, threshold_seconds: float) -> bool:
        """[ASCENSION 22]: Returns True if the file has not mutated recently."""
        return self.age(path_str) > threshold_seconds