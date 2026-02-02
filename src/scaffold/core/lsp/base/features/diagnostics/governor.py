# Path: core/lsp/features/diagnostics/governor.py
# -----------------------------------------------

import threading
import time
from typing import Dict, Callable


class BurstGovernor:
    """
    =============================================================================
    == THE ADAPTIVE GOVERNOR (V-Ω-KINETIC-FLOW-CONTROL)                        ==
    =============================================================================
    Manages the "Rate of Perception."

    [CAPABILITIES]:
    1. **Adaptive Debounce:** Adds penalty delay if triggers occur too frequently.
    2. **Version Sentinel:** Cancels old tasks if a newer document version arrives.
    3. **Atomic Scheduling:** Uses `RLock` to prevent race conditions.
    """

    def __init__(self):
        # Map[URI, Timer]
        self._timers: Dict[str, threading.Timer] = {}
        # Map[URI, Version]
        self._versions: Dict[str, int] = {}
        # Map[URI, LastTriggerTime]
        self._last_trigger: Dict[str, float] = {}

        self._lock = threading.RLock()

    def schedule(self, uri: str, version: int, base_delay: float, task: Callable[[], None], priority: bool = False):
        """
        [THE RITE OF SCHEDULING]
        """
        with self._lock:
            # 1. Update Version Truth
            if version < self._versions.get(uri, -1):
                return  # Obsolete request
            self._versions[uri] = version

            # 2. Cancel Existing
            if uri in self._timers:
                self._timers[uri].cancel()
                del self._timers[uri]

            # 3. Calculate Adaptive Delay
            now = time.time()
            last = self._last_trigger.get(uri, 0)
            self._last_trigger[uri] = now

            adaptive_delay = base_delay
            # If user is typing furiously (<100ms triggers), add penalty
            if not priority and (now - last < 0.1):
                adaptive_delay += 0.2

                # 4. Schedule Execution
            final_delay = 0.01 if priority else adaptive_delay

            timer = threading.Timer(final_delay, self._execute_safe, args=[uri, version, task])
            timer.name = f"GovWorker-{uri.split('/')[-1]}"
            timer.daemon = True

            self._timers[uri] = timer
            timer.start()

    def _execute_safe(self, uri: str, version: int, task: Callable):
        """
        [THE SAFE EXECUTION WRAPPER]
        Checks version consistency before running.
        """
        with self._lock:
            latest = self._versions.get(uri)
            if latest is not None and latest > version:
                return  # Obsolete

            if uri in self._timers:
                del self._timers[uri]

        try:
            task()
        except Exception:
            pass

    def cancel(self, uri: str):
        """[THE RITE OF CANCELLATION]"""
        with self._lock:
            if uri in self._timers:
                self._timers[uri].cancel()
                del self._timers[uri]
            if uri in self._versions:
                del self._versions[uri]