# Path: core/runtime/engine/resilience/circuit.py
# -----------------------------------------------

import time
import threading
from enum import Enum
from typing import Dict, Optional


class CircuitState(Enum):
    CLOSED = "CLOSED"  # Healthy, traffic flows
    OPEN = "OPEN"  # Failed, traffic blocked
    HALF_OPEN = "HALF"  # Probing for recovery


class CircuitBreaker:
    """
    =============================================================================
    == THE CIRCUIT BREAKER (V-Ω-CASCADING-FAILURE-SHIELD)                      ==
    =============================================================================
    Quarantines failing subsystems.
    """

    FAILURE_THRESHOLD = 5
    RESET_TIMEOUT = 30.0  # Seconds

    def __init__(self, logger):
        self.logger = logger
        # Map[ArtisanName, CircuitData]
        self._circuits: Dict[str, Dict] = {}
        self._lock = threading.RLock()

    def check_state(self, artisan_name: str) -> bool:
        """
        Returns True if the artisan is allowed to execute.
        Returns False if the circuit is OPEN (Broken).
        """
        with self._lock:
            if artisan_name not in self._circuits:
                self._circuits[artisan_name] = {"state": CircuitState.CLOSED, "failures": 0, "last_failure": 0}

            c = self._circuits[artisan_name]

            if c["state"] == CircuitState.OPEN:
                if time.time() - c["last_failure"] > self.RESET_TIMEOUT:
                    c["state"] = CircuitState.HALF_OPEN
                    self.logger.info(f"Circuit for {artisan_name} enters HALF-OPEN state. Probing...")
                    return True
                return False

            return True

    def record_success(self, artisan_name: str):
        """Heals the circuit on success."""
        with self._lock:
            if artisan_name in self._circuits:
                c = self._circuits[artisan_name]
                if c["state"] != CircuitState.CLOSED:
                    self.logger.success(f"Circuit Breaker RESTORED for {artisan_name}. System is healthy.")
                c["state"] = CircuitState.CLOSED
                c["failures"] = 0

    def record_failure(self, artisan_name: str):
        """Records a strike against the artisan."""
        with self._lock:
            if artisan_name not in self._circuits:
                self._circuits[artisan_name] = {"state": CircuitState.CLOSED, "failures": 0, "last_failure": 0}

            c = self._circuits[artisan_name]
            c["failures"] += 1
            c["last_failure"] = time.time()

            if c["state"] == CircuitState.HALF_OPEN or c["failures"] >= self.FAILURE_THRESHOLD:
                c["state"] = CircuitState.OPEN
                self.logger.warn(f"Circuit Breaker TRIPPED for {artisan_name}. System is shielded.")