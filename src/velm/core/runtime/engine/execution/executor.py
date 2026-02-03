# Path: core/runtime/engine/execution/executor.py
# -----------------------------------------------

import os
import sys
import threading
from typing import Any, Callable, TypeVar, Optional

T = TypeVar("T")

class KineticExecutor:
    """
    =============================================================================
    == THE KINETIC EXECUTOR (V-Ω-THREAD-SAFE)                                  ==
    =============================================================================
    Static utilities for executing logic within a managed thread context.
    """

    @staticmethod
    def execute_with_dna(
        func: Callable[[], T],
        req_id: str,
        job_id: str
    ) -> T:
        """
        [THE ATOMIC RITE]
        Executes a function with environment DNA injection (Request/Job IDs).
        This runs INSIDE the worker thread.
        """
        # 1. Inject DNA (Link Python thread to Request ID for logging)
        os.environ["GNOSTIC_REQUEST_ID"] = str(req_id)
        os.environ["GNOSTIC_JOB_ID"] = str(job_id)

        try:
            # 2. Execute
            return func()
        finally:
            # 3. Cleanse (Tabula Rasa)
            os.environ.pop("GNOSTIC_REQUEST_ID", None)
            os.environ.pop("GNOSTIC_JOB_ID", None)

    @staticmethod
    def transmute_result(result: Any) -> Any:
        """
        [THE REVELATION]
        Converts complex Python objects (Pydantic Models) into JSON-safe dicts.
        Handles V1/V2 Pydantic schemas.
        """
        if result is None:
            return None

        # V2 Pydantic
        if hasattr(result, 'model_dump'):
            return result.model_dump(mode='json')

        # V1 Pydantic
        if hasattr(result, 'dict'):
            return result.dict()

        # Raw Matter (Dict/List/Primtive)
        return result