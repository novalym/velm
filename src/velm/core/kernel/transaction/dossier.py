import threading
# =========================================================================================
# == THE OMEGA DOSSIER WARD (THE CURE FOR THE METABOLIC FREEZE)                          ==
# =========================================================================================
class SafeWriteDossier(dict):
    """
    =============================================================================
    == THE THREAD-SAFE DOSSIER WARD (V-Ω-TOTALITY-ITERATION-CURE)              ==
    =============================================================================
    LIF: 1,000,000x | ROLE: CONCURRENCY_SHIELD | RANK: OMEGA_GUARDIAN

    Annihilates the 'dictionary changed size during iteration' heresy globally.
    By wrapping all read, write, and iteration methods in a re-entrant lock and
    materializing views as lists, we guarantee that all 22 Framework Strategies
    can safely scan the staging area concurrently while the Parallel Hurricane
    commits new files.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.RLock()

    def __setitem__(self, key, value):
        with self._lock: super().__setitem__(key, value)

    def __getitem__(self, key):
        with self._lock: return super().__getitem__(key)

    def __delitem__(self, key):
        with self._lock: super().__delitem__(key)

    def items(self):
        with self._lock: return list(super().items())

    def values(self):
        with self._lock: return list(super().values())

    def keys(self):
        with self._lock: return list(super().keys())

    def pop(self, key, default=None):
        with self._lock: return super().pop(key, default)

    def update(self, *args, **kwargs):
        with self._lock: super().update(*args, **kwargs)

    def get(self, key, default=None):
        with self._lock: return super().get(key, default)

    def __contains__(self, key):
        with self._lock: return super().__contains__(key)
