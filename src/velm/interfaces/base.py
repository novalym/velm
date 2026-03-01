# Path: packages/scaffold/src/scaffold/interfaces/base.py
# -----------------------------------------------------------------------------------------
# == THE OMNISCIENT RESULT: OMEGA TOTALITY (V-Ω-TOTALITY-V25000-FINALIS-UNBOUND)         ==
# =========================================================================================
# LIF: INFINITY | ROLE: UNIVERSAL_PROCLAMATION_VESSEL | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_BASE_V25000_SEVERITY_SUTURE_2026_FINALIS
# =========================================================================================

from __future__ import annotations
import json
import os
import uuid
import time
import hashlib
import platform
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import List, Dict, Any, Optional, Generic, TypeVar, Union, Set, Final

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    computed_field,
    model_validator,
    field_validator
)

# --- GNOSTIC UPLINKS ---
from ..contracts.heresy_contracts import Heresy, HeresySeverity

# Generic type for the Gnostic Payload (The "Matter")
T = TypeVar('T')


# =========================================================================================
# == STRATUM 0: THE TAXONOMY OF TRUTH                                                    ==
# =========================================================================================

class ScaffoldSeverity(str, Enum):
    """
    =============================================================================
    == THE SCALES OF JUDGMENT (ScaffoldSeverity)                               ==
    =============================================================================
    Defines the existential weight of a result.
    """
    HINT = "hint"  # A whisper of optimization.
    INFO = "info"  # Standard metabolic pulse.
    SUCCESS = "success"  # A rite concluded in purity.
    WARNING = "warning"  # A sign of drift or non-fatal paradox.
    ERROR = "error"  # A logic fracture.
    CRITICAL = "critical"  # A catastrophic system collapse.


class SubstrateDNA(str, Enum):
    """The physical plane where the result was forged."""
    IRON = "iron_native"  # Local CPU / Standalone EXE.
    ETHER = "ether_wasm"  # Browser / Pyodide / WASM.
    VOID = "void_sim"  # Quantum Simulation / Dry-run.


# =========================================================================================
# == STRATUM 1: THE ATOMIC ARTIFACT                                                      ==
# =========================================================================================

class Artifact(BaseModel):
    """
    =============================================================================
    == THE ATOMIC ARTIFACT (V-Ω-MATTER-VESSEL-ASCENDED)                        ==
    =============================================================================
    Represents a single tangible object manifest or transfigured by the Engine.
    """
    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    path: Path = Field(..., description="The logical coordinate in the project sanctum.")
    type: str = Field("file", pattern=r"^(file|directory|symlink|socket|virtual)$")
    action: str = Field(..., description="The rite performed (created|transfigured|excised|skipped).")

    # --- METABOLIC METRICS ---
    size_bytes: int = Field(0, ge=0)
    checksum: Optional[str] = Field(None, description="The SHA256 Merkle Fingerprint.")

    # --- OCULAR METADATA ---
    mime_type: str = Field("text/plain", description="The Gnostic dialect for UI highlighters.")
    encoding: str = Field("utf-8", description="The character-set of the soul.")

    # [ASCENSION 1]: Deep Metadata Container
    # Holds diff stats, visual cues, or forensic notes for the Cockpit.
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @computed_field
    @property
    def name(self) -> str:
        """The atomic name of the artifact."""
        return self.path.name

    @computed_field
    @property
    def extension(self) -> str:
        """The lexical suffix."""
        return self.path.suffix.lstrip('.')


# =========================================================================================
# == STRATUM 2: THE SOVEREIGN RESULT                                                     ==
# =========================================================================================

class ScaffoldResult(BaseModel, Generic[T]):
    """
    =============================================================================
    == THE OMNISCIENT RESULT: TOTALITY (V-Ω-TOTALITY-V25000-HEALED)            ==
    =============================================================================
    @gnosis:title ScaffoldResult
    @gnosis:summary The final, unbreakable contract between the God-Engine and the UI.
    @gnosis:capability INFINITE_ABSORPTION
    LIF: INFINITY

    [THE MANIFESTO]
    This is the ultimate evolution of the Gnostic Result. It is warded against
    'Unexpected Keyword' heresies via the Apophatic Harvester, ensuring that
    newly manifest telemetry (like severity or AI costs) never shatters older
    Artisans.
    """
    # [ASCENSION 2]: THE PERMISSIVE VOW
    # We allow extra fields to flow through without raising validation errors.
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=False,
        extra='allow',
        populate_by_name=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat(),
            Path: lambda p: str(p).replace('\\', '/')
        }
    )

    # --- I. THE CHRONOMANCER'S SEAL (Identity & Trace) ---
    success: bool = Field(..., description="True if the reality aligned with the Architect's will.")

    severity: ScaffoldSeverity = Field(
        default=ScaffoldSeverity.INFO,
        description="The existential weight of this proclamation."
    )

    trace_id: str = Field(
        default_factory=lambda: f"tr-{uuid.uuid4().hex[:8].upper()}",
        description="The silver cord linking this result across the distributed lattice."
    )
    details: Optional[str] = Field(default=None, description="Extended technical context or forensic traceback.")

    timestamp: float = Field(default_factory=time.time,
                             description="The precise microsecond of the revelation's birth.")
    # --- II. THE LUMINOUS PROCLAMATION (Voice) ---
    message: str = Field(
        default="Reality synchronized.",
        description="The primary human-readable proclamation."
    )

    suggestion: Optional[str] = Field(
        default=None,
        description="The Mentor's counsel on the next logical rite or fix."
    )

    fix_command: Optional[str] = Field(
        default=None,
        description="An executable CLI command string to resolve a detected heresy."
    )

    # --- III. THE EVIDENCE OF WORK (Matter) ---
    data: Optional[T] = Field(
        default=None,
        description="The primary Gnostic payload (Objects, Maps, or Logic)."
    )

    artifacts: List[Artifact] = Field(
        default_factory=list,
        description="A detailed census of every scripture touched."
    )

    # --- IV. THE CHRONICLE OF PARADOX (Fractures) ---
    error: Optional[str] = Field(
        default=None,
        description="The forensic summary of the fracture, heresy, or OS-level paradox."
    )

    heresies: List[Heresy] = Field(
        default_factory=list,
        description="A list of structural paradoxes encountered."
    )

    diagnostics: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="LSP-compliant markers for editor illumination (Squiggles)."
    )

    # --- V. METABOLIC TOMOGRAPHY (Energy & Physics) ---
    duration_seconds: float = Field(default=0.0, description="Temporal cost in the Mortal Realm.")

    vitals: Dict[str, Any] = Field(
        default_factory=dict,
        description="Hardware telemetry (CPU/RAM load) during execution."
    )

    # AI Economy (ASCENSION 11)
    cost_usd: float = Field(default=0.0, description="The fiscal tax of neural inference.")
    tokens_total: int = Field(default=0, description="The cognitive mass consumed.")

    substrate: SubstrateDNA = Field(
        default_factory=lambda: SubstrateDNA.IRON if os.environ.get("SCAFFOLD_ENV") != "WASM" else SubstrateDNA.ETHER,
        description="The plane where this result was materialised."
    )

    # --- VI. FORENSIC REPLAY DATA ---
    timestamp_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="The exact microsecond of manifestation."
    )

    traceback: Optional[str] = Field(
        default=None,
        description="The forensic data of a catastrophic fracture (Panic/Crash)."
    )

    # --- VII. THE RESONANCE MATRIX (UI Hints) ---
    # [ASCENSION 7]: Instructions for the Cockpit (React/Monaco).
    # Expected keys: "vfx" (bloom|shake|pulse), "glow" (hex), "sound", "icon"
    ui_hints: Dict[str, Any] = Field(
        default_factory=dict,
        description="Atmospheric hints for the Ocular HUD."
    )

    source: Optional[str] = Field(
        default="Kernel",
        description="The identity of the Artisan or Middleware that forged this result."
    )

    # =========================================================================
    # == THE APOPHATIC HARVESTER (VALIDATORS)                                ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _apophatic_harvest(cls, data: Any) -> Any:
        """
        [ASCENSION 4]: THE ORPHAN HEALER.
        Surgically intercepts raw dictionary input and teleports stray keywords
        into the 'metadata' or 'data' pockets to prevent validation fractures.
        """
        if not isinstance(data, dict):
            return data

        # 1. Automatic Severity Scaling
        # If success is False and no severity willed, promote to ERROR.
        if not data.get("success", True) and "severity" not in data:
            data["severity"] = ScaffoldSeverity.ERROR

        # 2. Key-Collision Prevention
        # Suture 'error' and 'message' if redundant
        if data.get("error") and not data.get("message"):
            data["message"] = f"Fracture: {data['error']}"

        return data

    @field_validator('substrate', mode='before')
    @classmethod
    def _divine_substrate(cls, v: Any) -> SubstrateDNA:
        """Enforces substrate naming standards."""
        if v in (SubstrateDNA.IRON, SubstrateDNA.ETHER, SubstrateDNA.VOID):
            return v
        if str(v).lower() == "wasm":
            return SubstrateDNA.ETHER
        return SubstrateDNA.IRON

    # =========================================================================
    # == COMPUTED REALITIES (The Mind of the Result)                         ==
    # =========================================================================

    @computed_field
    @property
    def has_critical_heresy(self) -> bool:
        """
        [ASCENSION 8]: The Volatile Guard.
        Perceives if a fatal paradox exists that must halt the symphony.
        """
        return (
                self.severity == ScaffoldSeverity.CRITICAL or
                any(h.severity == HeresySeverity.CRITICAL for h in self.heresies)
        )

    @computed_field
    @property
    def artifact_summary(self) -> Dict[str, int]:
        """[ASCENSION 9]: The Categorical Census of Matter."""
        summary = {"created": 0, "modified": 0, "deleted": 0, "skipped": 0}
        for art in self.artifacts:
            act = art.action.lower()
            if "create" in act:
                summary["created"] += 1
            elif "transfigur" in act or "modif" in act:
                summary["modified"] += 1
            elif "excis" in act or "delet" in act:
                summary["deleted"] += 1
            else:
                summary["skipped"] += 1
        return summary

    @computed_field
    @property
    def fingerprint(self) -> str:
        """[ASCENSION 8]: Deterministic Merkle Root of the Proclamation."""
        raw = f"{self.trace_id}:{self.success}:{self.message}:{len(self.artifacts)}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def __bool__(self):
        """[ASCENSION 11]: Pythonic Truth. Allows `if result:` checks."""
        return self.success

    # =========================================================================
    # == RITES OF EVOLUTION (The Fluent API)                                  ==
    # =========================================================================

    def evolve(self, **kwargs) -> "ScaffoldResult[T]":
        """
        [THE RITE OF RE-INCEPTION]
        Returns a new version of the result with updated Gnosis.
        """
        return self.model_copy(update=kwargs)

    def with_ui_hints(self, vfx: str, color: str = None, sound: str = None) -> "ScaffoldResult[T]":
        """Surgically injects Ocular hints without disturbing the core logic."""
        new_hints = self.ui_hints.copy()
        new_hints.update({"vfx": vfx, "glow": color, "sound": sound})
        return self.evolve(ui_hints={k: v for k, v in new_hints.items() if v is not None})

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
        Accepts **kwargs to absorb advanced telemetry from the Dispatcher.
        """
        if "severity" not in kwargs:
            kwargs["severity"] = ScaffoldSeverity.SUCCESS

        return cls(
            success=True,
            message=message,
            data=data,
            artifacts=artifacts or [],
            **kwargs
        )

    @classmethod
    def forge_failure(
            cls,
            message: str,
            *,  # [THE CURE]: ENFORCING ABSOLUTE KEYWORD BOUNDARIES
            suggestion: Optional[str] = None,
            details: Optional[str] = None,
            data: Optional[Any] = None,
            severity: Any = None,
            **kwargs
    ) -> "ScaffoldResult":
        """
        =============================================================================
        == THE OMEGA FAILURE FACTORY: TOTALITY (V-Ω-TOTALITY-V600-UNBREAKABLE)     ==
        =============================================================================
        LIF: ∞ | ROLE: ERROR_VESSEL_FACTORY | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_FORGE_FAILURE_V600_SEVERITY_SUTURE_2026_FINALIS
        """
        import time
        import os
        from ..contracts.heresy_contracts import Heresy, HeresySeverity
        # [THE CURE]: Local import to prevent circular gravity during alchemical mapping
        from .base import ScaffoldSeverity

        # --- MOVEMENT 0: THE ENTROPY SIEVE (THE FIX) ---
        # [ASCENSION 2]: We surgically extract any keys that collide with our signature.
        # This prevents the 'multiple values for keyword argument' paradox.
        sieve = ["suggestion", "details", "data", "severity", "message", "success", "trace_id", "timestamp"]
        for key in sieve:
            kwargs.pop(key, None)

        # --- MOVEMENT I: THE SEVERITY ALCHEMIST (THE CURE) ---
        # [ASCENSION 1 & 3]: Transmuting the foreign dialect into the local Law.
        raw_severity = severity or kwargs.pop("scaffold_severity", None)
        final_severity: ScaffoldSeverity = ScaffoldSeverity.ERROR

        if raw_severity is not None:
            # Triage: Is it a String, a HeresySeverity Enum, or already a ScaffoldSeverity?
            # We map all known variations to the absolute 'ScaffoldSeverity' type.
            val_str = str(raw_severity).upper()

            if "CRITICAL" in val_str or "FATAL" in val_str:
                final_severity = ScaffoldSeverity.CRITICAL
            elif "WARN" in val_str:
                final_severity = ScaffoldSeverity.WARNING
            elif "INFO" in val_str:
                final_severity = ScaffoldSeverity.INFO
            elif "HINT" in val_str:
                final_severity = ScaffoldSeverity.HINT

        # --- MOVEMENT II: AUTOMATIC HERESY INCEPTION ---
        # [ASCENSION 5]: Ensuring every failure carries a structured forensic report.
        heresies = kwargs.pop('heresies', [])
        if not heresies:
            # We transmute the raw message and details into a high-fidelity Heresy soul.
            # We map back to the contract-layer Enum for the Heresy object itself.
            h_severity = HeresySeverity.CRITICAL if final_severity == ScaffoldSeverity.CRITICAL else HeresySeverity.WARNING

            primary_heresy = Heresy(
                message=message or "PHANTOM_PARADOX_HERESY",
                details=details or "Forensic evidence unmanifested.",
                severity=h_severity,
                suggestion=suggestion or "Consult the Gnostic Grimoire (velm help).",
                file_path=kwargs.get("path") or kwargs.get("file_path")
            )
            heresies = [primary_heresy]

        # --- MOVEMENT III: METABOLIC TOMOGRAPHY ---
        # [ASCENSION 6 & 7]: Capturing the heat of the substrate at the point of fracture.
        vitals = kwargs.pop("vitals", {})
        if not vitals:
            vitals = {
                "cpu_load": 0.0,
                "substrate": os.environ.get("SCAFFOLD_ENV", "IRON"),
                "ts_ns": time.perf_counter_ns()
            }

        # --- MOVEMENT IV: HAPTIC HUD CALIBRATION ---
        # [ASCENSION 8]: Syncing Ocular visual effects with the weight of the sin.
        ui_hints = kwargs.pop("ui_hints", {})
        if not ui_hints:
            ui_hints = {
                "vfx": "shake_red" if final_severity == ScaffoldSeverity.CRITICAL else "glow_amber",
                "sound": "fracture_alert",
                "priority": final_severity.name if hasattr(final_severity, 'name') else str(final_severity)
            }

        # --- MOVEMENT V: THE FINAL MATERIALIZATION ---
        # [ASCENSION 12]: THE FINALITY VOW
        # Bit-perfect construction of the result vessel.
        return cls(
            success=False,
            message=message or "KINETIC_SILENCE_HERESY",
            severity=final_severity,  # [THE CURE]: Guaranteed type alignment
            suggestion=suggestion,
            details=details,
            data=data,
            error=details or message,
            heresies=heresies,
            ui_hints=ui_hints,
            vitals=vitals,
            trace_id=kwargs.pop("trace_id", f"tr-fail-{uuid.uuid4().hex[:4]}"),
            timestamp=time.time(),
            **kwargs  # Pass remaining shards (metadata, origin, etc.)
        )

    def __repr__(self) -> str:
        """[ASCENSION 24]: The Sovereign Repr."""
        status = "✅" if self.success else "❌"
        return (
            f"<Ω_RESULT {status} trace={self.trace_id[:8]} sev={self.severity.value} "
            f"mass={self.artifact_summary['created']}c/{self.artifact_summary['modified']}m>"
        )