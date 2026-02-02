# Path: scaffold/artisans/shadow_clone/contracts.py
# -----------------------------------------------
# LIF: INFINITY // AUTH_CODE: #!@RECLAMATION_V15.5_CONTRACT_SINGULARITY
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# -----------------------------------------------

import time
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, List, Any, Union
from pydantic import BaseModel, Field, ConfigDict, computed_field


class ShadowStatus(str, Enum):
    """
    =============================================================================
    == THE GNOSTIC STATES OF EXISTENCE                                         ==
    =============================================================================
    Defines the physical alignment of a parallel reality within the OS Kernel.
    """
    INITIALIZING = "INITIALIZING"  # Matter is being forged
    ACTIVE = "ACTIVE"  # Kinetic energy is flowing (Process running)
    HIBERNATING = "HIBERNATING"  # Matter exists, energy is frozen
    FRACTURED = "FRACTURED"  # A logic error has shattered the reality
    ZOMBIE = "ZOMBIE"  # PID exists but the soul has departed
    VANISHED = "VANISHED"  # Returned to the void


class ShadowEntity(BaseModel):
    """
    =================================================================================
    == THE SOVEREIGN SHADOW ENTITY (V-Ω-PYDANTIC-TOTALITY-V15.5)                   ==
    =================================================================================
    @gnosis:title The Genetic Map of Reality
    @gnosis:summary The definitive data contract for a Materialized Shadow Reality.
    @gnosis:LIF INFINITY
    @gnosis:auth_code: #!@RECLAMATION_CONTRACT_V15.5

    [THE CURE]: This model now contains the 'aura' attribute and self-healing
    defaults to annihilate the AttributeError and close the Circuit Breaker.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        extra='allow',  # [ASCENSION 11]: Absorb future matter without fracture
        frozen=False  # Mutable for internal state updates
    )

    # --- I. CORE IDENTITY (THE NAME) ---
    id: str = Field(..., description="Unique UUID/Hash for this parallel dimension.")
    label: str = Field(..., description="Human-readable tag (e.g., project name).")
    target_ref: str = Field("HEAD", description="The Git reference / Rite ID from which matter was cloned.")
    parent_rite_id: Optional[str] = Field(None, description="The specific rite that birthed this fission.")

    # --- II. SPATIAL ANCHORS (THE PLACE) ---
    root_path: str = Field(..., description="Absolute physical path on the mortal filesystem.")

    # --- [ASCENSION 1]: THE AURA DIVINATION (THE 404 FIX) ---
    aura: str = Field(
        default="static",
        description="The perceived soul of the server: 'static', 'vite', 'fastapi', etc."
    )

    # --- III. NETWORK PHYSICS (THE FREQUENCY) ---
    port: int = Field(..., description="Primary web server resonance port.")
    debug_port: Optional[int] = Field(None, description="Debugpy/Node Inspector port.")
    host: str = Field("127.0.0.1", description="The local interface binding.")
    is_tunnel_active: bool = Field(False, description="True if a public wormhole is open.")
    tunnel_url: Optional[str] = Field(None, description="The public celestial URI.")

    # --- IV. KINETIC ANCHORS (THE LIFE) ---
    pid: Optional[int] = Field(None, description="OS Process ID of the breathing reality.")
    status: ShadowStatus = Field(default=ShadowStatus.INITIALIZING)

    # --- V. TELEMETRY PATHS (THE SENSES) ---
    stdout_log_path: Optional[str] = Field(None, description="Path to standard output stream.")
    stderr_log_path: Optional[str] = Field(None, description="Path to standard error stream.")

    # --- VI. INTEGRITY & DRIFT (THE TRUTH) ---
    # [ASCENSION 14]: Merkle Guard
    merkle_hash: Optional[str] = Field(
        default=None,
        description="SHA-256 fingerprint of the directory structure to detect drift."
    )

    # --- VII. TEMPORAL GOVERNANCE (THE CLOCK) ---
    created_at: float = Field(default_factory=time.time)
    last_accessed: float = Field(default_factory=time.time)
    ttl_seconds: int = Field(3600, description="Time-to-live before dimension recycling.")

    # --- VIII. RESOURCE CONTAINMENT (THE CAGE) ---
    cpu_limit_percent: float = Field(50.0, description="CPU containment field cap.")
    memory_limit_mb: float = Field(1024.0, description="RAM matter-state limit.")

    # --- IX. AI METADATA (THE CONTEXT) ---
    owner: str = Field("architect", description="The identity of the manifestor.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extension vessel.")

    # =============================================================================
    # == COMPUTED REALITIES (V-Ω)                                                ==
    # =============================================================================

    @computed_field
    @property
    def url(self) -> str:
        """[ASCENSION 9]: The primary Gnostic coordinate for the Ocular frame."""
        return f"http://{self.host}:{self.port}"

    @computed_field
    @property
    def is_expired(self) -> bool:
        """[ASCENSION 3]: Determines if entropy has reclaimed this reality."""
        return time.time() > (self.created_at + self.ttl_seconds)

    def to_dict(self) -> Dict[str, Any]:
        """Transmutes the vessel into a serializable dictionary."""
        return self.model_dump()


class StateCloningResult(BaseModel):
    """The result of the Database Fission rite."""
    success: bool
    db_url: Optional[str] = None
    container_id: Optional[str] = None
    host_port: Optional[int] = None
    error: Optional[str] = None
    duration_ms: float = 0.0

# == END OF SCRIPTURE ==