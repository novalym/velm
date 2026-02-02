# Path: core/lsp/base/features/semantic_tokens/differ.py
# ------------------------------------------------------

from typing import List, Union
from .models import SemanticTokensDelta, SemanticTokensEdit


class TokenDiffer:
    """
    =============================================================================
    == THE DIFFERENTIAL ENGINE (V-Ω-OPTIMIZED-DIFF)                            ==
    =============================================================================
    LIF: 10,000,000 | ROLE: BANDWIDTH_SAVER

    Calculates the minimal set of Edits to transform `old_tokens` into `new_tokens`.
    Optimized for LSP Semantic Token arrays (integers).
    """

    @staticmethod
    def compute_delta(previous_id: str, old_data: List[int], new_data: List[int]) -> SemanticTokensDelta:
        edits: List[SemanticTokensEdit] = []

        old_len = len(old_data)
        new_len = len(new_data)

        # 1. FIND COMMON PREFIX
        start_offset = 0
        while (start_offset < old_len and start_offset < new_len and
               old_data[start_offset] == new_data[start_offset]):
            start_offset += 1

        # If identical
        if start_offset == old_len and start_offset == new_len:
            return SemanticTokensDelta(resultId=previous_id, edits=[])

        # 2. FIND COMMON SUFFIX
        # We must not overlap with the prefix
        end_offset = 0
        while (end_offset < (old_len - start_offset) and
               end_offset < (new_len - start_offset) and
               old_data[old_len - 1 - end_offset] == new_data[new_len - 1 - end_offset]):
            end_offset += 1

        # 3. CALCULATE THE GAP
        # The changed region in OLD
        delete_count = old_len - start_offset - end_offset

        # The changed region in NEW
        # Slice syntax: [start : length - end]
        # Logic: we take from start_offset up to (total - end_offset)
        insert_data = new_data[start_offset: new_len - end_offset]

        # 4. FORGE EDIT
        # Optimization: If we are just appending, delete_count is 0
        # Optimization: If we are just deleting, insert_data is empty

        edits.append(SemanticTokensEdit(
            start=start_offset,
            deleteCount=delete_count,
            data=insert_data
        ))

        return SemanticTokensDelta(
            resultId=previous_id,  # Will be replaced by caller with NEW id
            edits=edits
        )