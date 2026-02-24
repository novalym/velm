# Path: core/runtime/engine/execution/simulacrum/shards/base.py
# --------------------------------------------------------------

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, Final

from .......logger import Scribe
from .......utils import atomic_write

class BaseShardArtisan(ABC):
    """
    =============================================================================
    == THE ANCESTRAL SHARD (V-Ω-PERSISTENCE-CONTRACT)                          ==
    =============================================================================
    The abstract soul of all simulation shards. Enforces atomic persistence
    and fault-isolated retrieval.
    """

    def __init__(self, storage_root: Path, shard_name: str):
        self.root = storage_root
        self.shard_name = shard_name
        self.path = self.root / f"{shard_name}_shard.json"
        self.logger = Scribe(f"Simulacrum:{shard_name.title()}")
        self._memory: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        """[THE RITE OF RECALL]"""
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding='utf-8'))
        except Exception as e:
            self.logger.error(f"Shard '{self.shard_name}' is profane (corrupt). Resetting: {e}")
            return {}

    def _persist(self):
        """[THE RITE OF INSCRIPTION]"""
        try:
            # Uses kernel-level atomic write for zero-loss integrity
            atomic_write(self.path, json.dumps(self._memory, indent=2), self.logger, self.root)
        except Exception as e:
            self.logger.error(f"Matter Inscription Fracture in {self.shard_name}: {e}")

    @abstractmethod
    def conduct(self, key: str, action: str, payload: Dict[str, Any]) -> Any:
        """The primary kinetic rite of the shard."""
        pass

    def get_manifest(self) -> Dict[str, Any]:
        """Returns a census of the shard's current state."""
        return {
            "shard": self.shard_name,
            "mass_bytes": self.path.stat().st_size if self.path.exists() else 0,
            "entry_count": len(self._memory),
            "state_snapshot": self._memory
        }