# Path: core/lsp/utils/validation.py
# ---------------------------------
from typing import Any
from ..types import Position, Range

class Validator:
    @staticmethod
    def is_valid_position(pos: Any) -> bool:
        return (
            hasattr(pos, 'line') and isinstance(pos.line, int) and pos.line >= 0 and
            hasattr(pos, 'character') and isinstance(pos.character, int) and pos.character >= 0
        )

    @staticmethod
    def is_valid_range(rng: Any) -> bool:
        return (
            hasattr(rng, 'start') and Validator.is_valid_position(rng.start) and
            hasattr(rng, 'end') and Validator.is_valid_position(rng.end)
        )