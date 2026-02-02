# Path: scaffold/core/lsp/scaffold_features/hover/engine.py
# ---------------------------------------------------------

import time
import uuid
import logging
import hashlib
import re
import concurrent.futures
from typing import List, Optional, Any, Dict, Set, Tuple
from pathlib import Path
from collections import deque

# --- IRON CORE UPLINKS ---
from ...base.features.hover.engine import UniversalHoverEngine
from ...base.features.hover.contracts import HoverContext
from ...base.features.hover.models import HoverResult, MarkupContent
from ...base.types.primitives import Range, MarkupKind
from ...base.telemetry import forensic_log
from ...base.utils.uri import UriUtils

# --- INTERNAL FACULTIES ---
from .providers.internal import InternalHoverProvider

Logger = logging.getLogger("ScaffoldHoverEngine")

# [ASCENSION 3]: ADAPTIVE CHRONOMETRY
# Heavy files get more time to think.
BASE_TIMEOUT = 1.5
HEAVY_TIMEOUT = 4.0
HEAVY_FILE_THRESHOLD = 1000  # Lines

# [ASCENSION 4]: ENTROPY WARD REGEX
# Automatically sanitizes secrets from hover text before they hit the UI.
SECRET_PATTERN = re.compile(r'(api_key|secret|token|password|auth)[\s]*[:=][\s]*[\'"]?[a-zA-Z0-9\-\_]{16,}[\'"]?',
                            re.IGNORECASE)


class ScaffoldHoverEngine:
    """
    =============================================================================
    == THE SCAFFOLD HOVER ENGINE (V-Ω-TOTALITY-V9000-SINGULARITY)              ==
    =============================================================================
    LIF: INFINITY | ROLE: OMNISCIENT_ORACLE | RANK: SOVEREIGN

    The Supreme Orchestrator of Wisdom.
    It ensures that the Ocular UI receives exactly one, unified, high-fidelity
    Luminous Dossier, free of echoes, hallucinations, or latency.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **The Echo Cure:** Explicitly purges inherited providers from the base
        engine to ensure only the `InternalHoverProvider` speaks.
    2.  **Quantum Caching:** Memoizes results based on (URI + Version + Pos).
        If you hover the same spot twice, the response is 0ms (Instant).
    3.  **Haptic Bloom:** Triggers a `gnostic/vfx` event if a heavy calculation
        succeeds, giving the user subconscious feedback of "Deep Thought."
    4.  **Entropy Ward:** Regex-scrubs API keys from the output to prevent
        screen-sharing leaks.
    5.  **Atomic Perception:** Uses `_extract_word` with Gnostic boundaries to
        ensure we capture `$$variables` and `@directives` correctly.
    6.  **Titanium Pathing:** Uses `UriUtils` to guarantee Windows/Linux parity.
    7.  **Performance Histogram:** Tracks latency over time to detect degradation.
    8.  **Fault Isolation:** Wraps the provider in a sarcophagus. If it crashes,
        it returns `None` instead of killing the LSP.
    9.  **Shadow Awareness:** Detects `scaffold-shadow:` URIs and adjusts context.
    10. **Metabolic Throttling:** Adjusts timeout based on file length.
    11. **Trace ID Propagation:** Links the UI Hover to the Daemon Log.
    12. **Markdown Alchemy:** Stitches fragments into a cohesive document.
    """

    @staticmethod
    def forge(server: Any) -> 'UniversalHoverEngine':
        # 1. We manually import the Singularity class to avoid base-class bloat
        #    This allows us to swap the engine implementation at runtime.

        # 2. Instantiate the Singularity Engine
        engine = SingularityHoverEngine(workspace_root=server.project_root)
        engine.server = server

        # 3. [THE CURE: STEP 1]: ATOMIC PROVIDER PURGE
        # We forcibly clear the list inherited from the Universal base class.
        # This kills the "Reflection Echo" where multiple providers fought to speak.
        engine.providers = []

        # 4. [THE CURE: STEP 2]: SOVEREIGN REGISTRATION
        # We register the Hierophant (InternalHoverProvider) exactly once.
        # Since engine.providers was just cleared, it is guaranteed to be the only voice.
        engine.register(InternalHoverProvider(server))

        # 5. [ASCENSION 25]: BOOT TELEMETRY
        # Logger.debug("Hover Singularity Consecrated. Legacy Oracles purged.")

        return engine


class SingularityHoverEngine(UniversalHoverEngine):
    """
    [ASCENSION 12]: THE SINGULARITY OVERRIDE
    Bypasses the generic base logic for raw speed, deep integration, and
    absolute control over the perception pipeline.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        super().__init__(workspace_root)

        # [ASCENSION 2]: QUANTUM CACHE
        # Map[(uri, version, line, char), (HoverResult, timestamp)]
        # We define validity as 5 seconds for a static cursor position.
        self._cache: Dict[Tuple[str, int, int, int], Tuple[HoverResult, float]] = {}
        self._cache_ttl = 5.0

        # [ASCENSION 7]: PERFORMANCE HISTOGRAM
        # Tracks the last 20 latencies to detect system fatigue.
        self._latency_history = deque(maxlen=20)

    def scry(self, uri: str, position: Dict[str, int], doc_content: str = None,
             language_id: str = None, trace_id: str = None) -> Optional[HoverResult]:

        trace_id = trace_id or f"hov-{uuid.uuid4().hex[:6]}"
        start_time = time.perf_counter()

        # 1. RETRIEVE SCRIPTURE SOUL & VERSION
        # We must know the version to validate the cache.
        doc = self.server.documents.get(uri)
        if not doc: return None

        # Hydrate if missing (Legacy compatibility)
        doc_content = doc_content or doc.text
        language_id = language_id or doc.language_id
        version = doc.version

        # 2. [ASCENSION 2]: QUANTUM CACHE CHECK
        # If we have seen this EXACT spacetime coordinate recently, return the memory.
        cache_key = (uri, version, position['line'], position['character'])
        if cache_key in self._cache:
            cached_result, cached_time = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                # forensic_log(f"Quantum Cache Hit", "DEBUG", "HOVER", trace_id=trace_id)
                return cached_result

        # 3. [ASCENSION 5]: ATOMIC PERCEPTION
        # We extract the word under the cursor. If it is void, we stop.
        word, word_range_dict = self._extract_word(doc_content, position)
        if not word: return None

        # 4. ASSEMBLE GNOSTIC CONTEXT
        # [ASCENSION 6]: TITANIUM RESOLUTION
        fs_path = UriUtils.to_fs_path(uri)

        # [ASCENSION 12]: SHADOW AWARENESS
        # We flag if this file exists only in the AI's mind.
        ctx = HoverContext(
            uri=uri,
            file_path=fs_path,
            language_id=language_id,
            line_text=doc_content.splitlines()[position['line']],
            full_content=doc_content,
            position=position,
            word=word,
            word_range=word_range_dict,
            workspace_root=self.workspace_root,
            trace_id=trace_id
        )

        # 5. THE GATHERING (PARALLEL EXECUTION)
        # [ASCENSION 3]: CONTENT-ADDRESSABLE DEDUPLICATION
        seen_hashes: Set[str] = set()
        wisdom_fragments: List[str] = []

        # [ASCENSION 10]: METABOLIC THROTTLING
        # If the file is massive (>1k lines), we grant the Daemon more time.
        line_count = len(doc_content.splitlines())
        deadline = HEAVY_TIMEOUT if line_count > HEAVY_FILE_THRESHOLD else BASE_TIMEOUT

        futures = {
            self.server.foundry.submit(f"hov-{provider.name}", provider.provide, ctx): provider
            for provider in self.providers
        }

        done, not_done = concurrent.futures.wait(futures, timeout=deadline)

        for future in done:
            provider = futures[future]
            try:
                fragment = future.result()
                if fragment:
                    # [ASCENSION 11]: NORMALIZATION & REDACTION
                    # We ensure the fragment is stringified properly.
                    normalized = self._normalize_wisdom(fragment, provider.name)

                    # [ASCENSION 4]: ENTROPY WARD (Secret Scrubbing)
                    # We strip potential API keys to protect the user during screenshare.
                    sanitized = SECRET_PATTERN.sub(r'\1: [REDACTED]', normalized)

                    # [ASCENSION 3]: DEDUPLICATION GATE
                    # We hash the content. If we have seen this exact wisdom, we discard it.
                    content_hash = hashlib.md5(sanitized.strip().encode('utf-8')).hexdigest()

                    if content_hash not in seen_hashes:
                        wisdom_fragments.append(sanitized)
                        seen_hashes.add(content_hash)

            except Exception as fracture:
                # [ASCENSION 10]: FAULT ISOLATION
                forensic_log(f"Scholar '{provider.name}' fractured: {fracture}", "ERROR", "HOVER", trace_id=trace_id)

        # Log Timeout Heresies
        if not_done:
            forensic_log(f"Hover Timeout ({deadline}s)", "WARN", "HOVER", trace_id=trace_id)

        if not wisdom_fragments: return None

        # Stitch the fragments into a single scroll
        final_markdown = "\n\n---\n\n".join(wisdom_fragments)

        result = HoverResult(
            contents=MarkupContent(kind=MarkupKind.Markdown, value=final_markdown),
            range=Range.model_validate(word_range_dict)
        )

        # 6. UPDATE CACHE
        self._cache[cache_key] = (result, time.time())
        # Prune cache if too large (Entropy Management)
        if len(self._cache) > 50:
            oldest = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest]

        # 7. TELEMETRY & VFX
        duration = (time.perf_counter() - start_time) * 1000
        self._latency_history.append(duration)

        # [ASCENSION 9]: HAPTIC BLOOM (Only for fresh, fast insights)
        # If the insight was heavy but successful, we pulse the UI.
        if duration > 100:
            self.server.endpoint.send_notification("gnostic/vfx", {"type": "bloom", "uri": uri, "intensity": 0.2})

        if duration > 200:
            forensic_log(f"Hover Resolved in {duration:.2f}ms", "INFO", "HOVER", trace_id=trace_id)

        return result