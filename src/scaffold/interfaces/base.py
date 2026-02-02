# Path: packages/scaffold/src/scaffold/interfaces/base.py
# -------------------------------------------------------

from __future__ import annotations
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Generic, TypeVar, Union, Set

from pydantic import BaseModel, Field, ConfigDict, computed_field, model_validator

# --- GNOSTIC UPLINKS ---
from ..contracts.heresy_contracts import Heresy, HeresySeverity

# Generic type for the Gnostic Payload
T = TypeVar('T')


class Artifact(BaseModel):
    """
    =============================================================================
    == THE ATOMIC ARTIFACT (V-Ω-MATTER-VESSEL)                                 ==
    =============================================================================
    Represents a single tangible object manifest or transfigured by the Engine.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    path: Path = Field(..., description="The physical coordinate in the sanctum.")
    type: str = Field("file", pattern=r"^(file|directory|symlink|socket)$")
    action: str = Field(..., description="The rite performed (created|transfigured|excised|skipped).")

    size_bytes: int = Field(0, ge=0)
    checksum: Optional[str] = Field(None, description="The SHA256 Merkle Fingerprint.")

    # [ASCENSION 1]: Deep Metadata Container
    # Holds diff stats, visual cues, or forensic notes for the Cockpit.
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.path.name


class ScaffoldResult(BaseModel, Generic[T]):
    """
    =============================================================================
    == THE OMNISCIENT RESULT (V-Ω-TOTALITY-FINALIS-UNBOUND)                    ==
    =============================================================================
    @gnosis:title ScaffoldResult
    @gnosis:summary The final, unbreakable contract between the God-Engine and the UI.
    @gnosis:capability INFINITE_ABSORPTION
    LIF: 100,000,000

    This vessel has been ascended to accept ALL Gnosis. It cannot be surprised by
    extra arguments; it simply absorbs them into its structure.
    """
    # [ASCENSION 2]: THE PERMISSIVE VOW
    # We allow extra fields to flow through without raising validation errors.
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=False, extra='allow')

    # --- I. THE BINARY TRUTH (VOICE) ---
    success: bool = Field(..., description="True if the reality aligned with the Architect's will.")

    message: str = Field(
        default="Reality synchronized.",
        description="The primary human-readable proclamation."
    )
    vitals: Dict[str, Any] = Field(default_factory=dict, description="Performance telemetry and cost metrics.")
    # [ASCENSION 3]: THE LUMINOUS COMPASS
    suggestion: Optional[str] = Field(
        default=None,
        description="The Mentor's counsel on the next logical rite or fix."
    )

    # [ASCENSION 4]: THE KINETIC SEED
    fix_command: Optional[str] = Field(
        default=None,
        description="An executable CLI command string to resolve a detected heresy."
    )

    # --- II. THE EVIDENCE OF WORK (MATTER) ---
    data: Optional[T] = Field(
        default=None,
        description="The primary Gnostic payload (Objects, Maps, or Logic)."
    )

    artifacts: List[Artifact] = Field(
        default_factory=list,
        description="A detailed census of every scripture touched."
    )

    # [ASCENSION 5]: THE FORENSIC MIRROR
    error: Optional[str] = Field(
        default=None,
        description="The forensic summary of the fracture, heresy, or OS-level paradox."
    )

    # --- III. THE CHRONICLE OF PARADOX (FRACTURES) ---
    heresies: List[Heresy] = Field(
        default_factory=list,
        description="A list of structural paradoxes encountered."
    )

    diagnostics: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="LSP-compliant markers for editor illumination."
    )

    # --- IV. THE GNOSTIC TELEMETRY (ENERGY) ---
    duration_seconds: float = Field(
        default=0.0,
        description="The temporal cost of the rite in the Mortal Realm."
    )

    timestamp_utc: datetime = Field(
        default_factory=datetime.utcnow,
        description="The moment of manifestation."
    )

    traceback: Optional[str] = Field(
        default=None,
        description="The forensic data of a catastrophic fracture (Panic/Crash)."
    )

    # [ASCENSION 6]: THE RESONANCE MATRIX
    # UI Tints, Icons, and Haptic hints for the React layer.
    ui_hints: Dict[str, Any] = Field(
        default_factory=dict,
        description="Atmospheric instructions for the Cockpit (vfx, sound, glow)."
    )

    # [ASCENSION 7]: THE CONTEXTUAL ANCHOR
    # Captures where this result came from (e.g., 'TwilioArtisan', 'CacheMiddleware')
    source: Optional[str] = Field(
        default=None,
        description="The identity of the Artisan or Middleware that forged this result."
    )

    # =========================================================================
    # == COMPUTED REALITIES (The Mind of the Result)                         ==
    # =========================================================================

    @computed_field
    @property
    def has_critical_heresy(self) -> bool:
        """
        [ASCENSION 8]: The Volatile Guard.
        Perceives if a fatal paradox exists that must halt the multiverse.
        """
        from ..contracts.heresy_contracts import HeresySeverity
        return any(h.severity == HeresySeverity.CRITICAL for h in self.heresies)

    @computed_field
    @property
    def artifact_summary(self) -> Dict[str, int]:
        """[ASCENSION 9]: The Categorical Census."""
        summary = {"created": 0, "modified": 0, "deleted": 0, "skipped": 0}
        for art in self.artifacts:
            action = art.action.lower()
            if "create" in action:
                summary["created"] += 1
            elif "transfigur" in action or "modif" in action:
                summary["modified"] += 1
            elif "excis" in action or "delet" in action:
                summary["deleted"] += 1
            else:
                summary["skipped"] += 1
        return summary

    @computed_field
    @property
    def is_actionable(self) -> bool:
        """[ASCENSION 10]: Actionability Check. True if success AND data exists."""
        return self.success and self.data is not None

    def __bool__(self):
        """[ASCENSION 11]: Pythonic Truth. Allows `if result:` checks."""
        return self.success

    # =========================================================================
    # == RITES OF GENERATION (The Universal Factories)                       ==
    # =========================================================================

    @classmethod
    def forge_success(cls,
                      message: str,
                      data: Optional[T] = None,
                      artifacts: Optional[List[Artifact]] = None,
                      **kwargs) -> "ScaffoldResult[T]":
        """
        [THE RITE OF VICTORY - UNBOUND]
        Forges a successful result.

        CRITICAL: Accepts `**kwargs` to allow Artisans to inject `ui_hints`,
        `duration_seconds`, `source`, or any other Gnostic field without
        triggering a TypeError.
        """
        return cls(
            success=True,
            message=message,
            data=data,
            artifacts=artifacts or [],
            **kwargs
        )

    @classmethod
    def forge_failure(cls,
                      message: str,
                      suggestion: Optional[str] = None,
                      details: Optional[str] = None,
                      data: Optional[T] = None,
                      **kwargs) -> "ScaffoldResult":
        """
        [THE RITE OF FAILURE - UNBOUND]
        Forges a failure result, populating a default heresy if none provided.

        CRITICAL: Accepts `**kwargs` to allow passing `traceback`, `error`,
        `diagnostics`, or `ui_hints` (e.g. for a red shake effect).
        """
        # If the caller didn't provide specific heresies, we forge a default one
        heresies = kwargs.pop('heresies', [])
        if not heresies:
            from ..contracts.heresy_contracts import Heresy, HeresySeverity
            h = Heresy(
                message=message,
                details=details,
                severity=HeresySeverity.CRITICAL,
                suggestion=suggestion
            )
            heresies = [h]

        return cls(
            success=False,
            message=message,
            suggestion=suggestion,
            heresies=heresies,
            data=data,  # [ASCENSION 12]: Failure can still carry data (Forensics)
            error=details or message,
            **kwargs
        )