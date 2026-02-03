# Path: core/lsp/utils/debounce.py
# --------------------------------
# LIF: INFINITY | SYSTEM: TEMPORAL_CONTROL
# =================================================================================

import threading
from typing import Callable, Any


class Debounce:
    """
    [THE TEMPORAL GOVERNOR]
    Delays the execution of a function until a period of silence has passed.
    """

    def __init__(self, interval: float, function: Callable, *args: Any, **kwargs: Any):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.timer: threading.Timer | None = None
        self.lock = threading.Lock()

    def __call__(self):
        """Resets the timer. The function will fire only if this isn't called again."""
        with self.lock:
            if self.timer is not None:
                self.timer.cancel()

            self.timer = threading.Timer(self.interval, self.function, self.args, self.kwargs)
            self.timer.start()

    def cancel(self):
        """Cancels any pending execution."""
        with self.lock:
            if self.timer is not None:
                self.timer.cancel()
                self.timer = None