# Path: core/daemon/server/signals.py
# -----------------------------------
# LIF: INFINITY | ROLE: INTERRUPT_HANDLER
import signal
import sys
from typing import Callable
from ....logger import Scribe

Logger = Scribe("SignalInterceptor")


class SignalInterceptor:
    """
    [THE SHIELD OF TERMINATION]
    Captures OS signals to ensure the Daemon can say goodbye before it dies.
    """

    def __init__(self, on_shutdown: Callable[[], None]):
        self.on_shutdown = on_shutdown
        self._triggered = False

    def arm(self):
        """Register signal handlers."""
        signal.signal(signal.SIGINT, self._handle)
        signal.signal(signal.SIGTERM, self._handle)

        # [ASCENSION 3]: WINDOWS BREAK SUPPORT
        if sys.platform == 'win32':
            try:
                signal.signal(signal.SIGBREAK, self._handle)
            except AttributeError:
                pass

    def _handle(self, signum, frame):
        if self._triggered:
            # [ASCENSION 4]: ZOMBIE ESCALATION
            # If user mashes Ctrl+C, force kill immediately
            Logger.warn("Forced Termination initiated by user.")
            sys.exit(1)

        self._triggered = True
        sig_name = signal.Signals(signum).name
        Logger.info(f"Signal {sig_name} received. Initiating Graceful Shutdown.")

        # Trigger the callback
        self.on_shutdown()