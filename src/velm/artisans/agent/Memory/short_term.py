# Path: scaffold/artisans/agent/Memory/short_term.py
# --------------------------------------------------

from typing import Dict, Any

class ShortTermMemory:
    """
    =================================================================================
    == THE AGENT'S SCRATCHPAD (V-Ω-VOLATILE-GNOSIS)                                ==
    =================================================================================
    The Agent's working memory for a single mission. It is a volatile vessel,
    returned to the void once the Great Work is complete.

    A future ascension will use this to cache file contents, intermediate thoughts,
    or complex data structures between cognitive cycles, preventing redundant tool
    calls and enriching the Agent's immediate context. For now, it stands as a
    sacred placeholder, honoring the architectural separation of memory.
    =================================================================================
    """
    def __init__(self):
        self._memory: Dict[str, Any] = {}

    def store(self, key: str, value: Any):
        """Inscribes a fleeting thought."""
        self._memory[key] = value

    def retrieve(self, key: str, default: Any = None) -> Any:
        """Recalls a fleeting thought."""
        return self._memory.get(key, default)

    def clear(self):
        """Returns the scratchpad to the void."""
        self._memory = {}