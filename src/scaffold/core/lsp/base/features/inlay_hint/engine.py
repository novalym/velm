# Path: core/lsp/base/features/inlay_hint/engine.py
# -------------------------------------------------

import time
import logging
import concurrent.futures
import uuid
from typing import List, Optional, Any, Dict
from .contracts import InlayHintProvider
from .models import InlayHint, InlayHintParams
from ...types.primitives import Range

Logger = logging.getLogger("InlayHintEngine")


class InlayHintEngine:
    """
    =============================================================================
    == THE GHOST CONDUCTOR (V-Ω-RANGE-DISPATCHER-V13-HEALED)                   ==
    =============================================================================
    LIF: 10,000,000 | ROLE: SPECTRAL_ORCHESTRATOR | RANK: SOVEREIGN

    The central intelligence that coordinates the Council of Ghost-Writers.

    [ASCENSION 13]: OBJECT-ORIENTED ACCESS
    Fixed 'AttributeError: get' by accessing Pydantic fields via dot notation.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[InlayHintProvider] = []

        # [ASCENSION 1]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="GhostWriterWorker"
        )

    def register(self, provider: InlayHintProvider):
        """Consecrates a new ghost-writer in the registry."""
        self.providers.append(provider)
        # Sort by priority descending
        self.providers.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Ghost-Writer Consecrated: {provider.name}")

    def compute(self, params: InlayHintParams) -> List[InlayHint]:
        """
        [THE RITE OF GHOST-WRITING]
        Aggregates spectral hints from all providers for the requested range.
        """
        start_time = time.perf_counter()
        trace_id = f"ghost-{uuid.uuid4().hex[:6]}"

        # 1. RETRIEVE THE LIVING SCRIPTURE
        # [THE CURE]: Universal Accessor Pattern
        # Handles both Pydantic Models (dot access) and legacy Dicts (.get)
        uri_data = params.text_document

        if hasattr(uri_data, 'uri'):
            uri = str(uri_data.uri)
        else:
            uri = str(uri_data.get('uri', ''))

        doc = self.server.documents.get(uri)
        if not doc:
            return []

        # 2. [ASCENSION 2]: SPATIAL RANGE TRIAGE
        target_range = params.range

        # 3. [ASCENSION 1]: PARALLEL INQUEST
        all_hints: List[InlayHint] = []

        # We poll all providers in the background to prevent UI lag
        futures = {self._executor.submit(p.provide_hints, doc, target_range): p for p in self.providers}

        # 500ms hard-timeout for spectral revelation
        done, not_done = concurrent.futures.wait(futures, timeout=0.5)

        for future in done:
            provider = futures[future]
            try:
                hints = future.result()
                if hints:
                    all_hints.extend(hints)
            except Exception as e:
                Logger.error(f"Ghost-Writer '{provider.name}' fractured range {target_range}: {e}", exc_info=True)

        # Log slow writers
        for f in not_done:
            Logger.warning(f"Ghost-Writer '{futures[f].name}' was too slow for range revelation.")

        # 4. FINAL TELEMETRY
        duration_ms = (time.perf_counter() - start_time) * 1000
        if duration_ms > 100:
            Logger.debug(f"[{trace_id}] Spectral Projection: {len(all_hints)} hints in {duration_ms:.2f}ms")

        return all_hints