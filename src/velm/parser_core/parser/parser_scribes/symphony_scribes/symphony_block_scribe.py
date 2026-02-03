# scaffold/parser_core/parser_scribes/symphony_scribes/symphony_block_scribe.py

from textwrap import dedent
from typing import List, Tuple, TYPE_CHECKING

from .symphony_base_scribe import SymphonyBaseScribe
from ....block_consumer import GnosticBlockConsumer
from .....contracts.data_contracts import GnosticVessel

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class SymphonyBlockScribe(SymphonyBaseScribe):
    """
    =================================================================================
    == THE MASTER OF INDENTED GNOSIS (V-Ω-SPATIAL-ARCHITECT)                       ==
    =================================================================================
    LIF: 10,000,000

    This abstract artisan provides the foundational logic for consuming indented
    blocks of scripture. It is the spatial engine used by the Logic, Polyglot,
    and Parallel scribes.

    It delegates the forensic analysis of whitespace to the `GnosticBlockConsumer`,
    ensuring that tab/space mixing and invisible characters do not shatter the
    hierarchy.
    """

    def __init__(self, parser: 'ApotheosisParser'):
        # We initialize with the base name. Concrete implementations (Logic, Polyglot)
        # will likely override the logger name via their own super().__init__ calls,
        # or rely on this base identity.
        super().__init__(parser, "SymphonyBlockScribe")

    def _consume_block(self, lines: List[str], i: int) -> Tuple[str, int]:
        """
        [THE RITE OF SPATIAL CONSUMPTION]
        Consumes a block of lines indented deeper than the line at index `i`.

        Args:
            lines: The full scripture.
            i: The index of the parent line (the block header, e.g., 'if x:').

        Returns:
            (dedented_content_string, next_line_index)
        """
        # 1. The Gaze of the Anchor
        # We determine the visual depth of the header line.
        # This is the "floor" - anything deeper than this belongs to the block.
        consumer = GnosticBlockConsumer(lines)
        parent_indent = consumer._measure_visual_depth(lines[i])

        self.Logger.verbose(
            f"L{i + 1 + self.parser.line_offset}: Measuring block depth against parent indent: {parent_indent}")

        # 2. The Greedy Consumption
        # The consumer eats lines until it hits a line shallower or equal to parent_indent.
        content_lines, end_index = consumer.consume_indented_block(i + 1, parent_indent)

        # 3. The Rite of Purification (Dedent)
        # We join the lines and use textwrap.dedent to strip the common leading whitespace.
        # This ensures that nested blocks become top-level to their sub-parsers.
        raw_block = "\n".join(content_lines)
        clean_block = dedent(raw_block)

        line_count = len(content_lines)
        self.Logger.verbose(f"   -> Consumed {line_count} lines. Block ends at L{end_index + self.parser.line_offset}.")

        return clean_block, end_index

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The Abstract Interface.
        Concrete Scribes (Logic, Polyglot, Parallel) MUST override this to
        perform their specific semantic handling of the consumed block.
        """
        raise NotImplementedError("SymphonyBlockScribe is an abstract artisan. Summon a concrete subclass.")