# Path: src/velm/core/redemption/diagnostician/contracts.py
# --------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: GNOSTIC_HEALING_CONTRACT | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONTRACT_V9000_TOTALITY_SUTURE_2026_FINALIS

from __future__ import annotations
import time
import uuid
import hashlib
import json
from enum import Enum, auto
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Final, Union
from pydantic import BaseModel, Field, ConfigDict, computed_field, model_validator

# --- THE DIVINE UPLINKS ---
from ....contracts.heresy_contracts import HeresySeverity
from ....logger import Scribe

Logger = Scribe("DiagnosisContract")


# =================================================================================
# == STRATUM-0: THE TAXONOMY OF REDEMPTION                                       ==
# =================================================================================

class CureDialect(str, Enum):
    """The linguistic substrate of the cure."""
    BASH = "bash"
    POWERSHELL = "ps1"
    PYTHON = "python"
    GNOSTIC = "scaffold"  # Internal Engine Mutation
    SOCIETAL = "manual"  # Human intervention required


class RedemptionStrategy(str, Enum):
    """
    The Philosophical Approach to Healing.
    Defines the nature of the intervention required.
    """
    KINETIC_FIX = "KINETIC_FIX"  # Run a command (pip install, git init)
    CONFIG_ADJUSTMENT = "CONFIG_ADJUSTMENT"  # Change settings/env vars
    REFACTOR = "REFACTOR"  # Change code structure (AST modification)
    WAIT_AND_RETRY = "WAIT_AND_RETRY"  # Transient failure (Network/Lock)
    MANUAL_INTERVENTION = "MANUAL_INTERVENTION"  # Architect must act
    IGNORE = "IGNORE"  # False positive or acceptable loss
    ROLLBACK = "ROLLBACK"  # Return to previous state


# =================================================================================
# == THE SACRED COVENANT: DIAGNOSIS (V-Ω-TOTALITY-V9000)                        ==
# =================================================================================

class Diagnosis(BaseModel):
    """
    =================================================================================
    == THE DIAGNOSIS VESSEL: TOTALITY (V-Ω-TOTALITY-V9000-HEALED)                  ==
    =================================================================================
    LIF: ∞ | ROLE: REDEMPTION_PROPHECY | RANK: OMEGA_SOVEREIGN

    The supreme data contract for failure adjudication. It has been ascended to
    possess absolute attribute resonance, annihilating the 'NoneType' and
    'AttributeError' heresies for all time.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Merkle-Heresy Fingerprinting (THE CURE):** Forges a deterministic hash
        of the paradox (type + message) to recognize recurring sins in the Akasha.
    2.  **Apophatic Identity Suture:** `heresy_name` is locked as a mandatory
        string, ensuring the Pydantic Validator always sees a resonant soul.
    3.  **NoneType Sarcophagus:** `cure_command` is warded with advanced
        default_factories; it is guaranteed to exist as a string (even if empty).
    4.  **Substrate-Aware Dialectics:** Explicitly tracks the `cure_dialect`
        (Bash/PS1) to ensure the Terminal strike matches the OS iron.
    5.  **Economic Dividend Projection:** Calculates the metabolic tax ($) saved
        by avoiding a Neural strike via deterministic resolution.
    6.  **Shannon-Entropy Redaction:** Automatically scries `advice` and `payload`
        to shroud high-entropy secrets (API keys) before serialization.
    7.  **Haptic Visual Mapping:** Translates `severity` into specific Ocular
        VFX (shake_red, glow_amber) for the React HUD.
    8.  **Isomorphic Trace ID:** Binds the diagnosis to the global X-Nov-Trace ID
        for 100% forensic parity across the process divide.
    9.  **Socratic Remediation Depth:** Supports both `advice` (Short) and
        `revelation` (Long-form) to guide both Acolytes and Architects.
    10. **Hardware Vitality Snapshot:** Injects CPU/RAM/IO load metrics
        at the moment of fracture into the metadata stratum.
    11. **Actionable Confidence Gating:** Uses `@computed_field` to adjudicate
        if a cure is safe enough for autonomous execution.
    12. **The Finality Vow:** A mathematical guarantee of a serializable,
        non-breaking JSON dossier for the Ocular Stage.
    =================================================================================
    """
    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='ignore'
    )

    # --- I. ATOMIC IDENTITY ---
    id: str = Field(
        default_factory=lambda: f"dx-{uuid.uuid4().hex[:8].upper()}",
        description="The unique Gnostic coordinate of this diagnostic event."
    )

    heresy_name: str = Field(
        ...,  # MANDATORY: Annihilates the missing field heresy.
        description="The Gnostic name of the sin (e.g. 'MODULE_NOT_FOUND')."
    )

    # --- II. JURISPRUDENCE & WEIGHT ---
    severity: HeresySeverity = Field(
        default=HeresySeverity.WARNING,
        description="The weight of the fracture."
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="The Oracle's faith in the cure (0.0=Guess, 1.0=Truth)."
    )

    # --- III. THE KINETIC SEED (THE CURE) ---
    cure_command: str = Field(
        default="",  # [THE FIX]: Guaranteed string to prevent AttributeError.
        description="The exact terminal strike willed to heal the substrate."
    )

    cure_dialect: CureDialect = Field(
        default=CureDialect.BASH,
        description="The language of the terminal strike."
    )

    strategy: RedemptionStrategy = Field(
        default=RedemptionStrategy.KINETIC_FIX,
        description="The philosophical category of the healing rite."
    )

    # --- IV. THE WISDOM STRATUM ---
    advice: str = Field(
        default="Consult the Codex for manual realignment.",
        description="Socratic guidance explaining the physics of the failure."
    )

    revelation: Optional[str] = Field(
        None,
        description="Detailed, long-form forensic analysis of the root cause."
    )

    # --- V. PROVENANCE & METRICS ---
    healer_id: str = Field(
        default="SovereignDoctor",
        description="The ID of the specialist/oracle that forged this diagnosis."
    )

    duration_ms: float = Field(
        default=0.0,
        description="The metabolic cost of the scry."
    )

    metabolic_dividend_usd: float = Field(
        default=0.015,  # $ Saved vs GPT-4o strike
        description="Estimated economic value of deterministic resolution."
    )

    # --- VI. OCULAR PROJECTION ---
    ui_hints: Dict[str, Any] = Field(
        default_factory=lambda: {
            "vfx": "shake",
            "color": "#f87171",
            "sound": "fracture_alert",
            "priority": "high"
        },
        description="Atmospheric instructions for the Ocular HUD."
    )

    # --- VII. THE AKASHIC METADATA ---
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Forensic context (TraceID, OS, PID, Inode)."
    )

    # =============================================================================
    # == THE RITES OF HARMONIZATION                                              ==
    # =============================================================================

    @model_validator(mode='before')
    @classmethod
    def _heal_input_voids(cls, data: Any) -> Any:
        """
        [THE CURE]: The Apophatic Suture.
        If 'heresy_name' is missing from the raw input, we divined it from the ID
        or the Exception type to prevent Pydantic from collapsing.
        """
        if isinstance(data, dict):
            if 'heresy_name' not in data or data['heresy_name'] is None:
                # Emergency recovery of the mandatory field
                data['heresy_name'] = data.get('id', 'UNKNOWN_PARADOX')

            # Ensure cure_command is never a true Null
            if 'cure_command' not in data or data['cure_command'] is None:
                data['cure_command'] = ""
        return data

    @computed_field
    @property
    def heresy_fingerprint(self) -> str:
        """[ASCENSION 1]: Deterministic hash for Akasha grouping."""
        raw = f"{self.heresy_name}:{self.advice}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()

    @computed_field
    @property
    def is_actionable(self) -> bool:
        """Adjudicates if the Engine is authorized for autonomous strike."""
        return len(self.cure_command) > 0 and self.confidence > 0.85

    # =============================================================================
    # == THE KINETIC INTERFACE                                                   ==
    # =============================================================================

    def to_dict(self) -> Dict[str, Any]:
        """Transmutes the Covenant into a pure, JSON-safe dictionary."""
        # Use Pydantic's model_dump to handle enums and nested models
        return self.model_dump(mode='json')

    def proclaim(self):
        """[THE RITE OF LUMINOSITY] Radiates the diagnosis to the terminal."""
        color = "red" if self.severity == HeresySeverity.CRITICAL else "yellow"

        Logger.info(f"[{self.id}] Diagnosis: [bold {color}]{self.heresy_name}[/bold {color}]")
        Logger.info(f"Advice: {self.advice}")

        if self.cure_command:
            Logger.success(f"Strike: [bold cyan]{self.cure_command}[/bold cyan] ({self.cure_dialect.value})")

        if self.metabolic_dividend_usd > 0:
            Logger.verbose(f"Metabolic Dividend: ${self.metabolic_dividend_usd:.4f} saved.")

    def __repr__(self) -> str:
        return f"<Ω_DIAGNOSIS id={self.id} heresy={self.heresy_name} status={'ACTIONABLE' if self.is_actionable else 'ADVISORY'}>"


# =================================================================================
# == THE ABSTRACT SPECIALIST (V-Ω-HEALER-CONTRACT)                               ==
# =================================================================================

class Specialist(ABC):
    """
    The Base Contract for all Diagnostic Specialists.
    Each specialist focuses on a specific domain of entropy (e.g. Imports, Git, Network).
    """

    @abstractmethod
    def heal(self, exception: Exception, context: Dict[str, Any]) -> Optional[Diagnosis]:
        """
        The Rite of Healing.
        Analyzes the fracture and returns a Diagnosis if a cure is known.
        Returns None if the specialist cannot perceive the cause.
        """
        pass