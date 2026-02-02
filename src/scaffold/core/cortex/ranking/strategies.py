# Path: artisans/distill/core/ranker/strategies.py
# ------------------------------------------------

import math
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from ....core.cortex.contracts import FileGnosis, CortexMemory
from ....logger import Scribe

Logger = Scribe("Strategos")


@dataclass
class RankingWeights:
    """The DNA of a Ranking Persona."""
    centrality: float = 1.0  # Importance in the graph
    pagerank: float = 2.0  # Recursive importance
    recency: float = 1.0  # Active development
    churn: float = 1.0  # Historical volatility
    complexity: float = 1.5  # Cognitive load
    semantic_match: float = 5.0  # Relevance to user query
    error_heat: float = 3.0  # Sentinel heresies
    keystone_bonus: float = 100.0  # Manifests/Entrypoints
    test_penalty: float = 0.1  # Multiplier for tests
    doc_penalty: float = 0.01  # Multiplier for docs

    @classmethod
    def FOR_BUG_HUNT(cls):
        """Persona: Focus on recent changes, errors, and complexity."""
        return cls(recency=3.0, churn=2.0, error_heat=5.0, complexity=2.0, test_penalty=0.5)

    @classmethod
    def FOR_ARCHITECT(cls):
        """Persona: Focus on structure, interfaces, and keystones."""
        return cls(centrality=2.0, pagerank=3.0, complexity=0.5, recency=0.1, doc_penalty=0.1)

    @classmethod
    def FOR_ONBOARDING(cls):
        """Persona: Balanced view including high-level docs."""
        return cls(doc_penalty=0.5, keystone_bonus=200.0)


class ScoringStrategy(ABC):
    """The Abstract Soul of Ranking."""

    def __init__(self, weights: Optional[RankingWeights] = None):
        self.weights = weights or RankingWeights()

    @abstractmethod
    def score(self, file: FileGnosis, memory: CortexMemory, context: Dict[str, Any]) -> float:
        """
        Calculates the Gnostic Value of a file.
        """
        pass


class MultiDimensionalStrategy(ScoringStrategy):
    """
    =============================================================================
    == THE STRATEGOS (V-Ω-MULTIDIMENSIONAL-JUDGE)                              ==
    =============================================================================
    A comprehensive ranking engine that fuses Topology, Telemetry, and Semantics.
    """

    KEYSTONE_PATTERNS = {
        r'^(main|app|index|server)\.(py|ts|js|go|rs)$',  # Entrypoints
        r'^(pyproject\.toml|package\.json|Cargo\.toml|go\.mod)$',  # Manifests
        r'^(README\.md|ARCHITECTURE\.md)$',  # Sacred Texts
        r'^src/__init__\.py$'  # Root Init
    }

    # Architectural Layers (Higher is more central)
    LAYER_WEIGHTS = {
        r'/core/': 1.5,
        r'/domain/': 1.5,
        r'/models/': 1.4,
        r'/api/': 1.3,
        r'/utils/': 0.8,
        r'/scripts/': 0.6,
        r'/tests/': 0.5,
    }

    def __init__(self, weights: Optional[RankingWeights] = None):
        super().__init__(weights)
        self._pagerank_cache: Dict[str, float] = {}
        self._pagerank_computed = False

    def _compute_pagerank(self, memory: CortexMemory):
        """
        [ELEVATION 2] The PageRank Algorithm.
        """
        if self._pagerank_computed: return

        graph = memory.dependency_graph.get('dependency_graph', {})
        all_nodes = {f.path.as_posix() for f in memory.inventory}

        ranks = {node: 1.0 for node in all_nodes}
        damping = 0.85
        iterations = 10

        for _ in range(iterations):
            new_ranks = {}
            for node in all_nodes:
                incoming = memory.get_dependents_of(node)
                rank_sum = 0.0
                for source in incoming:
                    out_degree = len(graph.get(source, []))
                    if out_degree > 0:
                        rank_sum += ranks.get(source, 1.0) / out_degree
                new_ranks[node] = (1 - damping) + (damping * rank_sum)
            ranks = new_ranks

        self._pagerank_cache = ranks
        self._pagerank_computed = True

    def score(self, file: FileGnosis, memory: CortexMemory, context: Dict[str, Any]) -> float:
        """The Grand Rite of Valuation."""

        self._compute_pagerank(memory)
        path_str = file.path.as_posix()
        name = file.name

        score = 10.0
        breakdown = []

        # 1. KEYSTONE BONUS
        is_keystone = any(re.match(p, name) for p in self.KEYSTONE_PATTERNS)
        if is_keystone:
            bonus = self.weights.keystone_bonus
            score += bonus
            breakdown.append(f"Keystone(+{bonus})")

        # 2. TOPOLOGY
        # Degree Centrality
        dependents = len(memory.get_dependents_of(path_str))
        centrality_score = dependents * self.weights.centrality * 2.0
        score += centrality_score

        # PageRank
        pr_val = self._pagerank_cache.get(path_str, 1.0)
        pr_score = pr_val * self.weights.pagerank * 10.0
        score += pr_score

        # 3. COMPLEXITY DENSITY
        ast_metrics = file.ast_metrics or {}
        cc = ast_metrics.get("cyclomatic_complexity", 1)
        sloc = max(1, ast_metrics.get("line_count", file.original_size // 40))
        density = cc / sloc if sloc > 0 else 0
        complexity_score = density * 100 * self.weights.complexity
        score += complexity_score

        # 4. TEMPORAL VITALITY
        recency_score = 0
        if file.days_since_last_change is not None:
            recency_factor = math.exp(-file.days_since_last_change / 30.0)
            recency_score = recency_factor * 50.0 * self.weights.recency
            score += recency_score

        churn_score = math.log1p(file.churn_score) * 5.0 * self.weights.churn
        score += churn_score

        # 5. SEMANTIC RESONANCE
        query = context.get('query', '').lower()
        if query:
            if query in path_str.lower():
                match_score = 100.0 * self.weights.semantic_match
                score += match_score
            for tag in file.semantic_tags:
                if tag in query:
                    tag_score = 50.0 * self.weights.semantic_match
                    score += tag_score

        # 6. ARCHITECTURAL LAYERS
        for pattern, weight in self.LAYER_WEIGHTS.items():
            if re.search(pattern, path_str):
                score *= weight
                break

        # 7. PENALTIES
        if "test" in path_str or "spec" in path_str:
            score *= self.weights.test_penalty
        if file.category.startswith("doc") and not is_keystone:
            score *= self.weights.doc_penalty

        # 8. ORPHAN PENALTY
        dependencies = len(memory.get_dependencies_of(path_str))
        if dependents == 0 and dependencies == 0 and not is_keystone:
            score *= 0.1

        setattr(file, '_score_breakdown', ", ".join(breakdown))
        return score