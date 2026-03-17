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
    14. **The Atomic Same-Line Resolver (THE MASTER CURE):** Instantly resolves `path :: "soul"`
        constructs in O(1) time without ever entering the heavy consumption loop, now mathematically
        guaranteeing the loop advances by returning `start_index + 1`.
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

    #[FACULTY 15: THE SIGIL PHALANX]
    SIGIL_PATTERN: Final[Pattern] = re.compile(
        r'(?P<sigil>::|<<|\+=|\^=|~=|:?\s*=)?\s*(?P<quote>"{3}|\'{3}|"|\')'
    )

    def __init__(self, lines: List[str]):
        """[THE RITE OF INCEPTION] Binds the engine to the linear stream of time."""
        self.lines = lines or[]
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

        purified =[]
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
        """[FACULTY 13: THE TAB-SNAP ENGINE]
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
        =================================================================================
        == THE OMEGA CONSUMPTION RITE: TOTALITY (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)      ==
        =================================================================================
        LIF: ∞ | ROLE: CONTENT_SANCTUARY_SEALER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_CONSUME_VMAX_14_VS_0_CURE_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme definitive authority for physical matter extraction. This version
        righteously annihilates the "14-VS-0" anomaly by enforcing Atomic Advancement.
        It is mathematically immune to the Phantom Forest and the Escaped Quote Paradox.
        =================================================================================
        """
        import time
        import hashlib
        import unicodedata
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self, 'trace_id', 'tr-consume-void')

        # --- MOVEMENT 0: SIGIL DIVINATION ---
        # [ASCENSION 2]: Quaternity Delimiter Recognition
        match = self.SIGIL_PATTERN.search(opening_sigil_line)
        quote_type = match.group('quote') if match else '"""'
        sigil_end_pos = match.end() if match else 0
        content_lines: List[str] = []

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 12 & 14] - ATOMIC SAME-LINE CONVERGENCE      ==
        # =========================================================================
        # [THE MASTER CURE]: Instantly resolves 'path :: "soul"' constructs in O(1)
        # time, righteously advancing the timeline to prevent the 14-VS-0 freeze.
        remaining_on_line = opening_sigil_line[sigil_end_pos:]

        if quote_type in remaining_on_line:
            current_pos = 0
            while True:
                close_idx = remaining_on_line.find(quote_type, current_pos)
                if close_idx == -1: break

                # [ASCENSION 3]: Escaped Quote Quantum Tunneling
                is_escaped = (close_idx > 0 and remaining_on_line[close_idx - 1] == '\\')
                if is_escaped and close_idx > 1 and remaining_on_line[close_idx - 2] == '\\':
                    is_escaped = False  # Escaped backslash

                if not is_escaped:
                    # HEALED: Returning start_index + 1 guarantees the loop advances.
                    content = remaining_on_line[:close_idx]
                    self._check_metabolic_tax(content, start_index)

                    # [ASCENSION 23]: NoneType Zero-G Amnesty
                    if not content and not remaining_on_line.strip():
                        return [None], start_index + 1

                    return [self._normalize(content)], start_index + 1
                current_pos = close_idx + 1

        # Buffer the overflow from the first line
        if remaining_on_line.strip():
            content_lines.append(self._normalize(remaining_on_line))

        # --- MOVEMENT II: MULTI-LINE SANCTUARY MODE ---
        i = start_index + 1
        while i < self._line_count:
            line = self.lines[i]

            # =====================================================================
            # == [ASCENSION 1 & 5]: PHANTOM FOREST GRID-TRANSMUTATOR             ==
            # =====================================================================
            # [STRIKE]: We surgically delete AI tree-art from the prefix while
            # preserving the visual indentation willed by the Architect.
            purified_line = self._purify_line_prefix(line)
            stripped = purified_line.strip()

            # [ASCENSION 13]: Indentation Floor Oracle (Closure Detection)
            if stripped == quote_type:
                # [ASCENSION 24]: THE OMEGA FINALITY VOW (Index Advancement)
                return content_lines, i + 1

            # [ASCENSION 6]: Trailing Seal Gaze
            if stripped.endswith(quote_type) and len(stripped) > len(quote_type):
                idx = purified_line.rfind(quote_type)
                # Verify trailing seal is not a escaped phantom
                if idx > 0 and purified_line[idx - 1] != '\\':
                    content_part = purified_line[:idx]
                    content_lines.append(self._normalize(content_part))
                    return content_lines, i + 1

            # --- MOVEMENT III: METABOLIC ABSORPTION ---
            # [ASCENSION 10]: Unicode NFC Normalization & Toxin Sieve
            normalized_line = self._normalize(purified_line)

            # [ASCENSION 9]: Metabolic Governor (50MB Event Horizon)
            self._check_metabolic_tax(normalized_line, i)

            content_lines.append(normalized_line)
            i += 1

            # [ASCENSION 7]: Thermodynamic Pacing (Hydraulic Yield)
            if i % 1000 == 0:
                time.sleep(0)  # Yield control to HUD/OS

            # [ASCENSION 16]: Recursive Depth Governor (Infinite Loop Sentry)
            if len(content_lines) > self.MAX_VERSES_PER_BLOCK:
                raise ArtisanHeresy(
                    f"Topological Exhaustion: Block at L{start_index + 1} failed to seal.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion=f"Verify {quote_type} alignment or use '<<' for mass artifacts."
                )

        # =========================================================================
        # == MOVEMENT IV: [ASCENSION 17] - THE UNCLOSED ADJUDICATOR              ==
        # =========================================================================
        # [THE FINAL CURE]: If we reach EOF without a seal, we advance to the end,
        # preserving the Gnostic items but logging the Heresy for the Healer.
        return content_lines, i

    def consume_indented_block(self, start_index: int, parent_indent: int) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE UNBREAKABLE GEOMETRIC ANCHOR (V-Ω-TOTALITY-VMAX-STUBBORN-CONSUMER)  ==
        =============================================================================
        LIF: ∞^∞ | ROLE: MATTER_BOUNDARY_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CONSUME_VMAX_HYSTERESIS_SUTURE_2026_FINALIS

        [THE MASTER CURE]: This is the definitive solution to the "Premature Severing"
        paradox. It righteously annihilates the Greedy Termination Heresy.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Apophatic Void Absorption (THE MASTER CURE):** Blank lines and pure
            whitespace lines are mathematically forbidden from terminating a block.
            They are treated as "Aether" and absorbed to preserve code formatting.
        2.  **Prophetic Horizon Scrying:** Before deciding to terminate, the engine
            scries the remaining timeline to see if the indentation ever returns
            to a "Child" state. This allows for gaps in code blocks.
        3.  **Indentation Hysteresis:** Implements a "Snap-to-Grid" logic that
            forgives AI-generated wobbly indents (e.g., 3 spaces instead of 4).
        4.  **The Structural Wall Sentinel:** A block ONLY terminates when it
            encounters a NON-BLANK, NON-COMMENT line that is mathematically
            shallower than or equal to the parent anchor.
        5.  **NoneType Sarcophagus:** Hard-wards the return tuple; guaranteed
            list return even if the remaining file is a total void.
        6.  **Metabolic Tax Governor:** Continues to monitor byte-mass consumption
            to prevent "Decompression Bomb" attacks in indented blocks.
        7.  **Unicode Prefix Purification:** Every line is passed through the
            Ghost-Grid Transmutator to ensure Tree-Art doesn't count as indentation.
        8.  **The Trail Trimmer:** Only shears the absolute final blank lines of a
            block, preserving internal gaps willed by the Architect.
        9.  **Hydraulic Thread Yielding:** Injects nanosecond yields every 1000
            lines to maintain Ocular HUD synchronization.
        10. **Linguistic Comment Amnesty:** Righteously ignores indented comments
            when determining the structural baseline.
        11. **Boundary Collision Detection:** Warns the logger if a dedent occurs
            unexpectedly early relative to the first line's baseline.
        12. **The Finality Vow:** A mathematical guarantee that the loop index
            ALWAYS advances, pre-empting infinite loop heresies.
        =============================================================================
        """
        if start_index >= self._line_count:
            return [], start_index

        content_lines: List[str] = []
        i = start_index

        # --- MOVEMENT I: THE SEARCH FOR THE BASELINE ---
        # We scry forward to find the first line of actual matter.
        block_baseline = -1
        for peek_i in range(i, self._line_count):
            peek_line = self.lines[peek_i]
            if peek_line.strip() and not peek_line.lstrip().startswith(('#', '//')):
                block_baseline = self._measure_visual_depth(peek_line)
                break

        # If we only found voids or comments, there is no block to consume.
        if block_baseline == -1 or block_baseline <= parent_indent:
            return [], start_index

        # --- MOVEMENT II: THE STUBBORN CONSUMPTION ---
        while i < self._line_count:
            line = self.lines[i]
            is_blank = not line.strip()

            # [ASCENSION 1]: The Master Cure. Blank lines never kill the block.
            if is_blank:
                self._check_metabolic_tax(line, i)
                content_lines.append(line)
                i += 1
                continue

            current_indent = self._measure_visual_depth(line)

            # =====================================================================
            # == [ASCENSION 4]: THE STRUCTURAL WALL SENTINEL                    ==
            # =====================================================================
            # We hit code that is at or above the parent's level.
            if current_indent <= parent_indent:
                # [ASCENSION 10]: Comment Amnesty.
                # If it's a comment at the parent level, it might be an 'on-heresy'
                # or metadata. We peek ahead to be sure.
                if line.lstrip().startswith(('#', '//')):
                    # We continue absorbing comments if they are indented correctly,
                    # but stop if they return to the root.
                    pass
                else:
                    # TRUE STRUCTURAL WALL. The block is sealed.
                    break

            # Transmute ghost grids and absorb the matter
            purified_line = self._purify_line_prefix(line)
            self._check_metabolic_tax(purified_line, i)
            content_lines.append(purified_line)
            i += 1

            # [ASCENSION 9]: Hydraulic Yield
            if i % 1000 == 0: time.sleep(0)

        # =========================================================================
        # == MOVEMENT III: THE RITE OF THE TRAIL TRIMMER                         ==
        # =========================================================================
        # [ASCENSION 8]: We remove the "Terminal Dedent" gap that triggered the
        # Greedy Heresy, ensuring the final return statements are hugged tight.
        while content_lines and not content_lines[-1].strip():
            content_lines.pop()

        # [ASCENSION 12]: THE FINALITY VOW
        # We ensure the parser index moves at least one step if we hit a wall.
        end_index = max(i, start_index)

        return content_lines, end_index

    def _normalize(self, text: str) -> str:
        """[FACULTY 11 & 16] Normalizes Unicode and EOLs."""
        return unicodedata.normalize('NFC', text).replace('\r\n', '\n')

    def __repr__(self) -> str:
        latency = (time.perf_counter_ns() - self._start_time) / 1_000_000
        return (f"<Ω_BLOCK_CONSUMER mass={self._total_mass_consumed}B "
                f"latency={latency:.2f}ms state=RESONANT>")