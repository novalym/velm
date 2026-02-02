# Path: scaffold/artisans/distill/core/governance/contracts.py
# ------------------------------------------------------------

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from pathlib import Path


class RepresentationTier(str, Enum):
    """
    The Hierarchy of Form (V-Ω-EXPANDED).
    Defines the resolution at which a scripture is rendered.
    """
    FULL = "full"  # The complete soul (Source Code).
    SKELETON = "skeleton"  # Structural signatures (AST).
    INTERFACE = "stub"  # Public API only (Apophatic).
    SUMMARY = "summary"  # Natural language description.
    PATH_ONLY = "path_only"  # A mere pointer.
    EXCLUDED = "excluded"  # Returned to the void.


@dataclass
class GovernanceDecision:
    """
    The Atomic Record of Judgment.
    Explains WHY a specific tier was chosen for a specific file.
    """
    tier: RepresentationTier
    cost: int
    reason: str
    score: float


@dataclass
class GovernancePlan:
    """
    The Economic Blueprint.
    The final output of the Governor, detailing the fate of every file.
    """
    # Map: Path -> Decision Details
    decisions: Dict[Path, GovernanceDecision] = field(default_factory=dict)

    # Map: Path -> Tier String (for simple lookup by Assembler)
    allocations: Dict[Path, str] = field(default_factory=dict)

    total_cost: int = 0
    utilization_percent: float = 0.0

    # Statistics breakdown
    stats: Dict[str, int] = field(default_factory=lambda: {t.value: 0 for t in RepresentationTier})