# Path: core/lsp/utils/position.py
# -------------------------------
from ..types.primitives import Position, Range

class PositionMath:
    """
    [THE GEOMETRIC RULER]
    Static utilities for comparing and calculating document spacetime.
    """
    @staticmethod
    def is_before(pos1: Position, pos2: Position) -> bool:
        if pos1.line < pos2.line: return True
        if pos1.line == pos2.line: return pos1.character < pos2.character
        return False

    @staticmethod
    def is_in_range(pos: Position, rng: Range) -> bool:
        # Check if pos is at or after start
        after_start = not PositionMath.is_before(pos, rng.start)
        # Check if pos is at or before end
        before_end = not PositionMath.is_before(rng.end, pos)
        return after_start and before_end

    @staticmethod
    def range_from_coords(line1, char1, line2, char2) -> Range:
        return Range(
            start=Position(line=line1, character=char1),
            end=Position(line=line2, character=char2)
        )