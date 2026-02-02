# Path: core/lsp/scaffold_features/folding_range/providers/content_block.py
# -------------------------------------------------------------------------

import re
from typing import List
from ....base.features.folding_range.contracts import FoldingRangeProvider
from ....base.features.folding_range.models import FoldingRange, FoldingRangeKind
from ....base.document import TextDocument


class ContentBlockProvider(FoldingRangeProvider):
    """
    =============================================================================
    == THE MATTER COMPRESSOR (V-Ω-TEXT-BLOCKS)                                 ==
    =============================================================================
    Specialist for collapsing large text blobs.
    Handles:
    - Triple-Quoted Strings: \"\"\" ... \"\"\"
    - Inline Content Markers: :: \"\"\"
    """

    # Detect start of a block string (Triple Quote)
    # We look for """ or '''
    TRIPLE_QUOTE = re.compile(r'("{3}|\'{3})')

    def provide_folding_ranges(self, doc: TextDocument) -> List[FoldingRange]:
        ranges = []
        lines = doc.text.splitlines()

        in_block = False
        start_line = -1
        delimiter = ""

        for i, line in enumerate(lines):
            # We scan for the delimiter
            # Note: This is a simplified scanner. It assumes one triple-quote per line max
            # or balanced pairs. A full tokenizer would be perfect, but this is fast.

            matches = list(self.TRIPLE_QUOTE.finditer(line))

            for match in matches:
                token = match.group(1)

                if not in_block:
                    # OPENING
                    in_block = True
                    start_line = i
                    delimiter = token
                else:
                    # CLOSING?
                    if token == delimiter:
                        # Close block
                        in_block = False
                        # Only fold if it spans multiple lines
                        if i > start_line:
                            ranges.append(FoldingRange(
                                startLine=start_line,
                                endLine=i,
                                kind=FoldingRangeKind.Region,
                                collapsedText='...'  # [ASCENSION 11]
                            ))
                            start_line = -1

        return ranges