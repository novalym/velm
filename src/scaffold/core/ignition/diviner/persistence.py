# Path: scaffold/core/ignition/diviner/persistence.py
# ----------------------------------------------------
# LIF: INFINITY // AUTH_CODE: DIVINER_PERSISTENCE_V1

import json
import hashlib
import time
from pathlib import Path
from typing import Optional, Dict, Any
from ..contracts import ExecutionPlan
from ....logger import Scribe

Logger = Scribe("GnosticPersistence")


class PersistenceMatrix:
    """
    =============================================================================
    == THE PERSISTENCE MATRIX (V-Ω-TEMPORAL-STABILITY)                         ==
    =============================================================================
    [ASCENSION 65]: Remembers the soul of a directory across incarnations.
    """

    def __init__(self, project_root: Path):
        self.cache_path = project_root / ".scaffold" / "cache" / "divination.json"
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

    def _forge_merkle_key(self, root: Path) -> str:
        """[ASCENSION 68]: Generates a structural fingerprint of the sanctum."""
        try:
            # We hash the names and mtimes of top-level artifacts
            items = sorted([f.name + str(f.stat().st_mtime) for f in root.iterdir() if f.is_file()])
            return hashlib.sha256("".join(items).encode()).hexdigest()
        except:
            return str(root)

    def recall(self, root: Path) -> Optional[Dict[str, Any]]:
        if not self.cache_path.exists():
            return None

        try:
            data = json.loads(self.cache_path.read_text())
            key = self._forge_merkle_key(root)

            if key in data:
                # [ASCENSION 70]: TTL Enforcement
                entry = data[key]
                if time.time() - entry["timestamp"] < 3600:  # 1 hour Gnostic TTL
                    Logger.verbose("Reality Recalled from Matrix Cache.")
                    return entry["plan"]
        except:
            pass
        return None

    def enshrine(self, root: Path, plan: ExecutionPlan):
        """[ASCENSION 72]: Saves the plan into the temporal vault."""
        key = self._forge_merkle_key(root)
        try:
            data = {}
            if self.cache_path.exists():
                data = json.loads(self.cache_path.read_text())

            data[key] = {
                "timestamp": time.time(),
                "plan": plan.model_dump(mode='json')
            }

            # Prune old memories (keep last 50)
            if len(data) > 50:
                sorted_keys = sorted(data.keys(), key=lambda k: data[k]["timestamp"])
                data.pop(sorted_keys[0])

            self.cache_path.write_text(json.dumps(data, indent=2))
        except Exception as e:
            Logger.warn(f"Persistence Fracture: {e}")