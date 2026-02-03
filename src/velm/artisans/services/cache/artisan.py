import logging
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import CacheRequest
from ....interfaces.base import ScaffoldResult
from .engine import RedisEngine

Logger = logging.getLogger("CacheArtisan")


class CacheArtisan(BaseArtisan[CacheRequest]):
    """
    =============================================================================
    == THE TIMEKEEPER (V-Ω-STATE-CONTROL)                                      ==
    =============================================================================
    LIF: ∞ | ROLE: STATE_MANAGER

    Manages ephemeral state, distributed locks, and rate limits.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self.redis = RedisEngine()

    def execute(self, request: CacheRequest) -> ScaffoldResult:
        try:
            result = self.redis.execute(request)

            # Contextual Messaging
            msg = f"Cache {request.action} on '{request.key}' succeeded."
            if request.action == "lock" and not result:
                msg = f"Lock acquisition failed for '{request.key}'."
                # We return success=True but data=False so caller can decide logic flow
                # (Soft failure pattern)

            return self.engine.success(msg, data=result)

        except Exception as e:
            Logger.error(f"Cache Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Cache Rite Failed: {str(e)}")