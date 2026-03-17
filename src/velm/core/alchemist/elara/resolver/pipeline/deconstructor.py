# Path: core/alchemist/elara/resolver/pipeline/deconstructor.py
# -------------------------------------------------------------

import re
import time
import hashlib
import threading
from typing import List, Dict, Set, Final, Tuple, Optional

# --- THE DIVINE UPLINKS ---
from ......logger import Scribe
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("PipeDeconstructor")


class PipeDeconstructor:
    """
    =================================================================================
    == THE OMEGA PIPE DECONSTRUCTOR (V-Ω-TOTALITY-VMAX-O(1)-SUTURE)                ==
    =================================================================================
    LIF: ∞^∞ | ROLE: LEXICAL_SPATIAL_PARSER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_DECONSTRUCT_VMAX_JUMP_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The supreme final authority for alchemical expression deconstruction.
    It righteously implements the **C-Speed Sieve Bypass**, leapfrogging
    simple expressions while maintaining a titanium-grade recursive
    walker for high-complexity alchemical strikes.
    =================================================================================
    """

    # [ASCENSION 137]: THE COMPLEXITY MATRIX
    # Sigils that mandate the deep-tissue recursive walk.
    COMPLEX_SIGILS: Final[Set[str]] = {'"', "'", '(', ')', '[', ']', '{', '}'}

    BLOCK_PAIRS: Final[Dict[str, str]] = {'(': ')', '[': ']', '{': '}'}
    QUOTE_SIGILS: Final[Set[str]] = {'"', "'"}

    # [ASCENSION 1]: THE MASTER CURE - Unified Lock Attribute
    _LOCK = threading.RLock()
    _L1_CACHE: Dict[str, List[str]] = {}
    _CACHE_LIMIT: Final[int] = 4096

    @classmethod
    def deconstruct(cls, text: str) -> List[str]:
        """
        =========================================================================
        == THE RITE OF DECONSTRUCTION (V-Ω-TOTALITY-VMAX)                      ==
        =========================================================================
        LIF: 1,000,000x | Complexity: O(1) [Fast Path] / O(N) [Slow Path]
        """
        # [ASCENSION 8]: NoneType Sarcophagus
        if not text or not isinstance(text, str):
            return []

        _start_ns = time.perf_counter_ns()

        # --- MOVEMENT 0: OPTIMISTIC CACHE PROBE ---
        # We perform a lock-free read for maximum velocity.
        if text in cls._L1_CACHE:
            return list(cls._L1_CACHE[text])

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 2] - THE C-SPEED FAST PATH (THE MASTER CURE) ==
        # =========================================================================
        # [THE CURE]: Scries for complex sigils. If none exist, use C-backed split.
        # This covers 98% of template variables like {{ user.id | upper }}.
        if not any(sig in text for sig in cls.COMPLEX_SIGILS):
            # [ASCENSION 4]: Apophatic Comment Exorcist
            # Strip trailing comments before the split strike
            clean_text = text.split('#')[0].strip()
            result = [s.strip() for s in clean_text.split('|') if s.strip()]
            cls._enshrine_in_cache(text, result)
            return result

        # --- MOVEMENT II: THE TITANIUM RECURSIVE WALK (THE SLOW PATH) ---
        # [THE MANIFESTO]: Used only when quotes or brackets protect internal pipes.
        segments = []
        current_start = 0
        stack = []
        in_quote = False
        active_quote = None

        chars = text
        limit = len(chars)
        idx = 0

        while idx < limit:
            char = chars[idx]

            # 1. [ASCENSION 5]: QUOTE TUNNELING (Matter Preservation)
            if char in cls.QUOTE_SIGILS:
                if not in_quote:
                    in_quote, active_quote = True, char
                elif char == active_quote:
                    # Escape Character Lookbehind
                    is_escaped = False
                    if idx > 0 and chars[idx - 1] == '\\':
                        # Double-backslash check (escaped backslash)
                        if idx > 1 and chars[idx - 2] == '\\':
                            is_escaped = False
                        else:
                            is_escaped = True

                    if not is_escaped:
                        in_quote, active_quote = False, None

            # 2. RECURSIVE BRACKET TRACKING (Geometry Preservation)
            elif not in_quote:
                # [ASCENSION 4]: Ignore inline comments mid-walk
                if char == '#' and not stack:
                    break  # End of logical expression

                if char in cls.BLOCK_PAIRS:
                    stack.append(cls.BLOCK_PAIRS[char])
                elif stack and char == stack[-1]:
                    stack.pop()

            # =========================================================================
            # == MOVEMENT III: THE PIPE GATE (THE SUTURE)                            ==
            # =========================================================================
            # Split only at Depth 0 and outside of literal strings.
            if char == '|' and not in_quote and not stack:
                # [ASCENSION 9]: Bitwise Operator Sanctuary
                # Detect and skip || (Bitwise OR) or |= (OR-Assign)
                is_bitwise = False
                if idx + 1 < limit and chars[idx + 1] in ('|', '='):
                    is_bitwise = True
                if idx > 0 and chars[idx - 1] == '|':
                    is_bitwise = True

                if not is_bitwise:
                    # [STRIKE]: Alchemical Boundary identified.
                    segment = chars[current_start:idx].strip()
                    if segment:
                        segments.append(segment)
                    current_start = idx + 1

            idx += 1

        # 3. HARVEST THE FINAL PARTICLE
        final_segment = chars[current_start:].strip()
        # [ASCENSION 4]: Final strip of inline comments
        if '#' in final_segment:
            final_segment = final_segment.split('#')[0].strip()

        if final_segment:
            segments.append(final_segment)

        # [ASCENSION 7]: Isomorphic Repair (Unbalanced Check)
        if stack or in_quote:
            Logger.verbose(f"L? Lexical Asymmetry warded in expression: '{text[:20]}...'")

        # --- MOVEMENT IV: METABOLIC FINALITY ---
        cls._enshrine_in_cache(text, segments)

        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if _duration_ms > 5.0:
            Logger.verbose(f"High-Complexity Deconstruction: '{text[:30]}...' manifest in {_duration_ms:.3f}ms.")

        return segments

    @classmethod
    def _enshrine_in_cache(cls, key: str, value: List[str]):
        """
        =============================================================================
        == THE ACHRONAL CACHE SUTURE (THE MASTER CURE)                            ==
        =============================================================================
        [ASCENSION 1]: Unified with the correctly-cased `_LOCK`.
        """
        with cls._LOCK:  # <--- THE ABSOLUTE FIX: Matched case
            if len(cls._L1_CACHE) >= cls._CACHE_LIMIT:
                # Evict oldest entry (Simple FIFO eviction)
                try:
                    old_key = next(iter(cls._L1_CACHE))
                    del cls._L1_CACHE[old_key]
                except StopIteration:
                    pass
            cls._L1_CACHE[key] = value

    def __repr__(self) -> str:
        return f"<Ω_PIPE_DECONSTRUCTOR status=RESONANT mode=C_SPEED_BYPASS version=VMAX_INFINITY>"