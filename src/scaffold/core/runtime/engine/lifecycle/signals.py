# Path: core/runtime/engine/lifecycle/signals.py
# ----------------------------------------------

import signal
import sys
from typing import Callable, Any

class SignalInterceptor:
    """
    [THE SHIELD OF TERMINATION]
    Captures OS signals to ensure the Engine can say goodbye before it dies.
    """

    def __init__(self, on_shutdown: Callable[[], None]):
        self.on_shutdown = on_shutdown
        self._triggered = False

    def arm(self):
        """Register signal handlers."""
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)

        if sys.platform == 'win32':
            try:
                signal.signal(signal.SIGBREAK, self._handle)
            except AttributeError:
                pass

    def _handle(self, signum, frame):
        if self._triggered:
            # Zombie Escalation: If user mashes Ctrl+C, force kill
            sys.exit(1)

        self._triggered = True
        # Trigger the callback (ShutdownManager.execute)
        self.on_shutdown()