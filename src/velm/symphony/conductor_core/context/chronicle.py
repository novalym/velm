# Path: scaffold/symphony/conductor_core/context/chronicle.py
# -----------------------------------------------------------

import time
from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .vault import GnosticVault

class GnosticChronicle:
    """
    =============================================================================
    == THE SCROLL OF CHANGES (V-Ω-AUDIT-LOG)                                   ==
    =============================================================================
    Records every mutation of the Gnostic State for forensic analysis.
    """

    def __init__(self, vault: 'GnosticVault'):
        self.vault = vault
        self._history: List[Dict[str, Any]] = []

    def record(self, action: str, key: str, old_value: Any, new_value: Any):
        """Inscribes a mutation into the ledger."""
        if old_value == new_value:
            return

        entry = {
            "timestamp": time.time(),
            "action": action,
            "key": key,
            "old": self.vault.mask(key, old_value),
            "new": self.vault.mask(key, new_value)
        }
        self._history.append(entry)

    def dump(self) -> List[Dict[str, Any]]:
        """Returns the full history."""
        return list(self._history)