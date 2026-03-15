# Path: parser_core/lexer_core/inquisitor/triage.py
# -------------------------------------------------

import re
from typing import List, Tuple, Callable
from ....contracts.data_contracts import GnosticLineType

class LexicalTriage:
    """
    =============================================================================
    == THE LEXICAL TRIAGE MATRIX (V-Ω-TOTALITY)                                ==
    =============================================================================
    ROLE: SIGIL_CLASSIFIER
    The rules engine that maps raw strings to Gnostic Line Types.
    """

    # [ASCENSION 32001]: The Legendary Assignment Barrier
    # Now explicitly excludes the Semantic Merge (*=) from Variable assignment.
    ASSIGNMENT_PATTERN = re.compile(
        r"^\s*"                                 
        r"(?![^=]*[\/\\])"                      
        r"(?P<name>[a-zA-Z_][a-zA-Z0-9_.-]*)"   
        r"(?:\s*:\s*[a-zA-Z_][\w\[\], ]*)?"     
        r"\s*(?P<op>=|\+=|\|=|\^=|~=)"          # *= IS EXCLUDED
        r"(?![=<>!])"
    )

    VOW_PATTERN = re.compile(
        r'^(?:->\s*)?'  
        r'(?:retry\([^)]*\):\s*)?'  
        r'(?:>>|\?\?|!!|proclaim:|echo\s|allow_fail:|(?:py|python|js|node|rs|rust|sh|bash|go):\s*$)',
        re.IGNORECASE
    )

    @classmethod
    def get_grimoire(cls) -> List[Tuple[Callable[[str], bool], GnosticLineType]]:
        """Returns the ordered list of perception rules."""
        return[
            (lambda s: not s.strip(), GnosticLineType.VOID),
            (lambda s: s.strip().startswith(('#', '//')), GnosticLineType.COMMENT),
            (lambda s: s.strip().startswith('{{') and not re.search(r'(/|:|::|<<|\+=|\^=|~=|\*=)\s*$', s.strip()), GnosticLineType.SGF_CONSTRUCT),
            (lambda s: s.strip().startswith(('{%', '{#')), GnosticLineType.SGF_CONSTRUCT),
            (lambda s: s.strip().startswith('%% contract'), GnosticLineType.CONTRACT_DEF),
            (lambda s: s.strip().startswith('%% trait'), GnosticLineType.TRAIT_DEF),
            (lambda s: s.strip().startswith('%% use'), GnosticLineType.TRAIT_USE),
            (lambda s: s.strip().startswith('%% on-heresy'), GnosticLineType.ON_HERESY),
            (lambda s: s.strip().startswith('%% on-undo'), GnosticLineType.ON_UNDO),
            (lambda s: s.strip().startswith('%%'), GnosticLineType.POST_RUN),
            (lambda s: bool(cls.VOW_PATTERN.match(s.strip())), GnosticLineType.VOW),
            (lambda s: s.strip().startswith(('$$', 'let ', 'def ', 'const ')) or bool(cls.ASSIGNMENT_PATTERN.match(s.strip())), GnosticLineType.VARIABLE),
            (lambda s: s.strip().startswith('@'), GnosticLineType.LOGIC),
        ]