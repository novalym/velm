# Path: core/runtime/engine/execution/locking.py
# ----------------------------------------------

import threading
from typing import Dict
from contextlib import contextmanager


class ResourceLockManager:
    """
    =============================================================================
    == THE RESOURCE SHIELD (V-Ω-MUTEX-GRID)                                    ==
    =============================================================================
    Provides named locks for critical resources.
    """

    _locks: Dict[str, threading.Lock] = {}
    _global_lock = threading.Lock()

    @classmethod
    @contextmanager
    def acquire(cls, resource_id: str):
        """
        Acquires a lock for a specific resource ID (e.g., 'file:package.json').
        """
        with cls._global_lock:
            if resource_id not in cls._locks:
                cls._locks[resource_id] = threading.Lock()
            lock = cls._locks[resource_id]

        lock.acquire()
        try:
            yield
        finally:
            lock.release()