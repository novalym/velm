# Path: artisans/shadow_clone/contracts.py
# -----------------------------------------------
# LIF: INFINITY // AUTH_CODE: #!@RECLAMATION_V15.5_CONTRACT_SINGULARITY
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# =================================================================================
# == THE DIMENSIONAL CONTRACTS (V-Ω-TOTALITY-V25000-BICAMERAL)                   ==
# =================================================================================

import time
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, List, Any, Union, Final
from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator


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


class ShadowMode(str, Enum):
    """
    =============================================================================
    == THE BICAMERAL MODES                                                     ==
    =============================================================================
    Distinguishes between ephemeral preview and high-status experimentation.
    """
    RUN = "run"  # Ephemeral execution (Cockpit Previews)
    LAB = "lab"  # High-risk refactoring / AI Laboratory


class SubstrateType(str, Enum):
    """The physical plane where the dimension manifests."""
    IRON = "iron_native"
    ETHER = "ether_wasm"


class ShadowEntity(BaseModel):
    """
    =================================================================================
    == THE SOVEREIGN SHADOW ENTITY (V-Ω-TOTALITY-V25000-HEALED)                    ==
    =================================================================================
    @gnosis:title The Genetic Map of Reality
    @gnosis:summary The definitive, unbreakable contract for a Materialized Shadow.
    @gnosis:LIF INFINITY
    @gnosis:auth_code: #!@RECLAMATION_CONTRACT_V25000_FINALIS

    [THE CURE]: This model has been ascended to include 'mode' and 'trace_id',
    annihilating the 'unexpected argument' heresy and closing the Causal Loop.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        extra='allow',  # [ASCENSION 11]: Absorb future matter without fracture
        frozen=False,  # Mutable for internal vitality updates
        populate_by_name=True
    )

    # --- I. CORE IDENTITY & CAUSALITY (THE SOUL) ---
    id: str = Field(..., description="Unique UUID/Hash for this parallel dimension.")
    label: str = Field(..., description="Human-readable tag (e.g., project name).")

    # [THE CURE]: Mode Suture
    mode: ShadowMode = Field(
        default=ShadowMode.RUN,
        description="The operational directive: RUN vs LAB."
    )

    # [THE CURE]: Causal Trace Suture
    trace_id: str = Field(
        default="tr-void",
        description="The Silver Cord linking this thought to the Prime timeline."
    )

    target_ref: str = Field("HEAD", description="The Git reference / Rite ID origin.")
    parent_rite_id: Optional[str] = Field(None, description="The birth-rite anchor.")

    # --- II. SPATIAL GEOMETRY (THE PLACE) ---
    root_path: str = Field(..., description="Absolute physical POSIX path coordinate.")
    substrate: SubstrateType = Field(default=SubstrateType.IRON)

    # --- III. OCULAR AURA (THE APPEARANCE) ---
    aura: str = Field(
        default="static",
        description="The perceived soul of the server: 'static', 'vite', 'fastapi', etc."
    )

    # --- IV. NETWORK PHYSICS (THE FREQUENCY) ---
    port: int = Field(..., description="Primary resonance port.")
    debug_port: Optional[int] = Field(None, description="Inquisitor/Debugger port.")
    host: str = Field("127.0.0.1", description="Interface binding.")
    is_tunnel_active: bool = Field(False, description="True if a public wormhole is open.")
    tunnel_url: Optional[str] = Field(None, description="Public celestial URI.")

    # --- V. KINETIC ANCHORS (THE LIFE) ---
    pid: Optional[int] = Field(None, description="OS Process ID of the breathing reality.")
    status: ShadowStatus = Field(default=ShadowStatus.INITIALIZING)

    # --- VI. TELEMETRY & CHRONICLES (THE SENSES) ---
    stdout_log_path: Optional[str] = Field(None, description="Path to standard output stream.")
    stderr_log_path: Optional[str] = Field(None, description="Path to standard error stream.")

    # --- VII. INTEGRITY & DRIFT (THE TRUTH) ---
    merkle_hash: str = Field(
        default="0xVOID",
        description="SHA-256 fingerprint of the directory structure."
    )

    # --- VIII. METABOLIC DATA (THE ENERGY) ---
    peak_cpu_percent: float = Field(0.0)
    peak_memory_mb: float = Field(0.0)
    injected_variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Gnostic DNA willed during fission."
    )

    # --- IX. TEMPORAL GOVERNANCE (THE CLOCK) ---
    created_at: float = Field(default_factory=time.time)
    last_accessed: float = Field(default_factory=time.time)
    ttl_seconds: int = Field(3600, description="Seconds before entropy reclamation.")

    # --- X. AI METADATA & REASONING (THE CONTEXT) ---
    owner: str = Field("architect", description="The identity of the manifestor.")
    reasoning: str = Field(
        default="Architect willed dimensional fission.",
        description="Socratic explanation of purpose."
    )
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extension vessel.")

    # =============================================================================
    # == THE RITES OF HARMONIZATION (VALIDATORS)                                 ==
    # =============================================================================

    @field_validator('root_path', mode='before')
    @classmethod
    def _canonize_path(cls, v: Any) -> str:
        """[ASCENSION 10]: Absolute POSIX Path Normalization."""
        if not v: return ""
        return str(Path(str(v)).resolve()).replace('\\', '/')

    # =============================================================================
    # == COMPUTED REALITIES (V-Ω)                                                ==
    # =============================================================================

    @computed_field
    @property
    def url(self) -> str:
        """The primary Gnostic coordinate for the Ocular frame."""
        return f"http://{self.host}:{self.port}"

    @computed_field
    @property
    def is_expired(self) -> bool:
        """Determines if the dimension has reached its thermal death."""
        return time.time() > (self.created_at + self.ttl_seconds)

    @computed_field
    @property
    def time_remaining(self) -> float:
        """Nanoseconds until entropy reclamation."""
        return max(0.0, (self.created_at + self.ttl_seconds) - time.time())

    def to_dict(self) -> Dict[str, Any]:
        """Transmutes the vessel into a serializable dictionary."""
        return self.model_dump()


class StateCloningResult(BaseModel):
    """
    =============================================================================
    == THE DATABASE FISSION RESULT (V-Ω-TOTALITY)                              ==
    =============================================================================
    The chronicle of a successful state replication rite.
    """
    success: bool
    db_url: Optional[str] = None
    container_id: Optional[str] = None
    host_port: Optional[int] = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    trace_id: Optional[str] = None