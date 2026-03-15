# Path: parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe/regex_phalanx.py
# -----------------------------------------------------------------------------------------

import re
from typing import Final


class VariableRegexPhalanx:
    """
    =============================================================================
    == THE REGEX PHALANX (V-Ω-LEXICAL-PERCEPTION)                              ==
    =============================================================================
    The optical nerve of the Variable Scribe. Pre-compiled for nanosecond
    velocity across infinite blueprint lines.
    """

    # [ASCENSION 1]: The Inline Perception Matrix
    # Matches: $$ name : type = value
    INLINE_DEF: Final[re.Pattern] = re.compile(
        r"^\s*(?:(?P<prefix>\$\$|let|const|def)\s+)?"
        r"(?P<name>[a-zA-Z0-9_.-]+)"
        r"(?:\s*:\s*(?P<type>[^=+\|:]+))?"
        r"\s*(?P<operator>=|\+=|\|=|\^=|~=)"
        r"\s*(?P<value>.*)$"
    )

    # [ASCENSION 2]: The Block Perception Matrix (Heredocs)
    # Matches: $$ name : type:
    BLOCK_DEF: Final[re.Pattern] = re.compile(
        r"^\s*(?:(?P<prefix>\$\$|let|const|def)\s+)?"
        r"(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)"
        r"(?:\s*:\s*(?P<type>[^:]+))?"
        r":\s*$"
    )

    # [ASCENSION 3]: The Substrate Expansions
    SHELL_EXEC: Final[re.Pattern] = re.compile(r"^\$\((.*)\)$")
    ENV_VAR: Final[re.Pattern] = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)(?::-([^}]+))?\}")

    # [ASCENSION 4]: Pure Math Divination
    MATH_CALC: Final[re.Pattern] = re.compile(r"^[\d\s+\-*/\(\).%]+$")

