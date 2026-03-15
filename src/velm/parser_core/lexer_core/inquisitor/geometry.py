# Path: parser_core/lexer_core/inquisitor/geometry.py
# ---------------------------------------------------

import re
from typing import Final, Pattern

class GeometricValidator:
    """
    =============================================================================
    == THE GEOMETRIC VALIDATOR (V-Ω-TOTALITY)                                  ==
    =============================================================================
    ROLE: PATH_SCRYER
    Validates structural sigils and identifies path boundaries.
    """

    #[ASCENSION 32000]: THE SEMANTIC SUTURE
    # Added '*=' to the structural sigils list.
    STRUCTURAL_SIGILS = ("::", "<<", "+=", "^=", "~=", "*=")

    @classmethod
    def is_explicit_form(cls, raw_line: str) -> bool:
        """Returns True if the line contains a structural sigil (e.g. ::, +=, *=)."""
        return any(sig in raw_line for sig in cls.STRUCTURAL_SIGILS)

    @classmethod
    def is_sanctum(cls, raw_line: str) -> bool:
        """Returns True if the line ends with a directory slash."""
        return raw_line.endswith(('/', '\\'))