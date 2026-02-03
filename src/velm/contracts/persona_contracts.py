# Path: scaffold/contracts/persona_contracts.py
# --------------------------------------------
# LIF: 100x | The Gnostic Mask Contract (V-Ω)

from enum import Enum, auto
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class WorkflowStyle(str, Enum):
    INITIATE = "INITIATE"  # Pure manual control, minimal noise.
    MAESTRO = "MAESTRO"  # High-velocity, generative, proactive.
    SENTINEL = "SENTINEL"  # Security, purity, and structural integrity.
    ARCHITECT = "ARCHITECT"  # Large-scale refactoring, system-wide health.
    POET = "POET"  # Documentation, knowledge, and narrative.


class UserGrade(str, Enum):
    STANDARD = "standard"
    POWER = "power"
    DEVELOPER = "developer"


class Persona(BaseModel):
    """The complete identity of the Conductor."""
    id: str
    name: str
    style: WorkflowStyle
    grade: UserGrade
    detectors: List[str] = Field(default_factory=list)
    auto_redeem: bool = False
    ui_tint: str = "#06b6d4"  # Default Cyan
    physics_gravity: float = 1.0
    neural_bias: str = "balanced"

