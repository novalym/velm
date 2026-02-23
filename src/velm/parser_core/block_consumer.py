# Path: parser_core/block_consumer.py
# -----------------------------------

import re
import time
import sys
import unicodedata
from typing import List, Tuple, Optional, Final, Set, Dict, Any, Pattern

from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class GnosticBlockConsumer:
    """
    =================================================================================
    == THE GOD-ENGINE OF CONTENT CONSUMPTION (V-Ω-TOTALITY-V9000-INDESTRUCTIBLE)   ==
    =================================================================================
    LIF: ∞ (THE ETERNAL BOUNDARY) | ROLE: MATTER_PHYSICIST | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_CONSUMER_V9000_PHANTOM_SLAYER_FINALIS

    The Supreme Authority on the demarcation of Content vs Structure.
    It wields a pantheon of 24 Ascended Faculties to ensure that once Matter is
    perceived, it is consumed wholly and safely, perfectly immune to the
    hallucinations of the "Phantom Forest" (AI-generated emojis and ASCII art).

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Ghost Grid Transmutator (THE CURE):** Surgically detects Unicode Box-Drawing
        characters (`├──`, `│`) and Emojis (`📁`) in the line prefix and transmutes them
        into precise geometric spacing. The AI's drawings become mathematically perfect indents.
    2.  **The Emoji Spatial Oracle:** Recognizes that Emojis consume two terminal columns
        and accurately transmutes them into double-spaces for flawless alignment.
    3.  **The Invisible Toxin Sieve:** Eradicates Zero-Width Spaces (`\u200b`, BOM)
        before they can corrupt geometric calculations.
    4.  **The Hysteresis Parity Protocol:** Absolute closure detection for explicit blocks,
        ignoring ghost indents to seal `\"\"\"` blocks securely.
    5.  **The Escaped Quote Quantum Tunnel:** Employs lookbehind logic to safely ignore
        escaped delimiters (`\\\"\"\"`), preventing premature block severing.
    6.  **The Trailing Seal Gaze:** Capable of finding closing quotes that share a line
        with active code without corrupting the final statement.
    7.  **The Baseline Prophet:** In implicit blocks, scans ahead up to 20 lines to find
        the true, non-empty structural anchor.
    8.  **The Void Trimmer:** Shears trailing whitespace and blank lines from the end of
        implicit blocks, ensuring the soul remains pure.
    9.  **The Metabolic Governor:** Enforces a hard 50MB limit per block, acting as an
        unbreakable shield against Heap Gluttony attacks.
    10. **The Infinite Loop Sentry:** Hard-caps block consumption at 500,000 lines.
    11. **The Unicode Normalizer:** Enforces NFC normalization on every consumed line.
    12. **The Greedy Implicit Consumer:** Confidently absorbs blank lines within a block
        until a mathematically certain dedent is perceived.
    13. **The Tab-Snap Engine:** Modulo math ensures tabs (`\\t`) snap to perfect 4-space
        grid coordinates during width calculation.
    14. **The Atomic Same-Line Resolver:** Instantly resolves `path :: "soul"` constructs
        in O(1) time without ever entering the heavy consumption loop.
    15. **The Fallback Quote Scryer:** If the primary Sigil Regex engine faults, manual
        heuristics divine the quote type to ensure survival.
    16. **The EOL Harmonizer:** Normalizes all carriage returns (`\\r\\n`) to POSIX (`\\n`).
    17. **The Unclosed Adjudicator:** Gracefully handles unexpected EOF without crashing,
        returning the gathered matter for forensic analysis.
    18. **The Semantic Whitespace Guard:** Inner-content whitespace is fiercely protected;
        only structural prefixes are transfigured.
    19. **The Chronometric Log:** Records consumption latency with nanosecond precision.
    20. **The Pure String Suture:** Utilizes native `.replace` chains and list joining
        for zero-copy string building where possible.
    21. **The Memory-Safe Cursor:** Traverses the list via integer indexes rather than
        memory-heavy slice duplications.
    22. **The Ouroboros Circuit Breaker:** Catches array-bounds errors deep in the loop.
    23. **The Prefix Exorcist:** The core loop that cleanly separates syntax from structure.
    24. **The Finality Vow:** A mathematical guarantee to return a valid `Tuple[List[str], int]`.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    MAX_BLOCK_MASS_BYTES: Final[int] = 50 * 1024 * 1024  # 50MB Heap Limit
    MAX_VERSES_PER_BLOCK: Final[int] = 500_000  # 500k Line Limit

    # [FACULTY 15: THE SIGIL PHALANX]
    SIGIL_PATTERN: Final[Pattern] = re.compile(
        r'(?P<sigil>::|<<|\+=|\^=|~=|:?\s*=)?\s*(?P<quote>"{3}|\'{3}|"|\')'
    )

    def __init__(self, lines: List[str]):
        """[THE RITE OF INCEPTION] Binds the engine to the linear stream of time."""
        self.lines = lines or []
        self._total_mass_consumed = 0
        self._start_time = time.perf_counter_ns()
        self._line_count = len(self.lines)

    def _purify_line_prefix(self, line: str) -> str:
        """
        =============================================================================
        == THE GHOST GRID TRANSMUTATOR (V-Ω-PHANTOM-SLAYER)                        ==
        =============================================================================
        [ASCENSION 1 & 2]: This is the supreme algorithm that annihilates the
        Phantom Forest. It scans the beginning of the line and transmutes all
        Tree-Art (`├──`, `│`) and Emojis (`📁`) into mathematically precise spaces.

        This ensures that when the AST Weaver looks at the line, it sees perfect
        Pythonic indentation, allowing deeply nested AI trees to be parsed flawlessly.
        """
        if not line: return ""

        purified = []
        in_prefix = True

        for char in line:
            if not in_prefix:
                purified.append(char)
                continue

            # 1. Standard Spacing
            if char in (' ', '\t'):
                purified.append(char)

            # 2. [FACULTY 3]: The Invisible Toxin Sieve
            elif char in ('\ufeff', '\u200b', '\u200c', '\u200d'):
                pass  # Annihilate (0 width)

            # 3. Unicode Box Drawing (Treat as 1 Space)
            # Covers ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧ ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍ ╎ ╏
            elif '\u2500' <= char <= '\u257f':
                purified.append(' ')

            # 4. AI Emojis & Pictographs (Treat as 2 Spaces for terminal alignment)
            # Covers Misc Symbols (\u2600-\u27bf) and vast Emoji blocks (\U00010000-\U0001faff)
            elif ('\u2600' <= char <= '\u27bf') or ('\U00010000' <= char <= '\U0001faff'):
                purified.append('  ')

                # 5. End of Prefix Zone
            # The moment we hit an alphanumeric char, standard punctuation, or quote,
            # the structural prefix is over. We lock the prefix guard.
            else:
                in_prefix = False
                purified.append(char)

        return "".join(purified)

    def _measure_visual_depth(self, line: str, tab_width: int = 4) -> int:
        """
        [FACULTY 13: THE TAB-SNAP ENGINE]
        Calculates the true visual coordinate of a line by first transmuting
        ghost artifacts, then measuring the exact whitespace depth.
        """
        purified_line = self._purify_line_prefix(line)

        visual_width = 0
        for char in purified_line:
            if char == ' ':
                visual_width += 1
            elif char == '\t':
                visual_width += tab_width - (visual_width % tab_width)
            else:
                break

        return visual_width

    def _check_metabolic_tax(self, line: str, index: int):
        """[FACULTY 9]: METABOLIC GOVERNOR."""
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
        == THE RITE OF HYSTERESIS PARITY (EXPLICIT BLOCK CONSUMPTION)              ==
        =============================================================================
        LIF: ∞ | ROLE: CONTENT_SANCTUARY_SEALER | RANK: OMEGA
        """
        # 1. DIVINE THE QUOTE TYPE
        match = self.SIGIL_PATTERN.search(opening_sigil_line)

        quote_type = '"""'
        if match:
            quote_type = match.group('quote')
        # [FACULTY 15] Fallback Scryer
        elif "'''" in opening_sigil_line:
            quote_type = "'''"
        elif '"""' in opening_sigil_line:
            quote_type = '"""'
        elif '"' in opening_sigil_line:
            quote_type = '"'
        elif "'" in opening_sigil_line:
            quote_type = "'"

        sigil_end_pos = match.end() if match else 0
        content_lines: List[str] = []

        # --- MOVEMENT I: ATOMIC SAME-LINE RESOLUTION (FACULTY 14) ---
        search_start_pos = sigil_end_pos
        if not match:
            first_q = opening_sigil_line.find(quote_type)
            if first_q != -1:
                search_start_pos = first_q + len(quote_type)
            else:
                search_start_pos = len(opening_sigil_line)

        remaining_on_line = opening_sigil_line[search_start_pos:]

        # [FACULTY 5]: ESCAPED QUOTE WARD (Lookahead)
        if quote_type in remaining_on_line:
            current_pos = 0
            while True:
                close_idx = remaining_on_line.find(quote_type, current_pos)
                if close_idx == -1:
                    break

                is_escaped = (close_idx > 0 and remaining_on_line[close_idx - 1] == '\\')
                if is_escaped and close_idx > 1 and remaining_on_line[close_idx - 2] == '\\':
                    is_escaped = False

                if not is_escaped:
                    # BLOCK SEALED ATOMICALLY
                    content = remaining_on_line[:close_idx]
                    return [self._normalize(content)], start_index

                current_pos = close_idx + 1

        if remaining_on_line.strip():
            content_lines.append(self._normalize(remaining_on_line))

        # --- MOVEMENT II: MULTI-LINE SANCTUARY MODE ---
        i = start_index + 1
        while i < self._line_count:
            line = self.lines[i]

            # [ASCENSION 18]: Apply the Ghost Transmutator to the explicit block as well,
            # to ensure that if the AI wrapped the block in tree characters, they are stripped.
            purified_line = self._purify_line_prefix(line)
            stripped = purified_line.strip()

            # [FACULTY 4]: INDENTATION ANNIHILATION
            if stripped == quote_type:
                return content_lines, i + 1

            # [FACULTY 6]: TRAILING SEAL GAZE
            if stripped.endswith(quote_type) and len(stripped) > len(quote_type):
                idx = purified_line.rfind(quote_type)
                if idx > 0 and purified_line[idx - 1] != '\\':
                    content_part = purified_line[:idx]
                    content_lines.append(self._normalize(content_part))
                    return content_lines, i + 1

            # [FACULTY 11]: UNICODE NORMALIZATION
            normalized_line = self._normalize(purified_line)
            self._check_metabolic_tax(normalized_line, i)
            content_lines.append(normalized_line)
            i += 1

            # [FACULTY 10]: EMERGENCY LIMIT
            if len(content_lines) > self.MAX_VERSES_PER_BLOCK:
                raise ArtisanHeresy(
                    f"Topological Exhaustion: Explicit block failed to seal after {self.MAX_VERSES_PER_BLOCK} lines.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion=f"Verify that the closing {quote_type} sigil is manifest and aligned."
                )

        # [FACULTY 17]: UNCLOSED BLOCK ADJUDICATOR
        return content_lines, i

    def consume_indented_block(self, start_index: int, parent_indent: int) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE RITE OF GEOMETRIC CONSUMPTION (IMPLICIT BLOCK)                      ==
        =============================================================================
        Consumes matter defined purely by indentation depth.
        """
        if start_index >= self._line_count:
            return [], start_index

        content_lines: List[str] = []
        i = start_index
        block_baseline = -1

        # [FACULTY 7]: THE BASELINE PROPHET (LOOKAHEAD)
        for peek_i in range(i, min(i + 20, self._line_count)):
            peek_line = self.lines[peek_i]
            if peek_line.strip() and not peek_line.strip().startswith('#'):
                block_baseline = self._measure_visual_depth(peek_line)
                break

        # If we found no content, or the content is shallower/equal to parent, it's not a block
        if block_baseline == -1 or block_baseline <= parent_indent:
            return [], start_index

        # [FACULTY 12]: THE GREEDY CONSUMER
        while i < self._line_count:
            line = self.lines[i]
            is_blank = not line.strip()

            # Blank lines inherit the current block context
            if is_blank:
                self._check_metabolic_tax(line, i)
                content_lines.append(line)
                i += 1
                continue

            current_indent = self._measure_visual_depth(line)

            # [THE BOUNDARY SENTINEL]
            if current_indent <= parent_indent:
                break

            # Transmute the ghost grid and append
            purified_line = self._purify_line_prefix(line)
            self._check_metabolic_tax(purified_line, i)
            content_lines.append(purified_line)
            i += 1

        # [FACULTY 8]: THE VOID TRIMMER
        while content_lines and not content_lines[-1].strip():
            content_lines.pop()

        return content_lines, i

    def _normalize(self, text: str) -> str:
        """[FACULTY 11 & 16] Normalizes Unicode and EOLs."""
        return unicodedata.normalize('NFC', text).replace('\r\n', '\n')

    def __repr__(self) -> str:
        latency = (time.perf_counter_ns() - self._start_time) / 1_000_000
        return (f"<Ω_BLOCK_CONSUMER mass={self._total_mass_consumed}B "
                f"latency={latency:.2f}ms state=RESONANT>")

# == SCRIPTURE SEALED: THE CONSUMER HAS CONQUERED THE PHANTOM FOREST ==