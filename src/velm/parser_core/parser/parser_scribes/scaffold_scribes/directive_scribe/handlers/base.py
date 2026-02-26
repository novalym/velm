# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/base.py
# -------------------------------------------------------------------------------------------------------------
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
    == THE ANCESTRAL SOUL OF DIRECTIVES (V-Ω-TOTALITY-V2000-QUOTE-PRESERVING)      ==
    =================================================================================
    LIF: ∞ | ROLE: HANDLER_CONSTITUTION | RANK: OMEGA_GUARDIAN

    The abstract base class for all Directive Handlers. It provides the shared Gnosis
    required to consume blocks and parse arguments.

    [THE CURE]:
    This version implements 'Bit-Perfect Argument Preservation'. It ensures that
    string literals passed as arguments (e.g., "auth-vault") retain their quotes,
    preventing the Alchemist from interpreting hyphens as subtraction operators.
    =================================================================================
    """

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF BINDING]"""
        self.parser = parser
        # Auto-name the logger based on the specific handler instance
        self.Logger = Scribe(self.__class__.__name__)

    @abstractmethod
    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[THE RITE OF CONDUCT]"""
        raise NotImplementedError("The child handler must define its own kinetic will.")

    def _consume_block(self, lines: List[str], start_i: int, end_marker: str) -> Tuple[List[str], int]:
        """
        [THE RITE OF CONSUMPTION]
        Consumes physical lines until the specific spiritual end marker is reached.
        """
        block_lines = []
        i = start_i
        while i < len(lines):
            line = lines[i]
            if line.strip() == end_marker:
                i += 1
                break
            block_lines.append(line)
            i += 1
        return block_lines, i

    def _lex_arguments(self, args_str: str) -> List[str]:
        """
        =============================================================================
        == THE RITE OF BIT-PERFECT LEXING (V-Ω-TOTALITY-V2000)                     ==
        =============================================================================
        [THE CURE]: This method uses a Non-Stripping Lookahead Sieve to split
        arguments by comma WITHOUT removing the quotes.

        Example: '8000, "auth-vault"' -> ['8000', '"auth-vault"']
        This ensures Jinja treats "auth-vault" as a string, not 'auth - vault'.
        """
        if not args_str or not args_str.strip():
            return []

        # [ASCENSION 1]: THE QUOTE-AWARE LOOKAHEAD
        # We split by comma only if it is NOT followed by an odd number of quotes.
        # This effectively ignores commas inside "..." or '...'
        pattern = r',(?=(?:[^\'"]*[\'"][^\'"]*[\'"])*[^\'"]*$)'

        try:
            # Atomic split and strip of external whitespace
            raw_args = re.split(pattern, args_str)
            return [a.strip() for a in raw_args if a.strip()]
        except Exception as e:
            # Fallback for truly fractured syntax
            self.Logger.warn(f"Lexical Triage failed on arguments: {e}")
            return [a.strip() for a in args_str.split(',') if a.strip()]

    def __repr__(self) -> str:
        return f"<Ω_BASE_HANDLER status=RESONANT>"