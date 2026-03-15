# Path: core/alchemist/elara/resolver/pipeline/deconstructor.py
# -------------------------------------------------------------

from typing import List, Dict, Set, Final


class PipeDeconstructor:
    """
    =============================================================================
    == THE RECURSIVE PIPE SIEVE (V-Ω-TOTALITY)                                 ==
    =============================================================================
    LIF: 10,000x | ROLE: SPATIAL_PARSER | RANK: MASTER[ASCENSION 97 & 136]: High-order walker that protects pipes inside brackets.
    It operates with O(N) complexity and zero external dependencies.
    """

    BLOCK_PAIRS: Final[Dict[str, str]] = {'(': ')', '[': ']', '{': '}'}
    QUOTE_SIGILS: Final[Set[str]] = {'"', "'"}

    @classmethod
    def deconstruct(cls, text: str) -> List[str]:
        """Safely splits a Gnostic string by '|' while protecting nested structures."""
        segments = []
        current = []
        stack = []
        in_quote = False
        active_quote = None

        chars = list(text)
        i = 0
        limit = len(chars)

        while i < limit:
            char = chars[i]

            # 1. QUOTE TUNNELING
            if char in cls.QUOTE_SIGILS:
                if not in_quote:
                    in_quote, active_quote = True, char
                elif char == active_quote:
                    # Forensic Escape Check
                    if i > 0 and chars[i - 1] == '\\':
                        if i > 1 and chars[i - 2] == '\\':
                            in_quote, active_quote = False, None
                    else:
                        in_quote, active_quote = False, None

            # 2. RECURSIVE BRACKET TRACKING
            elif not in_quote:
                if char in cls.BLOCK_PAIRS:
                    stack.append(cls.BLOCK_PAIRS[char])
                elif stack and char == stack[-1]:
                    stack.pop()

            # 3. THE PIPE GATE (THE SUTURE)
            if char == '|' and not in_quote and not stack:
                # Shield against bitwise OR '||' or '|='
                if i + 1 < limit and chars[i + 1] in ('|', '='):
                    current.append(char)
                else:
                    segments.append("".join(current).strip())
                    current = []
            else:
                current.append(char)

            i += 1

        if current:
            segments.append("".join(current).strip())

        return segments