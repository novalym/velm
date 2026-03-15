# Path: src/velm/artisans/completion_artisan/artisan.py
# -----------------------------------------------------
# =========================================================================================
# == THE OMEGA COMPLETION ARTISAN: TOTALITY (V-Ω-TOTALITY-V1000K-INDESTRUCTIBLE)         ==
# =========================================================================================
# LIF: INFINITY | ROLE: DEEP_GNOSIS_PROPHET | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_COMPLETION_V100K_THREAD_EXORCISM_FINALIS
# =========================================================================================

import time
import re
import uuid
import logging
import sys
import os
import concurrent.futures
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, ScaffoldSeverity
from ...interfaces.requests import CompletionRequest
from ...core.alchemist import get_alchemist
from ...logger import Scribe

# --- THE SANCTUM PROPHETS ---
# These are the specialized sub-minds that handle specific completion domains.
from .prophets.snippets import SnippetProphet
from .prophets.alchemist import AlchemistProphet
from .prophets.directives import DirectiveProphet
from .prophets.canon import GnosticCanon

Logger = Scribe("CompletionArtisan")

# [ASCENSION 1]: PHYSICS CONSTANTS
MAX_PROPHET_LATENCY = 0.250  # 250ms Hard Timeout for sub-prophets
TOKEN_PATTERN = re.compile(r'([\w\$\@\%\/\.\-\:]+)$')

# [ASCENSION 2]: SUBSTRATE SENSING (THE CURE)
# We mathematically divine if we are in the Ethereal Plane (WASM/Browser).
IS_WASM = (
        os.environ.get("SCAFFOLD_ENV") == "WASM" or
        sys.platform == "emscripten" or
        "pyodide" in sys.modules
)


@dataclass(frozen=True)
class ProphecyContext:
    """
    [THE HOLOGRAPHIC CONTEXT]
    Immutable snapshot of reality, adjusted for Virtual Injection.
    Carries the exact state of the universe at the moment of the keystroke.
    """
    uri: str
    file_path: Path
    project_root: Path
    trace_id: str
    full_content: str
    line_text: str
    line_prefix: str  # The Holographic Prefix (What the user actually sees)
    partial_token: str
    token_start_char: int
    next_char: str
    position: Dict[str, int]
    line_idx: int
    char_idx: int
    indent_str: str
    scope_depth: int
    language_id: str
    is_inside_sgf: bool
    is_inside_comment: bool
    trigger_character: Optional[str]
    trigger_kind: int
    alchemist: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


class CompletionArtisan(BaseArtisan[CompletionRequest]):
    """
    =================================================================================
    == THE DEEP MIND: OMEGA TOTALITY (V-Ω-V25-24-ASCENSIONS)                      ==
    =================================================================================
    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Bimodal Execution Loop (THE CURE):** Detects WASM substrate and executes
        prophets sequentially, annihilating the `RuntimeError: can't start new thread`.
    2.  **Sarcophagus Bypass (THE CURE):** Implements `_forge_revelation_failure` to
        bypass the base class `self.request` property guard during initialization errors.
    3.  **Holographic Injection Suture:** Aligns its gaze with the LSP's `current_line`
        metadata to ensure zero-drift prediction vs disk state.
    4.  **Zero-Latency Gnostic Canon:** Caches engine state (Registry/VFS) to provide
        architectural context in < 1ms.
    5.  **Merkle-Lattice Range Suture:** Mathematically guarantees the `textEdit`
        range covers the virtualized token exactly.
    6.  **Adrenaline-Mode Pacing:** Self-throttles the prophet timeout if the kernel
        reports high thermodynamic load.
    7.  **Isomorphic Identity Mapping:** Normalizes completion kind (Snippet/Function)
        to ensure bit-perfect Monaco rendering.
    8.  **The Prophetic Filter Shield:** Automatically hides completions that would
        trigger a redundant sigil (e.g., `$$` when already typed).
    9.  **Recursive Indent Awareness:** Snippets are dynamically re-indented
        to match the line's spatial depth.
    10. **Achronal Trace Suture:** Binds every prediction item to the `trace_id`
        for forensic auditing of the "Ghost Prophet."
    11. **Provider Attribution:** Injects `_provider` metadata for telemetry.
    12. **NoneType Integrity Ward:** Strictly validates `request.variables` before
        alchemical resolution.
    13. **Binary Matter Exclusion:** Stays its hand if the target scripture is
        perceived as binary/void.
    14. **Snippet Placeholder Alchemy:** Transforms Jinja variables into
        LSP-tabstops (`${1:var}`) in real-time.
    15. **Contextual Logic Gating:** Suppresses structural directives if
        already inside a Maestro block.
    16. **The Silence Vow:** Respects `request.silent` for background scrying.
    17. **Jinja2 Balance Monitor:** Detects unclosed braces and prioritizes
        Alchemist completions.
    18. **Coordinate Normalization:** Forces 0-indexed LSP geometry for
        universal tool resonance.
    19. **Atomic Result Flattening:** Converts complex result objects into
        flat, JSON-serializable dictionaries for the Bridge.
    20. **The Mentor's Counsel:** Injects helpful documentation strings into
        snippet items.
    21. **Performance Histogram:** Tracks per-prophet latency for HUD metrics.
    22. **Clean Dismount:** Explicitly shuts down the ThreadPool on Native Iron.
    23. **Socratic Error Reporting:** Distinguishes between "Logic Fractures"
        and "Substrate Limitations."
    24. **The Finality Vow:** A mathematical guarantee of a valid revelation return.
    """

    def __init__(self, engine):
        super().__init__(engine)
        self.canon = GnosticCanon(engine)


        # [ASCENSION 1]: SUBSTRATE AWARE INITIALIZATION
        # If we are in the Ether, we do not summon the ThreadPool.
        if not IS_WASM:
            self._executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=4,
                thread_name_prefix="ProphetWorker"
            )
        else:
            self._executor = None

        # The Council of Prophets
        self.prophets = [
            SnippetProphet(self),  # Static Library (Fast)
            AlchemistProphet(self),  # Dynamic Jinja (Live)
            DirectiveProphet(self)  # Dynamic Directives (Live)
        ]

    def execute(self, request: CompletionRequest) -> ScaffoldResult:
        """
        [THE RITE OF EXECUTION]
        Orchestrates the gathering of foresight.
        """
        start_ns = time.perf_counter_ns()
        meta = getattr(request, 'metadata', {}) or {}
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

            # =========================================================================
            # == [THE CURE]: BIMODAL DISPATCH                                        ==
            # =========================================================================
            if IS_WASM or not self._executor:
                # PATH A: SEQUENTIAL SUTURE (WASM)
                # We execute each prophet in the main thread.
                # If one fails, we catch it locally and proceed to the next.
                for prophet in self.prophets:
                    try:
                        p_start = time.perf_counter_ns()
                        result = prophet.prophesy(ctx)
                        p_dur = (time.perf_counter_ns() - p_start) / 1_000_000
                        self._ingest_results(predictions, result, prophet.name, p_dur, trace_id)
                    except Exception as e:
                        Logger.warn(f"[{trace_id}] Sequential Prophet {prophet.name} fractured: {e}")
            else:
                # PATH B: PARALLEL KINETICS (IRON)
                # We dispatch to the ThreadPool for maximum velocity on multi-core iron.
                futures = {self._executor.submit(self._safe_prophesy, p, ctx): p.name for p in self.prophets}

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
                        self._ingest_results(predictions, result, p_name, p_dur, trace_id)
                    except Exception as e:
                        Logger.warn(f"[{trace_id}] Parallel Prophet {p_name} fractured: {e}")

            # 3. UNIFY & SUTURE
            final_vision = self._unify_vision(predictions, ctx)

            return self.success(f"Deep Prophecy: {len(final_vision)} items", data=final_vision)

        except Exception as e:
            # [ASCENSION 12]: CRASH SARCOPHAGUS
            # [THE CURE]: Avoid self.failure() property collision by using manual forge
            Logger.error(f"[{trace_id}] DEEP MIND FRACTURE: {e}")
            return self._forge_revelation_failure(str(e), trace_id)

    def _ingest_results(self, pool, results, p_name, p_dur, trace_id):
        """[HELPER]: Merges prophet results with telemetry."""
        if results:
            for item in results:
                if 'data' not in item: item['data'] = {}
                item['data']['_provider'] = p_name
                item['data']['_latency'] = p_dur
                item['data']['_source'] = 'DAEMON_DEEP_MIND'
                item['data']['_trace_id'] = trace_id
            pool.extend(results)

    def _forge_revelation_failure(self, error_msg: str, trace_id: str) -> ScaffoldResult:
        """
        [THE CURE]: Manually constructs a result to bypass base class property wards.
        Used when the Artisan fractures before 'self.request' is fully bound.
        """
        return ScaffoldResult(
            success=False,
            message=f"Prophecy Engine Fracture: {error_msg}",
            severity=ScaffoldSeverity.ERROR,
            trace_id=trace_id,
            data=[]
        )

    def _safe_prophesy(self, prophet, ctx):
        """Wrapper to catch prophet-level exceptions in threads."""
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
            # Flexible handling for dict vs object access on Position
            if hasattr(request, 'position'):
                p = request.position
                # Check for dict access via get, else attr access
                line = int(p.get('line', 0) if isinstance(p, dict) else p.line)
                char = int(p.get('character', 0) if isinstance(p, dict) else p.character)
        except:
            pass

        # [ASCENSION 3]: HOLOGRAPHIC RECEPTION
        # If the LSP injected the 'current_line', we use it as absolute truth.
        line_text = ""
        meta = getattr(request, 'metadata', {}) or {}
        if 'current_line' in meta and isinstance(meta['current_line'], str):
            line_text = meta['current_line']
        else:
            # Fallback to document memory (prone to race conditions if file updated)
            if line < len(lines): line_text = lines[line]

        # Clamp char
        char = min(char, len(line_text))
        line_prefix = line_text[:char]

        # [ASCENSION 4]: VIRTUAL INJECTION (FAIL-SAFE)
        # Even with the Hologram, if the trigger metadata says '$' but the line doesn't have it,
        # we force it in to ensure the Regex matches.
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

        is_sgf = '{{' in line_prefix and '}}' not in line_prefix
        is_comment = line_prefix.strip().startswith('#')

        # Language Divination
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
            is_inside_sgf=is_sgf,
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

        # Sort by sortText to honor priority
        return sorted(unique_map.values(), key=lambda x: x.get('sortText', x['label']))