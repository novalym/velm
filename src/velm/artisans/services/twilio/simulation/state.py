# Path: scaffold/artisans/services/twilio/simulation/state.py
# -----------------------------------------------------------

import json
import os
import time
from pathlib import Path
from typing import Dict, Any, List


class SimulationState:
    """
    [THE AKASHIC MIRROR]
    Persists the state of the Phantom Network to disk.
    Allows 'buying' a number in one run and 'using' it in the next.
    """

    CACHE_PATH = Path(".scaffold/cache/twilio_phantom_state.json")

    def __init__(self):
        self.inventory: Dict[str, Dict] = {}  # Bought Numbers
        self.messages: List[Dict] = []  # Message Log
        self.blacklist: List[str] = []  # Opted Out Numbers
        self._load()

    def _load(self):
        if self.CACHE_PATH.exists():
            try:
                data = json.loads(self.CACHE_PATH.read_text())
                self.inventory = data.get("inventory", {})
                self.messages = data.get("messages", [])
                self.blacklist = data.get("blacklist", [])
            except:
                pass  # Corrupt cache, start fresh

    def _save(self):
        try:
            self.CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "inventory": self.inventory,
                "messages": self.messages[-100:],  # Keep last 100 for sanity
                "blacklist": self.blacklist,
                "updated_at": time.time()
            }
            self.CACHE_PATH.write_text(json.dumps(data, indent=2))
        except:
            pass

    def acquire_node(self, number: str, sid: str, metadata: Dict):
        self.inventory[sid] = {**metadata, "sid": sid, "number": number}
        self._save()

    def release_node(self, sid: str):
        if sid in self.inventory:
            del self.inventory[sid]
            self._save()

    def log_message(self, msg: Dict):
        self.messages.append(msg)
        self._save()

    def check_blacklist(self, number: str) -> bool:
        return number in self.blacklist

    def add_to_blacklist(self, number: str):
        if number not in self.blacklist:
            self.blacklist.append(number)
            self._save()


# Singleton
SimState = SimulationState()