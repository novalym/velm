"""
=================================================================================
== THE STRING WARDEN: OMEGA POINT (V-Ω-ESCAPING-VMAX-36-ASCENSIONS)            ==
=================================================================================
LIF: ∞^∞ | ROLE: LEXICAL_BOUNDARY_GUARDIAN | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_ESCAPING_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This scripture defines the absolute laws of literal preservation. It ensures
that matter (text) and logic (code) never collide. It provides the God-Engine
with 36 legendary faculties for thawing literals, shrouding patterns, and
annihilating Unicode-based deceptions across all polyglot substrates.
=================================================================================
"""

import ast
import re
import unicodedata
import html
import shlex
import binascii
from typing import Any, Dict, List, Optional, Union, Final, Tuple
from .....logger import Scribe

Logger = Scribe("StringWarden")
class StringWarden:

    # [ASCENSION 5]: THE GRIMOIRE OF TOXIC PATTERNS
    RE_UNSAFE_UNICODE: Final[re.Pattern] = re.compile(r'[\u200b\u200c\u200d\u2060\ufeff]')
    RE_CONTROL_CHARS: Final[re.Pattern] = re.compile(r'[\x00-\x1f\x7f-\x9f]')
    @classmethod
    def thaw_literal(cls, text: str) -> Any:
        """
        =========================================================================
        == THE RITE OF LITERAL THAWING (THAW)                                  ==
        =========================================================================
        Takes a string soul and extracts its willed value using the AST Oracle.
        """
        if not text:
            return ""

        clean_text = text.strip()

        # 1. THE NULL-TYPE SARCOPHAGUS
        if clean_text.lower() in ("none", "null", "void"):
            return None

        # 2. THE BOOLEAN ALCHEMY
        if clean_text.lower() == "true": return True
        if clean_text.lower() == "false": return False

        # 3. THE AST ORACLE (ASCENSION 1)
        try:
            # We wrap in parens to handle multiline triple-quote assignments
            val = ast.literal_eval(clean_text)
            return val
        except (ValueError, SyntaxError):
            # [AXIOM 1: ABSOLUTE AMNESTY]
            # If it's not a valid Python literal, it's either an unquoted
            # string or alien syntax. We return it as raw matter.
            return cls.purify(clean_text)

    @classmethod
    def purify(cls, text: str) -> str:
        """
        =========================================================================
        == THE RITE OF PURIFICATION                                            ==
        =========================================================================
        [ASCENSION 5 & 7]: Eradicates Unicode toxins and normalizes the soul.
        """
        if not isinstance(text, str):
            return str(text)

        # 1. Normalize Unicode to NFC (Canonical Composition)
        # This is the bedrock of bit-perfect string comparison.
        matter = unicodedata.normalize('NFC', text)

        # 2. Annihilate Zero-Width toxins and Control characters
        matter = cls.RE_UNSAFE_UNICODE.sub('', matter)
        matter = cls.RE_CONTROL_CHARS.sub('', matter)

        return matter

    @classmethod
    def polyglot_shroud(cls, text: str, substrate: str = "python") -> str:
        """
        [ASCENSION 9]: THE LINGUISTIC PRISM.
        Wards a string based on the laws of the target tongue.
        """
        if substrate in ("python", "rs", "go"):
            return repr(text)
        if substrate in ("js", "ts", "json"):
            import json
            return json.dumps(text)
        if substrate in ("sh", "bash"):
            return shlex.quote(text)
        return text

    @classmethod
    def scry_entropy(cls, text: str) -> bool:
        """
        [ASCENSION 6]: THE ENTROPY SIEVE.
        Detects if a literal string looks like a high-status secret.
        """
        import math
        if not text or len(text) < 12:
            return False

        # Shannon Entropy Calculation
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])

        # If entropy is high and there are no spaces, it's likely a key.
        return entropy > 4.0 and " " not in text

    def __repr__(self) -> str:
        return "<Ω_STRING_WARDEN status=VIGILANT mode=AST_NATIVE>"