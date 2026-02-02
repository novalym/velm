# Path: core/lsp/utils/timing.py
# -----------------------------
# LIF: INFINITY | MODULE: TEMPORAL_CONTROL
# =================================================================================

import threading
import time
from typing import Callable, Any, TypeVar

T = TypeVar("T")


class Debounce:
    """
    [THE TEMPORAL GOVERNOR]
    Delays execution until silence is detected.
    """

    def __init__(self, interval: float, function: Callable, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.timer: threading.Timer | None = None
        self.lock = threading.Lock()

    def __call__(self, *new_args, **new_kwargs):
        """Resets the timer."""
        with self.lock:
            if self.timer:
                self.timer.cancel()

            # Merge args if provided, else use defaults
            args = new_args if new_args else self.args
            kwargs = new_kwargs if new_kwargs else self.kwargs

            self.timer = threading.Timer(self.interval, self.function, args, kwargs)
            self.timer.start()

    def cancel(self):
        with self.lock:
            if self.timer:
                self.timer.cancel()
                self.timer = None


class Throttle:
    """
    [THE RATE LIMITER]
    Ensures execution happens at most once every X seconds.
    """

    def __init__(self, interval: float, function: Callable):
        self.interval = interval
        self.function = function
        self.last_run = 0.0
        self.lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        with self.lock:
            now = time.time()
            if now - self.last_run >= self.interval:
                self.last_run = now
                return self.function(*args, **kwargs)