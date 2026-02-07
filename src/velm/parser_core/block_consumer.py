# // Path: src/velm/parser_core/block_consumer.py
# ---------------------------------------------------------
# LIF: ∞ | ROLE: TOPOGRAPHICAL_ADJUDICATOR | RANK: OMEGA_SUPREME
# AUTH: Ω_BLOCK_CONSUMER_V300_ADAMANT_BEDROCK
# =========================================================================================

import re
from typing import List, Tuple, Optional, Final


class GnosticBlockConsumer:
    """
    =================================================================================
    == THE GOD-ENGINE OF CONTENT CONSUMPTION (V-Ω-TOTALITY-V300.0)                 ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE) | THE ADAMANT BEDROCK

    This is the divine, sentient, and hyper-performant God-Engine of textual
    perception. It adjudicates the boundaries between Form (Structure) and
    Matter (Content) with mathematical certainty.
    =================================================================================
    """

    # [FACULTY 8]: THE SIGIL PHALANX
    # Captures any valid Gnostic opening sequence and its quote type
    SIGIL_PATTERN: Final[re.Pattern] = re.compile(
        r'(?P<sigil>::|<<|\+=|\^=|~=)\s*(?P<quote>"""|\'\'\'|")?'
    )

    def __init__(self, lines: List[str]):
        """
        The Rite of Inception.
        Binds the engine to the linear stream of lines.
        """
        self.lines = lines or []
        self._max_depth = 100  # [FACULTY 9]

    def _measure_visual_depth(self, line: str, tab_width: int = 4) -> int:
        """
        =============================================================================
        == THE RITE OF SPATIAL PERCEPTION (V-Ω-TAB-SNAP)                           ==
        =============================================================================
        [FACULTY 2, 3, 4] The Invisible Sieve and Tabular Snap.
        Calculates the true visual indentation, immune to invisible characters,
        BOM markers, and ASCII tree artifacts.
        """
        if not line:
            return 0

        visual_width = 0
        char_cursor = 0

        # [FACULTY 2]: ANNIHILATE INVISIBLE HERESIES
        # Strip Byte Order Marks and Zero-Width spaces that poison copy-pastes.
        purified_line = line.lstrip('\ufeff\u200b')

        # [FACULTY 3]: TABULAR HARMONIZATION
        for char in purified_line:
            if char == ' ':
                visual_width += 1
            elif char == '\t':
                # Snap to the next virtual tab stop
                visual_width += tab_width - (visual_width % tab_width)
            else:
                break
            char_cursor += 1

        # [FACULTY 4]: THE TREE-SITTER SHIELD
        # If the remaining line starts with ASCII tree artifacts (e.g. │  ├──),
        # we treat the artifacts as part of the indentation mass (2 units per glyp).
        remaining_content = purified_line[char_cursor:]
        if remaining_content:
            artifact_match = re.match(r'^[│├──└─`\\:\s-]+', remaining_content)
            if artifact_match:
                artifact_prefix = artifact_match.group(0)
                # Only add if there is actual code/content following the artifact
                if len(remaining_content) > len(artifact_prefix):
                    for char in artifact_prefix:
                        if char == ' ':
                            visual_width += 1
                        elif char == '\t':
                            visual_width += tab_width - (visual_width % tab_width)
                        else:
                            # Complex glpyhs count as double-width anchors
                            visual_width += 2

        return visual_width

    def consume_indented_block(self, start_index: int, parent_indent: int) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE RITE OF GEOMETRIC CONSUMPTION (V-Ω-GREEDY-GAZE)                     ==
        =============================================================================
        [FACULTY 5, 6, 12] The Prophetic Lookahead and Greedy Gaze.
        Consumes a block of lines indented deeper than the parent.
        """
        if start_index >= len(self.lines):
            return [], start_index

        content_lines: List[str] = []
        i = start_index
        block_baseline = -1

        # [FACULTY 5]: PROPHETIC LOOKAHEAD
        # We peek forward to find the first non-empty line to establish the
        # true indentation "floor" of this block.
        for peek_i in range(i, len(self.lines)):
            line_to_peek = self.lines[peek_i]
            if line_to_peek.strip():
                block_baseline = self._measure_visual_depth(line_to_peek)
                break

        # [FACULTY 12]: THE VOID ADJUDICATION
        # If the block is empty or not actually indented deeper, we halt the rite.
        if block_baseline == -1 or block_baseline <= parent_indent:
            return [], start_index

        # [FACULTY 6]: BOUNDARY ENFORCEMENT
        while i < len(self.lines):
            line = self.lines[i]

            # Empty lines or lines with only whitespace are siphoned into the block,
            # but they do not define the boundary.
            if not line.strip():
                content_lines.append(line)
                i += 1
                continue

            current_indent = self._measure_visual_depth(line)

            # If we hit a line that is shallower or equal to the parent, the block is sealed.
            if current_indent <= parent_indent:
                break

            content_lines.append(line)
            i += 1

        # Cleanup: Remove trailing empty lines that don't belong to the matter.
        while content_lines and not content_lines[-1].strip():
            content_lines.pop()
            i -= 1

        return content_lines, i

    def consume_explicit_block(self, start_index: int, opening_sigil_line: str) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE RITE OF DELIMITER PARITY (V-Ω-INDENT-LOCKED-TOTALITY)               ==
        =============================================================================
        [FACULTY 1, 7, 8, 11] THE UNBREAKABLE VOW.
        Handles `::  ''' (three ")
        ` or ` += '''` blocks with mathematical certainty.

        [THE CURE]: This method uses 'Indentation Parity'. A block only closes if 
        the closing delimiter matches the EXACT visual depth of the opening line.
        """
        # 1. DIVINE THE SOUL OF THE OPENER
        # [FACULTY 8]: Extract Sigil and Quote Type
        match = self.SIGIL_PATTERN.search(opening_sigil_line)
        if not match:
            # Should be architecturally impossible if the Scribe called this.
            return [], start_index

        quote_type = match.group('quote') or '"""'
        sigil_end = match.end()

        # [FACULTY 1]: THE INDENTATION ANCHOR
        # We record the visual depth of the line that birthed this block.
        opening_depth = self._measure_visual_depth(opening_sigil_line)

        content_lines: List[str] = []

        # 2. CHECK FOR SAME-LINE TERMINATION (Atomic Shards)
        if sigil_end < len(opening_sigil_line):
            remainder = opening_sigil_line[sigil_end:]
            # Look for the closing quote on the same line
            closing_index = remainder.find(quote_type)

            if closing_index != -1:
                # [FACULTY 7]: BACKSLASH HEALING
                # Verify it isn't an escaped quote (e.g. \"\"\")
                is_escaped = (closing_index > 0 and remainder[closing_index - 1] == '\\')
                if not is_escaped:
                    # The soul is atomic. We return it instantly.
                    return [remainder[:closing_index]], start_index

            # If no same-line close, siphoning the remainder as the first line of the block.
            if remainder.strip():
                content_lines.append(remainder.rstrip('\r\n'))

        # 3. THE MULTI-LINE VIGIL
        i = start_index
        while i < len(self.lines):
            line = self.lines[i]
            stripped = line.strip()

            # [FACULTY 1 & 11]: THE LAW OF PARITY
            # A line is only a 'Closing Gate' if:
            # A. It exactly matches the delimiter (stripped).
            # B. Its visual depth is EQUAL to the opening depth.
            if stripped == quote_type:
                current_depth = self._measure_visual_depth(line)
                if current_depth == opening_depth:
                    # THE GATE IS REACHED. THE RITE IS COMPLETE.
                    return content_lines, i + 1

            # All other matter is consumed as pure content.
            content_lines.append(line)
            i += 1

        # [RECOVERY]: If the timeline ends without a seal, we return the matter.
        return content_lines, i

    def __repr__(self) -> str:
        return f"<Ω_BLOCK_CONSUMER lines={len(self.lines)} state=VIGILANT>"

# == SCRIPTURE SEALED: THE BEDROCK IS TITANIUM ==