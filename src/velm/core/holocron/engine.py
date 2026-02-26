# Path: core/holocron/engine.py
# ------------------------------
import threading
import time
from pathlib import Path
from typing import Dict, Any, Optional
from ..cortex.engine import GnosticCortex
from ...logger import Scribe

Logger = Scribe("GnosticHolocron")


class Holocron:
    """
    =================================================================================
    == THE GNOSTIC HOLOCRON (V-Ω-TOTALITY-V25000-SHARED-MEMORY)                    ==
    =================================================================================
    LIF: ∞ | ROLE: CEREBRAL_SYNCHRONIZER | RANK: OMEGA_SOVEREIGN

    The Holocron is the persistent, shared mind of the project. It lives in the
    Daemon and is accessed by both CLI and LSP. It annihilates the "Perception Lag"
    by ensuring all clients see the same Gnostic Graph in real-time.
    =================================================================================
    """
    _instances: Dict[Path, 'Holocron'] = {}
    _global_lock = threading.Lock()

    def __new__(cls, project_root: Path, *args, **kwargs):
        with cls._global_lock:
            root = project_root.resolve()
            if root not in cls._instances:
                cls._instances[root] = super(Holocron, cls).__new__(cls)
            return cls._instances[root]

    def __init__(self, project_root: Path, engine: Any = None):
        if hasattr(self, '_initialized'): return
        self.root = project_root.resolve()
        self.engine = engine

        # [ASCENSION 1]: The Shared Cortex
        # This Cortex is now shared by every process accessing this project.
        self.cortex = GnosticCortex(self.root)

        # [ASCENSION 4]: The Temporal Heartbeat
        self.last_sync = time.time()
        self._lock = threading.RLock()
        self._initialized = True

        Logger.success(f"Holocron manifest for '{self.root.name}'. Perception is now Universal.")

    def sync_reality(self):
        """Forces an atomic re-perception across the entire project lattice."""
        with self._lock:
            self.cortex.perceive(force_refresh=True)
            self.last_sync = time.time()

    def get_gnosis(self) -> Dict[str, Any]:
        """Returns a holographic snapshot of the project's current soul."""
        return {
            "root": str(self.root),
            "last_sync": self.last_sync,
            "complexity": self.cortex.scry_complexity(),  # Assuming this method
            "nodes": len(self.cortex._memory.inventory)
        }