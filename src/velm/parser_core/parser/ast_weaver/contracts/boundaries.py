# Path: parser_core/parser/ast_weaver/contracts/boundaries.py
# -----------------------------------------------------------

from typing import Final


class TopologicalBoundary:
    """
    =============================================================================
    == THE TOPOLOGICAL BOUNDARIES (V-Ω-PHYSICS-LIMITS)                         ==
    =============================================================================
    Defines the extreme limits of the AST geometry to prevent Stack Overflows
    and Heap Gluttony attacks.
    """

    # [ASCENSION 13]: Depth-Limit Sarcophagus
    MAX_STACK_DEPTH: Final[int] = 256

    # [ASCENSION 17]: Semantic Indentation Validation Limits
    # The maximum allowed jump in indentation spaces in a single leap.
    # Standard Python is 4, some aggressive configs use 8. 20 is a definitive typo.
    MAX_INDENT_LEAP: Final[int] = 20

    # The sacred floor of reality
    ROOT_INDENT: Final[int] = -1