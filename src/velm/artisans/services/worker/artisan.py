import logging
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import WorkerRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy
from .engine import TaskEngine

Logger = logging.getLogger("WorkerArtisan")


class WorkerArtisan(BaseArtisan[WorkerRequest]):
    """
    =============================================================================
    == THE TASKMASTER (V-Ω-TEMPORAL-WORKER)                                    ==
    =============================================================================
    LIF: ∞ | ROLE: ASYNC_ORCHESTRATOR

    Offloads logic to the background.
    Compatible with RQ (Redis Queue) out of the box.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self.task_engine = TaskEngine()

    def execute(self, request: WorkerRequest) -> ScaffoldResult:
        try:
            # Validate Redis Connection implicitly via execution
            result = self.task_engine.execute(request)

            return self.engine.success(
                f"Task '{request.task}' dispatched to '{request.queue}' queue.",
                data=result
            )

        except Exception as e:
            Logger.error(f"Queue Fracture: {e}", exc_info=True)
            return self.engine.failure(f"Task Dispatch Failed: {str(e)}")