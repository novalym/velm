# Path: core/daemon/dispatcher/executor.py
# ----------------------------------------
# LIF: INFINITY | ROLE: THREAD_CONTEXT_MANAGER
import os
from typing import Any, Callable


class KineticExecutor:
    """
    [THE HAND]
    Static utilities for executing logic within a managed context.
    """

    @staticmethod
    def execute_rite(engine_dispatch: Callable,
                     request_obj: Any,
                     req_id: Any) -> Any:
        """
        [THE ATOMIC RITE]
        Executes the dispatch call with environment DNA injection.
        This runs INSIDE the worker thread.
        """
        # 1. Inject DNA (Link Python thread to Request ID)
        os.environ["GNOSTIC_REQUEST_ID"] = str(req_id)

        try:
            # 2. Execute
            return engine_dispatch(request_obj)
        finally:
            # 3. Cleanse (Tabula Rasa)
            os.environ.pop("GNOSTIC_REQUEST_ID", None)

    @staticmethod
    def transmute_result(result: Any) -> Any:
        """
        [THE REVELATION]
        Converts complex Python objects (Pydantic) into JSON-safe dicts.
        """
        if result is None:
            return None

        # V2 Pydantic
        if hasattr(result, 'model_dump'):
            return result.model_dump(mode='json')

        # V1 Pydantic
        if hasattr(result, 'dict'):
            return result.dict()

        # Raw Matter
        return result