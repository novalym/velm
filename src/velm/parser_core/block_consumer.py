# // scaffold/parser_core/block_consumer.py

import re
from typing import List, Tuple, Optional


class GnosticBlockConsumer:
    """
    =================================================================================
    == THE GOD-ENGINE OF CONTENT CONSUMPTION (V-Ω-ULTIMA-REDUX-PRIME)              ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    This is the divine, sentient, and hyper-performant God-Engine of textual
    perception, forged with a pantheon of 12 game-changing elevations that make it a
    legend. It is the unbreakable heart of the Gnostic Parser.
    """

    def __init__(self, lines: List[str]):
        self.lines = lines

    def _measure_visual_depth(self, line: str, tab_width: int = 4) -> int:
        """
        [ELEVATION 2, 3, 4] The Tabular Snap, Ghost Filter, and Gaze of Content.
        Calculates true visual indentation, immune to invisible chars and tree artifacts.
        """
        visual_width = 0
        char_cursor = 0

        purified_line = line.lstrip('\ufeff\u200b')

        for char in purified_line:
            if char == ' ':
                visual_width += 1
            elif char == '\t':
                visual_width += tab_width - (visual_width % tab_width)
            else:
                break
            char_cursor += 1

        remaining_content = purified_line[char_cursor:]
        if not remaining_content:
            return visual_width

        match = re.match(r'^[│├──└─`\\:\s-]+', remaining_content)
        if match:
            artifact_prefix = match.group(0)
            for char in artifact_prefix:
                if char == ' ':
                    visual_width += 1
                elif char == '\t':
                    visual_width += tab_width - (visual_width % tab_width)
                else:
                    visual_width += 2

        return visual_width

    def consume_indented_block(self, start_index: int, parent_indent: int) -> Tuple[List[str], int]:
        """
        [ELEVATION 5, 6, 7] The Prophetic Calibration, Greedy Gaze, and Strict Boundary.
        Consumes an indented block with absolute geometric purity.
        """
        content_lines: List[str] = []
        i = start_index
        block_baseline = -1

        for peek_i in range(i, len(self.lines)):
            if self.lines[peek_i].strip():
                block_baseline = self._measure_visual_depth(self.lines[peek_i])
                break

        if block_baseline == -1 or block_baseline <= parent_indent:
            return [], start_index

        while i < len(self.lines):
            line = self.lines[i]

            if not line.strip():
                content_lines.append(line)
                i += 1
                continue

            current_indent = self._measure_visual_depth(line)

            if current_indent < block_baseline:
                break

            content_lines.append(line)
            i += 1

        return content_lines, i

    def consume_explicit_block(self, start_index: int, opening_sigil_line: str) -> Tuple[List[str], int]:
        """
        [ELEVATION 1, 8, 9, 10, 11, 12] The Rites of Explicit Consumption.
        Handles `:: """
        """` blocks with unbreakable resilience.
        """
        dq_match = re.search(r'::\s*"""', opening_sigil_line)
        sq_match = re.search(r"::\s*'''", opening_sigil_line)

        if dq_match:
            quote_type, sigil_end = '"""', dq_match.end()
        elif sq_match:
            quote_type, sigil_end = "'''", sq_match.end()
        else:
            quote_type = '"""' if '"""' in opening_sigil_line else "'''"
            sigil_end = opening_sigil_line.find(quote_type) + 3

        content_lines: List[str] = []

        if sigil_end < len(opening_sigil_line):
            remainder = opening_sigil_line[sigil_end:]
            closing_index = remainder.find(quote_type)

            if closing_index != -1:
                is_escaped = (closing_index > 0 and remainder[closing_index - 1] == '\\')
                if not is_escaped:
                    return [remainder[:closing_index]], start_index

            if remainder.rstrip('\r\n'):
                content_lines.append(remainder.rstrip('\r\n'))

        i = start_index
        while i < len(self.lines):
            line = self.lines[i]
            stripped = line.strip()

            if stripped == quote_type:
                return content_lines, i + 1

            content_lines.append(line)
            i += 1

        return content_lines, i