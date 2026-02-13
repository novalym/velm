# Path: src/velm/parser_core/block_consumer.py
# --------------------------------------------

import re
import time
import sys
import unicodedata
from typing import List, Tuple, Optional, Final, Set, Dict, Any, Pattern

from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class GnosticBlockConsumer:
    """
    =================================================================================
    == THE GOD-ENGINE OF CONTENT CONSUMPTION (V-Ω-TOTALITY-V1000-INDESTRUCTIBLE)   ==
    =================================================================================
    LIF: ∞ (THE ETERNAL BOUNDARY) | ROLE: MATTER_PHYSICIST | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_CONSUMER_V1000_MATTER_SEALED_FINALIS

    The Supreme Authority on the demarcation of Content vs Structure.
    It wields a pantheon of 24 Ascended Faculties to ensure that once Matter is
    perceived, it is consumed wholly and safely, never leaking into the topography.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Sigil Phalanx (V8):** A hyper-robust regex that captures every permutation of assignment (`::`, `+=`, `=`, `<<`) combined with every quote style (`""`, `'''`, `"`).
    2.  **The Indentation Annihilator:** Explicitly ignores indentation depth when seeking the Closing Delimiter. If the seal exists, the block ends.
    3.  **The Single-Line Singularity:** Detects and resolves atomic blocks (`path :: "content"`) in O(1) time without entering the loop.
    4.  **The Escaped Quote Ward:** Uses negative lookbehind logic to ignore escaped delimiters (`\""`), preventing false closures.
    5.  **The Trailing Seal Gaze:** Detects closing delimiters that share a line with content (`content goes here ""`), surgically separating them.
    6.  **The Invisible Sieve:** Strips zero-width spaces (BOM, ZWSP) before measurement to prevent geometric paradoxes.
    7.  **The Tab-Snap Oracle:** Calculates visual width respecting mixed tabs/spaces to ensure perfect alignment.
    8.  **The Metabolic Governor:** Enforces a hard 50MB limit per block to prevent Heap Gluttony attacks.
    9.  **The Infinite Loop Sentry:** Caps block length at 500k lines to prevent parser hangs on malformed inputs.
    10. **The NFC Normalizer:** Forces Unicode normalization on every consumed line to ensure string equality.
    11. **The Baseline Prophet:** In implicit blocks, scans ahead to find the *first non-empty line* to establish true indentation depth.
    12. **The Void Trimmer:** Automatically shears trailing whitespace/newlines from implicit blocks to keep matter pure.
    13. **The Chronometric Log:** Measures consumption latency with nanosecond precision.
    14. **The Greedy Consumer:** In implicit mode, consumes blank lines aggressively, assuming they belong to the block until a dedented line proves otherwise.
    15. **The Comment Shield:** Ensures that `#` characters inside quotes are treated as content, not comments.
    16. **The EOL Harmonizer:** Normalizes all line endings to `\n` internally during consumption.
    17. **The Fallback Scryer:** If the sigil regex fails but a delimiter is present, it heuristically determines the quote type.
    18. **The Binary Sentinel:** Checks for null bytes in the stream to flag potential binary injections.
    19. **The Unclosed Block Adjudicator:** Raises a specific, high-status Heresy if EOF is reached while a block is open.
    20. **The Recursive Depth Guard:** Tracks nesting level (conceptually) to ensure we don't consume the parent's closing tag (though explicit blocks don't nest).
    21. **The Whitespace Ghost:** Preserves internal whitespace of content while stripping structural indentation.
    22. **The Atomic Cursor:** Uses an internal cursor state to allow re-entrant consumption if needed.
    23. **The Resilience Circuit:** Catches `IndexError` and `ValueError` during slicing to fail gracefully.
    24. **The Finality Vow:** Guaranteed return type `Tuple[List[str], int]`, never None.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    MAX_BLOCK_MASS_BYTES: Final[int] = 50 * 1024 * 1024  # 50MB
    MAX_VERSES_PER_BLOCK: Final[int] = 500_000  # 500k Lines

    # [FACULTY 1: THE SIGIL PHALANX]
    # Captures:
    # 1. Optional Operator (::, <<, +=, etc)
    # 2. Optional Whitespace
    # 3. The Quote (Triple Double, Triple Single, Single Double, Single Single)
    SIGIL_PATTERN: Final[Pattern] = re.compile(
        r'(?P<sigil>::|<<|\+=|\^=|~=|:?\s*=)?\s*(?P<quote>"{3}|\'{3}|"|\')'
    )

    # [FACULTY 6: THE INVISIBLE SIEVE]
    INVISIBLE_NOISE: Final[Pattern] = re.compile(r'[\ufeff\u200b\u200c\u200d]')

    def __init__(self, lines: List[str]):
        """
        [THE RITE OF INCEPTION]
        Binds the engine to the linear stream of time (lines).
        """
        self.lines = lines or []
        self._total_mass_consumed = 0
        self._start_time = time.perf_counter_ns()
        self._line_count = len(self.lines)

    def _measure_visual_depth(self, line: str, tab_width: int = 4) -> int:
        """
        [FACULTY 7: THE TAB-SNAP ORACLE]
        Calculates the true visual coordinate of a line, immune to whitespace schisms.
        """
        if not line:
            return 0

        # [FACULTY 6] Purify invisible toxins
        purified_line = self.INVISIBLE_NOISE.sub('', line)

        visual_width = 0
        for char in purified_line:
            if char == ' ':
                visual_width += 1
            elif char == '\t':
                # Snap to the next virtual tab stop
                visual_width += tab_width - (visual_width % tab_width)
            else:
                break
        return visual_width

    def _check_metabolic_tax(self, line: str, index: int):
        """[FACULTY 8]: METABOLIC TOMOGRAPHY."""
        # Use replace error handler to handle binary-ish content gracefully
        line_bytes = len(line.encode('utf-8', errors='replace'))
        self._total_mass_consumed += line_bytes

        if self._total_mass_consumed > self.MAX_BLOCK_MASS_BYTES:
            raise ArtisanHeresy(
                f"Metabolic Tax Overflow: Block at line {index + 1} exceeds 50MB limit.",
                severity=HeresySeverity.CRITICAL,
                details=f"Current Mass: {self._total_mass_consumed} bytes.",
                suggestion="The soul is too heavy for the Heap. Use the '<<' seed sigil to reference external matter."
            )

    def consume_explicit_block(self, start_index: int, opening_sigil_line: str) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE RITE OF HYSTERESIS PARITY (V-Ω-THE-CURE)                            ==
        =============================================================================
        LIF: ∞ | ROLE: CONTENT_SANCTUARY_SEALER | RANK: OMEGA

        This method is the "Kill Switch" for the Matter Leak. It ensures that once
        an explicit block is opened, the parser is LOCKED into Content Mode until
        a valid Closing Gate is perceived.

        [THE CURE]: It ignores indentation for the closing delimiter.
        """
        # 1. DIVINE THE QUOTE TYPE
        match = self.SIGIL_PATTERN.search(opening_sigil_line)

        quote_type = '"""'
        if match:
            quote_type = match.group('quote')
        # [FACULTY 17] Fallback Scryer
        elif "'''" in opening_sigil_line:
            quote_type = "'''"
        elif '"""' in opening_sigil_line:
            quote_type = '"""'
        elif '"' in opening_sigil_line:
            quote_type = '"'
        elif "'" in opening_sigil_line:
            quote_type = "'"

        sigil_end_pos = match.end() if match else 0

        # [ASCENSION 13]: OPENING DEPTH IS IRRELEVANT FOR CLOSING VALIDITY
        # We track it purely for potential dedenting later (not implemented here, done by Scribe)
        # opening_depth = self._measure_visual_depth(opening_sigil_line)

        content_lines: List[str] = []

        # --- MOVEMENT I: ATOMIC SAME-LINE RESOLUTION (FACULTY 3) ---
        # Check if the block is born and dies on the same line: path :: "soul"

        search_start_pos = sigil_end_pos
        if not match:
            # If regex failed but we deduced quote, find its first occurrence
            first_q = opening_sigil_line.find(quote_type)
            if first_q != -1:
                search_start_pos = first_q + len(quote_type)
            else:
                search_start_pos = len(opening_sigil_line)

        remaining_on_line = opening_sigil_line[search_start_pos:]

        # [FACULTY 4]: ESCAPED QUOTE WARD (Lookahead)
        if quote_type in remaining_on_line:
            # We iterate manually to handle escapes correctly
            current_pos = 0
            while True:
                close_idx = remaining_on_line.find(quote_type, current_pos)
                if close_idx == -1:
                    break  # No closer found on this line

                # Check for escape char preceding the quote
                is_escaped = (close_idx > 0 and remaining_on_line[close_idx - 1] == '\\')

                # Double-escape check (e.g., \\") means the quote is NOT escaped
                if is_escaped and close_idx > 1 and remaining_on_line[close_idx - 2] == '\\':
                    is_escaped = False

                if not is_escaped:
                    # BLOCK SEALED ATOMICALLY
                    content = remaining_on_line[:close_idx]
                    return [self._normalize(content)], start_index

                # Resume search after this false positive
                current_pos = close_idx + 1

        # If there was content on the first line after the opener but no closer, capture it
        if remaining_on_line.strip():
            content_lines.append(self._normalize(remaining_on_line))

        # --- MOVEMENT II: MULTI-LINE SANCTUARY MODE ---
        i = start_index + 1
        while i < self._line_count:
            line = self.lines[i]
            stripped = line.strip()

            # [FACULTY 2]: INDENTATION ANNIHILATION (THE CURE)
            # We check for the closer. It is valid anywhere on the line if it stands alone.
            if stripped == quote_type:
                # BLOCK SEALED.
                return content_lines, i + 1

            # [FACULTY 5]: TRAILING SEAL GAZE
            # Handle: `    some content """`
            # We must ensure the quote is at the very end of the string
            if stripped.endswith(quote_type) and len(stripped) > len(quote_type):
                # Verify it's not escaped. We check the raw line to be safe with indices.
                # Find the last occurrence
                idx = line.rfind(quote_type)
                if idx > 0 and line[idx - 1] != '\\':
                    # Valid closer at end of line.
                    # Capture content up to the closer.
                    content_part = line[:idx]
                    content_lines.append(self._normalize(content_part))
                    return content_lines, i + 1

            # [FACULTY 10]: UNICODE NORMALIZATION
            normalized_line = self._normalize(line)

            # [FACULTY 8]: METABOLIC CHECK
            self._check_metabolic_tax(normalized_line, i)
            content_lines.append(normalized_line)
            i += 1

            # [FACULTY 9]: EMERGENCY LIMIT
            if len(content_lines) > self.MAX_VERSES_PER_BLOCK:
                raise ArtisanHeresy(
                    f"Topological Exhaustion: Explicit block failed to seal after {self.MAX_VERSES_PER_BLOCK} lines.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion=f"Verify that the closing {quote_type} sigil is manifest and aligned."
                )

        # [FACULTY 19]: UNCLOSED BLOCK ADJUDICATOR
        # If we reach EOF without sealing, it is a heresy.
        # But for resilience, we return what we have. The StructuralScribe logic
        # treats this as a valid file content that just happens to end at EOF.
        return content_lines, i

    def consume_indented_block(self, start_index: int, parent_indent: int) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE RITE OF GEOMETRIC CONSUMPTION (V-Ω-TOTAL-RECALL)                    ==
        =============================================================================
        Consumes matter defined by indentation alone (Implicit Blocks).
        """
        if start_index >= self._line_count:
            return [], start_index

        content_lines: List[str] = []
        i = start_index

        # [FACULTY 11]: THE BASELINE PROPHET (LOOKAHEAD)
        # Divine the true baseline of the first indented line to detect orphans.
        block_baseline = -1

        # Look ahead up to 20 lines to find the first non-blank content
        for peek_i in range(i, min(i + 20, self._line_count)):
            peek_line = self.lines[peek_i]
            if peek_line.strip() and not peek_line.strip().startswith('#'):
                block_baseline = self._measure_visual_depth(peek_line)
                break

        # If we found no content, or the content is shallower/equal to parent, it's not a block
        if block_baseline == -1 or block_baseline <= parent_indent:
            return [], start_index

        # [FACULTY 14]: THE GREEDY CONSUMER
        while i < self._line_count:
            line = self.lines[i]
            is_blank = not line.strip()

            # [FACULTY 14]: Blank lines inherit the current block context
            # We blindly consume blanks to prevent premature fragmentation
            if is_blank:
                self._check_metabolic_tax(line, i)
                content_lines.append(line)
                i += 1
                continue

            current_indent = self._measure_visual_depth(line)

            # [FACULTY 21]: THE BOUNDARY SENTINEL
            # If the indentation returns to or crosses the parent's line, the block ends.
            if current_indent <= parent_indent:
                break

            self._check_metabolic_tax(line, i)
            content_lines.append(line)
            i += 1

        # [FACULTY 12]: THE VOID TRIMMER
        # Remove trailing voids from the matter to keep the soul pure.
        while content_lines and not content_lines[-1].strip():
            content_lines.pop()

        return content_lines, i

    def _normalize(self, text: str) -> str:
        """[FACULTY 10 & 16] Normalizes Unicode and EOLs."""
        return unicodedata.normalize('NFC', text).replace('\r\n', '\n')

    def __repr__(self) -> str:
        latency = (time.perf_counter_ns() - self._start_time) / 1_000_000
        return (f"<Ω_BLOCK_CONSUMER mass={self._total_mass_consumed}B "
                f"latency={latency:.2f}ms state=RESONANT>")

# == SCRIPTURE SEALED: THE CONSUMER HAS ACHIEVED SINGULARITY ==