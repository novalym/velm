# Path: core/runtime/engine/execution/simulacrum/shards/signal.py
# --------------------------------------------------------------

from .base import BaseShardArtisan
from typing import Dict, Any, List
import time


class SignalShardArtisan(BaseShardArtisan):
    """
    =============================================================================
    == THE SIGNAL SHARD (V-Ω-COMMUNICATION-SENTINEL)                           ==
    =============================================================================
    LIF: ∞ | ROLE: THE_HERALD | RANK: MASTER

    Simulates Twilio (SMS/Voice) and Email services. It maintains a
    'Transmissions Ledger' to allow the Symphony to verify sent signals.
    """

    def __init__(self, storage_root):
        super().__init__(storage_root, "signal")

    def conduct(self, channel: str, action: str, payload: Dict[str, Any]) -> Any:
        """
        Actions: send, lookup, get_history
        """
        if channel not in self._memory:
            self._memory[channel] = {"history": [], "vitals": {"sent_count": 0}}

        # --- THE KINETIC TRIAGE ---
        if action == "send":
            transmission = {
                "id": f"msg_{int(time.time() * 1000)}",
                "ts": time.time(),
                "to": payload.get("to"),
                "body": payload.get("body"),
                "status": "DELIVERED_SIMULATED"
            }
            self._memory[channel]["history"].append(transmission)
            self._memory[channel]["vitals"]["sent_count"] += 1
            self._persist()
            return transmission

        elif action == "get_history":
            # Return the chronological scroll of signals
            return self._memory[channel]["history"]

        elif action == "lookup":
            # Mock HLR/Carrier lookup
            return {"status": "valid", "carrier": "VelmVirtual", "type": "mobile"}

        return None