# // Path: src/velm/parser_core/block_consumer.py
# ---------------------------------------------------------
# LIF: ∞ | ROLE: METABOLIC_TRIAGE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_BLOCK_CONSUMER_V400_SINGULARITY_FINALIS
# =========================================================================================

import re
import time
import hashlib
from typing import List, Tuple, Optional, Final, Set
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class GnosticBlockConsumer:
    """
    =================================================================================
    == THE GOD-ENGINE OF CONTENT CONSUMPTION (V-Ω-TOTALITY-V400.0)                 ==
    =================================================================================
    LIF: ∞ | THE OMEGA METABOLIC GOVERNOR

    This is the divine, sentient, and hyper-performant God-Engine of textual
    perception. It adjudicates the boundaries between Form (Structure) and
    Matter (Content) with mathematical certainty and metabolic restraint.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    # 25MB is the threshold of sanity for a single cognitive shard.
    MAX_BLOCK_MASS_BYTES: Final[int] = 25 * 1024 * 1024
    MAX_VERSES_PER_BLOCK: Final[int] = 100000
    MIN_INDENT_STEP: Final[int] = 1

    # [FACULTY 8]: THE SIGIL PHALANX
    # Captures any valid Gnostic opening sequence and its quote type
    SIGIL_PATTERN: Final[re.Pattern] = re.compile(
        r'(?P<sigil>::|<<|\+=|\^=|~=)\s*(?P<quote>"""|\'\'\'|")?'
    )

    def __init__(self, lines: List[str]):
        """
        The Rite of Inception.
        Binds the engine to the linear stream of lines and initializes the mass-sieve.
        """
        self.lines = lines or []
        self._total_mass_consumed = 0
        self._start_time = time.perf_counter()

    def _measure_visual_depth(self, line: str, tab_width: int = 4) -> int:
        """
        =============================================================================
        == THE RITE OF SPATIAL PERCEPTION (V-Ω-TAB-SNAP-HARDENED)                  ==
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
        # Strip Byte Order Marks and Zero-Width spaces that poison the typography.
        purified_line = line.lstrip('\ufeff\u200b\u200c\u200d')

        # [FACULTY 3]: TAB-SNAP CALIBRATION
        for char in purified_line:
            if char == ' ':
                visual_width += 1
            elif char == '\t':
                # Snap to the next virtual tab stop to annihilate "Space-Tab Collision"
                visual_width += tab_width - (visual_width % tab_width)
            else:
                break
            char_cursor += 1

        # [FACULTY 4]: THE TREE-SITTER SHIELD
        # Handles ASCII artifacts (│  ├──) by calculating their symbolic mass.
        remaining_content = purified_line[char_cursor:]
        if remaining_content:
            artifact_match = re.match(r'^[│├──└─`\\:\s-]+', remaining_content)
            if artifact_match:
                artifact_prefix = artifact_match.group(0)
                if len(remaining_content) > len(artifact_prefix):
                    for char in artifact_prefix:
                        if char == ' ':
                            visual_width += 1
                        elif char == '\t':
                            visual_width += tab_width - (visual_width % tab_width)
                        else:
                            visual_width += 2  # Complex glyphs possess double gravity

        return visual_width

    def _check_metabolic_tax(self, line: str, index: int):
        """
        =============================================================================
        == THE WARD OF GLUTTONY (V-Ω-METABOLIC-TRIAGE)                             ==
        =============================================================================
        [LIF-1]: Monitors byte-density to prevent the "OOM Execution."
        """
        line_bytes = len(line.encode('utf-8', errors='replace'))
        self._total_mass_consumed += line_bytes

        if self._total_mass_consumed > self.MAX_BLOCK_MASS_BYTES:
            raise ArtisanHeresy(
                f"Metabolic Tax Overflow: Block at line {index + 1} exceeds 25MB mass limit.",
                severity=HeresySeverity.CRITICAL,
                details=f"Current Mass: {self._total_mass_consumed} bytes.",
                suggestion="Use the '<<' seed sigil to link large artifacts instead of embedding them."
            )

    def consume_indented_block(self, start_index: int, parent_indent: int) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE RITE OF GEOMETRIC CONSUMPTION (V-Ω-TOTAL-RECALL)                    ==
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
        for peek_i in range(i, len(self.lines)):
            line_to_peek = self.lines[peek_i]
            if line_to_peek.strip():
                block_baseline = self._measure_visual_depth(line_to_peek)
                break

        if block_baseline == -1 or block_baseline <= parent_indent:
            return [], start_index

        # [FACULTY 6]: BOUNDARY ENFORCEMENT
        while i < len(self.lines):
            line = self.lines[i]

            if not line.strip():
                self._check_metabolic_tax(line, i)
                content_lines.append(line)
                i += 1
                continue

            current_indent = self._measure_visual_depth(line)

            # [LIF-4]: THE GEOMETRIC WARD
            if current_indent <= parent_indent:
                break

            self._check_metabolic_tax(line, i)
            content_lines.append(line)
            i += 1

            # [LIF-2]: THE VERSE LIMIT
            if len(content_lines) > self.MAX_VERSES_PER_BLOCK:
                raise ArtisanHeresy(
                    f"Topological Exhaustion: Block starting at L{start_index} exceeds 100k verses.",
                    severity=HeresySeverity.CRITICAL
                )

        # Cleanup: Remove trailing empty lines.
        while content_lines and not content_lines[-1].strip():
            content_lines.pop()
            i -= 1

        return content_lines, i

    def consume_explicit_block(self, start_index: int, opening_sigil_line: str) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE RITE OF DELIMITER PARITY (V-Ω-TOTALITY-V400.0)                      ==
        =============================================================================
        [FACULTY 1, 7, 8, 11] THE UNBREAKABLE VOW.
        Handles `:: ""
        ` or ` += '''` with mathematical certainty and mass-warding.
        """
        match = self.SIGIL_PATTERN.search(opening_sigil_line)
        if not match:
            return [], start_index

        quote_type = match.group('quote') or '"""'
        sigil_end = match.end()
        opening_depth = self._measure_visual_depth(opening_sigil_line)

        content_lines: List[str] = []

        # 1. ATOMIC SHARD CHECK (Same-line close)
        if sigil_end < len(opening_sigil_line):
            remainder = opening_sigil_line[sigil_end:]
            closing_index = remainder.find(quote_type)

            if closing_index != -1:
                is_escaped = (closing_index > 0 and remainder[closing_index - 1] == '\\')
                if not is_escaped:
                    return [remainder[:closing_index]], start_index

            if remainder.strip():
                content_lines.append(remainder.rstrip('\r\n'))

        # 2. THE MULTI-LINE METABOLIC VIGIL
        i = start_index
        while i < len(self.lines):
            line = self.lines[i]
            stripped = line.strip()

            # [FACULTY 1 & 11]: THE LAW OF PARITY
            # Check for the Closing Gate at identical indentation.
            if stripped == quote_type:
                current_depth = self._measure_visual_depth(line)
                if current_depth == opening_depth:
                    return content_lines, i + 1

            self._check_metabolic_tax(line, i)
            content_lines.append(line)
            i += 1

            # [LIF-2]: THE VERSE LIMIT
            if len(content_lines) > self.MAX_VERSES_PER_BLOCK:
                raise ArtisanHeresy(
                    f"Topological Exhaustion: Explicit block at L{start_index} failed to close.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion=f"Ensure the closing {quote_type} matches the opener's indentation."
                )

        # [RECOVERY]: If the timeline ends without a seal, we return the matter but warn the Architect.
        return content_lines, i

    def __repr__(self) -> str:
        return (f"<Ω_BLOCK_CONSUMER mass={self._total_mass_consumed}B "
                f"verses={len(self.lines)} state=TOTAL_SOVEREIGNTY>")

# == SCRIPTURE SEALED: THE CONSUMER HAS ACHIEVED SINGULARITY ==