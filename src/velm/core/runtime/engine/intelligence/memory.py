# Path: core/runtime/engine/intelligence/memory.py
# -----------------------------------------------

from collections import deque
from typing import Any, List, Optional

class CognitiveMemory:
    """
    =============================================================================
    == THE COGNITIVE MEMORY (V-Ω-SESSION-CONTEXT)                              ==
    =============================================================================
    Stores the stream of consciousness for the Engine.
    """

    def __init__(self, history_len: int = 50):
        self._rite_history = deque(maxlen=history_len)
        self._focus_history = deque(maxlen=10) # Last 10 files touched
        self._last_error: Optional[str] = None

    def record_rite(self, rite_name: str, success: bool):
        self._rite_history.append({"rite": rite_name, "success": success})

    def record_focus(self, file_path: str):
        if not self._focus_history or self._focus_history[-1] != file_path:
            self._focus_history.append(file_path)

    def record_error(self, error_msg: str):
        self._last_error = error_msg

    @property
    def last_rite(self) -> Optional[str]:
        return self._rite_history[-1]["rite"] if self._rite_history else None

    @property
    def active_context(self) -> List[str]:
        return list(self._focus_history)