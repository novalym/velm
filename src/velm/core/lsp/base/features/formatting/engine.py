# Path: core/lsp/features/formatting/engine.py
# ------------------------------------------------

import time
import logging
import concurrent.futures
import uuid
from typing import List, Optional, Any, Dict
from .contracts import FormattingProvider
from .models import DocumentFormattingParams, DocumentRangeFormattingParams, TextEdit, FormattingOptions
from ...types.primitives import Range, Position

Logger = logging.getLogger("FormattingEngine")


class FormattingEngine:
    """
    =============================================================================
    == THE MASTER PURIFIER (V-Ω-GEOMETRIC-ORCHESTRATOR-V12)                    ==
    =============================================================================
    LIF: 10,000,000 | ROLE: AESTHETIC_DISPATCHER | RANK: SOVEREIGN

    The central intelligence that coordinates the Council of Purifiers.
    It ensures that formatting requests are handled with nanosecond precision
    and that the resulting deltas are syntactically and geometrically pure.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[FormattingProvider] = []

        # [ASCENSION 5]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=2,  # Formatting is usually serial/blocking per file
            thread_name_prefix="FormattingWorker"
        )

    def register(self, provider: FormattingProvider):
        """Consecrates a new aesthetic purifier."""
        self.providers.append(provider)
        self.providers.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Formatting Provider Registered: {provider.name}")

    def compute_full(self, params: DocumentFormattingParams) -> List[TextEdit]:
        """
        [THE RITE OF TOTAL PURIFICATION]
        """
        start_time = time.perf_counter()
        trace_id = f"fmt-{uuid.uuid4().hex[:6]}"

        uri = str(params.text_document.uri.root) if hasattr(params.text_document.uri, 'root') else str(
            params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return []

        # [ASCENSION 1 & 9]: DELTA CALCULATION
        for provider in self.providers:
            try:
                # We currently take the first provider that claims the language
                # In Iteration 2, we will add language-id filtering
                edits = provider.format_document(doc, params.options)
                if edits:
                    duration = (time.perf_counter() - start_time) * 1000
                    Logger.debug(f"[{trace_id}] Document purified by '{provider.name}' in {duration:.2f}ms")
                    return edits
            except Exception as e:
                Logger.error(f"Purifier '{provider.name}' fractured: {e}")

        return []

    def compute_range(self, params: DocumentRangeFormattingParams) -> List[TextEdit]:
        """
        [THE RITE OF RANGE PURIFICATION]
        """
        uri = str(params.text_document.uri.root) if hasattr(params.text_document.uri, 'root') else str(
            params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return []

        for provider in self.providers:
            try:
                edits = provider.format_range(doc, params.range, params.options)
                if edits:
                    return edits
            except Exception as e:
                Logger.error(f"Range Purifier '{provider.name}' fractured: {e}")

        return []