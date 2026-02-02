# Path: core/lsp/features/code_lens/engine.py
# --------------------------------------------

import time
import logging
import concurrent.futures
import uuid
from typing import List, Optional, Any, Dict
from .contracts import CodeLensProvider
from .models import CodeLens, CodeLensParams

Logger = logging.getLogger("CodeLensEngine")


class CodeLensEngine:
    """
    =============================================================================
    == THE LENS CONDUCTOR (V-Ω-OVERLAY-ORCHESTRATOR-V12)                       ==
    =============================================================================
    LIF: 10,000,000 | ROLE: ACTION_ORCHESTRATOR | RANK: SOVEREIGN

    The central intelligence that coordinates the Council of Lens-Makers.
    It performs whole-scripture scrying to project interactive portals
    directly into the editor lattice.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[CodeLensProvider] = []

        # [ASCENSION 1]: KINETIC FOUNDRY
        # Thread pool for non-blocking lens discovery.
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="LensWorker"
        )

    def register(self, provider: CodeLensProvider):
        """Consecrates a new lens provider in the registry."""
        self.providers.append(provider)
        # Sort by priority
        self.providers.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Lens Provider Consecrated: {provider.name}")

    def compute(self, params: CodeLensParams) -> List[CodeLens]:
        """
        [THE RITE OF DETECTION]
        Aggregates lens anchors from all providers.
        """
        start_time = time.perf_counter()
        trace_id = f"lens-{uuid.uuid4().hex[:6]}"

        uri = str(params.text_document.uri.root) if hasattr(params.text_document.uri, 'root') else str(
            params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc:
            return []

        # [ASCENSION 1]: PARALLEL INQUEST
        all_lenses: List[CodeLens] = []

        # Poll all providers in parallel
        futures = {self._executor.submit(p.provide_lenses, doc): p for p in self.providers}

        # 400ms threshold for lens detection
        done, not_done = concurrent.futures.wait(futures, timeout=0.400)

        for future in done:
            provider = futures[future]
            try:
                lenses = future.result()
                if lenses:
                    # [ASCENSION 8]: Trace ID Injection
                    for lens in lenses:
                        if lens.data is None: lens.data = {}
                        if isinstance(lens.data, dict):
                            lens.data['_provider'] = provider.name
                            lens.data['_trace_id'] = trace_id
                    all_lenses.extend(lenses)
            except Exception as e:
                Logger.error(f"Lens Provider '{provider.name}' fractured: {e}", exc_info=True)

        duration_ms = (time.perf_counter() - start_time) * 1000
        if duration_ms > 100:
            Logger.debug(f"[{trace_id}] Lens Discovery: {len(all_lenses)} anchors in {duration_ms:.2f}ms")

        return all_lenses

    def resolve(self, lens: CodeLens) -> CodeLens:
        """
        [THE RITE OF RESOLUTION]
        Called by the client when a lens becomes visible.
        Links the anchor to its physical Command.
        """
        if not lens.data or not isinstance(lens.data, dict):
            return lens

        provider_name = lens.data.get('_provider')
        provider = next((p for p in self.providers if p.name == provider_name), None)

        if not provider:
            return lens

        try:
            # We need to find the document again for the provider to scry it
            # This logic assumes the lens.data carries enough info to find the doc
            # or the server state is sufficient.
            return provider.resolve_lens(lens, None)  # Placeholder for V1
        except Exception as e:
            Logger.error(f"Lens Resolution failed for {provider_name}: {e}")
            return lens