# Path: parser_core/lexer_core/inquisitor/triage.py
# -------------------------------------------------


import re
from typing import List, Tuple, Callable, Final
from ....contracts.data_contracts import GnosticLineType


class LexicalTriage:
    """
    =============================================================================
    == THE LEXICAL TRIAGE MATRIX (V-Ω-TOTALITY-VMAX-STATIC-GRIMOIRE)           ==
    =============================================================================
    LIF: 50,000x | ROLE: SIGIL_CLASSIFIER | RANK: OMEGA_SOVEREIGN

    [THE MASTER CURE]: The `get_grimoire` loop previously instantiated 13 anonymous
    lambda functions for every single line parsed in the God-Engine. This caused
    catastrophic garbage collection thrashing (The Lambda Swarm).

    The Matrix is now pre-compiled and permanently enshrined in the `_GRIMOIRE_MATRIX`
    constant at the microsecond the module is loaded. Parsing is now O(1) alloc.
    """

    ASSIGNMENT_PATTERN: Final[re.Pattern] = re.compile(
        r"^\s*"
        r"(?![^=]*[\/\\])"
        r"(?P<name>[a-zA-Z_][a-zA-Z0-9_.-]*)"
        r"(?:\s*:\s*[a-zA-Z_][\w\[\], ]*)?"
        r"\s*(?P<op>=|\+=|\|=|\^=|~=)"
        r"(?![=<>!])"
    )

    VOW_PATTERN: Final[re.Pattern] = re.compile(
        r'^(?:->\s*)?'
        r'(?:retry\([^)]*\):\s*)?'
        r'(?:>>|\?\?|!!|proclaim:|echo\s|allow_fail:|(?:py|python|js|node|rs|rust|sh|bash|go):\s*$)',
        re.IGNORECASE
    )

    # =========================================================================
    # ==[ASCENSION]: THE ACHRONAL GRIMOIRE MATRIX (THE MASTER CURE)         ==
    # =========================================================================
    # Bound to memory eternally. Zero CPU overhead to fetch.
    _GRIMOIRE_MATRIX: Final[List[Tuple[Callable[[str], bool], GnosticLineType]]] = [
        (lambda s: not s.strip(), GnosticLineType.VOID),
        (lambda s: s.strip().startswith(('#', '//')), GnosticLineType.COMMENT),
        (lambda s: s.strip().startswith('{{') and not re.search(r'(/|:|::|<<|\+=|\^=|~=|\*=)\s*$', s.strip()),
         GnosticLineType.SGF_CONSTRUCT),
        (lambda s: s.strip().startswith(('{%', '{#')), GnosticLineType.SGF_CONSTRUCT),
        (lambda s: s.strip().startswith('%% contract'), GnosticLineType.CONTRACT_DEF),
        (lambda s: s.strip().startswith('%% trait'), GnosticLineType.TRAIT_DEF),
        (lambda s: s.strip().startswith('%% use'), GnosticLineType.TRAIT_USE),
        (lambda s: s.strip().startswith('%% on-heresy'), GnosticLineType.ON_HERESY),
        (lambda s: s.strip().startswith('%% on-undo'), GnosticLineType.ON_UNDO),
        (lambda s: s.strip().startswith('%%'), GnosticLineType.POST_RUN),
        (lambda s: bool(LexicalTriage.VOW_PATTERN.match(s.strip())), GnosticLineType.VOW),
        (lambda s: s.strip().startswith(('$$', 'let ', 'def ', 'const ')) or bool(
            LexicalTriage.ASSIGNMENT_PATTERN.match(s.strip())), GnosticLineType.VARIABLE),
        (lambda s: s.strip().startswith('@'), GnosticLineType.LOGIC),
    ]

    @classmethod
    def get_grimoire(cls) -> List[Tuple[Callable[[str], bool], GnosticLineType]]:
        """O(1) Return of the Pre-Compiled Perception Matrix."""
        return cls._GRIMOIRE_MATRIX