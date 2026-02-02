# === [scaffold/artisans/distill/core/causality/contracts.py] - SECTION 1 of 1: Causality Contracts ===
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from enum import Enum, auto

from .constants import (
    DEFAULT_DEPENDENCY_DECAY,
    DEFAULT_DEPENDENT_DECAY,
    MAX_PROPAGATION_DEPTH,
    MIN_RELEVANCE_THRESHOLD
)


class PropagationDirection(Enum):
    """The vector of the Gnostic Gaze."""
    UPSTREAM = auto()  # Looking at Dependents (Who uses me?)
    DOWNSTREAM = auto()  # Looking at Dependencies (Who do I use?)
    SEED = auto()  # The Origin Point


@dataclass
class CausalityProfile:
    """
    The Configuration of the Physics Engine.
    Allows the Architect to tune the gravity of the graph traversal.
    """
    max_depth: int = MAX_PROPAGATION_DEPTH
    dependency_decay: float = DEFAULT_DEPENDENCY_DECAY
    dependent_decay: float = DEFAULT_DEPENDENT_DECAY
    min_threshold: float = MIN_RELEVANCE_THRESHOLD

    # Advanced Tuning
    dampen_hubs: bool = True
    prioritize_test_files: bool = False

    # [THE FIX] The Directional Vows
    # These fields were missing, causing the TypeError in the Propagator.
    include_dependents: bool = True
    include_dependencies: bool = True


@dataclass
class CausalNode:
    """A single point in the calculated web."""
    path: str
    score: int
    depth: int
    sources: Set[str] = field(default_factory=set)  # Which seeds caused this node to light up?


@dataclass
class ImpactReport:
    """The Final Dossier of the Causal Analysis."""
    scores: Dict[str, int]
    visited_count: int
    max_depth_reached: int
    hubs_encountered: List[str]