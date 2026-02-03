# Path: scaffold/core/runtime/middleware/tracing.py
# -------------------------------------------------

import uuid
import threading
from typing import Optional

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....logger import Scribe

# Thread-local storage for the active Trace ID
_trace_context = threading.local()


def get_current_trace_id() -> Optional[str]:
    return getattr(_trace_context, 'trace_id', None)


class DistributedTracingMiddleware(Middleware):
    """
    =============================================================================
    == THE SILVER CORD (V-Ω-UNIVERSAL-CAUSALITY)                               ==
    =============================================================================
    LIF: 10,000,000,000

    Assigns a unique Cosmic ID to every request chain.
    This ID survives network boundaries, linking CLI -> Daemon -> Remote -> Swarm.
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. Establish Identity
        # Use existing ID if passed (from remote caller), else forge new one
        trace_id = getattr(request, 'trace_id', None) or str(uuid.uuid4())

        # 2. Enshrine in Thread Context (For Scribe)
        _trace_context.trace_id = trace_id

        # 3. Inscribe on Request (For propagation)
        # We dynamically patch the request object to carry the ID if it doesn't have the field
        if not hasattr(request, 'trace_id'):
            setattr(request, 'trace_id', trace_id)

        # 4. Log the Bond
        self.logger.verbose(f"Trace ID established: [magenta]{trace_id}[/magenta]")

        try:
            # 5. Execute
            return next_handler(request)
        finally:
            # 6. Cleanup
            _trace_context.trace_id = None