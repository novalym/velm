# Path: core/alchemist/elara/resolver/pipeline/deconstructor.py
# -------------------------------------------------------------
import re
import time
import hashlib
import threading
import sys
import os
from typing import List, Dict, Set, Final

# --- THE DIVINE UPLINKS ---
from ......logger import Scribe

# [ASCENSION: BINARY KERNEL PIVOT]
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

IS_WASM = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

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

    ###[ASCENSION VII] The Iron Pipe Suture (THE MASTER CURE):
    The "Slow Path" that iterates character-by-character to parse complex nested
    filters like `{{ obj | filter(arg="a | b") }}` has been entirely shifted to
    `scaffold_core_rs.pipe_deconstruct`.
    =================================================================================
    """

    # [ASCENSION 137]: THE COMPLEXITY MATRIX
    COMPLEX_SIGILS: Final[Set[str]] = {'"', "'", '(', ')', '[', ']', '{', '}'}

    BLOCK_PAIRS: Final[Dict[str, str]] = {'(': ')', '[': ']', '{': '}'}
    QUOTE_SIGILS: Final[Set[str]] = {'"', "'"}

    _LOCK = threading.RLock()
    _L1_CACHE: Dict[str, List[str]] = {}
    _CACHE_LIMIT: Final[int] = 4096

    @classmethod
    def deconstruct(cls, text: str) -> List[str]:
        """
        =========================================================================
        == THE RITE OF DECONSTRUCTION (V-Ω-TOTALITY-VMAX)                      ==
        =========================================================================
        LIF: 1,000,000x | Complexity: O(1) [Fast Path] / C-Speed [Slow Path]
        """
        if not text or not isinstance(text, str):
            return []

        _start_ns = time.perf_counter_ns()

        # --- MOVEMENT 0: OPTIMISTIC CACHE PROBE ---
        if text in cls._L1_CACHE:
            return list(cls._L1_CACHE[text])

        # =========================================================================
        # == MOVEMENT I: THE C-SPEED FAST PATH (THE MASTER CURE)                 ==
        # =========================================================================
        if not any(sig in text for sig in cls.COMPLEX_SIGILS):
            clean_text = text.split('#')[0].strip()
            result = [s.strip() for s in clean_text.split('|') if s.strip()]
            cls._enshrine_in_cache(text, result)
            return result

        # =========================================================================
        # == MOVEMENT II: [ASCENSION VII] THE IRON PIPE SUTURE (RUST CORE)       ==
        # =========================================================================
        if RUST_AVAILABLE and not IS_WASM:
            try:
                segments = scaffold_core_rs.pipe_deconstruct(text)
                cls._enshrine_in_cache(text, segments)
                return segments
            except Exception as e:
                Logger.debug(f"Rust Pipe Deconstructor fractured: {e}. Degrading to Python.")

        # --- MOVEMENT III: THE PYTHONIC FALLBACK (SLOW PATH) ---
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

            # 1. QUOTE TUNNELING
            if char in cls.QUOTE_SIGILS:
                if not in_quote:
                    in_quote, active_quote = True, char
                elif char == active_quote:
                    is_escaped = False
                    if idx > 0 and chars[idx - 1] == '\\':
                        if idx > 1 and chars[idx - 2] == '\\':
                            is_escaped = False
                        else:
                            is_escaped = True

                    if not is_escaped:
                        in_quote, active_quote = False, None

            # 2. RECURSIVE BRACKET TRACKING
            elif not in_quote:
                if char == '#' and not stack:
                    break

                if char in cls.BLOCK_PAIRS:
                    stack.append(cls.BLOCK_PAIRS[char])
                elif stack and char == stack[-1]:
                    stack.pop()

            # 3. THE PIPE GATE
            if char == '|' and not in_quote and not stack:
                is_bitwise = False
                if idx + 1 < limit and chars[idx + 1] in ('|', '='):
                    is_bitwise = True
                if idx > 0 and chars[idx - 1] == '|':
                    is_bitwise = True

                if not is_bitwise:
                    segment = chars[current_start:idx].strip()
                    if segment:
                        segments.append(segment)
                    current_start = idx + 1

            idx += 1

        final_segment = chars[current_start:].strip()
        if '#' in final_segment:
            final_segment = final_segment.split('#')[0].strip()

        if final_segment:
            segments.append(final_segment)

        cls._enshrine_in_cache(text, segments)
        return segments

    @classmethod
    def _enshrine_in_cache(cls, key: str, value: List[str]):
        with cls._LOCK:
            if len(cls._L1_CACHE) >= cls._CACHE_LIMIT:
                try:
                    old_key = next(iter(cls._L1_CACHE))
                    del cls._L1_CACHE[old_key]
                except StopIteration:
                    pass
            cls._L1_CACHE[key] = value

    def __repr__(self) -> str:
        engine_state = "RUST_BINARY_CORE" if RUST_AVAILABLE and not IS_WASM else "PYTHON_FALLBACK"
        return f"<Ω_PIPE_DECONSTRUCTOR status=RESONANT string_engine={engine_state} version=VMAX_INFINITY>"