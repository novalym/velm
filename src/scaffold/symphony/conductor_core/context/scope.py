# Path: scaffold/symphony/conductor_core/context/scope.py
# -------------------------------------------------------

import copy
from typing import Dict, Any, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from .manager import GnosticContextManager


class EphemeralScope:
    """
    =============================================================================
    == THE EPHEMERAL SCOPE (V-Ω-DETERMINISTIC-CONTEXT)                         ==
    =============================================================================
    A dedicated, class-based context manager for temporary state mutations.
    It guarantees the restoration of the Gnostic State.
    """

    def __init__(self, manager: 'GnosticContextManager', overrides: Dict[str, Any]):
        self.manager = manager
        self.overrides = overrides
        self.snapshots: Dict[str, Any] = {}
        self.keys_to_delete: Set[str] = set()

    def __enter__(self):
        # 1. Snapshot Reality
        # We must access the internal store directly via the manager's lock
        with self.manager._lock:
            for key in self.overrides.keys():
                if key in self.manager:
                    self.snapshots[key] = copy.deepcopy(self.manager[key])
                else:
                    self.keys_to_delete.add(key)

            # 2. Apply Mutations
            self.manager.update(self.overrides)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.manager._lock:
            # 3. Restore Reality
            # Restore modified keys
            for key, value in self.snapshots.items():
                self.manager[key] = value

            # Remove keys that didn't exist before
            for key in self.keys_to_delete:
                if key in self.manager:
                    del self.manager[key]