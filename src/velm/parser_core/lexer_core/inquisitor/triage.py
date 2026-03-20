# Path: parser_core/lexer_core/inquisitor/triage.py
# -------------------------------------------------


import re
from typing import List, Tuple, Callable, Final, Dict, Set
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

    # [STRATUM 0: THE CONSTITUTIONAL GATES]
    # Gates that open a new dimensional stratum (Containers)
    # [ASCENSION]: Added 'component' and 'mount' for the Isomorphic Component Model.
    CONTAINER_GATES: Final[Set[str]] = {
        'if', 'for', 'match', 'slot', 'macro', 'component', 'task', 'try',
        'forge_class', 'refactor', 'call', 'mount', 'with', 'filter'
    }

    # [STRATUM 1: THE SIBLING SUTURE MAP]
    # Gates that branch an existing stratum (e.g. elif, else, catch)
    SIBLING_SUTURE_MAP: Final[Dict[str, Tuple[str, ...]]] = {
        'elif': ('if', 'elif'),
        'else': ('if', 'elif'),
        'case': ('match', 'case'),
        'default': ('match', 'case'),
        'catch': ('try', 'catch'),
        'finally': ('try', 'catch'),
        'except': ('try', 'catch')  # Alias Support
    }

    # [STRATUM 2: THE CLOSER ORACLE]
    # Maps end-tags to their primordial openers for stack validation
    CLOSER_TO_OPENER: Final[Dict[str, str]] = {
        'endif': 'if',
        'endfor': 'for',
        'endmatch': 'match',
        'endswitch': 'match',
        'endslot': 'slot',
        'endmacro': 'macro',
        'endcomponent': 'component',
        'endtask': 'task',
        'endtry': 'try',
        'endcall': 'call',
        'endmount': 'mount',
        'endforge': 'forge_class',
        'endrefactor': 'refactor',
        'endwith': 'with',
        'endfilter': 'filter'
    }

    # [STRATUM 3: THE ALIAS LATTICE]
    # Normalizes visual variation into semantic unity
    ALIAS_MAP: Final[Dict[str, str]] = {
        'elseif': 'elif',
        'else if': 'elif',
        'switch': 'match',
        'except': 'catch',
        'stop': 'break',
        'next': 'continue'
    }

    # =========================================================================
    # == [ASCENSION]: THE ACHRONAL GRIMOIRE MATRIX (THE MASTER CURE)         ==
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
        # [ASCENSION]: Added component and mount to the logic prefix catch
        (lambda s: s.strip().startswith(('@', 'component ', 'mount ')), GnosticLineType.LOGIC),
    ]

    @classmethod
    def get_grimoire(cls) -> List[Tuple[Callable[[str], bool], GnosticLineType]]:
        """O(1) Return of the Pre-Compiled Perception Matrix."""
        return cls._GRIMOIRE_MATRIX

    @classmethod
    def analyze(cls, content: str) -> Tuple[str, str]:
        """
        =============================================================================
        == THE RITE OF ANALYTIC DECONSTRUCTION (V-Ω-TOTALITY-VMAX)                 ==
        =============================================================================
        Surgically extracts the gate keyword and the remaining expression.

        [THE MASTER CURE]: Strips the '@' sigil at nanosecond zero, ensuring
        '@return' resolves to 'return' and '@if' resolves to 'if'. It now also
        natively recognizes bare 'component' and 'mount' words as logic gates.
        """
        import unicodedata

        if not content:
            return "", ""

        # --- MOVEMENT I: PURIFICATION ---
        clean_content = unicodedata.normalize('NFC', content.strip())
        clean_content = clean_content.replace('\u200b', '').replace('\ufeff', '')

        # --- MOVEMENT II: SIGIL AMNESTY STRIKE ---
        content_stripped = clean_content.lstrip('@')

        # --- MOVEMENT III: ATOMIC FISSION ---
        parts = content_stripped.split(None, 1)
        raw_gate = parts[0].lower() if parts else ""
        expression = parts[1] if len(parts) > 1 else ""

        # --- MOVEMENT IV: ALIAS TRANSMUTATION ---
        gate = cls.ALIAS_MAP.get(raw_gate, raw_gate)

        # --- MOVEMENT V: TRAILING COLON EXORCISM ---
        if expression.endswith(':'):
            expression = expression[:-1].strip()

        return gate, expression

    @classmethod
    def divine_intent(cls, gate: str) -> str:
        """Categorizes the gate into its topological role."""
        if gate in cls.CONTAINER_GATES:
            return "CONTAINER"
        if gate in cls.SIBLING_SUTURE_MAP:
            return "SUTURE"
        if gate in cls.CLOSER_TO_OPENER:
            return "CLOSER"
        return "DIRECTIVE"

    def __repr__(self) -> str:
        return f"<Ω_TOKEN_TRIAGE status=RESONANT mode=SIGIL_AMNESTY version=VMAX_TOTALITY>"