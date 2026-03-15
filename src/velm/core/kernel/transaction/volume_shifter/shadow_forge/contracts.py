# Path: src/velm/core/kernel/transaction/volume_shifter/shadow_forge/contracts.py
# -------------------------------------------------------------------------------

import threading
from typing import Dict, Any


class ForgeMetrics:
    """
    =============================================================================
    == THE ACHRONAL METRICS LEDGER (V-Ω-THREAD-SAFE-TOMOGRAPHY)                ==
    =============================================================================
    LIF: 1,000x | ROLE: METABOLIC_ACCOUNTANT

    A mathematically secure, thread-safe accumulator for forensic metrics.
    Annihilates the "Race Condition Ledger" heresy present in standard dicts
    during the Iron Hurricane's parallel strike.
    """

    def __init__(self):
        self._lock = threading.RLock()
        self._hardlinks: int = 0
        self._copies: int = 0
        self._dirs: int = 0
        self._bytes: int = 0
        self._errors: int = 0

    def record_link(self, mass: int):
        with self._lock:
            self._hardlinks += 1
            self._bytes += mass

    def record_copy(self, mass: int):
        with self._lock:
            self._copies += 1
            self._bytes += mass

    def record_dir(self):
        with self._lock:
            self._dirs += 1

    def record_error(self):
        with self._lock:
            self._errors += 1

    def snapshot(self) -> Dict[str, Any]:
        """Returns a frozen, JSON-safe view of the ledger."""
        with self._lock:
            return {
                "hardlinks": self._hardlinks,
                "copies": self._copies,
                "dirs": self._dirs,
                "bytes": self._bytes,
                "errors": self._errors
            }