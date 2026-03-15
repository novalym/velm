# Path: core/alchemist/elara/scanner/buffer/engine.py
# ---------------------------------------------------

import time
import os
import sys
import gc
import threading
from typing import Final, Optional, Dict, Any

from ......logger import Scribe
from .cursor import SpatiotemporalCursor

Logger = Scribe("HydraulicBuffer")


class HydraulicBuffer:
    """
    =============================================================================
    == THE HYDRAULIC BUFFER (V-Ω-TOTALITY-VMAX-36-ASCENSIONS)                  ==
    =============================================================================
    LIF: ∞^∞ | ROLE: MATTER_STREAM_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME

    [THE MANIFESTO]
    Provides the L1 Scanner with a high-pressure, zero-copy conduit to the raw
    text stream. Inherits its dimensional logic directly from the SpatiotemporalCursor.
    """

    __slots__ = ('text', 'length', 'cursor_mgr', '_start_ns')

    def __init__(self, text: Optional[str]):
        """[THE RITE OF INCEPTION]"""
        self.text: str = text if text is not None else ""
        self.length: int = len(self.text)

        # [ASCENSION 1]: Isomorphic Cursor Engine Integration
        self.cursor_mgr = SpatiotemporalCursor(self.text)
        self._start_ns: int = time.perf_counter_ns()

    def peek(self, chars: int = 1) -> str:
        """Perceives the future of the stream without moving the cursor."""
        if self.cursor_mgr.cursor >= self.length:
            return ""
        return self.text[self.cursor_mgr.cursor: self.cursor_mgr.cursor + chars]

    def peek_until(self, substring: str) -> int:
        """Scries the stream for the next occurrence of a pattern."""
        idx = self.text.find(substring, self.cursor_mgr.cursor)
        if idx == -1: return -1
        return idx - self.cursor_mgr.cursor

    def consume(self, chars: int = 1) -> str:
        """Moves the cursor forward and returns the consumed matter."""
        if self.cursor_mgr.cursor >= self.length:
            return ""

        count = min(chars, self.length - self.cursor_mgr.cursor)
        chunk = self.text[self.cursor_mgr.cursor: self.cursor_mgr.cursor + count]

        self.cursor_mgr.advance(chunk, count)
        return chunk

    def consume_until(self, offset: int) -> str:
        """Surgically consumes a chunk up to a specific offset."""
        if offset <= 0: return ""
        return self.consume(offset)

    def is_exhausted(self) -> bool:
        """Adjudicates if the stream has reached the void."""
        return self.cursor_mgr.cursor >= self.length

    @property
    def remaining_mass(self) -> int:
        return self.length - self.cursor_mgr.cursor

    @property
    def cursor(self) -> int:
        return self.cursor_mgr.cursor

    @property
    def current_line(self) -> int:
        return self.cursor_mgr.current_line

    @property
    def current_col(self) -> int:
        return self.cursor_mgr.current_col

    def reset(self):
        """Temporal Reversal. Returns the cursor to the primordial origin."""
        self.cursor_mgr.reset()
        self._start_ns = time.perf_counter_ns()

    def tomography(self) -> Dict[str, Any]:
        """METABOLIC TOMOGRAPHY. Proclaims stream health."""
        duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000
        return {
            "total_mass_bytes": self.length,
            "cursor_pos": self.cursor_mgr.cursor,
            "line": self.current_line,
            "col": self.current_col,
            "latency_ms": round(duration_ms, 4),
            "pressure": round(self.cursor_mgr.cursor / max(1, self.length), 4)
        }

    def __repr__(self) -> str:
        return f"<Ω_HYDRAULIC_BUFFER pos={self.cursor}/{self.length} status=LAMINAR>"