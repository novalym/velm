# Path: src/velm/core/runtime/engine/intelligence/predictor/contracts.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: COGNITIVE_DNA_SCHEMA | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONTRACTS_V400_TOTALITY_FINALIS
# =========================================================================================

from __future__ import annotations
import time
import uuid
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Set, Final
from pydantic import BaseModel, Field, ConfigDict, computed_field


# =========================================================================================
# == I. THE ATOMS OF CONSCIOUSNESS                                                       ==
# =========================================================================================

class HeresyState(str, Enum):
    """The logical polarity of a past moment in time."""
    PURE = "PURE"  # Rite succeeded without friction
    TAINTED = "TAINTED"  # Rite succeeded but with warnings
    FRACTURED = "FRACTURED"  # Rite collapsed into a paradox (Failure)
    VOID = "VOID"  # State is unmanifest


class WeightNode(BaseModel):
    """
    =======================================================================================
    == THE WEIGHT NODE (V-Ω-TOTALITY)                                                    ==
    =======================================================================================
    A single point of probabilistic gravity in the Engine's memory.
    """
    model_config = ConfigDict(frozen=False, extra='allow')

    value: float = Field(1.0, description="The raw alchemical weight of this transition.")
    frequency: int = Field(1, description="Number of times this path was willed.")
    last_summoned: float = Field(default_factory=time.time, description="Unix timestamp of the last pulse.")

    @computed_field
    @property
    def recency_score(self) -> float:
        """Calculates the temporal relevance based on a 24-hour half-life."""
        age = time.time() - self.last_summoned
        # Half-life of 86400 seconds
        return math.exp(-age / 86400.0) if age > 0 else 1.0


# =========================================================================================
# == II. THE STRATA OF MEMORY                                                            ==
# =========================================================================================

class CognitiveStratum(BaseModel):
    """
    A single layer of the Markov chain or Heuristic Grimoire.
    Structure: { ContextKey: { TargetRite: WeightNode } }
    """
    model_config = ConfigDict(default_factory=dict)

    order: int = Field(..., description="The lookback depth of this stratum (e.g. 1 or 2).")
    lattice: Dict[str, Dict[str, WeightNode]] = Field(default_factory=dict)

    def scry(self, context: str) -> Dict[str, float]:
        """Perceives the normalized probabilities for a given context."""
        targets = self.lattice.get(context, {})
        if not targets: return {}

        total = sum(node.value for node in targets.values())
        return {rite: (node.value / total) for rite, node in targets.items()}


# =========================================================================================
# == III. THE ROOT DOSSIER (PERSISTENCE)                                                 ==
# =========================================================================================

class GnosticWeightsDossier(BaseModel):
    """
    =======================================================================================
    == THE GNOSTIC WEIGHTS DOSSIER (V-Ω-SINGULARITY-FINALIS)                             ==
    =======================================================================================
    The complete, serializable soul of the Engine's intelligence.
    Stored at .scaffold/cache/intelligence/gnostic_weights.json
    """
    model_config = ConfigDict(frozen=False)

    # --- 1. PROVENANCE ---
    schema_version: str = "4.0.0-Totality"
    gnostic_epoch: int = Field(0, description="The cumulative count of all cognitive evolutions.")
    machine_id: str = Field(default_factory=lambda: str(uuid.getnode()))

    # --- 2. THE MULTI-ORDER LATTICE ---
    # Map[Order, Stratum]
    brain_strata: Dict[int, CognitiveStratum] = Field(default_factory=dict)

    # --- 3. THE SEMANTIC REPOSITORY ---
    # Maps keywords to high-probability Request classes
    semantic_anchors: Dict[str, List[str]] = Field(default_factory=dict)

    # --- 4. INTEGRITY SEAL ---
    # Merkle root of the entire brain state
    state_hash: Optional[str] = None
    last_updated: float = Field(default_factory=time.time)

    def evolve(self):
        """Increments the epoch and stamps the time."""
        self.gnostic_epoch += 1
        self.last_updated = time.time()


# =========================================================================================
# == IV. THE OUTPUT PROPHECY (REVELATION)                                                ==
# =========================================================================================

class PredictionProphecy(BaseModel):
    """
    =======================================================================================
    == THE PREDICTION PROPHECY (V-Ω-OCULAR-READY)                                        ==
    =======================================================================================
    The high-fidelity revelation returned to the Architect.
    """
    model_config = ConfigDict(frozen=True)

    # --- 1. THE REVELATION ---
    suggestions: List[str] = Field(..., description="The ordered list of likely next Rites.")
    primary_recommendation: Optional[str] = None

    # --- 2. THE CONFIDENCE ---
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)
    reasoning_path: str = Field(..., description="Socratic explanation of the prediction logic.")

    # --- 3. HAPTIC FEEDBACK ---
    ui_hints: Dict[str, Any] = Field(
        default_factory=lambda: {"vfx": "pulse", "glow": "#64ffda", "priority": "low"},
        description="Atmospheric instructions for the Ocular HUD."
    )

    # --- 4. METABOLIC TAX ---
    metabolic_tax_ms: float = Field(0.0, description="The computational cost of this prophecy.")

    @computed_field
    @property
    def is_resonant(self) -> bool:
        """True if the Oracle is certain of the path (>80% confidence)."""
        return self.confidence_score > 0.8

# == SCRIPTURE SEALED: THE DNA OF INTELLIGENCE IS OMEGA ==