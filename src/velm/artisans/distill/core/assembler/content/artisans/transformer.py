# Path: scaffold/artisans/distill/core/assembler/content/artisans/transformer.py

import re
from pathlib import Path
from .......core.cortex.contracts import FileGnosis


class Transformer:
    """The artisan of content alchemy: truncating, compressing, and distilling."""

    MAX_LINES_FULL = 2000
    COMMENT_SYNTAX = {'.py': '#', '.js': '//', '.ts': '//', '.html': '<!--', '.css': '/*'}  # Abbreviated

    def truncate_large_file(self, content: str, gnosis: FileGnosis) -> str:
        """The Large File Warden (Head/Tail)."""
        lines = content.splitlines()
        if len(lines) <= self.MAX_LINES_FULL:
            return content

        head = lines[:500]
        tail = lines[-500:]
        skipped = len(lines) - 1000

        comment_char = self.COMMENT_SYNTAX.get(gnosis.path.suffix.lower(), '#')
        gap_marker = f"\n{comment_char} ... [Gnostic Gap: {skipped} lines omitted for brevity] ...\n"

        return "\n".join(head) + gap_marker + "\n".join(tail)

    def distill_docstrings(self, content: str) -> str:
        """The Docstring Distiller."""

        def reducer(match):
            quotes = match.group(1)
            body = match.group(2).strip()
            if '\n' in body:
                summary = body.splitlines()[0]
                return f"{quotes}{summary} ...{quotes}"
            return match.group(0)

        # This regex is now more robust, handling both """ and '''
        return re.sub(r'("""|\'\'\')(.*?)(\1)', reducer, content, flags=re.DOTALL)

    def compress_whitespace(self, content: str) -> str:
        """The Token Compressor."""
        # Replace 3+ newlines with exactly 2 to preserve paragraph breaks.
        return re.sub(r'\n{3,}', '\n\n', content)