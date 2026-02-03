# Path: core/lsp/features/semantic_tokens/encoder.py
# --------------------------------------------------

from typing import List, Tuple, NamedTuple


class RawToken(NamedTuple):
    line: int
    start: int
    length: int
    token_type: int
    modifiers: int


class SemanticEncoder:
    """
    [THE GEOMETER]
    The algorithm that transmutes absolute positions into delta-encoded integers.
    """

    @staticmethod
    def encode(tokens: List[RawToken]) -> List[int]:
        # 1. THE MONOTONICITY VOW: Must be sorted by line, then char.
        sorted_tokens = sorted(tokens, key=lambda t: (t.line, t.start))

        encoded_data = []
        prev_line = 0
        prev_char = 0

        for t in sorted_tokens:
            line_delta = t.line - prev_line

            if line_delta > 0:
                char_delta = t.start
            else:
                char_delta = t.start - prev_char

            # [LSP PACK FORMAT]: 5 integers per token
            encoded_data.extend([
                line_delta,
                char_delta,
                t.length,
                t.token_type,
                t.modifiers
            ])

            prev_line = t.line
            prev_char = t.start

        return encoded_data