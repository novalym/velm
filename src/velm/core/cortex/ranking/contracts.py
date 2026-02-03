# Path: artisans/distill/core/ranker/contracts.py
# -----------------------------------------------



from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class RankDossier:
    """The detailed breakdown of a file's score."""
    base_score: float = 0.0
    topological_score: float = 0.0  # PageRank
    temporal_score: float = 0.0  # Churn/Recency
    structural_score: float = 0.0  # AST Density
    semantic_score: float = 0.0  # Focus Keywords
    symbiosis_score: float = 0.0  # Test/Impl pairing
    # ★★★ PILLAR I ASCENSION ★★★
    cohesion_score: float = 0.0      # Co-change graph
    # ★★★ APOTHEOSIS COMPLETE ★★★
    resonance_score: float = 0.0 # Content keyword match
    penalties: float = 1.0 # Multiplier, not additive

    @property
    def total(self) -> float:
        return (
                self.base_score +
                self.topological_score +
                self.temporal_score +
                self.structural_score +
                self.semantic_score +
                self.symbiosis_score +
                self.cohesion_score +
                self.resonance_score
        ) * self.penalties


@dataclass
class RankingStrategy:
    """A configuration profile for the Tribunal."""
    name: str
    description: str
    category_weights: Dict[str, float]
    multipliers: Dict[str, float]


