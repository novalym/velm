# Path: core/lsp/features/references/engine.py
# --------------------------------------------

import time
import logging
import concurrent.futures
import uuid
from typing import List, Optional, Any, Dict, Set
from .contracts import ReferenceProvider
from .models import ReferenceParams, Location
from ...utils.text import TextUtils
from ...utils.uri import UriUtils

Logger = logging.getLogger("ReferenceEngine")


class ReferenceEngine:
    """
    =============================================================================
    == THE ECHO CONDUCTOR (V-Ω-RELATIONAL-DISPATCHER-V12)                      ==
    =============================================================================
    LIF: 10,000,000 | ROLE: RELATIONAL_MAPPER | RANK: SOVEREIGN

    The central intelligence that orchestrates the search for symbolic echoes.
    It coordinates a Council of Seeker-Providers to map every usage of a particle
    across the entire project constellation.
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[ReferenceProvider] = []

        # [ASCENSION 1]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=6,
            thread_name_prefix="ReferenceSeekerWorker"
        )

    def register(self, provider: ReferenceProvider):
        """Consecrates a new reference seeker in the registry."""
        self.providers.append(provider)
        # Sort by priority descending
        self.providers.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Reference Seeker Consecrated: {provider.name}")

    def compute(self, params: ReferenceParams) -> List[Location]:
        """
        [THE RITE OF DISCOVERY]
        Aggregates references from all providers in parallel.
        """
        start_time = time.perf_counter()
        trace_id = f"ref-{uuid.uuid4().hex[:6]}"

        # 1. RETRIEVE THE LIVING SCRIPTURE
        uri = str(params.text_document.uri.root) if hasattr(params.text_document.uri, 'root') else str(
            params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc:
            return []

        # 2. DIVINE THE ATOM (Word Identification)
        info = TextUtils.get_word_at_position(doc, params.position)
        if not info:
            return []

        # 3. [ASCENSION 1]: PARALLEL GATHERING
        all_locations: List[Location] = []

        # We poll all providers in the background to prevent UI lag
        futures = {self._executor.submit(p.find_references, doc, info, params.context): p for p in self.providers}

        # [ASCENSION 8]: Wait for the Council (with 2s threshold for global scans)
        done, not_done = concurrent.futures.wait(futures, timeout=2.0)

        for future in done:
            provider = futures[future]
            try:
                locations = future.result()
                if locations:
                    all_locations.extend(locations)
            except Exception as e:
                Logger.error(f"Seeker '{provider.name}' fractured for '{info.text}': {e}", exc_info=True)

        if not_done:
            Logger.warning(f"Global Reference scan partially timed out for {info.text}.")

        # 4. [ASCENSION 5]: GEOMETRIC DEDUPLICATION
        final_locations = self._deduplicate(all_locations)

        # 5. TELEMETRY
        duration_ms = (time.perf_counter() - start_time) * 1000
        Logger.debug(f"[{trace_id}] Found {len(final_locations)} echoes in {duration_ms:.2f}ms")

        return final_locations

    def _deduplicate(self, locations: List[Location]) -> List[Location]:
        """
        [ASCENSION 5]: ANNIHILATE DUPLICATE REALITIES
        Ensures that multiple providers hitting the same range are merged.
        """
        seen: Set[str] = set()
        unique: List[Location] = []

        for loc in locations:
            # Create a unique fingerprint for the location
            # [ASCENSION 4]: Normalize URI for the signature
            norm_uri = UriUtils.normalize_uri(str(loc.uri.root if hasattr(loc.uri, 'root') else loc.uri))
            sig = f"{norm_uri}:{loc.range.start.line}:{loc.range.start.character}"

            if sig not in seen:
                seen.add(sig)
                unique.append(loc)

        return unique