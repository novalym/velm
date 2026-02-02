# Path: scaffold/core/state/ledger.py
# -----------------------------------

import threading
from typing import List
from ...core.state.contracts import LedgerEntry


class _GnosticLedger:
    """The append-only, thread-safe Write-Ahead Log of all mutations."""
    _instance = None
    _lock = threading.RLock()

    def __init__(self):
        self._entries: List[LedgerEntry] = []
        self._is_active = False

    def begin_rite(self):
        """Opens the sacred scroll for a new symphony of actions."""
        with self._lock:
            self._entries = []
            self._is_active = True

    def record(self, entry: LedgerEntry):
        """Inscribes a new Gnostic vow of intent upon the scroll."""
        with self._lock:
            if not self._is_active: return
            self._entries.append(entry)

    def commit_rite(self) -> List[LedgerEntry]:
        """Seals the scroll, returning its contents and preparing for the next."""
        with self._lock:
            committed_entries = self._entries
            self._entries = []
            self._is_active = False
            return committed_entries

    def rollback(self):
        """Annihilates the current, unsealed scroll in case of heresy."""
        with self._lock:
            self._entries = []
            self._is_active = False


# The one true, sacred, and now unambiguously named instance.
ActiveLedger = _GnosticLedger()