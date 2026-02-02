# Path: scaffold/core/blueprint_scribe/sorting_hat.py
# ---------------------------------------------------
from typing import List
from ...contracts.data_contracts import _GnosticNode


class SortingHat:
    """
    =================================================================================
    == THE ARBITER OF ORDER (V-Ω-SEMANTIC-SORTER)                                  ==
    =================================================================================
    [EVOLUTION 2] The Semantic Sorter.
    Enforces the Gnostic Law of Order:
    1. Directories First
    2. Dotfiles (Hidden Gnosis) Second
    3. Standard Files Third
    4. Alphabetical within tiers.
    """

    def sort(self, nodes: List[_GnosticNode]) -> List[_GnosticNode]:
        return sorted(nodes, key=self._sort_key)

    def _sort_key(self, node: _GnosticNode):
        # Tier 0: Directories
        # Tier 1: Files
        type_score = 0 if node.is_dir else 1

        # Within Files:
        # Tier A: Dotfiles (0)
        # Tier B: Standard (1)
        name_score = 0 if node.name.startswith('.') else 1

        return (type_score, name_score, node.name.lower())