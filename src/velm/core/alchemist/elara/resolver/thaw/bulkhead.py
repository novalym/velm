import threading
from typing import Final

class RecursiveBulkhead:
    """
    =============================================================================
    == THE RECURSIVE BULKHEAD (V-Ω-TOTALITY)                                   ==
    =============================================================================
    LIF: ∞ | ROLE: DEPTH_GOVERNOR | RANK: MASTER
    [ASCENSION 145]: Thread-local depth management.
    """
    MAX_DEPTH: Final[int] = 100
    _THREAD_DEPTH = threading.local()

    @classmethod
    def enter(cls):
        """Descends one level into the recursive reactor."""
        if not hasattr(cls._THREAD_DEPTH, 'val'):
            cls._THREAD_DEPTH.val = 0
        cls._THREAD_DEPTH.val += 1
        return cls._THREAD_DEPTH.val

    @classmethod
    def exit(cls):
        """Ascends from the recursive reactor."""
        cls._THREAD_DEPTH.val = max(0, cls._THREAD_DEPTH.val - 1)

    @classmethod
    def is_saturated(cls) -> bool:
        """Returns True if the recursion ceiling has been breached."""
        return getattr(cls._THREAD_DEPTH, 'val', 0) >= cls.MAX_DEPTH