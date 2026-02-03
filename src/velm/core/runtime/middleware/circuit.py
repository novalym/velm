import time
from enum import Enum
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy


class CircuitState(Enum):
    CLOSED = "CLOSED"  # Normal Operation
    OPEN = "OPEN"  # Failing, rejecting requests
    HALF_OPEN = "HALF"  # Testing recovery


class CircuitBreakerMiddleware(Middleware):
    """
    =============================================================================
    == THE LAZARUS CIRCUIT (V-Ω-CASCADING-FAILURE-PREVENTION)                  ==
    =============================================================================
    LIF: 10,000,000,000

    Monitors the health of Artisans. If an Artisan becomes sick (throws critical
    heresies), this middleware quarantines it to prevent systemic collapse.
    """

    FAILURE_THRESHOLD = 5
    RESET_TIMEOUT = 30.0  # Seconds

    _circuits = {}  # {ArtisanName: {state, failures, last_failure}}

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        artisan_name = type(request).__name__.replace("Request", "Artisan")

        # 1. Check Circuit Health
        circuit = self._get_circuit(artisan_name)

        if circuit["state"] == CircuitState.OPEN:
            if time.time() - circuit["last_failure"] > self.RESET_TIMEOUT:
                # Transition to Half-Open (Allow one scout)
                circuit["state"] = CircuitState.HALF_OPEN
                self.logger.info(f"Circuit for {artisan_name} enters HALF-OPEN state. Probing...")
            else:
                # Fast Fail (Zero Latency)
                raise ArtisanHeresy(
                    f"Circuit Breaker is OPEN for {artisan_name}.",
                    suggestion="The subsystem is recovering from repeated failures. Please wait."
                )

        # 2. Attempt Execution
        try:
            result = next_handler(request)

            # 3. Analyze Result for Critical Heresy
            if result.success:
                self._reset_circuit(artisan_name)
            elif result.has_critical_heresy:
                # Logic failure (not user error) triggers the breaker
                self._record_failure(artisan_name)

            return result

        except Exception:
            # Crashes definitely trigger the breaker
            self._record_failure(artisan_name)
            raise

    def _get_circuit(self, name: str):
        if name not in self._circuits:
            self._circuits[name] = {"state": CircuitState.CLOSED, "failures": 0, "last_failure": 0}
        return self._circuits[name]

    def _record_failure(self, name: str):
        c = self._circuits[name]
        c["failures"] += 1
        c["last_failure"] = time.time()
        if c["state"] == CircuitState.HALF_OPEN or c["failures"] >= self.FAILURE_THRESHOLD:
            c["state"] = CircuitState.OPEN
            self.logger.warn(f"Circuit Breaker TRIPPED for {name}. System is shielded.")

    def _reset_circuit(self, name: str):
        c = self._circuits[name]
        if c["state"] != CircuitState.CLOSED:
            self.logger.success(f"Circuit Breaker RESTORED for {name}. System is healthy.")
        c["state"] = CircuitState.CLOSED
        c["failures"] = 0