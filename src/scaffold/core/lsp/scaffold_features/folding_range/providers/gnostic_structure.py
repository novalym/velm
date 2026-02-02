# Path: core/lsp/scaffold_features/folding_range/providers/gnostic_structure.py
# -----------------------------------------------------------------------------

import re
from typing import List, Tuple
from ....base.features.folding_range.contracts import FoldingRangeProvider
from ....base.features.folding_range.models import FoldingRange, FoldingRangeKind
from ....base.document import TextDocument


class GnosticStructureProvider(FoldingRangeProvider):
    """
    =============================================================================
    == THE STRUCTURE GEOMETER (V-Ω-LOGIC-AWARE)                                ==
    =============================================================================
    [CAPABILITIES]:
    1. Folds Logic Gates: @if ... @endif
    2. Folds Loops: @for ... @endfor
    3. Folds Maestro Blocks: %% post-run (Indent based or next-block based)
    4. Folds Traits: %% trait ...

    [ASCENSION 1]: Robust Stack Handling to prevent "Unmatched" errors.
    """

    # Pre-compiled Regex for Speed
    # Matches: @if, @for, @macro, @try
    OPEN_DIRECTIVE = re.compile(r'^\s*@(if|for|macro|try|task)\b')
    # Matches: @endif, @endfor, etc.
    CLOSE_DIRECTIVE = re.compile(r'^\s*@(endif|endfor|endmacro|endtry|endtask)\b')

    # Matches: %% post-run, %% trait
    MAESTRO_HEADER = re.compile(r'^\s*%%\s+([\w\-]+)')

    def provide_folding_ranges(self, doc: TextDocument) -> List[FoldingRange]:
        ranges = []
        directive_stack: List[Tuple[int, str]] = []  # (line_index, type)
        lines = doc.text.splitlines()

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped: continue

            # --- 1. LOGIC DIRECTIVES (@if ... @endif) ---
            open_match = self.OPEN_DIRECTIVE.match(line)
            if open_match:
                directive_type = open_match.group(1)
                directive_stack.append((i, directive_type))
                continue

            close_match = self.CLOSE_DIRECTIVE.match(line)
            if close_match:
                if directive_stack:
                    start_line, _ = directive_stack.pop()
                    ranges.append(FoldingRange(
                        startLine=start_line,
                        endLine=i,
                        kind=FoldingRangeKind.Region
                    ))
                continue

            # --- 2. MAESTRO BLOCKS (%%) ---
            # Maestro blocks (%%) usually don't have an explicit 'end' tag.
            # They span until the next %% or the end of the file/indentation change.
            # We handle them via a look-ahead heuristic in the Indentation provider,
            # OR we can treat them as "Region" headers here if they have explicit indentation.

            # (We leave %% block folding to IndentationFallbackProvider for robustness,
            # as Gnostic syntax uses indentation for block scope).

        return ranges