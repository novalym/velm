# Path: parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe/identity.py
# --------------------------------------------------------------------------------------


import re
import os
import threading
import time
import hashlib
import unicodedata
from typing import List, Tuple, Any, Final, Set, Dict, Optional
from pathlib import Path

# --- CORE UPLINKS ---
from ......contracts.data_contracts import GnosticVessel
from ......logger import Scribe

Logger = Scribe("OntologicalIdentity:Apotheosis")


class OntologicalIdentity:
    """
    =================================================================================
    == THE ONTOLOGICAL IDENTITY ORACLE (V-Ω-TOTALITY-VMAX-73-ASCENSIONS)           ==
    =================================================================================
    LIF: ∞^∞ | ROLE: GEOMETRIC_FORM_CLASSIFIER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: !#()_IDENTITY_VMAX_SOVEREIGN_FILES_FINALIS

    The supreme arbiter of physical existence within the God-Engine. It makes the
    Final Decree: Is this atom a File (Scripture) or a Directory (Sanctum)?

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (49-73):
    49.  **The Law of the Trailing Colon (THE MASTER CURE):** Mathematically forces
         `is_dir=False` if an explicit colon (:) exists, annihilating the
         Makefile-directory hallucination for all time.
    73.  **Sovereign File Recognition (THE MASTER CURE):** Enshrines extension-less
         files (`Makefile`, `Dockerfile`, `.gitignore`) natively, preventing them
         from being misidentified as Directories if they house indented recipes.
    =================================================================================
    """

    __slots__ = ('_lock', '_identity_cache', '_trace_id')

    # [ASCENSION 61]: THE EXTENSION SOVEREIGNTY ORACLE (O(1) Matrix)
    EXTENSION_LATTICE: Final[Set[str]] = {
        'py', 'js', 'ts', 'tsx', 'jsx', 'css', 'scss', 'less', 'html', 'htm', 'json',
        'md', 'markdown', 'yaml', 'yml', 'toml', 'ini', 'cfg', 'conf', 'sh', 'bash',
        'zsh', 'fish', 'go', 'rs', 'c', 'cpp', 'h', 'hpp', 'java', 'kt', 'kts', 'rb',
        'php', 'pl', 'lua', 'zig', 'arch', 'symphony', 'scaffold', 'lock', 'env',
        'txt', 'xml', 'svg', 'png', 'jpg', 'jpeg', 'gif', 'ico', 'pdf', 'zip', 'gz',
        'tar', 'rar', '7z', 'sql', 'dockerignore', 'gitignore', 'editorconfig',
        'eslintrc', 'prettierrc', 'dockerfile', 'makefile', 'gemfile', 'rakefile'
    }

    # [ASCENSION 73]: SOVEREIGN FILE RECOGNITION
    SOVEREIGN_FILES: Final[Set[str]] = {
        'makefile', 'dockerfile', 'caddyfile', 'gemfile', 'rakefile', 'procfile',
        '.gitignore', '.dockerignore', '.env', '.env.example', 'cmakelists.txt', 'license'
    }

    #[ASCENSION 54]: THE WINDOWS IRON PHALANX
    WINDOWS_RESERVED: Final[Set[str]] = {
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5",
        "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
        "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # [ASCENSION 51]: EMOJI SEMANTIC RADIANCE
    RE_SANCTUM_EMOJI: Final[re.Pattern] = re.compile(r'[\U0001F4C1\U0001F4C2\U0001F5C2]')
    RE_SCRIPTURE_EMOJI: Final[re.Pattern] = re.compile(r'[\U0001F4C4\U0001F4DD\U0001F4DC]')

    # [ASCENSION 62]: EXPLICIT SIGIL ANCHORS
    RAW_BLOCK_START_REGEX: Final[re.Pattern] = re.compile(r'(::|:?\s*=|\+=|\^=|~=|<<)\s*("""|\'\'\')')
    SGF_VAR_REGEX: Final[re.Pattern] = re.compile(r'\{\{.*?\}\}')

    def __init__(self, trace_id: str = "tr-identity-void"):
        """[THE RITE OF INCEPTION]"""
        self._lock = threading.RLock()
        self._identity_cache: Dict[str, bool] = {}
        self._trace_id = trace_id

    @classmethod
    def check_explicit_lock(cls, vessel: GnosticVessel) -> Tuple[bool, str]:
        """
        =============================================================================
        == THE EXPLICIT LOCK RITE (V-Ω-TOTALITY)                                   ==
        =============================================================================
        [ASCENSION 62]: Adjudicates if the line is forced into being a Scripture via
        explicit alchemical sigils.
        """
        # --- MOVEMENT I: PURIFICATION ---
        # Exorcise comments to find the pure kinetic intent
        raw_no_comment = vessel.raw_scripture.split('#')[0].split('//')[0].strip()

        # --- MOVEMENT II: SIGIL INQUEST ---
        # 1. Delimiter Logic
        if vessel.content and ('"""' in str(vessel.content) or "'''" in str(vessel.content)):
            return True, "Lock: Delimiter Detected"

        # 2. Block Start Logic
        if cls.RAW_BLOCK_START_REGEX.search(vessel.raw_scripture):
            # We enforce triple-quote mode on the vessel
            vessel.content = '"""' if '"""' in vessel.raw_scripture else "'''"
            return True, "Lock: Regex Scry Match"

        # 3. Inline Assignment Logic (::, +=, <<, etc.)
        if vessel.content or vessel.seed_path or vessel.mutation_op:
            return True, "Lock: Inline Sigil Perceived"

        return False, ""

    @classmethod
    def divine_form(cls, vessel: GnosticVessel, pure_name: str, lines: List[str], i: int, parser: Any) -> str:
        """
        =============================================================================
        == THE SUPREME DECREE OF FORM (V-Ω-TOTALITY-VMAX-73)                       ==
        =============================================================================
        LIF: ∞ | ROLE: ONTOLOGICAL_ADJUDICATOR
        """
        # --- MOVEMENT 0: THE VOID GUARD ---
        if not pure_name:
            vessel.is_dir = False
            return "Decree: Void Nullification"

        #[ASCENSION 60]: Linguistic Purity Suture
        # Normalize Unicode and exorcise zero-width toxins
        clean_name = unicodedata.normalize('NFC', pure_name)
        clean_name = clean_name.replace('\u200b', '').replace('\ufeff', '').strip()

        # [ASCENSION 69]: Trailing Phantom Exorcist
        # Strip trailing dots and spaces that fracture Windows Iron
        test_name = clean_name.rstrip(' .')
        if test_name.endswith(':'):
            test_name = test_name[:-1].strip()
        test_name = test_name.strip('"\'')

        # --- MOVEMENT I: [ASCENSION 53] - ACHRONAL STATE-LOCK ---
        path_key = test_name.lower().replace('\\', '/')
        if path_key in getattr(parser, '_identity_cache', {}):
            is_dir = parser._identity_cache[path_key]
            vessel.is_dir = is_dir
            return f"Decree: Achronal Memory Recall ({'Dir' if is_dir else 'File'})"

        # --- MOVEMENT II: THE SENSORY GAZE (EMOJI & SIGILS) ---
        # [ASCENSION 51]: Emoji Semantic Gaze
        has_dir_emoji = bool(cls.RE_SANCTUM_EMOJI.search(test_name))
        has_file_emoji = bool(cls.RE_SCRIPTURE_EMOJI.search(test_name))

        # [ASCENSION 52]: Apophatic SGF Sanctuary
        # We strip variables before extension check to avoid false positives
        phantom_name = cls.SGF_VAR_REGEX.sub('GNOSTIC_ATOM', test_name)

        #[ASCENSION 61 & 73]: Extension & File Sovereignty Oracle
        ext_match = re.search(r'\.([a-zA-Z0-9]+)$', phantom_name)
        ext = ext_match.group(1).lower() if ext_match else None
        has_sovereign_ext = ext in cls.EXTENSION_LATTICE

        is_sovereign_file = phantom_name.lower().split('/')[-1] in cls.SOVEREIGN_FILES

        # --- MOVEMENT III: GEOMETRIC ADJUDICATION ---
        # [ASCENSION 50]: POSIX Slash Harmony
        has_dir_slash = clean_name.endswith(('/', '\\'))

        # [ASCENSION 49]: The Law of the Trailing Colon
        # If the line ends with ':' but isn't part of a drive letter (e.g. C:), it is a FILE block.
        raw_strip = pure_name.split('#')[0].strip()
        has_trailing_colon = raw_strip.endswith(':') and not (len(raw_strip) == 2 and raw_strip[0].isalpha())

        # [ASCENSION 58]: Hydraulic Lookahead
        has_disciples = cls.is_followed_by_indented_children(lines, i, parser)

        # =========================================================================
        # == THE FINAL JUDGMENT (TIERED ADJUDICATION)                            ==
        # =========================================================================
        decision = "Triage: Default Form"

        if vessel.is_dir:
            decision = "Triage: Pre-Ordained by Kernel"
        elif has_dir_emoji:
            vessel.is_dir = True
            decision = "Triage: Emoji Sanctum Divination"
        elif has_file_emoji:
            vessel.is_dir = False
            decision = "Triage: Emoji Scripture Divination"
        elif has_dir_slash:
            vessel.is_dir = True
            decision = "Triage: Geometric Trailing Slash"
        elif has_trailing_colon:
            # Forced File status for Makefile/Recipe blocks
            vessel.is_dir = False
            decision = "Triage: Explicit Block Authority (:)"
        elif has_sovereign_ext or is_sovereign_file:
            vessel.is_dir = False
            decision = "Triage: Extension/File Sovereignty"
        elif has_disciples:
            vessel.is_dir = True
            decision = "Triage: Indented Disciple Perception"
        else:
            vessel.is_dir = False

        # --- MOVEMENT IV:[ASCENSION 54] - WINDOWS IRON PHALANX ---
        # Security Ward for forbidden names
        for segment in test_name.split('/'):
            stem = segment.split('.')[0].upper()
            if stem in cls.WINDOWS_RESERVED:
                Logger.warn(f"L{vessel.line_num}: Windows Reserved Name detected: '{segment}'. Inscription risk high.")

        # --- MOVEMENT V: STATE LOCKING & RADIATION ---
        if not hasattr(parser, '_identity_cache'):
            parser._identity_cache = {}
        parser._identity_cache[path_key] = vessel.is_dir

        #[ASCENSION 67]: HUD Pulse
        cls._radiate_identity_pulse(vessel, test_name, parser)

        return decision

    @classmethod
    def is_followed_by_indented_children(cls, lines: List[str], current_idx: int, parser: Any) -> bool:
        """
        [ASCENSION 58]: Hydraulic Lookahead Oracle.
        Scries the future of the timeline (up to 20 lines) to find indented children.
        """
        if current_idx + 1 >= len(lines):
            return False

        parent_indent = parser._calculate_original_indent(lines[current_idx])

        # We scan up to 20 lines to find the next meaningful atom
        for next_idx in range(current_idx + 1, min(current_idx + 21, len(lines))):
            line = lines[next_idx]
            stripped = line.strip()

            # Skip Voids and Comments
            if not stripped or stripped.startswith(('#', '//')):
                continue

            next_indent = parser._calculate_original_indent(line)
            return next_indent > parent_indent

        return False

    @staticmethod
    def _radiate_identity_pulse(vessel: GnosticVessel, name: str, parser: Any):
        """[ASCENSION 67]: Ocular HUD Multicast."""
        if parser.engine and hasattr(parser.engine, 'akashic') and parser.engine.akashic:
            try:
                # Teal (#64ffda) for Files, Blue (#3b82f6) for Directories
                aura = "#3b82f6" if vessel.is_dir else "#64ffda"

                parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "IDENTITY_DECREED",
                        "label": f"{'SANCTUM' if vessel.is_dir else 'SCRIPTURE'}: {name[:20]}",
                        "color": aura,
                        "trace": getattr(parser, 'parse_session_id', 'void'),
                        "line": vessel.line_num
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_ONTOLOGICAL_IDENTITY_ORACLE status=RESONANT mode=VMAX_73 version=2026.FINALIS>"