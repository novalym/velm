# Path: core/lsp/scaffold_features/folding_range/providers/commentary.py
# ----------------------------------------------------------------------

from typing import List
from ....base.features.folding_range.contracts import FoldingRangeProvider
from ....base.features.folding_range.models import FoldingRange, FoldingRangeKind
from ....base.document import TextDocument


class CommentaryProvider(FoldingRangeProvider):
    """
    =============================================================================
    == THE SILENCE KEEPER (V-Ω-COMMENT-MERGER)                                 ==
    =============================================================================
    Aggregates consecutive lines of comments (#) into a single foldable region.
    """

    def provide_folding_ranges(self, doc: TextDocument) -> List[FoldingRange]:
        ranges = []
        lines = doc.text.splitlines()

        start_line = -1

        for i, line in enumerate(lines):
            stripped = line.strip()
            is_comment = stripped.startswith("#")

            if is_comment:
                if start_line == -1:
                    start_line = i
            else:
                if start_line != -1:
                    # Block ended
                    if i - 1 > start_line:
                        ranges.append(FoldingRange(
                            startLine=start_line,
                            endLine=i - 1,
                            kind=FoldingRangeKind.Comment
                        ))
                    start_line = -1

        # EOF Check
        if start_line != -1 and len(lines) - 1 > start_line:
            ranges.append(FoldingRange(
                startLine=start_line,
                endLine=len(lines) - 1,
                kind=FoldingRangeKind.Comment
            ))

        return ranges