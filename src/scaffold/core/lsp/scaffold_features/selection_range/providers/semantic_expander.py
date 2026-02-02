# Path: core/lsp/scaffold_features/selection_range/providers/semantic_expander.py
# -------------------------------------------------------------------------------
import re
from typing import List, Optional
from ....base.features.selection_range.contracts import SelectionRangeProvider
from ....base.features.selection_range.models import SelectionRange, Range, Position
from ....base.document import TextDocument


class SemanticExpanderProvider(SelectionRangeProvider):
    """
    =============================================================================
    == THE SEMANTIC GEOMETER (V-Ω-SCAFFOLD-AWARE)                              ==
    =============================================================================
    LIF: 100x | ROLE: INTELLIGENT_EXPANSION

    A sophisticated engine that expands selection based on Gnostic Grammar.
    It understands:
    1.  **Atoms:** Words, identifiers.
    2.  **Molecules:** Strings ("..."), Jinja expressions ({{ ... }}).
    3.  **Constructs:** Full lines, Variable definitions ($$ ...).
    4.  **Blocks:** Indented regions, @if ... @endif blocks.
    5.  **Cosmos:** The file.
    """

    @property
    def name(self) -> str:
        return "ScaffoldSemanticExpander"

    # --- THE GRIMOIRE OF REGEX ---
    RE_WORD = re.compile(r'[\w\-\$\@\%]+')  # Matches $$var, @if, word
    RE_JINJA = re.compile(r'\{\{.*?\}\}')
    RE_STRING_DOUBLE = re.compile(r'"(?:[^"\\]|\\.)*"')
    RE_STRING_SINGLE = re.compile(r"'(?:[^'\\]|\\.)*'")
    RE_BLOCK_START = re.compile(r'^\s*(@if|@for|@macro|@try|@task|%%)\b')
    RE_BLOCK_END = re.compile(r'^\s*(@endif|@endfor|@endmacro|@endtry|@endtask)\b')

    def provide_selection_ranges(self, doc: TextDocument, positions: List[Position]) -> List[SelectionRange]:
        results = []
        lines = doc.text.splitlines()

        for pos in positions:
            if pos.line >= len(lines): continue

            ranges: List[Range] = []

            # --- LAYER 1: ATOMIC WORD ---
            word_range = self._get_word_range(doc.get_line(pos.line), pos)
            if word_range: ranges.append(word_range)

            # --- LAYER 2: MOLECULAR (String/Jinja) ---
            mol_range = self._get_molecular_range(doc.get_line(pos.line), pos)
            if mol_range and (not ranges or ranges[-1] != mol_range):
                ranges.append(mol_range)

            # --- LAYER 3: LINE CONTENT (Trimmed) ---
            line_text = doc.get_line(pos.line)
            stripped = line_text.strip()
            if stripped:
                start_char = line_text.find(stripped)
                end_char = start_char + len(stripped)
                ranges.append(Range(start=Position(line=pos.line, character=start_char),
                                    end=Position(line=pos.line, character=end_char)))

            # --- LAYER 4: FULL LINE ---
            ranges.append(Range(start=Position(line=pos.line, character=0),
                                end=Position(line=pos.line, character=len(line_text))))

            # --- LAYER 5: INDENTATION BLOCK ---
            block_range = self._get_indentation_block(lines, pos.line)
            if block_range and (not ranges or ranges[-1] != block_range):
                ranges.append(block_range)

            # --- LAYER 6: DIRECTIVE PARENT (Recursive) ---
            # e.g. Inside an @if block, expand to the @if...@endif wrapper
            directive_range = self._get_directive_wrapper(lines, pos.line)
            if directive_range and (not ranges or ranges[-1] != directive_range):
                ranges.append(directive_range)

            # --- LAYER 7: DOCUMENT ---
            doc_range = Range(
                start=Position(line=0, character=0),
                end=Position(line=len(lines), character=0)
            )
            ranges.append(doc_range)

            # --- CONSTRUCT HIERARCHY ---
            # Chain the ranges: ranges[0] -> parent ranges[1] -> parent ranges[2] ...
            # Filter duplicates or invalids
            unique_ranges = []
            seen = set()
            for r in ranges:
                sig = f"{r.start.line}:{r.start.character}-{r.end.line}:{r.end.character}"
                if sig not in seen:
                    unique_ranges.append(r)
                    seen.add(sig)

            # Build linked list from outside in (or inside out)
            # The API expects the INNERMOST range, which has a .parent pointing to the next.
            root = None
            current = None

            # Iterate smallest to largest
            for r in unique_ranges:
                node = SelectionRange(range=r)
                if root is None:
                    root = node
                    current = node
                else:
                    current.parent = node
                    current = node

            results.append(root)

        return results

    def _get_word_range(self, line: str, pos: Position) -> Optional[Range]:
        for match in self.RE_WORD.finditer(line):
            if match.start() <= pos.character <= match.end():
                return Range(
                    start=Position(line=pos.line, character=match.start()),
                    end=Position(line=pos.line, character=match.end())
                )
        return None

    def _get_molecular_range(self, line: str, pos: Position) -> Optional[Range]:
        # Check Strings
        for pattern in [self.RE_STRING_DOUBLE, self.RE_STRING_SINGLE, self.RE_JINJA]:
            for match in pattern.finditer(line):
                if match.start() <= pos.character <= match.end():
                    # If inside content (excluding quotes/braces), return content first?
                    # For simplicity, we return the whole string/jinja block including delimiters
                    return Range(
                        start=Position(line=pos.line, character=match.start()),
                        end=Position(line=pos.line, character=match.end())
                    )
        return None

    def _get_indentation_block(self, lines: List[str], line_idx: int) -> Optional[Range]:
        """
        Expands to the block of lines with the same or greater indentation,
        bounded by lines with lesser indentation or whitespace.
        """
        if line_idx >= len(lines): return None
        target_line = lines[line_idx]
        if not target_line.strip(): return None

        target_indent = len(target_line) - len(target_line.lstrip())

        start = line_idx
        end = line_idx

        # Scan Up
        while start > 0:
            prev_line = lines[start - 1]
            if not prev_line.strip():  # Skip empty lines? Or stop? Usually stop or include.
                # If we want contiguous block, stop at empty line depending on style.
                # Let's stop at lesser indent or empty.
                # Actually, standard behavior: Stop if indent is LESS.
                # If empty, ignore indentation check but include?
                pass

            prev_indent = len(prev_line) - len(prev_line.lstrip())
            if prev_line.strip() and prev_indent < target_indent:
                break
            start -= 1

        # Scan Down
        while end < len(lines) - 1:
            next_line = lines[end + 1]
            next_indent = len(next_line) - len(next_line.lstrip())
            if next_line.strip() and next_indent < target_indent:
                break
            end += 1

        if start == end: return None

        return Range(
            start=Position(line=start, character=0),
            end=Position(line=end + 1, character=0)
        )

    def _get_directive_wrapper(self, lines: List[str], line_idx: int) -> Optional[Range]:
        """
        Expands to the enclosing @if ... @endif block.
        Naively scans upwards for a start block with lower/equal indentation,
        and downwards for a matching end block.
        """
        # 1. Scan Up for Start
        stack_depth = 0
        start = -1

        # We need to find the specific start of the current block.
        # This requires parsing nesting.
        # Scanning UP:
        # If we see END, depth++. If we see START, depth--.
        # If depth < 0, we found our parent.

        for i in range(line_idx, -1, -1):
            line = lines[i]
            if self.RE_BLOCK_END.match(line):
                stack_depth += 1
            elif self.RE_BLOCK_START.match(line):
                if stack_depth > 0:
                    stack_depth -= 1
                else:
                    start = i
                    break

        if start == -1: return None

        # 2. Scan Down for End from Start
        # We restart scanning from the found start to find the matching end
        # to ensure correct pairing.
        end = -1
        scan_depth = 0

        for i in range(start, len(lines)):
            line = lines[i]
            if self.RE_BLOCK_START.match(line):
                scan_depth += 1
            elif self.RE_BLOCK_END.match(line):
                scan_depth -= 1
                if scan_depth == 0:
                    end = i
                    break

        if end == -1: return None

        # Ensure our cursor is actually inside this range
        if not (start <= line_idx <= end): return None

        return Range(
            start=Position(line=start, character=0),
            end=Position(line=end + 1, character=0)
        )