# scaffold/core/traceback/contracts.py

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


# =================================================================================
# == THE SACRED CONTRACTS OF FORENSIC GNOSIS (V-Ω-IMMUTABLE-SCHEMA)              ==
# =================================================================================
# LIF: 10,000,000,000,000
#
# These vessels hold the frozen state of the universe at the moment of entropy.
# They are forged to be:
# 1. Immutable: History cannot be rewritten.
# 2. Serializable: Truth must be transmittable (Daemon -> Client -> UI).
# 3. Context-Aware: They carry the weight of the Project Root and the Rite.
# =================================================================================

@dataclass
class GnosticFrame:
    """
    =============================================================================
    == THE ATOM OF EXECUTION (STACK FRAME)                                     ==
    =============================================================================
    A single slice of the call stack. It captures the 'Where' and the 'What'.
    """
    # --- Spatial Coordinates ---
    filename: str  # Relative path for display (e.g., "core/engine.py")
    abs_path: str  # Absolute path for linking (e.g., "/usr/home/.../core/engine.py")
    lineno: int  # The line number where time stopped
    name: str  # The function or module name (e.g., "dispatch")

    # --- The Scripture ---
    line_content: str  # The specific line of code executed
    context_lines: List[str] = field(default_factory=list)  # Surrounding lines for context
    context_start_lineno: int = 0  # The line number where context begins

    # --- The State of the Soul ---
    locals: Dict[str, str] = field(default_factory=dict)  # Captured local variables (Sanitized)

    # --- Gnostic Metadata ---
    is_scaffold_code: bool = False  # True if part of the God-Engine
    is_library_code: bool = False  # True if part of site-packages/stdlib
    component_type: str = "Unknown"  # 'Artisan', 'Middleware', 'Kernel', 'Plugin'
    component_name: str = ""  # The class name (e.g., 'WeaveArtisan')

    # --- The Neural Link ---
    editor_link: str = ""  # URI scheme to open this frame in the Editor

    def to_dict(self) -> Dict[str, Any]:
        """Transmutes the Frame into a pure dictionary for serialization."""
        return asdict(self)


@dataclass
class GnosticError:
    """
    =============================================================================
    == THE DOSSIER OF PARADOX (EXCEPTION WRAPPER)                              ==
    =============================================================================
    The complete chronicle of a crash. It holds the stack, the environment, and
    the chain of causality.
    """
    # --- Core Identity ---
    exc_type: str  # e.g., "ArtisanHeresy", "ValueError"
    exc_value: str  # The message payload
    timestamp: str  # ISO-8601 timestamp of the crash

    # --- The Stack ---
    frames: List[GnosticFrame]

    # --- Contextual Gnosis ---
    active_rite: str = "Unknown"  # The command being executed (e.g., "scaffold weave")
    project_root: str = "Unknown"  # The root of the sanctum
    session_id: str = "Unknown"  # The tracing ID

    # --- The Echoes ---
    polyglot_context: Optional[str] = None  # Stderr from foreign processes (Node/Go/Rust)

    # --- The Chain of Causality (Recursive Error Tracking) ---
    cause: Optional['GnosticError'] = None  # from 'raise ... from cause'
    context: Optional['GnosticError'] = None  # from implicit exception chaining

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the entire error tree.
        Manually handles recursive fields to prevent infinite recursion or dict errors.
        """
        data = asdict(self)
        # Recursively serialize cause/context if they exist
        if self.cause:
            data['cause'] = self.cause.to_dict()
        if self.context:
            data['context'] = self.context.to_dict()
        return data

    @property
    def critical_frame(self) -> Optional[GnosticFrame]:
        """
        [THE GAZE OF RELEVANCE]
        Returns the most significant frame.
        Prioritizes the last frame of *User Code* or *Scaffold Code* over *Library Code*.
        """
        # Iterate backwards
        for frame in reversed(self.frames):
            # If we find scaffold code, that's likely the culprit or the catch point
            if frame.is_scaffold_code:
                return frame

        # Fallback: Return the actual last frame (even if it's in a library)
        return self.frames[-1] if self.frames else None

    @property
    def is_heresy(self) -> bool:
        """Determines if this is a known ArtisanHeresy or a raw system crash."""
        return "Heresy" in self.exc_type

    def summary(self) -> str:
        """A concise proclamation of the failure."""
        return f"[{self.timestamp}] {self.exc_type}: {self.exc_value} (Rite: {self.active_rite})"