# Path: core/lsp/base/features/inline_completion/engine.py
# --------------------------------------------------------

import time
import logging
import concurrent.futures
import uuid
from typing import List, Any
from .contracts import InlineCompletionProvider
from .models import InlineCompletionList, InlineCompletionItem, InlineCompletionParams

Logger = logging.getLogger("InlineCompletionEngine")


class InlineCompletionEngine:
    """
    =============================================================================
    == THE PROPHET ORCHESTRATOR (V-Ω-PREDICTIVE-CORE)                          ==
    =============================================================================
    LIF: 10,000,000 | ROLE: GHOST_TEXT_DISPATCHER | RANK: SOVEREIGN

    Coordinates the Council of Prophets (AI, Snippets, Heuristics) to generate
    inline ghost text. Enforces strict timeouts to prevent typing lag.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[InlineCompletionProvider] = []

        # [ASCENSION 1]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="ProphetWorker"
        )

    def register(self, provider: InlineCompletionProvider):
        """Consecrates a new prophet."""
        self.providers.append(provider)
        self.providers.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Prophet Consecrated: {provider.name}")

    def compute(self, params: InlineCompletionParams) -> InlineCompletionList:
        """
        [THE RITE OF FORESIGHT]
        Aggregates predictions from all providers in parallel.
        """
        start_time = time.perf_counter()
        trace_id = f"pred-{uuid.uuid4().hex[:6]}"

        # 1. PARALLEL GATHERING
        all_items: List[InlineCompletionItem] = []

        # Map futures to providers
        futures = {self._executor.submit(p.prophesy, params): p for p in self.providers}

        # [ASCENSION 2]: HARD TIMEOUT
        # Ghost text must be fast (< 300ms) or it is useless noise.
        done, not_done = concurrent.futures.wait(futures, timeout=0.300)

        for future in done:
            provider = futures[future]
            try:
                items = future.result()
                if items:
                    all_items.extend(items)
            except Exception as e:
                Logger.error(f"Prophet '{provider.name}' fractured: {e}", exc_info=True)

        if not_done:
            Logger.warning(f"[{trace_id}] Prophets timed out: {[futures[f].name for f in not_done]}")

        # [ASCENSION 3]: TELEMETRY
        duration_ms = (time.perf_counter() - start_time) * 1000
        if duration_ms > 50:
            Logger.debug(f"[{trace_id}] Prophecy: {len(all_items)} visions in {duration_ms:.2f}ms")

        return InlineCompletionList(items=all_items)