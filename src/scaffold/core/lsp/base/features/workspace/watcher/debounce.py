# Path: core/lsp/features/workspace/watcher/debounce.py
# -----------------------------------------------------
import threading
import time
from typing import List, Callable
from ..models import FileEvent

class FluxDebouncer:
    """[THE GOVERNOR] Prevents event avalanches."""
    def __init__(self, callback: Callable[[List[FileEvent]], None], window_ms: int = 150):
        self.callback = callback
        self.window = window_ms / 1000.0
        self._buffer: List[FileEvent] = []
        self._timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()

    def add(self, events: List[FileEvent]):
        with self._lock:
            self._buffer.extend(events)
            if self._timer: self._timer.cancel()
            self._timer = threading.Timer(self.window, self._flush)
            self._timer.start()

    def _flush(self):
        with self._lock:
            batch = list(self._buffer)
            self._buffer.clear()
            self._timer = None
        if batch: self.callback(batch)