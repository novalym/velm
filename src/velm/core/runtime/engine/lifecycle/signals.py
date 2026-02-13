# Path: src/velm/core/runtime/engine/lifecycle/signals.py
# -------------------------------------------------------

import signal
import sys
import os
from typing import Callable, Any

class SignalInterceptor:
    """
    [THE SHIELD OF TERMINATION]
    Captures OS signals to ensure the Engine can say goodbye before it dies.
    [ASCENSION 1]: WASM-AWARE SILENCE.
    """

    def __init__(self, on_shutdown: Callable[[], None]):
        self.on_shutdown = on_shutdown
        self._triggered = False
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

    def arm(self):
        """Register signal handlers."""
        # [THE CURE]: In WASM, signal handlers can cause boot deadlocks.
        if self._is_wasm:
            return

        try:
            signal.signal(signal.SIGINT, self._handle)
            signal.signal(signal.SIGTERM, self._handle)

            if sys.platform == 'win32':
                try:
                    signal.signal(signal.SIGBREAK, self._handle)
                except AttributeError:
                    pass
        except (ValueError, AttributeError):
            # Graceful degradation if signals are not supported
            pass

    def _handle(self, signum, frame):
        if self._triggered:
            sys.exit(1)

        self._triggered = True
        self.on_shutdown()