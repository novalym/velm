# Path: core/alchemist/sieve/purifier.py
# --------------------------------------

import re
import math
from typing import Final


class SievePurifier:
    """
    =============================================================================
    == THE SIEVE PURIFIER (V-Ω-TOTALITY)                                       ==
    =============================================================================
    ROLE: ENTROPY_AND_ESCAPE_WARDEN

    Houses the static methods for cleaning strings, calculating Shannon Entropy,
    and un-escaping the double-brace shield.
    """

    # [ASCENSION 43]: The Double-Brace Shield
    RE_ESCAPED_BRACES: Final[re.Pattern] = re.compile(r'\\(\{\{|\}\})')

    @classmethod
    def unescape_braces(cls, text: str) -> str:
        """
        Transmutes `\\{\\{` back into `{{` after the Sieve has completed its run,
        ensuring literal UI framework bindings (Vue/Angular) are restored.
        """
        if not text: return ""
        return cls.RE_ESCAPED_BRACES.sub(r'\1', text)

    @classmethod
    def redact_entropy(cls, text: str) -> str:
        """[ASCENSION 16 & 31]: Entropy Redaction Matrix.
        Automatically masks high-entropy strings (potential secrets) if they leak
        into the template stream unexpectedly.
        """
        if not text or len(text) < 16 or " " in text:
            return text

        # Calculate Shannon Entropy
        prob =[float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])

        if entropy > 4.5:
            # It's highly random, likely a key or hash. We mask the center.
            return f"{text[:4]}...[REDACTED_BY_SIEVE]...{text[-4:]}"

        return text