# Path: core/lsp/base/features/hover/engine.py
# --------------------------------------------
# LIF: INFINITY | ROLE: KNOWLEDGE_AGGREGATOR | RANK: BASE_CLASS
# auth_code: Ω_UNIVERSAL_HOVER_V100_TITANIUM

import time
import logging
import concurrent.futures
import uuid
import re
from typing import List, Optional, Any, Dict, Tuple
from pathlib import Path

# --- GNOSTIC UPLINKS ---
from .contracts import HoverProvider, HoverContext
from .models import HoverResult, MarkupContent
from ...types.primitives import Range, MarkupKind
from ...telemetry import forensic_log
from ...utils.uri import UriUtils

Logger = logging.getLogger("UniversalHoverEngine")

# [ASCENSION 1]: CHRONOMETRIC CONSTANTS
DEFAULT_TIMEOUT = 1.0  # 1s limit for standard queries
HEAVY_TIMEOUT = 2.0  # 2s limit for massive scriptures
MAX_WORKERS = 8  # Parallelism limit


class UniversalHoverEngine:
    """
    =============================================================================
    == THE UNIVERSAL SCHOLAR (V-Ω-BASE-HOVER-ENGINE-ASCENDED)                  ==
    =============================================================================
    LIF: INFINITY | ROLE: KNOWLEDGE_AGGREGATOR | RANK: BASE_CLASS

    The foundational intelligence that coordinates the Council of Providers.
    It provides the physics for parallel execution, fault isolation, and
    result transmutation.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root
        self.providers: List[HoverProvider] = []
        self.server = None  # Injected after forge

        # [ASCENSION 1]: KINETIC FOUNDRY
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=MAX_WORKERS,
            thread_name_prefix="HoverScholar"
        )

        # [ASCENSION 11]: REGEX HARDENING
        # Matches typical identifiers: words, dots, dashes, $, @, %, /, :
        self._word_pattern = re.compile(r'[\w\@\$\%\-\.\/\:]+')

    def register(self, provider: HoverProvider):
        """
        [RITE OF CONSECRATION]
        Adds a new source of wisdom to the council, sorted by authority.
        """
        self.providers.append(provider)
        # [ASCENSION 12]: PRIORITY SORTING
        self.providers.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Hover Provider Registered: {provider.name} (Priority {provider.priority})")

    def scry(self,
             uri: str,
             position: Dict[str, int],
             doc_content: str = None,
             language_id: str = None,
             trace_id: str = "0xVOID") -> Optional[HoverResult]:
        """
        [THE RITE OF REVELATION]
        Orchestrates the parallel inquest for information.
        """
        start_time = time.perf_counter()

        # 1. [ASCENSION 10]: CONTEXT HYDRATION
        # If content wasn't passed, try to fetch from the Server's Librarian
        if not doc_content and self.server:
            doc = self.server.documents.get(uri)
            if doc:
                doc_content = doc.text
                language_id = doc.language_id
            else:
                forensic_log(f"Document Void in Memory: {uri}", "WARN", "HOVER", trace_id=trace_id)
                return None

        if not doc_content:
            return None

        # 2. [ASCENSION 3]: ATOMIC WORD EXTRACTION
        word, word_range = self._extract_word(doc_content, position)

        if not word:
            return None

        # 3. ASSEMBLE CONTEXT
        # [ASCENSION 4]: TITANIUM PATHING
        fs_path = Path(UriUtils.to_fs_path(uri)) if UriUtils else Path(uri)

        try:
            line_text = doc_content.splitlines()[position['line']]
        except IndexError:
            line_text = ""

        ctx = HoverContext(
            uri=uri,
            file_path=fs_path,
            language_id=language_id or 'plaintext',
            line_text=line_text,
            full_content=doc_content,
            position=position,
            word=word,
            word_range=word_range,
            workspace_root=self.workspace_root,
            trace_id=trace_id
        )

        # 4. [ASCENSION 2]: PARALLEL INQUEST
        wisdom_fragments: List[str] = []

        # Map futures to providers
        futures = {
            self._executor.submit(p.provide, ctx): p
            for p in self.providers
        }

        # [ASCENSION 6]: METABOLIC THROTTLING
        timeout = HEAVY_TIMEOUT if len(doc_content) > 50000 else DEFAULT_TIMEOUT

        done, not_done = concurrent.futures.wait(futures, timeout=timeout)

        for future in done:
            provider = futures[future]
            try:
                fragment = future.result()
                if fragment:
                    # [ASCENSION 4]: MARKDOWN ALCHEMY
                    wisdom_fragments.append(self._normalize_wisdom(fragment, provider.name))
            except Exception as e:
                # [ASCENSION 2]: FAULT SARCOPHAGUS
                forensic_log(f"Provider '{provider.name}' fractured: {e}", "ERROR", "HOVER", trace_id=trace_id)

        # Log slow providers
        if not_done:
            for f in not_done:
                p_name = futures[f].name
                forensic_log(f"Provider '{p_name}' timed out (> {timeout}s).", "WARN", "HOVER", trace_id=trace_id)

        if not wisdom_fragments:
            return None

        # 5. [ASCENSION 9]: VISUAL SEPARATION
        final_markdown = "\n\n---\n\n".join(wisdom_fragments)

        # [ASCENSION 7]: TELEMETRY PULSE
        duration_ms = (time.perf_counter() - start_time) * 1000
        if duration_ms > 50:
            forensic_log(f"Revelation achieved in {duration_ms:.2f}ms.", "INFO", "HOVER", trace_id=trace_id)

        return HoverResult(
            contents=MarkupContent(kind=MarkupKind.Markdown, value=final_markdown),
            range=Range.model_validate(word_range)
        )

    def _extract_word(self, content: str, pos: Dict[str, int]) -> Tuple[str, Dict]:
        """
        [ASCENSION 3]: ATOMIC WORD EXTRACTION
        Surgically extracts the token under the cursor using pre-compiled Gnostic Boundaries.
        """
        try:
            lines = content.splitlines()
            line_idx = pos['line']
            char_idx = pos['character']

            if line_idx >= len(lines): return "", {}

            line = lines[line_idx]

            # Simple boundary check
            if char_idx > len(line): char_idx = len(line)
            if char_idx < 0: return "", {}

            # Iterate matches to find the one containing the cursor
            for match in self._word_pattern.finditer(line):
                if match.start() <= char_idx <= match.end():
                    return match.group(0), {
                        "start": {"line": line_idx, "character": match.start()},
                        "end": {"line": line_idx, "character": match.end()}
                    }
            return "", {}
        except Exception:
            return "", {}

    def _normalize_wisdom(self, fragment: Any, source_name: str) -> str:
        """
        [ASCENSION 4]: ALCHEMICAL FORMATTER
        Ensures all wisdom is presented as readable Markdown.
        """
        if isinstance(fragment, str):
            return fragment
        if isinstance(fragment, list):
            return "\n\n".join(str(f) for f in fragment)
        if isinstance(fragment, dict):
            # Transmute dictionary to a readable key-value markdown list
            lines = [f"**{source_name}**"]
            for k, v in fragment.items():
                lines.append(f"- **{k}**: {v}")
            return "\n".join(lines)
        return str(fragment)