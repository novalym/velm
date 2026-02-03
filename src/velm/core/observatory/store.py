# Path: scaffold/core/observatory/store.py
# ----------------------------------------
import json
import threading
import time
from pathlib import Path
from typing import Optional

from .contracts import ObservatoryState
from ...utils import atomic_write
from ...logger import Scribe

Logger = Scribe("ObservatoryStore")


class GnosticStore:
    """
    =============================================================================
    == THE PERSISTENCE LAYER (V-Ω-SELF-HEALING-STORE)                          ==
    =============================================================================
    LIF: 1,000,000,000

    Handles atomic reads/writes to ~/.scaffold/observatory.json.
    [ASCENSION]: Now handles the Genesis of the store file if it is missing.
    """

    DB_PATH = Path.home() / ".scaffold" / "observatory.json"
    _lock = threading.RLock()

    def __init__(self):
        self._ensure_db()

    def _ensure_db(self):
        """Forges the physical store if it is a void."""
        if not self.DB_PATH.exists():
            self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            Logger.info("Observatory scripture is a void. Forging initial state...")
            self.save(ObservatoryState())

    def load(self) -> ObservatoryState:
        """Perceives the state from the persistent scroll."""
        with self._lock:
            try:
                if not self.DB_PATH.exists():
                    return ObservatoryState()
                content = self.DB_PATH.read_text(encoding='utf-8')
                return ObservatoryState.model_validate_json(content)
            except Exception as e:
                Logger.error(f"Observatory corruption detected: {e}. Resetting state.")
                # Self-healing: Backup corrupt file and reset
                if self.DB_PATH.exists():
                    backup = self.DB_PATH.with_suffix(f".corrupt.{int(time.time())}.json")
                    self.DB_PATH.rename(backup)

                empty = ObservatoryState()
                self.save(empty)
                return empty

    def save(self, state: ObservatoryState):
        """Inscribes the state atomically into the mortal realm."""
        with self._lock:
            try:
                json_str = state.model_dump_json(indent=2)
                # Use the universal atomic_write to ensure zero corruption
                atomic_write(self.DB_PATH, json_str, Logger, self.DB_PATH.parent, verbose=False)
            except Exception as e:
                Logger.critical(f"Failed to seal Observatory state: {e}")