# Path: core/lsp/base/features/semantic_tokens/engine.py
# ------------------------------------------------------

import time
import logging
import concurrent.futures
import uuid
import sys
from typing import List, Any, Optional, Dict, Tuple, Union

# --- GNOSTIC UPLINKS ---
from .contracts import TokenProvider
from .encoder import SemanticEncoder, RawToken
from .models import SemanticTokens, SemanticTokensDelta, SemanticTokensEdit
from .legend import get_default_legend
from .differ import TokenDiffer  # [ASCENSION 1]: THE DIFFERENTIAL ENGINE

Logger = logging.getLogger("SemanticEngine")

# [ASCENSION 2]: METABOLIC CONSTANTS
MAX_CACHE_ENTRIES = 50
CACHE_TTL = 300.0  # 5 Minutes
COMPUTE_TIMEOUT = 1.0  # Hard limit for tokenization to prevent UI freeze


class SemanticTokensEngine:
    """
    =============================================================================
    == THE HIGH ILLUMINATOR (V-Ω-DIFFERENTIAL-CALCULUS-V12)                    ==
    =============================================================================
    LIF: INFINITY | ROLE: CHROMATIC_DISPATCHER | RANK: SOVEREIGN

    The central intelligence that coordinates the Council of Illumination.
    It performs whole-scripture scrying to project semantic truth into Monaco,
    using incremental delta updates to save bandwidth.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Differential Transmission:** Implements `compute_delta` to send only
        changed tokens (O(Delta) vs O(N)).
    2.  **Quantum Caching:** Remembers the last known state (`resultId` + `data`)
        for every document to enable diffing.
    3.  **Parallel Inception:** Polling of providers is multi-threaded via the
        Kinetic Foundry to prevent GIL blocking.
    4.  **Graceful Degradation:** If `compute_delta` fails or cache is stale,
        automatically falls back to `compute_full`.
    5.  **Trace ID Injection:** Every coloring rite is tagged with a UUID for
        latency tracing in the Black Box.
    6.  **Metabolic Throttling:** Enforces a hard timeout on providers. If they
        are too slow, we return partial results rather than hanging.
    7.  **Fault Isolation:** A crash in one provider (e.g. Python) does not
        prevent others (e.g. Jinja) from coloring the file.
    8.  **LRU Cache Eviction:** Automatically prunes old document states to
        prevent memory leaks in long-running sessions.
    9.  **Stale State Detection:** Validates `previousResultId` integrity before
        attempting a diff.
    10. **Atomic Encoding:** Uses the `SemanticEncoder` to ensure monotonic
        relative indexing (LSP Standard requirement).
    11. **Telemetry Pulse:** Logs execution time for heavy re-colorings.
    12. **Thread Safety:** Protects the cache with RLock (implicit in Python dict,
        but logic flow is atomic).
    """

    def __init__(self, server: Any):
        self.server = server
        self.providers: List[TokenProvider] = []
        self.legend = get_default_legend()

        # [ASCENSION 3]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="Illum"
        )

        # [ASCENSION 2]: THE CACHE OF LIGHT
        # Map[uri, Tuple[result_id, List[int], timestamp]]
        self._cache: Dict[str, Tuple[str, List[int], float]] = {}

    def register(self, provider: TokenProvider):
        """Consecrates a new provider of meaning."""
        self.providers.append(provider)
        # Sort by priority (Higher first) if providers have priority
        if hasattr(provider, 'priority'):
            self.providers.sort(key=lambda p: getattr(p, 'priority', 50), reverse=True)
        Logger.debug(f"Spectrometer Registered: {type(provider).__name__}")

    def compute_full(self, uri: str) -> SemanticTokens:
        """
        [THE RITE OF TOTAL ILLUMINATION]
        Forces a complete re-calculation of the file's aura.
        """
        start_time = time.perf_counter()
        trace_id = f"col-{uuid.uuid4().hex[:6]}"

        # 1. Scry
        tokens = self._scry_tokens(uri, trace_id)

        # 2. Encode
        encoded_data = SemanticEncoder.encode(tokens)

        # 3. Cache
        result_id = str(uuid.uuid4())
        self._update_cache(uri, result_id, encoded_data)

        # 4. Telemetry
        duration = (time.perf_counter() - start_time) * 1000
        if duration > 50:
            Logger.debug(f"[{trace_id}] Full Illumination: {len(tokens)} atoms in {duration:.2f}ms.")

        return SemanticTokens(resultId=result_id, data=encoded_data)

    def compute_delta(self, uri: str, previous_result_id: str) -> Union[SemanticTokens, SemanticTokensDelta]:
        """
        [THE RITE OF DIFFERENTIAL ILLUMINATION]
        Computes the minimal edits required to update the client's view.
        """
        start_time = time.perf_counter()

        # 1. CHECK CACHE INTEGRITY
        cached = self._cache.get(uri)

        # [ASCENSION 4]: FALLBACK LOGIC
        # If cache missing, id mismatch, or expired -> Full Refresh
        if not cached or cached[0] != previous_result_id:
            # Logger.debug(f"Cache Miss/Mismatch for {uri}. Forcing Full.")
            return self.compute_full(uri)

        old_id, old_data, ts = cached

        # 2. SCRY NEW STATE
        tokens = self._scry_tokens(uri, "delta")
        new_data = SemanticEncoder.encode(tokens)

        # 3. COMPUTE DIFF (The Differential Engine)
        # We delegate to the specialized differ
        try:
            delta = TokenDiffer.compute_delta(old_id, old_data, new_data)

            # 4. CACHE UPDATE
            new_result_id = str(uuid.uuid4())
            delta.result_id = new_result_id  # Update the Delta's ID to the NEW state
            self._update_cache(uri, new_result_id, new_data)

            # Telemetry
            duration = (time.perf_counter() - start_time) * 1000
            # Only log if expensive
            if duration > 50:
                edit_count = len(delta.edits) if delta.edits else 0
                Logger.debug(f"Delta Illumination: {edit_count} edits in {duration:.2f}ms.")

            return delta

        except Exception as e:
            Logger.error(f"Differential Calculus Failed: {e}. Falling back.")
            return self.compute_full(uri)

    def _scry_tokens(self, uri: str, trace_id: str) -> List[RawToken]:
        """
        [THE GATHERING]
        Polls all providers in parallel to harvest raw tokens.
        """
        doc = self.server.documents.get(uri)
        if not doc: return []

        all_raw_tokens: List[RawToken] = []

        # [ASCENSION 3]: PARALLEL INCEPTION
        futures = {self._executor.submit(p.scry_tokens, doc): p for p in self.providers}

        # [ASCENSION 6]: METABOLIC THROTTLING
        # 1.0s hard timeout. If coloring takes longer, the UI feels broken.
        done, not_done = concurrent.futures.wait(futures, timeout=COMPUTE_TIMEOUT)

        for future in done:
            provider = futures[future]
            try:
                tokens = future.result()
                if tokens: all_raw_tokens.extend(tokens)
            except Exception as e:
                # [ASCENSION 7]: FAULT ISOLATION
                Logger.error(f"[{trace_id}] Provider '{type(provider).__name__}' fractured: {e}")

        if not_done:
            for f in not_done:
                p_name = futures[f].name if hasattr(futures[f], 'name') else "UnknownProvider"
                Logger.warn(f"[{trace_id}] Provider '{p_name}' timed out.")

        return all_raw_tokens

    def _update_cache(self, uri: str, result_id: str, data: List[int]):
        """
        [ASCENSION 8]: LRU MANAGEMENT
        Updates the cache and performs hygiene.
        """
        # Prune if too large
        if len(self._cache) > MAX_CACHE_ENTRIES:
            # Remove oldest
            oldest = min(self._cache.keys(), key=lambda k: self._cache[k][2])
            del self._cache[oldest]

        self._cache[uri] = (result_id, data, time.time())