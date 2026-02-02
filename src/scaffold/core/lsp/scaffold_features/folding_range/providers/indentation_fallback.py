# Path: core/lsp/scaffold_features/folding_range/providers/indentation_fallback.py
# --------------------------------------------------------------------------------

from typing import List
from ....base.features.folding_range.contracts import FoldingRangeProvider
from ....base.features.folding_range.models import FoldingRange
from ....base.document import TextDocument


class IndentationFallbackProvider(FoldingRangeProvider):
    """
    =============================================================================
    == THE GEOMETER (V-Ω-INDENTATION-PHYSICS)                                  ==
    =============================================================================
    The universal fallback. Maps regions based on indentation depth.
    Handles `%%` blocks, nested lists, and any structured text.
    """

    def provide_folding_ranges(self, doc: TextDocument) -> List[FoldingRange]:
        ranges = []
        lines = doc.text.splitlines()

        # Stack: [(line_index, indent_level)]
        stack = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped: continue

            # Calculate indentation (4 spaces = 1 level)
            indent = len(line) - len(stripped)

            # Resolve Stack: Close ranges that are deeper or equal to current
            while stack and stack[-1][1] >= indent:
                start_i, start_indent = stack.pop()
                # A block ends at the line BEFORE the current line (i-1)
                # But we must scan back to ignore empty lines
                end_i = self._find_last_content_line(lines, i - 1, start_i)

                if end_i > start_i:
                    ranges.append(FoldingRange(startLine=start_i, endLine=end_i))

            stack.append((i, indent))

        # Close remaining open blocks at EOF
        last_valid_line = self._find_last_content_line(lines, len(lines) - 1, 0)
        while stack:
            start_i, _ = stack.pop()
            if last_valid_line > start_i:
                ranges.append(FoldingRange(startLine=start_i, endLine=last_valid_line))

        return ranges

    def _find_last_content_line(self, lines: List[str], start_search: int, limit: int) -> int:
        """Walks backwards to find the last non-empty line."""
        for i in range(start_search, limit, -1):
            if lines[i].strip():
                return i
        return limit