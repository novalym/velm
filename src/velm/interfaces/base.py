# Path: interfaces/base.py
# ------------------------

from __future__ import annotations
import json
import os
import uuid
import time
import hashlib
import platform
import traceback
import mimetypes
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
# == STRATUM 0: THE TAXONOMY OF TRUTH (ENUMS)                                            ==
# =========================================================================================

class ScaffoldSeverity(str, Enum):
    """
    =============================================================================
    == THE SCALES OF JUDGMENT (V-Ω-SEVERITY-LATTICE)                           ==
    =============================================================================
    Defines the existential weight of a Gnostic Proclamation.
    """
    HINT = "hint"  # A whisper of architectural optimization.
    INFO = "info"  # Standard metabolic pulse.
    SUCCESS = "success"  # A rite concluded in total purity.
    WARNING = "warning"  # A sign of drift or non-fatal paradox.
    ERROR = "error"  # A logic fracture requiring immediate mending.
    CRITICAL = "critical"  # A catastrophic collapse of the multiversal context.


class SubstrateDNA(str, Enum):
    """
    =============================================================================
    == THE SUBSTRATE DNA (V-Ω-GEOSPATIAL-ANCHOR)                               ==
    =============================================================================
    Defines the physical plane where the result was forged.
    """
    IRON = "iron_native"  # Local CPU / Standalone Binary on physical metal.
    ETHER = "ether_wasm"  # Browser / Pyodide / WASM Ethereal Plane.
    VOID = "void_sim"  # Quantum Simulation / Shadow Clone / Dry-run.


# =========================================================================================
# == STRATUM 1: THE ATOMIC ARTIFACT (PHYSICAL MATTER)                                    ==
# =========================================================================================

class Artifact(BaseModel):
    """
    =============================================================================
    == THE ATOMIC ARTIFACT (V-Ω-MATTER-VESSEL-ASCENDED)                        ==
    =============================================================================
    LIF: 1,000,000 | ROLE: MATTER_FINGERPRINT
    """
    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={Path: lambda p: str(p).replace('\\', '/')}
    )

    # --- I. THE COORDINATE (SPACETIME) ---
    path: Path = Field(..., description="The logical coordinate in the project sanctum.")
    type: str = Field("file", pattern=r"^(file|directory|symlink|socket|virtual)$")

    # [ASCENSION 18]: Action Verb Normalization via validation
    action: str = Field(..., description="The rite performed (created|modified|deleted|skipped).")

    # --- II. THE MASS (METABOLISM) ---
    size_bytes: int = Field(0, ge=0)
    checksum: Optional[str] = Field(None, description="The SHA256 Merkle Fingerprint.")

    # --- III. THE SOUL (LANGUAGE) ---
    mime_type: str = Field("text/plain", description="The Gnostic dialect for UI highlighters.")
    encoding: str = Field("utf-8", description="The character-set of the soul.")

    # --- IV. THE CONTEXT (FORENSICS) ---
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # =========================================================================
    # == COMPUTED REALITIES & VALIDATORS                                     ==
    # =========================================================================

    @computed_field
    @property
    def name(self) -> str:
        """The atomic name of the artifact, extracted from the coordinate."""
        return self.path.name

    @computed_field
    @property
    def extension(self) -> str:
        """The lexical suffix of the matter."""
        return self.path.suffix.lstrip('.')

    @field_validator('path', mode='before')
    @classmethod
    def _normalize_geometry(cls, v: Any) -> Path:
        """Absolute POSIX slash harmony."""
        if isinstance(v, str):
            v = Path(os.path.expanduser(v.replace('\\', '/')))
        return v

    @model_validator(mode='before')
    @classmethod
    def _divine_mime_type(cls, data: Any) -> Any:
        """
        [ASCENSION 4]: THE MIME-TYPE ORACLE.
        Automatically guesses the MIME type if the Architect left it void.
        """
        if isinstance(data, dict):
            # Normalize Action Verb
            if 'action' in data:
                act = str(data['action']).lower()
                if 'create' in act:
                    data['action'] = 'created'
                elif 'transfigur' in act or 'modif' in act or 'updat' in act:
                    data['action'] = 'modified'
                elif 'excis' in act or 'delet' in act or 'remov' in act:
                    data['action'] = 'deleted'

            # Divine Mime Type
            if 'mime_type' not in data or data['mime_type'] == 'text/plain':
                path_obj = data.get('path')
                if path_obj:
                    p_str = str(path_obj)
                    mime, _ = mimetypes.guess_type(p_str)
                    if mime:
                        data['mime_type'] = mime
                    elif p_str.endswith(('.ts', '.tsx')):
                        data['mime_type'] = 'application/typescript'
                    elif p_str.endswith(('.scaffold', '.arch', '.symphony')):
                        data['mime_type'] = 'text/x-scaffold'
                    elif p_str.endswith(('.rs',)):
                        data['mime_type'] = 'text/rust'
                    elif p_str.endswith(('.go',)):
                        data['mime_type'] = 'text/x-go'
        return data


# =========================================================================================
# == STRATUM 2: THE SOVEREIGN RESULT (THE HEART)                                         ==
# =========================================================================================

class ScaffoldResult(BaseModel, Generic[T]):
    """
    =============================================================================
    == THE OMNISCIENT RESULT: TOTALITY (V-Ω-TOTALITY-V500000-HEALED-FINALIS)   ==
    =============================================================================
    @gnosis:title ScaffoldResult
    @gnosis:summary The final, unbreakable contract between the God-Engine and the UI.
    @gnosis:LIF INFINITY
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=False,
        extra='allow',
        populate_by_name=True,
        validate_assignment=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat(),
            Path: lambda p: str(p).replace('\\', '/')
        }
    )

    # --- I. THE CHRONOMANCER'S SEAL (Identity & Spacetime) ---
    success: bool = Field(..., description="True if reality aligned with intent.")
    severity: ScaffoldSeverity = Field(default=ScaffoldSeverity.INFO)
    trace_id: str = Field(default_factory=lambda: f"tr-{uuid.uuid4().hex[:8].upper()}")
    details: Optional[str] = Field(default=None)

    # [ASCENSION 9]: IMMUTABLE GENESIS TIMESTAMP
    timestamp: float = Field(default_factory=time.time)
    timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # --- II. THE LUMINOUS PROCLAMATION (Voice) ---
    message: str = Field(default="Reality synchronized.")
    suggestion: Optional[str] = Field(default=None)
    fix_command: Optional[str] = Field(default=None)

    # --- III. THE EVIDENCE OF WORK (Matter) ---
    data: Optional[T] = Field(default=None)
    artifacts: List[Artifact] = Field(default_factory=list)

    # --- IV. THE CHRONICLE OF PARADOX (Fractures) ---
    error: Optional[str] = Field(default=None)
    heresies: List[Heresy] = Field(default_factory=list)
    diagnostics: List[Dict[str, Any]] = Field(default_factory=list)

    # --- V. METABOLIC TOMOGRAPHY (Energy & Physics) ---
    duration_seconds: float = Field(default=0.0)
    vitals: Dict[str, Any] = Field(default_factory=dict)
    cost_usd: float = Field(default=0.0)
    tokens_total: int = Field(default=0)
    substrate: SubstrateDNA = Field(
        default_factory=lambda: SubstrateDNA.IRON if os.environ.get("SCAFFOLD_ENV") != "WASM" else SubstrateDNA.ETHER
    )

    # --- VI. FORENSIC REPLAY DATA ---
    traceback: Optional[str] = Field(default=None)

    # --- VII. THE RESONANCE MATRIX (UI Hints) ---
    ui_hints: Dict[str, Any] = Field(default_factory=dict)
    source: str = Field(default="Kernel")

    # =========================================================================
    # == THE APOPHATIC HARVESTER (PRE-VALIDATION)                            ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _apophatic_harvest(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        # [ASCENSION 3]: ARTIFACT DEDUPLICATION
        if 'artifacts' in data and isinstance(data['artifacts'], list):
            unique_arts = {}
            new_arts = []
            for art in data['artifacts']:
                if isinstance(art, dict) and 'path' in art:
                    p = str(art['path'])
                    if p not in unique_arts:
                        unique_arts[p] = True
                        new_arts.append(art)
                elif hasattr(art, 'path'):
                    p = str(art.path)
                    if p not in unique_arts:
                        unique_arts[p] = True
                        new_arts.append(art)
            data['artifacts'] = new_arts

        # Automatic Severity Scaling
        if not data.get("success", True) and "severity" not in data:
            data["severity"] = ScaffoldSeverity.ERROR

        # Key-Collision Prevention
        if data.get("error") and not data.get("message"):
            data["message"] = f"Fracture: {data['error']}"

        # Substrate Reconciliation
        if "scaffold_env" in data:
            env = str(data.pop("scaffold_env")).lower()
            if "wasm" in env:
                data["substrate"] = SubstrateDNA.ETHER
            elif "sim" in env:
                data["substrate"] = SubstrateDNA.VOID
            else:
                data["substrate"] = SubstrateDNA.IRON

        # [ASCENSION 7]: RECURSIVE NULL EXORCISM
        for dict_key in ('ui_hints', 'metadata', 'vitals'):
            if dict_key in data and isinstance(data[dict_key], dict):
                data[dict_key] = {k: v for k, v in data[dict_key].items() if v is not None}

        # [ASCENSION 16]: ERROR CODE EXTRACTION
        msg = data.get("message", "")
        if isinstance(msg, str) and "[" in msg and "]" in msg:
            import re
            match = re.search(r'\[([A-Z0-9_]+)\]', msg)
            if match and 'metadata' not in data:
                data['metadata'] = {}
            if match and 'metadata' in data:
                data['metadata']['error_code'] = match.group(1)

        return data

    @field_validator('substrate', mode='before')
    @classmethod
    def _divine_substrate(cls, v: Any) -> SubstrateDNA:
        """[ASCENSION 11]: SUBSTRATE COERCION MATRIX."""
        if v in (SubstrateDNA.IRON, SubstrateDNA.ETHER, SubstrateDNA.VOID): return v
        val_str = str(v).lower()
        if "wasm" in val_str or "ether" in val_str or "browser" in val_str: return SubstrateDNA.ETHER
        if "sim" in val_str or "void" in val_str or "dry" in val_str: return SubstrateDNA.VOID
        return SubstrateDNA.IRON

    # =========================================================================
    # == COMPUTED REALITIES                                                  ==
    # =========================================================================

    @computed_field
    @property
    def has_critical_heresy(self) -> bool:
        return (self.severity == ScaffoldSeverity.CRITICAL or any(
            h.severity == HeresySeverity.CRITICAL for h in self.heresies))

    @computed_field
    @property
    def is_fatal(self) -> bool:
        """[ASCENSION 19]: The Bipartition Gaze."""
        return not self.success and self.has_critical_heresy

    @computed_field
    @property
    def is_recoverable(self) -> bool:
        """[ASCENSION 19]: The Bipartition Gaze."""
        return not self.success and not self.has_critical_heresy

    @computed_field
    @property
    def artifact_summary(self) -> Dict[str, int]:
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
        """[ASCENSION 15]: The Fingerprint Oracle."""
        # Include artifact paths in the hash to ensure structural uniqueness
        art_fingerprint = ",".join(sorted(str(a.path) for a in self.artifacts))
        raw = f"{self.trace_id}:{self.success}:{self.message}:{art_fingerprint}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def __bool__(self):
        return self.success

    def evolve(self, **kwargs) -> "ScaffoldResult[T]":
        """[ASCENSION 8]: Deeply preserves the generic type payload during copy."""
        return self.model_copy(update=kwargs)

    def with_ui_hints(self, vfx: str, color: Optional[str] = None, sound: Optional[str] = None) -> "ScaffoldResult[T]":
        new_hints = self.ui_hints.copy()
        new_hints.update({"vfx": vfx, "glow": color, "sound": sound})
        return self.evolve(ui_hints={k: v for k, v in new_hints.items() if v is not None})

    # =========================================================================
    # == RITES OF GENERATION (THE TITANIUM FACTORIES)                        ==
    # =========================================================================

    @classmethod
    def forge_success(
            cls,
            message: str = "Reality synchronized.",
            **kwargs
    ) -> "ScaffoldResult[T]":
        """
        =============================================================================
        == THE RITE OF VICTORY: UNBOUND (V-Ω-TOTALITY-HEALED-V500K)                ==
        =============================================================================
        [THE MASTER CURE]: Trace ID and Severity are surgically extracted from **kwargs.
        This completely annihilates the `got multiple values for keyword argument`
        TypeError when BaseArtisan passes them dynamically.
        """
        # 1. Surgically extract reserved keys
        trace_id = kwargs.pop("trace_id", None)
        severity = kwargs.pop("severity", ScaffoldSeverity.SUCCESS)

        # 2. Exorcise duplicate definitions
        kwargs.pop("success", None)
        kwargs.pop("message", None)
        kwargs.pop("data", None)
        kwargs.pop("artifacts", None)

        # 3. Retrieve payload and artifacts from kwargs if present (since popped above from args list)
        # Note: If passed as kwargs to THIS function, they are in kwargs dict.
        # But we just popped them with None default above, losing them if they WERE in kwargs.
        # CORRECTION: We assume the caller might pass `data=...` inside kwargs.
        # To be safe, we retrieve them before popping if they weren't passed as args to this func.
        # Actually, forge_success signature has explicit args for data/artifacts in some versions.
        # This version has `**kwargs`. Let's assume standard usage:
        # forge_success(msg, data=d, artifacts=a).
        # These end up in kwargs.

        # RE-IMPLEMENTATION TO BE SAFE:
        data = kwargs.get("data")  # Use get, will be in kwargs dict
        artifacts = kwargs.get("artifacts", [])

        # Now pop safely to avoid double-passing to cls()
        kwargs.pop("data", None)
        kwargs.pop("artifacts", None)

        return cls(
            success=True,
            message=message,
            data=data,
            artifacts=artifacts or [],
            trace_id=trace_id or f"tr-ok-{uuid.uuid4().hex[:6].upper()}",
            severity=severity,
            **kwargs
        )

    @classmethod
    def forge_failure(
            cls,
            message: str = "KINETIC_SILENCE_HERESY",
            **kwargs
    ) -> "ScaffoldResult":
        """
        =============================================================================
        == THE OMEGA FAILURE FACTORY: TOTALITY (V-Ω-TOTALITY-V600-UNBREAKABLE)     ==
        =============================================================================
        [THE MASTER CURE]: Identical to `forge_success`, this factory surgically
        extracts all known Pydantic fields from `**kwargs` before instantiation.
        """
        # --- 1. SURGICAL PARAMETER DISTILLATION ---
        suggestion = kwargs.pop("suggestion", None)
        details = kwargs.pop("details", None)
        data = kwargs.pop("data", None)
        trace_id = kwargs.pop("trace_id", None)
        raw_error = kwargs.pop("error", message)
        raw_severity = kwargs.pop("severity", ScaffoldSeverity.ERROR)
        heresies = kwargs.pop("heresies", [])
        vitals = kwargs.pop("vitals", {})
        ui_hints = kwargs.pop("ui_hints", {})
        traceback_data = kwargs.pop("traceback", None)
        fix_command = kwargs.pop("fix_command", None)

        # --- 2. EXORCISE DUPLICATES ---
        kwargs.pop("success", None)
        kwargs.pop("message", None)

        # --- 3. THE SEVERITY ALCHEMIST ---
        final_severity = ScaffoldSeverity.ERROR
        if raw_severity is not None:
            val_str = str(raw_severity).upper()
            if "CRITICAL" in val_str or "FATAL" in val_str:
                final_severity = ScaffoldSeverity.CRITICAL
            elif "WARN" in val_str:
                final_severity = ScaffoldSeverity.WARNING
            elif "INFO" in val_str:
                final_severity = ScaffoldSeverity.INFO

        # --- 4. HERESY TRANSMUTATION ENGINE ---
        sanitized_heresies = []
        for h in heresies:
            if isinstance(h, Heresy):
                sanitized_heresies.append(h)
            elif isinstance(h, dict):
                try:
                    sanitized_heresies.append(Heresy(**h))
                except Exception:
                    pass
            elif isinstance(h, Exception):
                sanitized_heresies.append(Heresy(
                    message=type(h).__name__,
                    details=str(h),
                    severity=HeresySeverity.CRITICAL if final_severity == ScaffoldSeverity.CRITICAL else HeresySeverity.WARNING
                ))
            elif isinstance(h, str):
                sanitized_heresies.append(Heresy(message=h, severity=HeresySeverity.WARNING))

        # --- 5. AUTOMATIC HERESY INCEPTION ---
        if not sanitized_heresies:
            h_severity = HeresySeverity.CRITICAL if final_severity == ScaffoldSeverity.CRITICAL else HeresySeverity.WARNING
            sanitized_heresies = [Heresy(
                message=message or "PHANTOM_PARADOX_HERESY",
                details=details or "Forensic evidence unmanifested.",
                severity=h_severity,
                suggestion=suggestion or "Consult the Gnostic Grimoire (velm help).",
                file_path=kwargs.get("path") or kwargs.get("file_path")
            )]

        # --- 6. METABOLIC TOMOGRAPHY & VITALS FUSION (ASCENSION 20) ---
        default_vitals = {
            "cpu_load": 0.0,
            "substrate": os.environ.get("SCAFFOLD_ENV", "IRON"),
            "ts_ns": time.perf_counter_ns()
        }

        # [THE CURE]: Safe PSUtil Access
        try:
            import psutil
            # We use Process() instead of virtual_memory() to get RSS correctly
            proc = psutil.Process()
            default_vitals["cpu_load"] = proc.cpu_percent()
            # This is the line that was fracturing. Now fixed.
            default_vitals["memory_mb"] = proc.memory_info().rss / (1024 * 1024)
        except Exception:
            # Broad exception catch to ensure we never crash during failure reporting
            pass

        # Fuse explicitly provided vitals with the default system snapshot
        if vitals and isinstance(vitals, dict):
            default_vitals.update(vitals)

        # --- 7. HAPTIC HUD CALIBRATION ---
        if not ui_hints:
            ui_hints = {
                "vfx": "shake_red" if final_severity == ScaffoldSeverity.CRITICAL else "glow_amber",
                "sound": "fracture_alert",
                "priority": final_severity.value
            }

        # --- 8. FIX COMMAND NORMALIZATION ---
        if fix_command:
            fix_command = fix_command.strip().strip("`").strip()

        # --- 9. THE FINALITY DISPATCH ---
        return cls(
            success=False,
            message=message or "KINETIC_SILENCE_HERESY",
            severity=final_severity,
            suggestion=suggestion,
            fix_command=fix_command,
            details=details,
            data=data,
            error=raw_error,
            heresies=sanitized_heresies,
            ui_hints=ui_hints,
            vitals=default_vitals,
            trace_id=trace_id or f"tr-fail-{uuid.uuid4().hex[:4].upper()}",
            timestamp=time.time(),
            traceback=traceback_data,
            **kwargs
        )

    def __repr__(self) -> str:
        """[ASCENSION 24]: THE SOVEREIGN REPR."""
        status = "✅" if self.success else "❌"
        try:
            summary = self.artifact_summary
            mass_str = f"mass={summary['created']}c/{summary['modified']}m"
        except Exception:
            mass_str = f"mass={len(self.artifacts)}"

        return (
            f"<Ω_RESULT {status} trace={self.trace_id[:8]} sev={self.severity.value} {mass_str}>"
        )