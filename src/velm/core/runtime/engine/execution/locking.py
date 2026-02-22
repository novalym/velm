# Path: core/runtime/engine/execution/locking.py
# ----------------------------------------------

import threading
from typing import Dict
from contextlib import contextmanager


class ResourceLockManager:
    """
    =============================================================================
    == THE RESOURCE SHIELD (V-Ω-MUTEX-GRID-ASCENDED)                           ==
    =============================================================================
    Provides named locks for critical resources.
    """

    _locks: Dict[str, threading.RLock] = {}
    _global_lock = threading.Lock()

    @classmethod
    @contextmanager
    def acquire(cls, resource_id: str, exclusive: bool = True):
        """
        Acquires a lock for a specific resource ID (e.g., 'file:package.json').
        [ASCENSION 2]: Accepts `exclusive` parameter to satisfy Dispatcher and uses RLock for re-entrancy.
        """
        with cls._global_lock:
            if resource_id not in cls._locks:
                cls._locks[resource_id] = threading.RLock()
            lock = cls._locks[resource_id]

        lock.acquire()
        try:
            yield
        finally:
            lock.release()