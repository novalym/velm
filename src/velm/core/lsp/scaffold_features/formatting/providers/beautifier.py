# Path: core/lsp/scaffold_features/formatting/providers/beautifier.py
# --------------------------------------------------------------------
import re
from typing import List, Optional
from ....base.features.formatting.contracts import FormattingProvider
from ....base.features.formatting.models import TextEdit, FormattingOptions
from ....document import TextDocument
from ....types.primitives import Range, Position


class ScaffoldBeautifier(FormattingProvider):
    """
    =============================================================================
    == THE GNOSTIC PURIFIER (V-Ω-GEOMETRIC-BEAUTIFIER)                         ==
    =============================================================================
    LIF: 10,000,000 | ROLE: AESTHETIC_RECONSTRUCTOR

    Transmutes raw, chaotic text into a state of Gnostic Purity.
    """

    @property
    def name(self) -> str:
        return "ScaffoldPurifier"

    @property
    def priority(self) -> int:
        return 100

    def format_document(self, doc: TextDocument, options: FormattingOptions) -> List[TextEdit]:
        """Calculates edits for the total scripture."""
        return self._purify(doc.text, doc, options)

    def format_range(self, doc: TextDocument, range: Range, options: FormattingOptions) -> List[TextEdit]:
        """Calculates edits for a specific range of lines."""
        # For simplicity in V12, we extract the range, format it,
        # and return the edit for that block.
        lines = doc.text.splitlines()
        target_lines = lines[range.start.line: range.end.line + 1]
        raw_fragment = "\n".join(target_lines)

        return self._purify(raw_fragment, doc, options, range)

    def _purify(self, text: str, doc: TextDocument, options: FormattingOptions, target_range: Optional[Range] = None) -> \
    List[TextEdit]:
        """
        The Master Rite of Purification.
        """
        lines = text.splitlines()
        purified_lines = []

        indent_size = options.tabSize or 4
        indent_char = " " if options.insertSpaces else "\t"

        for i, line in enumerate(lines):
            # [ASCENSION 1 & 5]: Indentation and Trailing Whitespace
            stripped = line.strip()
            if not stripped:
                purified_lines.append("")
                continue

            # Preserve original indentation level
            leading_ws = line[:line.find(stripped)]
            # Normalize indentation (Tabs to Spaces)
            norm_indent = leading_ws.replace("\t", " " * indent_size)

            # [ASCENSION 3]: Sigil Spacing Discipline
            # Align $$ and operators: $$ var = val
            line_content = stripped

            # 1. Variable definitions
            if line_content.startswith("$$"):
                line_content = re.sub(r'^\$\$\s*([\w_]+)\s*(:?)\s*=\s*', r'$$ \1\2 = ', line_content)

            # 2. File operators
            line_content = re.sub(r'\s*(::|<<|->|\+=|-=|~=|\^=)\s*', r' \1 ', line_content)

            # [ASCENSION 2]: Jinja2 Alchemical Spacing
            # {{var}} -> {{ var }}
            line_content = re.sub(r'\{\{\s*(.*?)\s*\}\}', r'{{ \1 }}', line_content)
            # |filter -> | filter
            line_content = re.sub(r'\s*\|\s*([\w_]+)', r' | \1', line_content)

            # [ASCENSION 10]: Comment Harmonizer
            if "#" in line_content and not any(q in line_content for q in ["'", '"']):
                line_content = re.sub(r'\s*#\s*(.*)', r'  # \1', line_content)

            purified_lines.append(norm_indent + line_content.strip())

        # Assemble the final matter
        new_text = "\n".join(purified_lines)

        # [ASCENSION 6]: Final Newline Vow
        if options.insertFinalNewline and not new_text.endswith("\n"):
            new_text += "\n"

        # Construct the minimal TextEdit
        if target_range:
            return [TextEdit(range=target_range, newText=new_text)]
        else:
            # Document-wide edit
            full_range = Range(
                start=Position(line=0, character=0),
                end=Position(line=doc.line_count, character=999)
            )
            return [TextEdit(range=full_range, newText=new_text)]