# Path: parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/base.py
# ------------------------------------------------------------------------------------------

import re
from abc import ABC, abstractmethod
from typing import List, Tuple, TYPE_CHECKING, Optional
from .......contracts.data_contracts import GnosticVessel
from .......logger import Scribe

if TYPE_CHECKING:
    from ......parser.engine import ApotheosisParser


class BaseDirectiveHandler(ABC):
    """
    =================================================================================
    == THE ANCESTRAL SOUL OF DIRECTIVES (V-Ω-TOTALITY-V3000-PYTHONIC-SUTURE)       ==
    =================================================================================
    LIF: ∞ | ROLE: HANDLER_CONSTITUTION | RANK: OMEGA_GUARDIAN

    [THE CURE]:
    This version implements 'Laminar Block Consumption' for the Scaffold stratum.
    It eradicates the reliance on string-based end markers (like `@endif`), favoring
    the mathematical purity of geometric indentation.
    =================================================================================
    """

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF BINDING]"""
        self.parser = parser
        self.Logger = Scribe(self.__class__.__name__)

    @abstractmethod
    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[THE RITE OF CONDUCT]"""
        raise NotImplementedError("The child handler must define its own kinetic will.")

    def _consume_block(self, lines: List[str], start_i: int, end_marker: str) -> Tuple[List[str], int]:
        """
        =========================================================================
        == THE RITE OF PYTHONIC CONSUMPTION                                    ==
        =========================================================================
        Consumes physical lines based on Indentation Gravity, naturally closing
        when the indentation recedes. Legacy @end_markers are gracefully absorbed
        and ignored if present.
        """
        # 1. Capture Parent Anchor Gravity
        parent_indent = self.parser._calculate_original_indent(lines[start_i - 1])

        # 2. Delegate to the native Indentation-Aware Engine
        block_lines, next_i = self.parser._consume_indented_block_with_context(
            lines, start_i, parent_indent
        )

        # 3. [ASCENSION]: Silent Legacy Amnesty
        # If the Architect used a legacy `@endmacro` or `@endif` at the exact
        # same indentation level as the parent, we elegantly leap over it so it
        # doesn't pollute the next parse cycle.
        if next_i < len(lines):
            next_line = lines[next_i].strip()
            # Catch @endmacro, @endif, or just endif
            if next_line == f"@{end_marker}" or next_line == end_marker:
                self.Logger.debug(f"L{next_i + 1}: Legacy closer '{next_line}' absorbed by the Pythonic Suture.")
                next_i += 1

        return block_lines, next_i

    def _lex_arguments(self, args_str: str) -> List[str]:
        """
        [THE CURE]: Bit-Perfect Lexing.
        Uses a Non-Stripping Lookahead Sieve to split arguments by comma
        WITHOUT removing the quotes.
        """
        if not args_str or not args_str.strip():
            return []

        pattern = r',(?=(?:[^\'"]*[\'"][^\'"]*[\'"])*[^\'"]*$)'

        try:
            raw_args = re.split(pattern, args_str)
            return [a.strip() for a in raw_args if a.strip()]
        except Exception as e:
            self.Logger.warn(f"Lexical Triage failed on arguments: {e}")
            return [a.strip() for a in args_str.split(',') if a.strip()]

    def __repr__(self) -> str:
        return f"<Ω_BASE_HANDLER status=RESONANT>"