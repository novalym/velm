# Path: src/scaffold/core/symbolic/contracts.py
# ---------------------------------------------
# LIF: ∞ | ROLE: GNOSTIC_DATA_CONTRACTS | RANK: LEGENDARY
# AUTH: Ω_SYMBOLIC_VESS_TOTALITY_V100
# =========================================================================================

from __future__ import annotations
import time
from enum import Enum, IntEnum
from typing import Dict, List, Any, Optional, Union, Final
from pydantic import BaseModel, Field, ConfigDict, computed_field


# =============================================================================
# == SECTION I: THE TAXONOMY OF INTENT (ENUMS)                               ==
# =============================================================================

class AdjudicationIntent(str, Enum):
    """
    The Gnostic Verdicts of the Symbolic Eye.
    Defines the "Spiritual Direction" of the signal.
    """
    DISQUALIFY = "DISQUALIFY"  # Hard Stop: Tenant/Pro-Bono/Bad-Fit
    EMERGENCY = "EMERGENCY"  # DEFCON 1: Fire/Flood/Legal-Arrest
    FINANCIAL = "FINANCIAL"  # Money Matter: Quote/Price/Deposit
    TEMPORAL = "TEMPORAL"  # Spacetime: Schedule/Hours/Availability
    FACTUAL = "FACTUAL"  # Knowledge: Warranty/License/Process
    VISUAL_WAIT = "VISUAL_WAIT"  # Media: Waiting for lead to send photo
    NEURAL_GENESIS = "NEURAL"  # Complexity: Hand off to LLM (S-04)
    HUMAN_TAKEOVER = "HUMAN"  # Critical: Hand off to Architect (Owner)
    NEURAL_REQUIRED = "NEURAL_REQUIRED"
    HUMAN_REQUIRED = "HUMAN_REQUIRED"
    INQUIRY = "INQUIRY"
    HAZARD = "HAZARD"
    OPT_OUT = "OPT_OUT"
class UrgencyLevel(IntEnum):
    """The metabolic priority of the signal."""
    ZEN = 1  # Background / Informational
    NOMINAL = 2  # Standard Sales Cycle
    HIGH = 3  # Active Buying Signal
    CRITICAL = 4  # Asset/Property Risk
    DEFCON_1 = 5  # Life/Safety Risk


# =============================================================================
# == SECTION II: THE ATOMIC MATTER (VESSESLS)                                ==
# =============================================================================

class GnosticAtom(BaseModel):
    """
    [THE ATOM]
    A single unit of meaning extracted from raw text.
    Examples: A price ($500), a time (tomorrow), or a keyword (leak).
    """
    model_config = ConfigDict(frozen=True)

    key: str  # 'currency', 'temporal', 'disqualifier'
    value: Any  # 500.0, '2026-01-30', 'tenant'
    category: str  # 'FINANCIAL', 'TEMPORAL', 'MECHANICAL'
    raw_source: str  # The original snippet of text
    confidence: float = 1.0  # 1.0 for Regex, <1.0 for Fuzzy


class VisualInquest(BaseModel):
    """
    [THE RETINA SPEC]
    Instructions for the Vision AI when matter (images) arrives.
    """
    model_config = ConfigDict(extra='allow')

    requires_visual: bool = False
    targets: List[str] = Field(default_factory=list)  # e.g. ["Rusted Flashing"]
    prompts: List[str] = Field(default_factory=list)  # e.g. ["Is it leaking?"]
    complexity_threshold: float = 0.85


# =============================================================================
# == SECTION III: THE TOTALITY VERDICT (THE MANIFEST)                       ==
# =============================================================================

class SymbolicVerdict(BaseModel):
    """
    [THE VERDICT]
    The output of a single Inquisitor's gaze.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    intent: AdjudicationIntent
    confidence: float = Field(..., ge=0.0, le=1.0)
    diagnosis: str  # Socratic explanation (e.g. "Matched 'tenant' in Disqualifiers")

    # The Response template pulled from the Strata
    response_template: Optional[str] = None

    # Metadata for the next movement
    # [THE CURE]: Changed from List[GnosticAtom] to Dict to prevent Pydantic Type Heresy
    extracted_atoms: Dict[str, Any] = Field(default_factory=dict)
    urgency: UrgencyLevel = UrgencyLevel.NOMINAL
    ui_aura: str = "#64ffda"  # The HUD color frequency


class SymbolicManifest(BaseModel):
    """
    [THE TOTALITY REVELATION]
    The final packet produced by the GnosticSymbolicEngine.
    It determines if the AI even needs to speak.
    """
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    # --- THE VERDICT ---
    primary_intent: AdjudicationIntent
    is_terminal: bool = False  # If True, DO NOT CALL AI. Use 'output_text'.

    # --- THE MATTER ---
    output_text: Optional[str] = None  # The humanized response
    vision_specs: Optional[VisualInquest] = None

    # --- THE FORENSICS ---
    trace_id: str
    latency_ms: float = 0.0
    inquisitor_path: List[str] = Field(default_factory=list)  # The chain of specialists used

    # Economic Tomography
    metabolic_cost_saved_usd: float = 0.01  # The cost of the AI call we avoided
    confidence: float = 0.0  # [THE FIX] Added for direct access in Scribes
    diagnosis_reason: Optional[str] = None  # [THE FIX] Added for clarity
    diagnosis: Optional[str] = None  # [CRITICAL FIX] Added for direct access by Archive Scribe
    @computed_field
    @property
    def status_label(self) -> str:
        """Translates intent to high-status HUD label."""
        return f"SYMBOLIC_RESOLVED_{self.primary_intent.value}"

# == SCRIPTURE SEALED: THE CONTRACTS ARE TOTAL ==