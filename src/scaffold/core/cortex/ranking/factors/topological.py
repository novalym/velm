# Path: scaffold/artisans/distillation/ranker/factors/topological.py
# ------------------------------------------------------------------

from typing import Dict, Set, Tuple
from .....logger import Scribe

Logger = Scribe("TopologicalFactor")


class TopologicalJudge:
    """
    =============================================================================
    == THE GNOSTIC PAGERANK (INFLUENCE CALCULATOR)                             ==
    =============================================================================
    Calculates the transitive influence of every file based on the Dependency Graph.
    """

    def __init__(self, dependents_graph: Dict[str, Set[str]]):
        self.dependents_graph = dependents_graph
        self.scores = self._calculate_pagerank()

    def _calculate_pagerank(self, iterations: int = 20, d: float = 0.85) -> Dict[str, float]:
        """Iterative PageRank algorithm."""
        if not self.dependents_graph:
            return {}

        all_nodes = set(self.dependents_graph.keys())
        for importers in self.dependents_graph.values():
            all_nodes.update(importers)

        num_nodes = len(all_nodes)
        if num_nodes == 0: return {}

        ranks = {node: 1.0 / num_nodes for node in all_nodes}

        for _ in range(iterations):
            new_ranks = {}
            teleport = (1 - d) / num_nodes

            for node in all_nodes:
                # In standard PageRank: Sum(Rank(Inbound) / OutDegree(Inbound))
                # Here, "Inbound" means files that import ME (Dependents).
                importers = self.dependents_graph.get(node, set())

                # Simplified "Prestige" model:
                # We sum the rank of everyone who needs us.
                # Ideally we normalize by their total dependencies, but for code,
                # being imported by a God Object is high value regardless.
                rank_sum = sum(ranks[imp] for imp in importers)

                new_ranks[node] = teleport + (d * rank_sum)

            ranks = new_ranks

        # Normalize to 0-1 range for the score multiplier
        max_rank = max(ranks.values()) if ranks else 1.0
        normalized = {k: v / max_rank for k, v in ranks.items()}

        return normalized

    def judge(self, path_str: str) -> float:
        return self.scores.get(path_str, 0.0)