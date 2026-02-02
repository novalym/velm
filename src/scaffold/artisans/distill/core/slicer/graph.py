# scaffold/artisans/distill/core/slicer/graph.py
# ----------------------------------------------------

from typing import Dict, List, Set, Optional
from .contracts import SymbolNode, RelevanceLevel


class SemanticGraph:
    """
    =============================================================================
    == THE WEB OF LOCAL CAUSALITY (V-Ω-GRAPH-ENGINE-CASE-AGNOSTIC)             ==
    =============================================================================
    Models the relationships between symbols within a single scripture.

    [ASCENSION]: It now possesses the **Gaze of Tolerance**. It performs all relevance
    calculations using case-insensitive matching, ensuring that "distillationoracle"
    in the CLI correctly resonates with "DistillationOracle" in the code.
    """

    def __init__(self):
        self.nodes: Dict[str, SymbolNode] = {}  # Name -> Node
        self.roots: List[SymbolNode] = []  # Top-level nodes

    def add_node(self, node: SymbolNode):
        self.nodes[node.name] = node
        if not node.parent_name:
            self.roots.append(node)
        # Note: We assume children are already attached or we attach them here logic-wise
        # For V1, we rely on the Adapter to build the tree structure in the Node objects.

    def calculate_relevance(self, focus_symbols: Set[str]) -> Dict[str, RelevanceLevel]:
        """
        The Rite of Propagation.
        Determines the relevance of every node based on the focus set.
        """
        scores: Dict[str, RelevanceLevel] = {name: RelevanceLevel.IRRELEVANT for name in self.nodes}

        # [THE FIX] Normalize focus symbols for case-insensitive matching
        lower_focus = {s.lower() for s in focus_symbols}

        # 1. Direct Hit (Case-Insensitive Substring Match)
        for name, node in self.nodes.items():
            name_lower = name.lower()

            # Check exact match or substring match (flexible gaze)
            # If any focus symbol is a substring of the node name (e.g. "oracle" in "DistillationOracle")
            if any(f in name_lower for f in lower_focus):
                scores[name] = RelevanceLevel.FOCUSED

                # 2. Ascend to Parents (Structural Necessity)
                # If a method is focused, its class must be STRUCTURAL to hold it.
                curr = node
                while curr.parent_name and curr.parent_name in self.nodes:
                    parent = self.nodes[curr.parent_name]
                    if scores[parent.name].value < RelevanceLevel.STRUCTURAL.value:
                        scores[parent.name] = RelevanceLevel.STRUCTURAL
                    curr = parent

        # 3. Descend to Children (Containment)
        # If a class is Focused, all its methods are Focused.
        # If a class is only Structural, its methods remain Irrelevant (unless individually focused).
        for root in self.roots:
            self._propagate_down(root, scores)

        # 4. Trace Dependencies (The Causal Web)
        # If Focused Node A uses Symbol B, B becomes DEPENDENCY.
        # We iterate until stability (fixpoint).
        changed = True
        while changed:
            changed = False
            for name, node in self.nodes.items():
                current_score = scores[name]

                # Only Focused or Dependency nodes can infect others
                if current_score.value >= RelevanceLevel.DEPENDENCY.value:
                    for dep_name in node.dependencies:
                        if dep_name in self.nodes:
                            # Dependency inherits the DEPENDENCY level
                            if scores[dep_name].value < RelevanceLevel.DEPENDENCY.value:
                                scores[dep_name] = RelevanceLevel.DEPENDENCY
                                changed = True

        return scores

    def _propagate_down(self, node: SymbolNode, scores: Dict[str, RelevanceLevel]):
        """If a parent is focused, the children inherit the focus."""
        parent_score = scores[node.name]

        if parent_score == RelevanceLevel.FOCUSED:
            for child in node.children:
                if scores[child.name].value < RelevanceLevel.FOCUSED.value:
                    scores[child.name] = RelevanceLevel.FOCUSED

        for child in node.children:
            self._propagate_down(child, scores)