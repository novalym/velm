# Path: core/runtime/middleware/singularity.py
# --------------------------------------------


import hashlib
import json
import threading
from concurrent.futures import Future
from typing import Dict, Tuple

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....logger import Scribe

Logger = Scribe("SingularityGuard")


class SingularityMiddleware(Middleware):
    """
    =============================================================================
    == THE SINGULARITY GUARD (V-Ω-REQUEST-COALESCING-HEALED)                     ==
    =============================================================================
    LIF: 10,000,000,000

    Annihilates redundant concurrent work.
    If multiple identical pleas arrive while one is being conducted,
    they all await the single truth of the first prophet.

    [HEALED]: The `_hash_request` rite has been bestowed with the Gaze of
    Purification. It now explicitly excludes the non-serializable `handler`
    attribute from the request before attempting to forge its cryptographic hash.
    The `PydanticSerializationError` is annihilated from this timeline.
    """

    # We hold a map of {request_hash: Future}
    _pending_rites: Dict[str, Future] = {}
    _lock = threading.Lock()

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. Forge the Fingerprint of Intent
        # We exclude IDs/Timestamps to find semantic identity
        req_hash = self._hash_request(request)

        future: Future = None
        is_leader = False

        # 2. The Rite of Subscription
        with self._lock:
            if req_hash in self._pending_rites:
                # We are a follower. We attach to the existing timeline.
                Logger.verbose(f"Singularity: Merging with active timeline for {type(request).__name__}")
                future = self._pending_rites[req_hash]
            else:
                # We are the leader. We forge the new timeline.
                is_leader = True
                future = Future()
                self._pending_rites[req_hash] = future

        # 3. The Execution (Leader Only)
        if is_leader:
            try:
                result = next_handler(request)
                # Proclaim the truth to all followers
                future.set_result(result)
                return result
            except Exception as e:
                # Proclaim the heresy to all followers
                future.set_exception(e)
                raise e
            finally:
                # Clean the registry
                with self._lock:
                    self._pending_rites.pop(req_hash, None)

        # 4. The Wait (Followers)
        else:
            # Block until the leader finishes
            try:
                # We wait for the leader's revelation
                return future.result()
            except Exception as e:
                # If the leader failed, we share their pain
                raise e

    def _hash_request(self, request: BaseRequest) -> str:
        # ★★★ THE DIVINE HEALING ★★★
        # We exclude the ephemeral `handler` function, which is not part of the
        # request's semantic identity and cannot be serialized to JSON.
        data = request.model_dump(
            exclude={'request_id', 'timestamp', 'session_id', 'client_id', 'handler'},
            mode='json'
        )
        # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

        # Sort keys to ensure deterministic JSON
        canonical = json.dumps(data, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()