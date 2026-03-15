# Path: core/alchemist/elara/scanner/retina/purifier.py
# -----------------------------------------------------

import unicodedata
import re

class RetinalPurifier:
    """
    =============================================================================
    == THE RETINAL PURIFIER (V-Ω-TOTALITY)                                     ==
    =============================================================================
    """
    @classmethod
    def purify(cls, text: str) -> str:
        """Exorcises BOMs, normalizes EOLs and enforces NFC."""
        text = text.lstrip('\ufeff')
        return unicodedata.normalize('NFC', text.replace('\r\n', '\n'))