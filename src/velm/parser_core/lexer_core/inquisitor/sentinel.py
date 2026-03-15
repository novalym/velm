# Path: parser_core/lexer_core/inquisitor/sentinel.py
# ---------------------------------------------------

import re
from typing import Final, Pattern


class CodeSentinel:
    """
    =============================================================================
    == THE APOPHATIC CODE SENTINEL (V-Ω-TOTALITY)                              ==
    =============================================================================
    LIF: 10,000x | ROLE: MATTER_DISAMBIGUATOR

    [ASCENSION 32004]: Aggressively matches lines that are clearly code (Python,
    JS, Go), preventing them from being hallucinated as Topography (Form).
    """

    # [THE MASTER CURE]: Prevents `build-backend = "..."` from becoming a file.
    CODE_SENTINEL_REGEX: Final[Pattern] = re.compile(
        r'^\s*('
        r'\bimport\b|\bfrom\b.*?\bimport\b|'
        r'\bexport\b|'
        r'\bdef\b|\bclass\b|'
        r'[a-zA-Z0-9_.-]+\s*(=|\+=|\|=|\^=|~=)|'
        r'\bfunction\b|\bconst\b|\blet\b|\bvar\b|'
        r'<[a-zA-Z]+.*?>|'
        r'\bconsole\.log\b|\bprint\b\(|'
        r'\breturn\b|'
        r'\bpackage\b|'
        r'\bfunc\b|'
        r'\buse\b.*::|'
        r'.*==.*|'  # Comparators are Mind, not Form
        r'.*\(.*'  # Function calls are Mind, not Form
        r')'
    )

    RAW_ASSIGNMENT_REGEX: Final[Pattern] = re.compile(r'(::|\+=|\^=|~=|<<|\*=)')

    @classmethod
    def is_mental_matter(cls, raw_line: str) -> bool:
        """Returns True if the line is definitively Code, not a Path."""
        return bool(cls.CODE_SENTINEL_REGEX.match(raw_line)) and not cls.RAW_ASSIGNMENT_REGEX.search(raw_line)