# Path: src/velm/parser_core/lexer_core/deconstructor/purifier.py
# ---------------------------------------------------------------

import re
import unicodedata
from typing import Final, Tuple, Dict, Pattern


class PathPurifier:
    """
    =============================================================================
    == THE PATH PURIFIER (V-Ω-TOTALITY-VMAX-C-SPEED-MATRIX)                    ==
    =============================================================================
    LIF: 10,000,000x | ROLE: GEOMETRIC_CLEANSER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_PURIFIER_VMAX_C_MATRIX_ANNIHILATOR_2026_FINALIS

    [THE MASTER CURE: THE UNIVERSAL TRANSLATION MATRIX]
    Bypasses `re.sub` entirely for zero-width characters, control codes, and
    box-drawing elements. It utilizes Python's native C-backed `str.translate`
    for instantaneous, O(N) single-pass purification.

    It mathematically deletes the entire Phantom Forest (Tree-Art, Emojis,
    and Markdown Lists) without consuming CPU cycles.
    """

    # =========================================================================
    # == [ASCENSION 48]: THE OMEGA TRANSLATION MATRIX (O(1) C-LEVEL CURE)    ==
    # =========================================================================
    # Instantly maps toxins to None (Deletion) at the C-level during module load.
    _TOXIN_MAP: Final[Dict[int, None]] = {
        # Zero-Width & BOM
        0xFEFF: None, 0x200B: None, 0x200C: None, 0x200D: None, 0x2060: None,
        # Control Characters (C0 and C1)
        **{i: None for i in range(0x00, 0x20)},
        **{i: None for i in range(0x7F, 0xA0)},
        # Box Drawing (U+2500 - U+257F)  -> ├──, │, └──, ┐, ┬
        **{i: None for i in range(0x2500, 0x2580)},
        # Block Elements (U+2580 - U+259F) -> ▀, ▂, ▓
        **{i: None for i in range(0x2580, 0x25A0)},
        # Geometric Shapes (U+25A0 - U+25FF) -> ■, ▲, ○
        **{i: None for i in range(0x25A0, 0x2600)},
        # Dingbats (U+2700 - U+27BF) -> ✂, ✆, ✏
        **{i: None for i in range(0x2700, 0x27C0)},
    }

    # [FACULTY 1]: THE EMOJI ORACLE PATTERNS (Survives translation for semantic detection)
    DIR_EMOJI_REGEX: Final[Pattern] = re.compile(r'[\U0001F4C1\U0001F4C2\U0001F5C2]')
    FILE_EMOJI_REGEX: Final[Pattern] = re.compile(r'[\U0001F4C4\U0001F4DD\U0001F4DC\U0001F5C3]')

    # Markdown Artifacts (Lists, Quotes) and remaining high-plane emojis
    PHANTOM_REGEX: Final[Pattern] = re.compile(
        r'('
        r'^[\s\t]*[\*\-\+]\s+|'  # Markdown lists (*, -, +)
        r'^[\s\t]*\d+\.\s+|'  # Markdown numbered lists (1., 2.)
        r'^[\s\t]*>\s+|'  # Markdown blockquotes
        r'[\u2600-\u26FF]+|'  # Misc Symbols (⚙️, ⚡)
        r'[\U0001F300-\U0001FAFF]+'  # Vast Emoji/Pictograph range
        r')'
    )

    @classmethod
    def purify(cls, raw: str) -> Tuple[str, bool]:
        """
        =========================================================================
        == THE RITE OF PURIFICATION (V-Ω-ASCII-FAST-PATH)                      ==
        =========================================================================
        """
        if not raw:
            return "", False

        # 1. THE INLINE COMMENT ANNIHILATOR
        if '#' in raw and not ('"' in raw or "'" in raw):
            raw = raw.split('#')[0]

        oracle_is_dir = False
        clean = raw

        # =========================================================================
        # == [THE MASTER CURE]: THE ASCII FAST-PATH BYPASS                       ==
        # =========================================================================
        # The Regex Engine is heavy. Emojis and Box Drawing characters exist in less
        # than 1% of paths. If the string is purely ASCII, we bypass the heavy regex!
        if not raw.isascii():
            # [ASCENSION 48]: C-SPEED TRANSLATION
            # Instantly destroys all Box Drawing, Control Chars, and Zero-Widths.
            clean = clean.translate(cls._TOXIN_MAP)

            # Scry for emojis before deleting them
            is_dir_intent = bool(cls.DIR_EMOJI_REGEX.search(clean))
            is_file_intent = bool(cls.FILE_EMOJI_REGEX.search(clean))
            oracle_is_dir = is_dir_intent and not is_file_intent

            # [ASCENSION 27]: Only run the phantom regex for Markdown & Emojis
            clean = cls.PHANTOM_REGEX.sub('', clean)
        else:
            # FAST PATH: We still need to strip markdown lists which are ASCII
            if raw.lstrip().startswith(('* ', '- ', '+ ', '1. ', '> ')):
                clean = re.sub(r'^[\s\t]*[\*\-\+]\s+|^[\s\t]*\d+\.\s+|^[\s\t]*>\s+', '', raw)

        clean = clean.strip()

        # [ASCENSION 28]: THE QUOTE GUILLOTINE
        if len(clean) >= 2 and (
                (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'"))):
            clean = clean[1:-1].strip()

        # [ASCENSION 29]: TRAILING COLON SUTURE
        if clean.endswith(':'):
            if not (len(clean) == 2 and clean[0].isalpha()):
                clean = clean[:-1].strip()

        # [ASCENSION 30]: O(1) SLASH NORMALIZATION
        clean = clean.replace('\\', '/')
        if '//' in clean:
            # Native split/join is significantly faster than regex for multi-slashes
            clean = '/'.join(filter(None, clean.split('/')))

        # [ASCENSION 31]: NFC NORMALIZATION
        clean = unicodedata.normalize('NFC', clean)

        # The Void Check
        if clean in ('.', './', '.\\', ''):
            return "", False

        return clean, oracle_is_dir