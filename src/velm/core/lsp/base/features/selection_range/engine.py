# Path: core/lsp/base/features/selection_range/engine.py
# ------------------------------------------------------
import time
import logging
import concurrent.futures
import uuid
from typing import List, Any
from .contracts import SelectionRangeProvider
from .models import SelectionRange, SelectionRangeParams

Logger = logging.getLogger("SelectionRangeEngine")


class SelectionRangeEngine:
    """
    =============================================================================
    == THE EXPANSION ORCHESTRATOR (V-Ω-GEOMETRIC-CORE)                         ==
    =============================================================================
    LIF: 10,000,000 | ROLE: SELECTION_DISPATCHER

    Coordinates the providers to calculate smart selection ranges.
    Usually, only one provider is active per language, but this supports composition.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[SelectionRangeProvider] =[]

    def register(self, provider: SelectionRangeProvider):
        self.providers.append(provider)
        Logger.debug(f"Selection Strategy Registered: {provider.name}")

    def compute(self, params: SelectionRangeParams) -> List[SelectionRange]:
        """
        [THE RITE OF EXPANSION]
        """
        start_time = time.perf_counter()
        trace_id = f"sel-{uuid.uuid4().hex[:6]}"

        uri = str(params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return[]

        for provider in self.providers:
            try:
                # Execute in thread to prevent blocking
                future = self.server.foundry.submit(f"sel-{provider.name}", provider.provide_selection_ranges, doc, params.positions)
                results = future.result(timeout=0.5)  # Fast timeout for UI responsiveness

                if results:
                    duration = (time.perf_counter() - start_time) * 1000
                    return results
            except Exception as e:
                Logger.error(f"Strategy '{provider.name}' fractured: {e}")

        return[]