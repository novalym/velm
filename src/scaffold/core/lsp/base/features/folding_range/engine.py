# Path: core/lsp/base/features/folding_range/engine.py
# ----------------------------------------------------

import time
import logging
import concurrent.futures
import uuid
from typing import List, Any
from .contracts import FoldingRangeProvider
from .models import FoldingRange, FoldingRangeParams

Logger = logging.getLogger("FoldingEngine")

class FoldingRangeEngine:
    """
    =============================================================================
    == THE COMPRESSION CONDUCTOR (V-Ω-FOLDING-ORCHESTRATOR-V12)                ==
    =============================================================================
    LIF: 10,000,000 | ROLE: GEOMETRIC_DISPATCHER | RANK: SOVEREIGN

    The central intelligence that coordinates the Council of Compressors.
    It aggregates folding ranges from all registered providers.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[FoldingRangeProvider] = []

        # [ASCENSION 1]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=2, # Folding is usually fast, low concurrency needed
            thread_name_prefix="FoldingWorker"
        )

    def register(self, provider: FoldingRangeProvider):
        """Consecrates a new folding strategy."""
        self.providers.append(provider)
        Logger.debug(f"Folding Strategy Registered: {provider.name}")

    def compute(self, params: FoldingRangeParams) -> List[FoldingRange]:
        """
        [THE RITE OF COMPRESSION]
        Aggregates ranges from all providers.
        """
        start_time = time.perf_counter()
        trace_id = f"fold-{uuid.uuid4().hex[:6]}"

        # [THE CURE]: Universal Accessor Pattern
        uri_data = params.text_document
        if hasattr(uri_data, 'uri'):
            uri = str(uri_data.uri)
        else:
            uri = str(uri_data.get('uri', ''))

        doc = self.server.documents.get(uri)
        if not doc: return []

        all_ranges: List[FoldingRange] = []

        # [ASCENSION 1]: PARALLEL GATHERING
        futures = {self._executor.submit(p.provide_folding_ranges, doc): p for p in self.providers}

        # 200ms threshold for folding calculation
        done, not_done = concurrent.futures.wait(futures, timeout=0.2)

        for future in done:
            provider = futures[future]
            try:
                ranges = future.result()
                if ranges:
                    all_ranges.extend(ranges)
            except Exception as e:
                Logger.error(f"Strategy '{provider.name}' fractured: {e}", exc_info=True)

        # [ASCENSION 2]: LIMIT GOVERNOR
        # VS Code has a limit on folding ranges (usually 5000). We clamp it to be safe.
        if len(all_ranges) > 5000:
            all_ranges = all_ranges[:5000]

        duration_ms = (time.perf_counter() - start_time) * 1000
        if duration_ms > 50:
            Logger.debug(f"[{trace_id}] Folding Calculation: {len(all_ranges)} ranges in {duration_ms:.2f}ms")

        return all_ranges