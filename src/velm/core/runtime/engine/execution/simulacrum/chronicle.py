# Path: core/runtime/engine/execution/simulacrum/chronicle.py
# ---------------------------------------------------------

import hashlib
import time
from typing import List, Dict


class RealityChronicle:
    """
    =============================================================================
    == THE CHRONICLE (V-Ω-MERKLE-HISTORY)                                     ==
    =============================================================================
    Tracks every mutation of the Simulacrum to allow for Achronal Rollbacks.
    """

    def __init__(self):
        self.history: List[str] = []
        self.merkle_root: str = "0xVOID"

    def inscribe_mutation(self, shard_id: str, state_diff: Dict):
        """Calculates the new Merkle Root after a mutation."""
        timestamp = str(time.time())
        mutation_hash = hashlib.sha256(f"{shard_id}{state_diff}{timestamp}".encode()).hexdigest()

        self.history.append(mutation_hash)

        # Update Root
        combined = "".join(self.history)
        self.merkle_root = hashlib.sha256(combined.encode()).hexdigest()