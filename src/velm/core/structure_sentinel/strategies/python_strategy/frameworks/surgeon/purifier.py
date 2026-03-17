# ---------------------------------------------------------------------------------
# FILE: purifier.py
# ---------------------------------------------------------------------------------
import re
import ast
from typing import Dict, Final, List, Tuple
from .......logger import Scribe

Logger = Scribe("ApophaticPurifier")

class ApophaticPurifier:
    """
    =============================================================================
    == THE APOPHATIC PURIFIER (V-Ω-TOTALITY-VMAX-TOXIN-SIEVE)                  ==
    =============================================================================
    LIF: 10,000x | ROLE: LEXICAL_TOXIN_EXORCIST | RANK: MASTER

    [ASCENSION 7]: Employs a C-optimized translation matrix to purge terminal
    null-bytes and invisible toxins (\u200b) before the first parse strike.
    """

    TOXIN_TRANSLATE_TABLE: Final[Dict[int, None]] = {
        0xFEFF: None, 0x200B: None, 0x200C: None, 0x200D: None, 0x2060: None,
        0x0000: None, 0x0001: None, 0x0002: None, 0x0003: None
    }

    @classmethod
    def purify(cls, payload: str) -> str:
        """Vectorized Toxin Purge."""
        if not payload:
            return ""
        clean = payload.translate(cls.TOXIN_TRANSLATE_TABLE)
        clean = clean.replace('\r\n', '\n').replace('\r', '\n')
        return clean.strip()

    @classmethod
    def parse_import(cls, import_line: str) -> ast.AST | None:
        """Safely parses the import statement into an AST node."""
        clean = cls.purify(import_line)
        if not clean: return None
        try:
            return ast.parse(clean).body[0]
        except SyntaxError as e:
            Logger.critical(f"Import Inception Fracture: {clean} -> {e}")
            raise e

    @classmethod
    def parse_wiring(cls, wiring_line: str) -> List[ast.stmt]:
        """Safely parses the wiring statement into AST nodes."""
        clean = cls.purify(wiring_line)
        if not clean: return[]
        try:
            return ast.parse(clean).body
        except SyntaxError as e:
            Logger.critical(f"Wiring Inception Fracture: {clean} -> {e}")
            raise e