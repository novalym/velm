# Path: artisans/completion_artisan/artisan.py
# --------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_COMPLETION_SPLIT_BRAIN_V24
# ROLE: DEEP_MAGIC_ORCHESTRATOR | RANK: SOVEREIGN
# =================================================================================

import time
import re
import uuid
import logging
import traceback
import concurrent.futures
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import CompletionRequest
from ...core.alchemist import get_alchemist

# --- THE SANCTUM PROPHETS (DEEP MIND ONLY) ---
# [ASCENSION 1]: THE GREAT SEVERANCE
# We purge Keyword, Variable, and Path prophets.
# They live in the LSP now (0ms Latency).
from .prophets.snippets import SnippetProphet
from .prophets.alchemist import AlchemistProphet
from .prophets.directives import DirectiveProphet
from .prophets.canon import GnosticCanon  # [ASCENSION 1]: IMPORT CANON

# [ASCENSION 2]: ORACLE UPLINK
# We ensure the Grimoire Reader is accessible for the SnippetProphet
from .grimoire.reader import ORACLE as SNIPPET_ORACLE

Logger = logging.getLogger("CompletionArtisan")

# Physics Constants
MAX_PROPHET_LATENCY = 0.250  # 250ms Hard Timeout
TOKEN_PATTERN = re.compile(r'([\w\$\@\%\/\.\-\:]+)$')


@dataclass(frozen=True)
class ProphecyContext:
    """
    [THE HOLOGRAPHIC CONTEXT]
    Immutable snapshot of reality, adjusted for Virtual Injection.
    """
    uri: str
    file_path: Path
    project_root: Path
    trace_id: str
    full_content: str
    line_text: str
    line_prefix: str  # The Holographic Prefix
    partial_token: str
    token_start_char: int
    next_char: str
    position: Dict[str, int]
    line_idx: int
    char_idx: int
    indent_str: str
    scope_depth: int
    language_id: str
    is_inside_jinja: bool
    is_inside_comment: bool
    trigger_character: Optional[str]
    trigger_kind: int
    alchemist: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


class CompletionArtisan(BaseArtisan[CompletionRequest]):
    """
    =================================================================================
    == THE DEEP MIND (V-Ω-SPLIT-BRAIN-ASCENDED)                                    ==
    =================================================================================
    This Artisan now serves ONLY the "Heavy" Gnosis:
    1. Snippets (JSONC Grimoire)
    2. Alchemical Functions (Jinja2 Logic)
    3. Structural Directives (@if, @for logic)

    It yields the floor to the Local LSP for all Syntax, Variables, and Paths.
    """

    def __init__(self, engine):
        super().__init__(engine)
        self.alchemist = get_alchemist()

        # [ASCENSION 2]: INITIALIZE CANON
        # This object will cache the live state of the engine.
        self.canon = GnosticCanon(engine)

        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="ProphetWorker"
        )

        # [ASCENSION 3]: REGISTER DYNAMIC PROPHETS
        self.prophets = [
            SnippetProphet(self),  # Static Library (Fast)
            AlchemistProphet(self),  # Dynamic Jinja (Live)
            DirectiveProphet(self)  # Dynamic Directives (Live)
        ]

    def execute(self, request: CompletionRequest) -> ScaffoldResult:
        start_ns = time.perf_counter_ns()

        # [ASCENSION 8]: TRACE DNA
        meta = getattr(request, 'metadata', {})
        if not isinstance(meta, dict): meta = {}
        trace_id = str(meta.get('trace_id', f"deep-{uuid.uuid4().hex[:6]}"))

        try:
            # 1. FORGE THE CONTEXT (With Holographic Injection)
            ctx = self._forge_context(request, trace_id)
            if not ctx: return self.success("Void Context", data=[])

            # [ASCENSION 7]: CONTEXTUAL AURA
            # Deep magic usually doesn't happen inside comments
            if ctx.is_inside_comment:
                return self.success("Suppressed in comment", data=[])

            predictions: List[Dict[str, Any]] = []

            # 2. DISPATCH DEEP PROPHETS
            futures = {}
            for prophet in self.prophets:
                futures[self._executor.submit(self._safe_prophesy, prophet, ctx)] = prophet.name

            # [ASCENSION 9]: METABOLIC THROTTLING
            done, not_done = concurrent.futures.wait(
                futures, timeout=MAX_PROPHET_LATENCY, return_when=concurrent.futures.ALL_COMPLETED
            )

            for future in done:
                p_name = futures[future]
                try:
                    p_start = time.perf_counter_ns()
                    result = future.result()
                    p_dur = (time.perf_counter_ns() - p_start) / 1_000_000

                    if result:
                        # [ASCENSION 11]: PROVIDER ATTRIBUTION
                        for item in result:
                            if 'data' not in item: item['data'] = {}
                            item['data']['_provider'] = p_name
                            item['data']['_latency'] = p_dur
                            item['data']['_source'] = 'DAEMON_DEEP_MIND'
                        predictions.extend(result)
                except Exception as e:
                    Logger.warn(f"[{trace_id}] Deep Prophet {p_name} fractured: {e}")

            # 3. UNIFY & SUTURE
            final_vision = self._unify_vision(predictions, ctx)

            return self.success(f"Deep Prophecy: {len(final_vision)} items", data=final_vision)

        except Exception as e:
            # [ASCENSION 12]: CRASH SARCOPHAGUS
            Logger.error(f"[{trace_id}] DEEP MIND FRACTURE: {e}")
            return self.failure(str(e))

    def _safe_prophesy(self, prophet, ctx):
        try:
            return prophet.prophesy(ctx)
        except:
            return []

    def _forge_context(self, request: CompletionRequest, trace_id: str) -> Optional[ProphecyContext]:
        """
        [THE HOLOGRAPHIC FORGE]
        Reconstructs the user's reality using Metadata Truth first, Document Memory second.
        """
        content = request.content or ""
        lines = content.splitlines()

        # Coordinate Extraction
        line = 0
        char = 0
        try:
            if hasattr(request, 'position'):
                p = request.position
                line = int(getattr(p, 'line', p.get('line', 0)) if hasattr(p, 'get') else p.line)
                char = int(getattr(p, 'character', p.get('character', 0)) if hasattr(p, 'get') else p.character)
        except:
            pass

        # [ASCENSION 3]: HOLOGRAPHIC RECEPTION
        # If the LSP injected the 'current_line', we use it as absolute truth.
        # This aligns the Daemon's eye with the Client's eye.
        line_text = ""
        meta = getattr(request, 'metadata', {}) or {}
        if 'current_line' in meta and isinstance(meta['current_line'], str):
            line_text = meta['current_line']
        else:
            # Fallback to document memory (prone to race conditions)
            if line < len(lines): line_text = lines[line]

        # Clamp char
        char = min(char, len(line_text))
        line_prefix = line_text[:char]

        # [ASCENSION 4]: VIRTUAL INJECTION (FAIL-SAFE)
        # Even with the Hologram, if the trigger metadata says '$' but the line doesn't have it,
        # we force it in.
        trigger_char = getattr(request, 'trigger_character', None)
        if not trigger_char and 'trigger_character' in meta:
            trigger_char = meta['trigger_character']

        if trigger_char and not line_prefix.endswith(trigger_char):
            line_prefix += trigger_char
            char += 1  # Advance virtual cursor

        # Token Geometry
        match = TOKEN_PATTERN.search(line_prefix)
        partial = match.group(1) if match else ""
        token_start = char - len(partial)

        indent_match = re.match(r'^(\s*)', line_text)
        indent_str = indent_match.group(1) if indent_match else ""

        is_jinja = '{{' in line_prefix and '}}' not in line_prefix
        is_comment = line_prefix.strip().startswith('#')

        ext = Path(request.file_path).suffix.lower()
        lang = 'symphony' if ext == '.symphony' else 'scaffold'

        return ProphecyContext(
            uri=f"file://{request.file_path}",
            file_path=Path(request.file_path),
            project_root=Path(request.project_root or ".").resolve(),
            trace_id=trace_id,
            position={"line": line, "character": char},
            full_content=content,
            line_text=line_text,
            line_prefix=line_prefix,  # Holographic & Injected
            partial_token=partial,
            token_start_char=token_start,
            next_char=line_text[char] if char < len(line_text) else "",
            line_idx=line,
            char_idx=char,
            indent_str=indent_str,
            scope_depth=len(indent_str) // 4,
            language_id=lang,
            is_inside_jinja=is_jinja,
            is_inside_comment=is_comment,
            trigger_character=trigger_char,
            trigger_kind=getattr(request, 'trigger_kind', 1),
            alchemist=self.alchemist,
            metadata=meta
        )

    def _unify_vision(self, items: List[Dict], ctx: ProphecyContext) -> List[Dict]:
        """
        [ASCENSION 5]: GEOMETRIC SUTURE
        Ensures the replacement range covers the Virtualized Token.
        """
        unique_map = {}

        # Canonical Range: Replaces the token + sigil we detected/injected
        edit_range = {
            "start": {"line": ctx.line_idx, "character": ctx.token_start_char},
            "end": {"line": ctx.line_idx, "character": ctx.char_idx}
        }

        for item in items:
            # 1. APPLY SUTURE
            if 'textEdit' not in item:
                item['textEdit'] = {
                    "range": edit_range,
                    "newText": item.get('insertText', item['label'])
                }

            # 2. [ASCENSION 10]: FILTER TEXT ALIGNMENT
            # Ensure client filtering works even if label doesn't match token exactly
            if 'filterText' not in item:
                item['filterText'] = item['label']

            # 3. DEDUPLICATION MATRIX
            key = f"{item['label']}_{item.get('kind')}"
            if key not in unique_map:
                unique_map[key] = item

        # Sort by sortText
        return sorted(unique_map.values(), key=lambda x: x.get('sortText', x['label']))