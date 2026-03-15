# Path: core/alchemist/elara/emitter/geometry/indenter.py
# -------------------------------------------------------

import textwrap
import unicodedata
import re
import hashlib
from typing import Final, List

from ...contracts.atoms import GnosticToken
from ......logger import Scribe

Logger = Scribe("GeometricIndenter")


class IsomorphicIndenter:
    """
    =============================================================================
    == THE ISOMORPHIC INDENTER (V-Ω-TOTALITY-VMAX-ASCENDED)                    ==
    =============================================================================
    LIF: ∞^∞ | ROLE: GEOMETRIC_PHYSICIST | RANK: OMEGA_SOVEREIGN_PRIME

    The supreme authority for Spatial Resonance. Indentation in ELARA is a
    mathematical invariant.
    """

    TAB_SIZE: Final[int] = 4

    # [ASCENSION 3]: Markdown Table Alignment Scryer
    RE_MD_TABLE: Final[re.Pattern] = re.compile(r'^\s*\|.*\|.*\s*$')

    @classmethod
    def align(cls, token: GnosticToken) -> str:
        """
        =========================================================================
        == THE EVENT HORIZON ANCHOR: OMEGA POINT                               ==
        =========================================================================
        """
        content = token.raw_text
        if not content: return ""

        content = unicodedata.normalize('NFC', content)
        content = content.replace('\u200b', '').replace('\ufeff', '')

        if '\n' not in content:
            return content

        if token.column_index <= 0:
            return content

        # [ASCENSION 1]: THE HOLOGRAPHIC BASELINE SUTURE
        # Dedent to absolute zero before applying gravity.
        soul_of_matter = textwrap.dedent(content)

        # [ASCENSION 3]: Markdown Table Auto-Alignment Check
        if cls._is_markdown_table(soul_of_matter):
            soul_of_matter = cls._align_markdown_table(soul_of_matter)

        lines = soul_of_matter.splitlines(keepends=False)
        if not lines: return content

        is_makefile = token.metadata.get("is_makefile", False)
        padding_char = "\t" if is_makefile else " "

        if is_makefile:
            multiplier = token.column_index // 4
        else:
            multiplier = token.column_index

        padding = padding_char * multiplier
        aligned_lines = []

        # [ASCENSION 2]: Docstring Sanctuary V2
        in_docstring = False
        doc_sigil = None

        for idx, line in enumerate(lines):
            # 1. Anchor Preservation
            if idx == 0:
                aligned_lines.append(line)
                continue

            # 2. Docstring Resonance
            if '"""' in line or "'''" in line:
                if not in_docstring:
                    in_docstring = True
                    doc_sigil = '"""' if '"""' in line else "'''"
                elif doc_sigil in line:
                    in_docstring = False

            # 3. Ghost-Line Exorcism
            if not line.strip():
                aligned_lines.append("")
                continue

            # 4. The Kinetic Shift
            if in_docstring:
                # Preserve relative internal formatting of docstrings
                aligned_lines.append(padding + line)
            else:
                aligned_lines.append(padding + line)

        result = "\n".join(aligned_lines)
        if content.endswith('\n'):
            result += '\n'

        if hasattr(token, 'metadata'):
            token.metadata["geometric_seal"] = hashlib.md5(result.encode()).hexdigest()[:8]

        return result

    @classmethod
    def calculate_visual_width(cls, segment: str) -> int:
        """[ASCENSION 4]: East-Asian Width Tomography."""
        visual_width = 0
        for char in segment:
            if char == '\t':
                visual_width += cls.TAB_SIZE - (visual_width % cls.TAB_SIZE)
            else:
                if unicodedata.east_asian_width(char) in ('W', 'F'):
                    visual_width += 2
                else:
                    visual_width += 1
        return visual_width

    @classmethod
    def _is_markdown_table(cls, text: str) -> bool:
        lines = text.splitlines()
        if len(lines) < 2: return False
        return bool(cls.RE_MD_TABLE.match(lines[0])) and bool(cls.RE_MD_TABLE.match(lines[1]))

    @classmethod
    def _align_markdown_table(cls, text: str) -> str:
        """Surgically aligns Markdown table columns."""
        lines = text.splitlines()
        rows = []
        for line in lines:
            if not line.strip(): continue
            cols = [c.strip() for c in line.strip('|').split('|')]
            rows.append(cols)

        if not rows: return text

        col_widths = [0] * len(rows[0])
        for row in rows:
            for i, col in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(col))

        aligned_lines = []
        for r_idx, row in enumerate(rows):
            formatted_cols = []
            for i, col in enumerate(row):
                if r_idx == 1 and set(col).issubset({'-', ':'}):
                    # Alignment row
                    formatted_cols.append('-' * col_widths[i])
                else:
                    formatted_cols.append(col.ljust(col_widths[i]))
            aligned_lines.append("| " + " | ".join(formatted_cols) + " |")

        return "\n".join(aligned_lines)