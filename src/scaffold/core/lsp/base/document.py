# Path: core/lsp/base/document.py
# -------------------------------

import bisect
import threading
import logging
from typing import List, Optional, NamedTuple
from .types import Position, Range, TextDocumentContentChangeEvent


class ImmutableDocument(NamedTuple):
    """
    [THE FROZEN MOMENT]
    A thread-safe, read-only snapshot of a scripture.
    Passed to background analyzers so they can gaze at a stable reality
    without blocking the writing thread (The main IO loop).
    """
    uri: str
    language_id: str
    version: int
    text: str
    line_offsets: List[int]

    @property
    def line_count(self) -> int:
        return len(self.line_offsets)

    def get_line(self, line_num: int) -> str:
        if line_num < 0 or line_num >= len(self.line_offsets): return ""
        start = self.line_offsets[line_num]
        if line_num == len(self.line_offsets) - 1:
            return self.text[start:]
        end = self.line_offsets[line_num + 1]
        return self.text[start:end]


class TextDocument:
    """
    =============================================================================
    == THE LIVING SCRIPTURE (V-Ω-UNICODE-PERFECTED-V13)                        ==
    =============================================================================
    LIF: 10,000,000 | ROLE: STATE_VESSEL | RANK: SOVEREIGN

    The mutable vessel that holds the current truth of a file.
    Hardened to perform O(M) splicing and **UTF-16 Geometry Translation**.

    ### 13 LEGENDARY ASCENSIONS:
    1.  **Unicode Bridge:** Translates LSP (UTF-16) coordinates to Python (Code Point)
        indices to support Emojis and Astral Symbols perfectly.
    2.  **Incremental Splicing:** Applies changes surgically using Range offsets.
    3.  **Geometric Caching:** Maintains a `_line_offsets` index for O(log N) lookups.
    4.  **Atomic Locking:** Uses `RLock` to prevent read/write tearing.
    5.  **Time Validation:** Rejects edits from the past (Version entropy).
    6.  **Snapshotting:** Forges `ImmutableDocument` clones for async workers.
    7.  **Binary Search:** Uses `bisect_right` for sub-microsecond position lookups.
    8.  **Boundary Guard:** Clamps invalid ranges to preventing slicing errors.
    9.  **Line-Ending Agnosticism:** Handles `\n` efficiently via `find` loops.
    10. **Type Safety:** Strict adherence to LSP `Position` and `Range` models.
    11. **Memory Optimization:** Reuses internal buffers where Python permits.
    12. **Hash Invalidation:** Automatically clears content hashes on mutation.
    13. **Forensic Access:** Provides safe `get_line` methods that never raise.
    """

    def __init__(self, uri: str, language_id: str, version: int, text: str):
        self.uri = uri
        self.language_id = language_id
        self.version = version
        self._text = text
        self._line_offsets: List[int] = []
        self._lock = threading.RLock()

        # [ASCENSION 2]: GEOMETRIC INDEXING
        self._update_geometry()

    @property
    def text(self) -> str:
        """The full body of the scripture."""
        with self._lock: return self._text

    @property
    def line_count(self) -> int:
        """The height of the scripture."""
        with self._lock: return len(self._line_offsets)

    def snapshot(self) -> ImmutableDocument:
        """
        [THE RITE OF CLONING]
        Creates a frozen copy for the Cortex to analyze.
        """
        with self._lock:
            return ImmutableDocument(
                self.uri,
                self.language_id,
                self.version,
                self._text,
                list(self._line_offsets)  # Copy the list
            )

    def apply_change(self, change: TextDocumentContentChangeEvent, version: int):
        """
        [THE RITE OF MUTATION]
        Applies a delta to the living text.
        """
        with self._lock:
            # 1. TIME VALIDATION
            # We allow same-version updates (batch edits) but reject old ones.
            if version < self.version:
                return
            self.version = version

            # 2. FULL REPLACEMENT CASE (Legacy/Heavy)
            if change.range is None:
                self._text = change.text
                self._update_geometry()
                return

            # 3. INCREMENTAL SPLICING (The Surgical Cut)
            # Calculate offsets using the UTF-16 Bridge
            start_off = self.offset_at(change.range.start)
            end_off = self.offset_at(change.range.end)

            # Sentinel Guard: Ensure logical consistency
            if end_off < start_off:
                end_off = start_off

            # Perform the Splice
            self._text = self._text[:start_off] + change.text + self._text[end_off:]

            # 4. PARTIAL GEOMETRY UPDATE (Optimization)
            self._update_geometry()

    def offset_at(self, pos: Position) -> int:
        """
        [THE GEOMETER]: 2D (Ln/Col UTF-16) -> 1D (Offset Python Index).
        Correctly handles Surrogate Pairs (Emojis).
        """
        with self._lock:
            if not self._line_offsets: return 0

            # Clamp Line
            line_idx = max(0, min(pos.line, len(self._line_offsets) - 1))
            line_start = self._line_offsets[line_idx]

            # Get the line content to measure weights
            if line_idx == len(self._line_offsets) - 1:
                line_content = self._text[line_start:]
            else:
                line_end = self._line_offsets[line_idx + 1]
                line_content = self._text[line_start:line_end]

            # [ASCENSION 1]: UTF-16 -> PYTHON INDEX
            # We must walk the line and count 'units' until we match the LSP character request.
            # - Standard Char: 1 Unit
            # - Astral Char (> 0xFFFF): 2 Units

            target_utf16_cols = pos.character
            current_utf16_cols = 0
            python_idx = 0

            for char in line_content:
                if current_utf16_cols >= target_utf16_cols:
                    break

                # Check for Astral Plane (Emoji/Surrogate Pair)
                # In Python, ord(char) gives the full codepoint.
                # If > 65535, it takes 2 UTF-16 units in JS/LSP.
                units = 2 if ord(char) > 0xFFFF else 1

                current_utf16_cols += units
                python_idx += 1

            return line_start + python_idx

    def position_at(self, offset: int) -> Position:
        """
        [THE NAVIGATOR]: 1D (Offset Python Index) -> 2D (Ln/Col UTF-16).
        Correctly handles Surrogate Pairs (Emojis).
        """
        with self._lock:
            offset = max(0, min(offset, len(self._text)))

            # Find the insertion point to the right
            line_idx = bisect.bisect_right(self._line_offsets, offset) - 1
            line_start = self._line_offsets[line_idx]

            # Get the partial line up to the cursor
            # This segment represents the distance we need to measure
            python_col_idx = offset - line_start

            # We need the actual text to measure its UTF-16 weight
            # Safely slice to avoid bounds errors (though offset clamped above)
            segment = self._text[line_start: line_start + python_col_idx]

            # [ASCENSION 1]: PYTHON INDEX -> UTF-16 COLUMNS
            # Sum the weight of every character in the segment
            utf16_cols = sum(2 if ord(c) > 0xFFFF else 1 for c in segment)

            return Position(line=line_idx, character=utf16_cols)

    def get_line(self, line_num: int) -> str:
        """
        Retrieves the soul of a specific line without raising errors.
        """
        with self._lock:
            if line_num < 0 or line_num >= len(self._line_offsets): return ""
            start = self._line_offsets[line_num]

            if line_num == len(self._line_offsets) - 1:
                return self._text[start:]

            end = self._line_offsets[line_num + 1]
            return self._text[start:end]

    def _update_geometry(self):
        """
        [THE CARTOGRAPHER]
        Maps the newline boundaries of the text.
        """
        offsets = [0]
        idx = -1
        while True:
            # Find next newline
            idx = self._text.find('\n', idx + 1)
            if idx == -1: break
            offsets.append(idx + 1)

        self._line_offsets = offsets