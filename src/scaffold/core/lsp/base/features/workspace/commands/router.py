# Path: core/lsp/features/workspace/commands/router.py
# ----------------------------------------------------
import logging
from typing import List, Any, Dict, Callable

Logger = logging.getLogger("CommandRouter")


class CommandRouter:
    """[THE HAND] Routes UI intents to Kinetic Rites."""

    def __init__(self, server):
        self.server = server
        self._registry: Dict[str, Callable] = {}

    def register(self, command_id: str, handler: Callable):
        self._registry[command_id] = handler

    def dispatch(self, command_id: str, args: List[Any]) -> Any:
        # [ASCENSION 7]: FAULT-TOLERANT SARCOPHAGUS
        handler = self._registry.get(command_id)
        if not handler:
            Logger.error(f"Edict Unmanifest: {command_id}")
            return None

        try:
            return handler(*args)
        except Exception as e:
            Logger.error(f"Rite Execution Fracture: {command_id} -> {e}")
            return {"success": False, "error": str(e)}