# Path: src/velm/parser_core/lexer_core/deconstructor/state.py
# ------------------------------------------------------------

from typing import List, Dict, Any, Final
from ..contracts import Token


class DeconstructionState:
    """
    =============================================================================
    == THE DECONSTRUCTION STATE (V-Ω-ZERO-ALLOCATION-CURSOR)                   ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_STREAM_TRACKER | RANK: OMEGA_GUARDIAN

    A purely ephemeral, zero-overhead tracking object. It encapsulates the token
    stream and the current cursor, allowing the decoupled Handlers to mutate the
    parsing state without returning complex tuples.
    """

    __slots__ = ('tokens', 'cursor', 'variables', 'length')

    def __init__(self, tokens: List[Token], variables: Dict[str, Any]):
        self.tokens = tokens
        self.length = len(tokens)
        self.cursor = 0
        self.variables = variables

    def current(self) -> getattr(Token, '__class__', Any):
        """Returns the token at the active cursor, or None if the void is reached."""
        if self.cursor < self.length:
            return self.tokens[self.cursor]
        return None

    def advance(self):
        """Moves the cursor forward by one atom."""
        self.cursor += 1

    def peek(self) -> getattr(Token, '__class__', Any):
        """Gazes into the future by one atom without shifting the cursor."""
        if self.cursor + 1 < self.length:
            return self.tokens[self.cursor + 1]
        return None

    def __repr__(self) -> str:
        return f"<Ω_DECONSTRUCTION_STATE pos={self.cursor}/{self.length} status=RESONANT>"