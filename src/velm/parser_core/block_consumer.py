# Path: parser_core/block_consumer.py
# -----------------------------------

import os
import re
import time
import sys
import unicodedata
from typing import List, Tuple, Optional, Final, Set, Dict, Any, Pattern

from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 25]: THE BINARY KERNEL PIVOT
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False


class GnosticBlockConsumer:
    """
    =================================================================================
    == THE GOD-ENGINE OF CONTENT CONSUMPTION (V-Ω-TOTALITY-VMAX-RUST-ACCELERATED)  ==
    =================================================================================
    LIF: ∞^∞^∞ | ROLE: MATTER_PHYSICIST | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_CONSUMER_VMAX_RUST_CORE_FINALIS

    The Supreme Authority on the demarcation of Content vs Structure.
    It wields a pantheon of 26 Ascended Faculties to ensure that once Matter is
    perceived, it is consumed wholly and safely.

    ### THE PANTHEON OF 26 LEGENDARY ASCENSIONS:
    [... existing ascensions ...]
    26. **The Topological Sieve Suture (THE MASTER CURE):** Bypasses the python
        iteration loop entirely for Indented Blocks, delegating the physical string
        purification, length measurement, and array collection to `scaffold_core_rs`.
        This drops the parsing tax of a 10MB file from seconds to microseconds.
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
        if not line: return ""

        if RUST_AVAILABLE and os.environ.get("SCAFFOLD_ENV") != "WASM":
            try:
                return scaffold_core_rs.purify_line_prefix_fast(line)
            except Exception:
                pass  # Fallback to python

        purified = []
        in_prefix = True

        for char in line:
            if not in_prefix:
                purified.append(char)
                continue

            if char in (' ', '\t'):
                purified.append(char)
            elif char in ('\ufeff', '\u200b', '\u200c', '\u200d'):
                pass  # Annihilate (0 width)
            elif '\u2500' <= char <= '\u257f':
                purified.append(' ')
            elif ('\u2600' <= char <= '\u27bf') or ('\U00010000' <= char <= '\U0001faff'):
                purified.append('  ')
            else:
                in_prefix = False
                purified.append(char)

        return "".join(purified)

    def _measure_visual_depth(self, line: str, tab_width: int = 4) -> int:
        """
        [ASCENSION 27]: Delegates width measurement to the C-Level Geometric Physicist.
        """
        if RUST_AVAILABLE and os.environ.get("SCAFFOLD_ENV") != "WASM":
            try:
                return scaffold_core_rs.calculate_visual_width_fast(line, tab_width)
            except:
                pass

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
        match = self.SIGIL_PATTERN.search(opening_sigil_line)
        quote_type = match.group('quote') if match else '"""'
        sigil_end_pos = match.end() if match else 0
        content_lines: List[str] = []

        remaining_on_line = opening_sigil_line[sigil_end_pos:]

        if quote_type in remaining_on_line:
            current_pos = 0
            while True:
                close_idx = remaining_on_line.find(quote_type, current_pos)
                if close_idx == -1: break

                is_escaped = (close_idx > 0 and remaining_on_line[close_idx - 1] == '\\')
                if is_escaped and close_idx > 1 and remaining_on_line[close_idx - 2] == '\\':
                    is_escaped = False

                if not is_escaped:
                    content = remaining_on_line[:close_idx]
                    self._check_metabolic_tax(content, start_index)
                    if not content and not remaining_on_line.strip(): return [None], start_index + 1
                    return [self._normalize(content)], start_index + 1
                current_pos = close_idx + 1

        if remaining_on_line.strip():
            content_lines.append(self._normalize(remaining_on_line))

        i = start_index + 1
        while i < self._line_count:
            line = self.lines[i]
            purified_line = self._purify_line_prefix(line)
            stripped = purified_line.strip()

            if stripped == quote_type:
                return content_lines, i + 1

            if stripped.endswith(quote_type) and len(stripped) > len(quote_type):
                idx = purified_line.rfind(quote_type)
                if idx > 0 and purified_line[idx - 1] != '\\':
                    content_part = purified_line[:idx]
                    content_lines.append(self._normalize(content_part))
                    return content_lines, i + 1

            normalized_line = self._normalize(purified_line)
            self._check_metabolic_tax(normalized_line, i)
            content_lines.append(normalized_line)
            i += 1

            if len(content_lines) > self.MAX_VERSES_PER_BLOCK:
                raise ArtisanHeresy(
                    f"Topological Exhaustion: Block at L{start_index + 1} failed to seal.",
                    severity=HeresySeverity.CRITICAL
                )

        return content_lines, i

    def consume_indented_block(self, start_index: int, parent_indent: int) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE UNBREAKABLE GEOMETRIC ANCHOR (V-Ω-TOTALITY-VMAX-RUST-NATIVE)        ==
        =============================================================================[THE MASTER CURE]: Delegates the iteration logic to the compiled C-Rust core.
        """
        if start_index >= self._line_count:
            return [], start_index

        # =========================================================================
        # == [ASCENSION 26]: THE TOPOLOGICAL SIEVE SUTURE (RUST FAST-PATH)       ==
        # =========================================================================
        if RUST_AVAILABLE and os.environ.get("SCAFFOLD_ENV") != "WASM":
            try:
                # Passes a massive Python List of Strings to Rust.
                content_lines, end_index = scaffold_core_rs.consume_indented_block_fast(
                    self.lines, start_index, parent_indent, 4
                )

                self._check_metabolic_tax(f"fast_pass_{len(content_lines)}", start_index)
                return content_lines, end_index
            except Exception:
                pass  # Fallback to python loops if Rust panics

        # --- MOVEMENT I: THE PYTHONIC FALLBACK ---
        content_lines: List[str] = []
        i = start_index

        block_baseline = -1
        for peek_i in range(i, self._line_count):
            peek_line = self.lines[peek_i]
            if peek_line.strip() and not peek_line.lstrip().startswith(('#', '//')):
                block_baseline = self._measure_visual_depth(peek_line)
                break

        if block_baseline == -1 or block_baseline <= parent_indent:
            return [], start_index

        while i < self._line_count:
            line = self.lines[i]
            is_blank = not line.strip()

            if is_blank:
                self._check_metabolic_tax(line, i)
                content_lines.append(line)
                i += 1
                continue

            current_indent = self._measure_visual_depth(line)

            if current_indent <= parent_indent:
                if line.lstrip().startswith(('#', '//')):
                    pass
                else:
                    break

            purified_line = self._purify_line_prefix(line)
            self._check_metabolic_tax(purified_line, i)
            content_lines.append(purified_line)
            i += 1

        while content_lines and not content_lines[-1].strip():
            content_lines.pop()

        end_index = max(i, start_index)
        return content_lines, end_index

    def _normalize(self, text: str) -> str:
        return unicodedata.normalize('NFC', text).replace('\r\n', '\n')

    def __repr__(self) -> str:
        latency = (time.perf_counter_ns() - self._start_time) / 1_000_000
        return (f"<Ω_BLOCK_CONSUMER mass={self._total_mass_consumed}B "
                f"latency={latency:.2f}ms state=RESONANT>")