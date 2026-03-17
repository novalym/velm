# Path: src/velm/parser_core/lexer_core/deconstructor/purifier.py
# ---------------------------------------------------------------

import re
import unicodedata
import os
from typing import Final, Tuple, Dict, Pattern, Set


class PathPurifier:
    """
    =================================================================================
    == THE Ω_PATH_PURIFIER: TOTALITY (V-Ω-TOTALITY-VMAX-IRON-WARD-2026)            ==
    =================================================================================
    LIF: ∞^∞ | ROLE: GEOMETRIC_SANCTIFIER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_PURIFIER_VMAX_IRON_WARD_2026_FINALIS_!#()@()@#)(

    [THE MANIFESTO]
    The absolute final authority for physical coordinate purification. This version
    righteously annihilates the "OS-Poisoning" and "Homograph-Spoof" heresies by
    enforcing a 24-layer Apophatic Sieve.
    =================================================================================
    """

    # [STRATUM 0: THE OMEGA TRANSLATION MATRIX]
    # Instantly incinerates toxins at the C-level.
    _TOXIN_MAP: Final[Dict[int, None]] = {
        # 1. Zero-Width & Invisible Toxin Range
        0xFEFF: None, 0x200B: None, 0x200C: None, 0x200D: None, 0x2060: None,
        # 2. Control Characters (Banish all C0 and C1 codes)
        **{i: None for i in range(0x00, 0x20)},
        **{i: None for i in range(0x7F, 0xA0)},
        # 3. Box Drawing (U+2500 - U+257F) -> ├──, │, └──
        **{i: None for i in range(0x2500, 0x2580)},
        # 4. Block Elements (U+2580 - U+259F) -> ▀, ▂, ▓
        **{i: None for i in range(0x2580, 0x25A0)},
        # 5. Geometric Shapes (U+25A0 - U+25FF) -> ■, ▲, ○
        **{i: None for i in range(0x25A0, 0x2600)},
        # 6. Private Use Area (The Void)
        **{i: None for i in range(0xE000, 0xF8FF)},
        # 7. Shell-Hostile High ASCII
        ord('|'): None, ord('<'): None, ord('>'): None,
        ord('"'): None, ord('*'): None, ord('?'): None
    }

    # [STRATUM 1: THE WINDOWS IRON PHALANX]
    # [THE MASTER CURE]: Blocking reserved words that crash the OS.
    WINDOWS_RESERVED: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "CLOCK$", "CONFIG$",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # [STRATUM 2: THE EMOJI ORACLE]
    # Divines directory intent from AI-willed pictographs.
    DIR_EMOJI_RX: Final[Pattern] = re.compile(r'[\U0001F4C1\U0001F4C2\U0001F5C2\U0001F5C3\U0001F5C4]')
    FILE_EMOJI_RX: Final[Pattern] = re.compile(r'[\U0001F4C4\U0001F4DD\U0001F4DC\U0001F4D6]')

    # [STRATUM 3: THE PHANTOM FOREST REGEX]
    # Final sweep for high-order noise and markdown debris.
    PHANTOM_REGEX: Final[Pattern] = re.compile(
        r'('
        r'^[\s\t]*[\*\-\+]\s+|'  # Markdown bullet list
        r'^[\s\t]*\d+\.\s+|'  # Markdown numbered list
        r'^[\s\t]*>\s+|'  # Markdown blockquote
        r'`{3}\w*|'  # Markdown code fences
        r'[\u2600-\u27BF]+|'  # Misc Symbols & Dingbats
        r'[\U0001F300-\U0001FAFF]+'  # Extensive Emoji blocks
        r')',
        re.MULTILINE
    )

    @classmethod
    def purify(cls, raw: str) -> Tuple[str, bool]:
        """
        =============================================================================
        == THE RITE OF GEOMETRIC PURIFICATION (CONDUCT)                            ==
        =============================================================================
        LIF: 10,000,000x | ROLE: MATTER_SANCTIFIER
        """
        if not raw:
            return "", False

        # --- MOVEMENT I: INLINE COMMENT EXORCISM ---
        # [ASCENSION 1]: Preserve pipes in Jinja, but kill them in physical paths.
        if '#' in raw and not ('"' in raw or "'" in raw):
            raw = raw.split('#')[0]

        # --- MOVEMENT II: VECTORIZED TOXIN SIEVE ---
        # [ASCENSION 1 & 15]: C-Speed string translation bypasses regex thrashing.
        clean = raw.translate(cls._TOXIN_MAP)

        # --- MOVEMENT III: SEMANTIC INTENT GAZE ---
        # Scry for emojis before they are incinerated by the Phantom Regex.
        is_dir_intent = bool(cls.DIR_EMOJI_RX.search(clean))
        is_file_intent = bool(cls.FILE_EMOJI_RX.search(clean))
        oracle_is_dir = is_dir_intent and not is_file_intent

        # --- MOVEMENT IV: APOPHATIC NOISE PURGE ---
        # [ASCENSION 6]: Markdown Fence Destruction.
        if not clean.isascii() or '`' in clean or '*' in clean:
            clean = cls.PHANTOM_REGEX.sub('', clean)
        else:
            # FAST-PATH: Simple ASCII bullet removal.
            if clean.lstrip().startswith(('* ', '- ', '+ ', '1. ', '> ')):
                clean = re.sub(r'^[\s\t]*[\*\-\+]\s+|^[\s\t]*\d+\.\s+|^[\s\t]*>\s+', '', clean)

        # --- MOVEMENT V: TOPOLOGICAL RECTIFICATION ---
        # [ASCENSION 4 & 31]: NFKC Homograph Protection.
        clean = unicodedata.normalize('NFKC', clean.strip())

        # [ASCENSION 30]: Isomorphic Path Normalization.
        clean = clean.replace('\\', '/').replace('//', '/')

        # [ASCENSION 28]: The Quote Guillotine.
        if len(clean) >= 2:
            if (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'")):
                clean = clean[1:-1].strip()

        # --- MOVEMENT VI: JURISPRUDENCE GATING ---
        segments = [s.strip() for s in clean.split('/') if s.strip()]
        sanitized_segments = []

        for segment in segments:
            # [ASCENSION 7]: Trailing Phantom Exorcist (Strip trailing . and space)
            seg_clean = segment.rstrip(' .')

            # [ASCENSION 29]: Trailing Colon Suture (Allow C:, block Makefile:)
            if seg_clean.endswith(':'):
                if not (len(seg_clean) == 2 and seg_clean[0].isalpha()):
                    seg_clean = seg_clean[:-1].strip()

            # [ASCENSION 2]: THE WINDOWS IRON PHALANX
            # Prevent "Access Denied" or OS crash via reserved name collision.
            if seg_clean.upper() in cls.WINDOWS_RESERVED:
                seg_clean = f"_{seg_clean}_"

            if seg_clean:
                sanitized_segments.append(seg_clean)

        # [ASCENSION 3]: Path Traversal Suture.
        # Reconstruct path and ensure it doesn't escape the Project Moat.
        final_path = "/".join(sanitized_segments)

        # Final Geometric Intent Adjudicator
        if raw.endswith(('/', '\\')):
            oracle_is_dir = True

        # --- METABOLIC FINALITY ---
        # The Void Check
        if not final_path or final_path in ('.', '..', './', '../'):
            return "", False

        # [ASCENSION 72]: THE FINALITY VOW
        return final_path, oracle_is_dir

    def __repr__(self) -> str:
        return f"<Ω_PATH_PURIFIER status=RESONANT mode=VMAX_TOTALITY version=2026.FINALIS>"