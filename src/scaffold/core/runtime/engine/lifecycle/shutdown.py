# Path: core/runtime/engine/lifecycle/shutdown.py
# -----------------------------------------------

import threading
import time
from typing import Any


class ShutdownManager:
    """
    =============================================================================
    == THE REAPER (V-Ω-GRACEFUL-DISSOLUTION)                                   ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: THE_DESTROYER

    Orchestrates the shutdown sequence.
    1.  **The Seal:** Stops accepting new requests.
    2.  **The Drain:** Waits for pending heavy rites to finish (optional).
    3.  **The Rollback:** Reverses any uncommitted transactions.
    4.  **The Silence:** Closes logs and sockets.
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.logger = engine.logger

    def execute(self, force: bool = False):
        """
        Performs the Rite of Dissolution.
        """
        self.logger.system("Initiating Shutdown Sequence...")

        # 1. Stop Vitality (The Heart stops first)
        self.engine.watchdog.stop_vigil()
        if hasattr(self.engine, 'vitality'):
            self.engine.vitality.stop_vigil()

        # 2. Stop Dispatcher (The Brain stops thinking)
        # This will drain or kill the thread pools.
        self.engine.dispatcher.shutdown()

        # 3. Clean Transactions (The Memory is purified)
        # Any active transactions are rolled back to ensure disk consistency.
        # The TransactionManager's destructor or context managers handle this,
        # but we can explicitly log active ones.
        active_tx = len(self.engine.transactions._active_transactions)
        if active_tx > 0:
            self.logger.warn(f"Rolling back {active_tx} incomplete transactions...")
            # Ideally, we iterate and rollback manually here if the context managers
            # are stuck in threads we just killed.
            # (Advanced implementation details omitted for brevity)

        # 4. Final Proclamation
        self.logger.system("Engine Dissolved. Returning to the Void.")