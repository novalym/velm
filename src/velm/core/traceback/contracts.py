# Path: scaffold/core/traceback/contracts.py
# ------------------------------------------
# LIF: ∞ | ROLE: FORENSIC_LEDGER_SCHEMA | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONTRACTS_V9001_TOTALITY_SUTURE_2026

from __future__ import annotations
import json
import hashlib
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Final
from datetime import datetime, timezone


# =================================================================================
# == THE SACRED CONTRACTS OF FORENSIC GNOSIS (V-Ω-TOTALITY-V9001)                ==
# =================================================================================
# LIF: ∞ | ROLE: IMMUTABLE_PARADOX_VESSELS
#
# These vessels hold the frozen state of the universe at the moment of entropy.
# They are forged to be the absolute source of truth for Stratum-4 (The Akasha).
# =================================================================================

@dataclass(frozen=True)
class GnosticFrame:
    """
    =============================================================================
    == THE ATOM OF EXECUTION (V-Ω-STACK-FRAME-ASCENDED)                        ==
    =============================================================================
    A single slice of the call stack. It captures the 'Where', the 'What',
    and the 'Contextual Soul' of the variables at that coordinate.
    """
    # --- Spatial Coordinates ---
    filename: str  # Relative path: "core/engine/dispatcher.py"
    abs_path: str  # Physical anchor: "/vault/project/src/..."
    lineno: int  # The line number where time stopped
    name: str  # The function/module name: "conduct_rite"

    # --- The Scripture ---
    line_content: str  # The specific line of code executed
    context_lines: List[str] = field(default_factory=list)
    context_start_lineno: int = 0

    # --- The State of the Soul ---
    # Captured local variables, stringified and warded against high-entropy secrets.
    locals: Dict[str, str] = field(default_factory=dict)

    # --- Gnostic Metadata ---
    is_scaffold_code: bool = False
    is_library_code: bool = False
    component_type: str = "Unknown"  # 'Artisan', 'Middleware', 'Kernel', 'Plugin'
    component_name: str = ""  # e.g., 'GenesisMaterializer'

    # --- The Neural Link ---
    # Isomorphic URI for Monaco/VSCode linking (e.g. file:///...)
    editor_link: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF SELF-PROCLAMATION (THE FIX)                                 ==
        =============================================================================
        [THE CURE]: Explicitly materializes the frame as a pure dictionary.
        """
        return asdict(self)

    @property
    def fingerprint(self) -> str:
        """[ASCENSION 6]: Deterministic hash of the frame's coordinate and content."""
        raw = f"{self.abs_path}:{self.lineno}:{self.line_content.strip()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]


@dataclass
class GnosticError:
    """
    =============================================================================
    == THE DOSSIER OF PARADOX: TOTALITY (V-Ω-TOTALITY-V9002-FINALIS)           ==
    =============================================================================
    LIF: ∞ | ROLE: CAUSAL_CHRONICLE_VESSEL | RANK: OMEGA

    The complete, forensic chronicle of a crash. It bridges the gap between
    the physical failure and the architectural redemption path.
    """
    # --- I. THE IDENTITY PHALANX ---
    exc_type: str  # e.g., "ArtisanHeresy", "ConnectionError"
    exc_value: str  # The scrubbed message payload
    timestamp: str  # ISO-8601 UTC

    # --- II. THE STACK LATTICE ---
    frames: List[GnosticFrame]

    # --- III. CONTEXTUAL GNOSIS (THE ANCHORS) ---
    active_rite: str = "Unknown"
    project_root: str = "Unknown"
    session_id: str = "Unknown"

    # [ASCENSION 1]: MERKLE HERESY FINGERPRINT
    # Unique ID derived from the stack and type to detect recurring paradoxes.
    heresy_id: str = field(default="0xVOID")
    trace_id: str = field(default="tr-unbound")

    # --- IV. THE METADATA SANCTUM (THE SUTURE) ---
    # [ASCENSION 13]: ARBITRARY FORENSIC EXTENSIBILITY
    # Holds ephemeral tags, specific hardware fingerprints, or session-drift data.
    metadata: Dict[str, Any] = field(default_factory=dict)

    # --- V. METABOLIC TOMOGRAPHY ---
    # System vitals (CPU/RAM/Substrate) at the moment of collapse.
    vitals: Dict[str, Any] = field(default_factory=dict)

    # --- VI. THE REDEMPTION STRATUM ---
    # Predicted cure provided by the Diagnostician.
    suggestion: Optional[str] = None
    fix_command: Optional[str] = None

    # --- VII. THE OCULAR RESONANCE ---
    # Haptic instructions for the UI (vfx, sound, priority).
    ui_hints: Dict[str, Any] = field(default_factory=lambda: {
        "vfx": "shake_red",
        "sound": "fracture_alert",
        "priority": "CRITICAL"
    })

    # --- VIII. THE CAUSAL CHAIN ---
    cause: Optional[GnosticError] = None  # Explicit 'raise ... from'
    context: Optional[GnosticError] = None  # Implicit nested exceptions
    polyglot_context: Optional[str] = None  # Foreign stderr (Node/Rust/Go)

    def to_dict(self) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF RECURSIVE SERIALIZATION (V-Ω-TOTALITY)                      ==
        =============================================================================
        Transmutes the entire error tree into a JSON-safe dictionary.
        """
        # 1. Materialize base data (Including the newly sutured Metadata)
        data = {
            "exc_type": self.exc_type,
            "exc_value": self.exc_value,
            "timestamp": self.timestamp,
            "heresy_id": self.heresy_id,
            "trace_id": self.trace_id,
            "session_id": self.session_id,
            "active_rite": self.active_rite,
            "project_root": self.project_root,
            "metadata": self.metadata,  # [THE FIX]: Metadata is manifest
            "vitals": self.vitals,
            "suggestion": self.suggestion,
            "fix_command": self.fix_command,
            "ui_hints": self.ui_hints,
            "polyglot_context": self.polyglot_context,
            # Call to_dict() on every frame
            "frames": [f.to_dict() for f in self.frames if hasattr(f, 'to_dict')]
        }

        # 2. [ASCENSION 12]: RECURSIVE CAUSALITY SUTURE
        # We manually recurse to avoid any dataclass-depth limitations.
        if self.cause:
            data['cause'] = self.cause.to_dict() if hasattr(self.cause, 'to_dict') else asdict(self.cause)
        if self.context:
            data['context'] = self.context.to_dict() if hasattr(self.context, 'to_dict') else asdict(self.context)

        return data

    @property
    def critical_frame(self) -> Optional[GnosticFrame]:
        """
        [THE GAZE OF RELEVANCE]
        Surgically extracts the frame representing the true locus of fracture.
        Prioritizes: Plugin Code -> Artisan Code -> Middleware -> Kernel.
        """
        # Prioritized Component Scan
        priority = ["Plugin", "Artisan", "Middleware", "Kernel"]
        for p_type in priority:
            for frame in reversed(self.frames):
                if frame.component_type == p_type:
                    return frame

        # Fallback: Last non-library frame
        for frame in reversed(self.frames):
            if not frame.is_library_code:
                return frame

        return self.frames[-1] if self.frames else None

    @property
    def is_heresy(self) -> bool:
        """Adjudicates if this is a warded ArtisanHeresy or a profane system crash."""
        return "Heresy" in self.exc_type or self.exc_type == "ArtisanHeresy"

    def summary(self) -> str:
        """A high-status proclamation of the failure for the terminal."""
        return (
            f"[bold red]FRACTURE[/] [{self.heresy_id}] "
            f"Type: {self.exc_type} | "
            f"Rite: {self.active_rite}\n"
            f"Message: {self.exc_value}"
        )