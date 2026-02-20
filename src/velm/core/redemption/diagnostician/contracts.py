# Path: src/velm/core/redemption/diagnostician/contracts.py
# --------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: GNOSTIC_HEALING_CONTRACT | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONTRACT_V3000_LAZARUS_COVENANT_2026_FINALIS

import time
import uuid
from typing import Optional, Dict, Any, List, Final
from pydantic import BaseModel, Field, ConfigDict, computed_field

# --- THE DIVINE UPLINKS ---
from ....contracts.heresy_contracts import HeresySeverity
from ....logger import Scribe

Logger = Scribe("DiagnosisContract")


class Diagnosis(BaseModel):
    """
    =================================================================================
    == THE SACRED COVENANT OF HEALING (V-Ω-TOTALITY-V3000)                         ==
    =================================================================================
    @gnosis:title The Diagnosis Vessel
    @gnosis:summary The definitive contract for failure analysis and redemption.
    @gnosis:LIF INFINITY

    This is no longer a simple record; it is a sentient decree of restoration.
    It carries the "Who, What, Why, and How" of the Path to Redemption.
    =================================================================================
    """
    model_config = ConfigDict(
        frozen=True,  # Immutable Vow
        arbitrary_types_allowed=True,
        extra='ignore'  # Future-Proofing Sieve
    )

    # --- I. ATOMIC IDENTITY ---
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="The unique, globally resonant ID of this specific diagnostic event."
    )

    heresy_name: str = Field(
        ...,
        description="The machine-readable name of the malady (e.g. 'PYTHON_MODULE_VOID')."
    )

    # --- II. JURISPRUDENCE & WEIGHT ---
    severity: HeresySeverity = Field(
        default=HeresySeverity.WARNING,
        description="The Gnostic weight of the sin. Determines the Ocular UI response."
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="The Oracle's faith in this cure (0.0 to 1.0)."
    )

    # --- III. THE KINETIC SEED (THE CURE) ---
    cure_command: Optional[str] = Field(
        None,
        description="The executable edict willed to heal the substrate. The 'Strike'."
    )

    # --- IV. THE WISDOM STRATUM ---
    advice: str = Field(
        default="Consult the Architect for manual realignment.",
        description="The Socratic explanation of the failure. The 'Wisdom'."
    )

    # --- V. PROVENANCE & METRICS ---
    healer_id: str = Field(
        default="UnknownHealer",
        description="The specific specialist that performed the successful biopsy."
    )

    duration_ms: float = Field(
        default=0.0,
        description="The metabolic cost of the diagnostic deliberation."
    )

    # --- VI. OCULAR PROJECTION ---
    ui_hints: Dict[str, Any] = Field(
        default_factory=lambda: {
            "vfx": "pulse",
            "color": "#fbbf24",
            "icon": "medkit"
        },
        description="Atmospheric instructions for the Cockpit HUD."
    )

    # --- VII. THE AKASHIC METADATA ---
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Catch-all vessel for substrate-specific forensics (OS, PID, TraceID)."
    )

    # =============================================================================
    # == THE RITES OF REVELATION                                                 ==
    # =============================================================================

    @computed_field
    @property
    def is_actionable(self) -> bool:
        """Proclaims True if the cure can be struck immediately."""
        return self.cure_command is not None and self.confidence > 0.6

    def to_string(self) -> str:
        """
        [THE RITE OF LEGACY]
        Returns the simple command string to satisfy the ancient conductors.
        """
        return self.cure_command or "# No automated cure manifest. Manual intervention willed."

    def proclaim(self):
        """[THE RITE OF LUMINOSITY] Logs the diagnosis with high status."""
        color = "red" if self.severity == HeresySeverity.CRITICAL else "yellow"
        Logger.info(f"Diagnosis: [bold {color}]{self.heresy_name}[/bold {color}]")
        Logger.info(f"Advice: {self.advice}")
        if self.cure_command:
            Logger.success(f"Cure: [bold cyan]{self.cure_command}[/bold cyan]")

    def __repr__(self) -> str:
        return f"<Ω_DIAGNOSIS id={self.id[:8]} heresy={self.heresy_name} conf={self.confidence:.2f}>"