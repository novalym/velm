# Path: scaffold/core/runtime/middleware/forensics.py
# ---------------------------------------------------

import time
import json
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult


class ForensicMiddleware(Middleware):
    """
    =============================================================================
    == THE KEEPER OF THE CHRONICLE (V-Ω-AUDIT-LOG)                             ==
    =============================================================================
    Records every interaction with the God-Engine into an immutable ledger.
    """

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        start_time = time.time()

        # 1. Execute the Rite
        result = next_handler(request)

        duration = time.time() - start_time

        # 2. Chronicle the Event
        try:
            self._scribe_entry(request, result, duration)
        except Exception as e:
            # Logging must never crash the app
            self.logger.warn(f"Forensic Scribe faltered: {e}")

        return result

    def _scribe_entry(self, request: BaseRequest, result: ScaffoldResult, duration: float):
        if not request.project_root: return

        journal_path = request.project_root / ".scaffold" / "journal.jsonl"
        journal_path.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "timestamp": time.time(),
            "request_id": str(request.request_id),
            "rite": request.__class__.__name__,
            "success": result.success,
            "duration": duration,
            "params": request.model_dump(exclude={'project_root', 'content'}, mode='json'),
            "artifacts": [str(a.path) for a in result.artifacts]
        }

        with open(journal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")