# Path: core/lsp/base/foundry.py
# ------------------------------
import os
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Dict, Union, Any, Optional
from .telemetry import forensic_log


class KineticFoundry:
    """
    =============================================================================
    == THE KINETIC FOUNDRY (V-Ω-MULTITHREADED-FORGE)                          ==
    =============================================================================
    The engine room of the server. It manages the pool of worker threads that
    perform the heavy lifting of analysis and refactoring.
    """

    def __init__(self):
        # [ASCENSION 1]: Hardware-Aware Scaling
        cpu_count = os.cpu_count() or 4
        self._max_workers = cpu_count * 2

        self._executor = ThreadPoolExecutor(
            max_workers=self._max_workers,
            thread_name_prefix="GnosticWorker"
        )

        # [ASCENSION 3]: The Hall of Records
        self._pending_futures: Dict[Union[str, int], Future] = {}
        self._lock = threading.RLock()

    def submit(self, rite_id: Union[str, int], task: Any, *args, **kwargs) -> Future:
        """Dispatches a task to the pool and records its causality."""
        with self._lock:
            future = self._executor.submit(task, *args, **kwargs)
            if rite_id is not None:
                self._pending_futures[rite_id] = future
                # Auto-purge from registry upon manifestation
                future.add_done_callback(lambda f: self._clear_future(rite_id))
            return future

    def cancel(self, rite_id: Union[str, int]) -> bool:
        """Surgically severs a pending causal thread."""
        with self._lock:
            future = self._pending_futures.get(rite_id)
            if future:
                return future.cancel()
        return False

    def _clear_future(self, rite_id: Union[str, int]):
        with self._lock:
            if rite_id in self._pending_futures:
                del self._pending_futures[rite_id]

    def shutdown(self, wait: bool = True):
        """Drains the foundry and releases threads."""
        self._executor.shutdown(wait=wait, cancel_futures=not wait)

    @property
    def active_count(self) -> int:
        return len(self._pending_futures)