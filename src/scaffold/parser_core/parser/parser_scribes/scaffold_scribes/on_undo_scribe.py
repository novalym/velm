# Path: scaffold/parser_core/parser/parser_scribes/scaffold_scribes/on_undo_scribe.py
# -----------------------------------------------------------------------------------

from typing import List
from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel


class OnUndoScribe(ScaffoldBaseScribe):
    """A specialist scribe that consumes `%% on-undo` blocks and stores them in the parser's memory."""

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        parent_indent = self.parser._calculate_original_indent(lines[i])
        content_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        # Store the raw, dedented command lines for the next post-run block
        from textwrap import dedent
        raw_content = "\n".join(content_lines)
        clean_content = dedent(raw_content).strip()

        self.parser.pending_undo_block = clean_content.splitlines()
        self.Logger.verbose(f"Captured on-undo block with {len(self.parser.pending_undo_block)} command(s).")

        return end_index