# Path: core/alchemist/elara/scanner/buffer/cursor.py
# ---------------------------------------------------

class SpatiotemporalCursor:
    """
    =============================================================================
    == THE SPATIOTEMPORAL CURSOR (V-Ω-GEOMETRIC-TRACKER)                       ==
    =============================================================================
    LIF: ∞ | ROLE: COORDINATE_CALCULATOR
    """

    __slots__ = ('text', 'cursor', '_line_base', '_line_count')

    def __init__(self, text: str):
        self.text = text
        self.cursor = 0
        self._line_base = 0
        self._line_count = 1

    def advance(self, chunk: str, count: int):
        """Updates internal tomography based on consumed chunk."""
        newlines = chunk.count('\n')
        if newlines > 0:
            self._line_count += newlines
            self._line_base = self.cursor + chunk.rfind('\n') + 1
        self.cursor += count

    @property
    def current_line(self) -> int:
        return self._line_count

    @property
    def current_col(self) -> int:
        """The visual column index, transmuting tabs to Gnostic units."""
        fragment = self.text[self._line_base: self.cursor]
        col = 0
        for char in fragment:
            if char == '\t':
                col += 4 - (col % 4)
            else:
                col += 1
        return col

    def reset(self):
        self.cursor = 0
        self._line_base = 0
        self._line_count = 1