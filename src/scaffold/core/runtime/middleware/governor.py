# Path: scaffold/core/runtime/middleware/governor.py
# --------------------------------------------------

import time
import threading
from typing import Dict, Tuple

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class RateLimitMiddleware(Middleware):
    """
    =============================================================================
    == THE QUANTUM GOVERNOR (V-Ω-FLOW-CONTROL-CORRECTED)                        ==
    =============================================================================
    LIF: 10,000,000,000

    Enforces Gnostic limits on the rate of reality manipulation.

    **CORRECTION:** The Bucket now initializes to the BURST limit (Full),
    ensuring that fresh CLI invocations or the first request to the Daemon
    are never rejected immediately.
    """

    # (Burst Capacity, Refill Rate per Second)
    LIMITS: Dict[str, Tuple[float, float]] = {
        "GenesisRequest": (5.0, 0.5),  # Heavy creation: 5 burst, 1 per 2s refill
        "DistillRequest": (10.0, 0.5),  # Heavy analysis: 10 burst, 1 per 2s refill
        "AnalyzeRequest": (50.0, 5.0),  # Fast analysis: 50 burst, 5 per 1s refill
        "RunRequest": (50.0, 20.0),  # Execution: High burst, fast refill for tests/scripts
        "default": (100.0, 10.0)  # Standard: Very generous
    }

    # We do not use defaultdict here because we need the 'burst' value
    # to initialize the token count.
    _buckets: Dict[str, Dict[str, float]] = {}
    _lock = threading.Lock()

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. The Rite of Absolute Will (Admin Bypass)
        if request.force:
            return next_handler(request)

        # 2. Identify the Rite & Client
        rite_name = type(request).__name__
        burst, rate = self.LIMITS.get(rite_name, self.LIMITS["default"])

        # We segregate buckets by client_id (IP/Session) to prevent one user starving others
        # In local CLI, client_id defaults to 'unknown' or 'local', which is fine (single user)
        client_id = getattr(request, "client_id", "local")
        key = f"{client_id}:{rite_name}"

        # 3. The Calculus of Flow
        with self._lock:
            now = time.time()

            if key not in self._buckets:
                # [THE FIX] Initialize with FULL burst.
                # The user starts with a full tank.
                self._buckets[key] = {
                    "tokens": burst,
                    "last_check": now
                }

            bucket = self._buckets[key]

            # Calculate Refill
            elapsed = now - bucket["last_check"]
            bucket["last_check"] = now

            # Add tokens based on time passed, capped at burst limit
            bucket["tokens"] = min(burst, bucket["tokens"] + (elapsed * rate))

            # Attempt Consumption
            cost = 1.0  # Future: Could vary cost by request complexity

            if bucket["tokens"] >= cost:
                bucket["tokens"] -= cost
            else:
                # 4. The Halt
                # Calculate wait time for helpful error message
                tokens_needed = cost - bucket["tokens"]
                wait_seconds = tokens_needed / rate

                raise ArtisanHeresy(
                    f"Rate Limit Exceeded for {rite_name}.",
                    severity=HeresySeverity.WARNING,
                    suggestion=f"The Governor demands patience. Limit: {rate}/s. Retry in {wait_seconds:.1f}s."
                )

        # 5. Proceed
        return next_handler(request)