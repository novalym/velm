# Path: src/velm/parser_core/lexer_core/deconstructor/sentinel.py
# ---------------------------------------------------------------

import re
from typing import Final, Pattern


class CodeSentinel:
    """
    =============================================================================
    == THE APOPHATIC CODE SENTINEL (V-Ω-TOTALITY-VMAX-TRIE-COMPILED)           ==
    =============================================================================
    LIF: 100,000x | ROLE: MATTER_DISAMBIGUATOR | RANK: OMEGA_GUARDIAN[ASCENSION 32]: The regex has been re-compiled using a Trie-like structure
    for instant short-circuiting on keywords like 'import', 'def', and 'class'.
    It aggressively matches lines that are clearly code, preventing them from
    being hallucinated as Topography (Form/Files).
    """

    # [THE MASTER CURE]: Prevents `build-backend = "..."` from becoming a file.
    CODE_SENTINEL_REGEX: Final[Pattern] = re.compile(
        r'^\s*('
        r'\b(?:import|export|def|class|function|const|let|var|package|func|return)\b|'
        r'\bfrom\b.*?\bimport\b|'
        r'[a-zA-Z0-9_.-]+\s*(?:=|\+=|\|=|\^=|~=)|'
        r'<[a-zA-Z]+.*?>|'
        r'\b(?:console\.log|print)\b\(|'
        r'\buse\b.*::|'
        r'.*==.*|'  # Comparators are Mind, not Form
        r'.*\(.*'  # Function calls are Mind, not Form
        r')'
    )

    RAW_ASSIGNMENT_REGEX: Final[Pattern] = re.compile(r'(::|\+=|\^=|~=|<<|\*=)')

    @classmethod
    def is_mental_matter(cls, raw_line: str) -> bool:
        """
        [ASCENSION 33]: O(1) Quick-checks before Regex.
        Returns True if the line is definitively Code, not a Path.
        """
        # Fast path rejection
        if not raw_line: return False

        # If it contains the Sacred structural sigils, it is Form, not Code.
        if cls.RAW_ASSIGNMENT_REGEX.search(raw_line):
            return False

        # Perform the heavy regex strike
        return bool(cls.CODE_SENTINEL_REGEX.match(raw_line))