# Path: scaffold/core/ignition/diviner/contracts.py
# --------------------------------------------------
# LIF: 10,000,000,000,000 // AUTH_CODE: Ω_SINGULARITY_CONTRACTS_V12_FINAL
# SYSTEM: IDEABOX QUANTUM // MODULE: IGNITION.DIVINER
# -------------------------------------------------------------------------------------

import time
import uuid
import hashlib
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any, Union, Set
from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator


# =================================================================================
# == SECTION I: THE GNOSTIC ENUMS (THE NATURE OF REALITY)                        ==
# =================================================================================

class IgnitionAura(str, Enum):
    """
    [ASCENSION 1]: The Expanded Aura Spectrum.
    Defines the perceived framework 'soul' of the project.
    """
    # --- Frontend Realities ---
    VITE = "vite"
    NEXT = "next"
    NUXT = "nuxt"
    ASTRO = "astro"
    REMIX = "remix"
    SVELTE = "svelte"
    STATIC = "static"

    # --- Python Realities ---
    FASTAPI = "fastapi"
    FLASK = "flask"
    DJANGO = "django"
    STREAMLIT = "streamlit"
    GRADIO = "gradio"
    PYTHON_SCRIPT = "python_script"

    # --- Intelligence Realities (AI) ---
    LANGCHAIN = "langchain"
    LLM_AGENT = "llm_agent"
    JUPYTER = "jupyter"

    # --- Systems Realities ---
    CARGO = "cargo"
    GO_MOD = "go_mod"
    CMAKE = "cmake"
    MAKEFILE = "makefile"

    # --- Fallbacks ---
    GENERIC = "generic"
    SHELL = "shell"


class VitalityState(str, Enum):
    """
    [ASCENSION 8]: The Lifecycle Oracle.
    Defines the perceived state of a manifested process.
    """
    DORMANT = "dormant"  # Matter exists but is not breathing
    IGNITING = "igniting"  # Process starting, port not yet bound
    ONLINE = "online"  # Stable resonance achieved (Port Bound)
    FRACTURED = "fractured"  # Process crashed or returned error code
    ZOMBIE = "zombie"  # PID manifest but non-responsive to heartbeat
    STALE = "stale"  # Running code differs from physical disk matter


class Protocol(str, Enum):
    """[ASCENSION 5]: The sacred tongues of network communication."""
    HTTP = "http"
    HTTPS = "https"
    WSS = "wss"
    GRPC = "grpc"
    TCP = "tcp"


# =================================================================================
# == SECTION II: COMPONENTS OF MATTER (SUB-VESSELS)                              ==
# =================================================================================

class SemanticVersion(BaseModel):
    """[ASCENSION 7]: Structured temporal identification for toolchains."""
    major: int = 0
    minor: int = 0
    patch: int = 0
    raw: str = "0.0.0"

    @classmethod
    def from_str(cls, v_str: str) -> "SemanticVersion":
        import re
        match = re.search(r'(\d+)\.(\d+)\.(\d+)', v_str)
        if match:
            return cls(major=int(match.group(1)), minor=int(match.group(2)),
                       patch=int(match.group(3)), raw=v_str)
        return cls(raw=v_str)


class HardwareConstraint(BaseModel):
    """
    [ASCENSION 2]: The Physical Cage.
    Defines the limits of the process's consumption.
    """
    model_config = ConfigDict(frozen=True)

    cpu_limit_percent: float = Field(default=50.0, ge=1.0, le=100.0)
    memory_limit_mb: int = Field(default=1024, ge=128)
    priority: int = Field(default=10, ge=0, le=20)  # OS Niceness


class BiologicalSupport(BaseModel):
    """
    [ASCENSION 4]: The dependency tomography vessel.
    Distinguishes between "Manifest Intent" and "Physical Matter".
    """
    model_config = ConfigDict(frozen=True)

    manifest_type: str = Field(..., description="e.g. 'package.json' or 'poetry.lock'")
    is_installed: bool = False
    runtime_version: Optional[SemanticVersion] = None
    missing_elements: List[str] = Field(default_factory=list)
    suggested_install_cmd: Optional[str] = None
    lockfile_hash: Optional[str] = None


class NetworkPhysics(BaseModel):
    """[ASCENSION 5]: Frequency and Protocol Resonance."""
    model_config = ConfigDict(frozen=True)

    port: int = Field(..., ge=0, le=65535)
    host: str = "127.0.0.1"
    protocol: Protocol = Protocol.HTTP
    is_public: bool = False


# =================================================================================
# == SECTION III: THE DIVINE RESULT (THE PROPHECY)                               ==
# =================================================================================

class HeuristicResonance(BaseModel):
    """[ASCENSION 1]: A single potential reality discovered by the Bayesian brain."""
    aura: IgnitionAura
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: List[str] = Field(default_factory=list)


class ExecutionPlan(BaseModel):
    """
    =================================================================================
    == THE SOVEREIGN EXECUTION PLAN (V-Ω-TOTALITY)                                 ==
    =================================================================================
    The definitive contract for bringing code to life.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # --- 1. CORE IDENTITY ---
    trace_id: str = Field(default_factory=lambda: f"tr-{uuid.uuid4().hex[:8]}")
    command: List[str] = Field(..., description="Tokenized shell command sequence.")
    cwd: Path = Field(..., description="The physical anchor root for the process.")
    aura: IgnitionAura = Field(default=IgnitionAura.GENERIC)

    # --- 2. ENVIRONMENT & PHYSICS ---
    env: Dict[str, str] = Field(default_factory=dict, description="Redacted environment DNA.")
    network: NetworkPhysics
    constraints: HardwareConstraint = Field(default_factory=HardwareConstraint)

    # --- 3. BIOLOGY & TRUST ---
    support: Optional[BiologicalSupport] = None
    confidence: float = Field(default=1.0)

    # --- 4. FORENSIC REASONING (ASCENSION 12) ---
    # The step-by-step chronicle of the Diviner's logic.
    reasoning_trace: List[str] = Field(default_factory=list)

    # --- 5. TEMPORAL ANCHORS ---
    divination_timestamp: float = Field(default_factory=time.time)

    @computed_field
    @property
    def merkle_seal(self) -> str:
        """
        [ASCENSION 3]: The Deterministic Fingerprint.
        Hashes the entire intent to detect environmental drift.
        """
        fingerprint = f"{self.command}{self.cwd}{self.aura}{sorted(self.env.items())}"
        return hashlib.sha256(fingerprint.encode()).hexdigest()[:16]

    @computed_field
    @property
    def ui_hint_color(self) -> str:
        """[ASCENSION 11]: Chromatic resonance for the React layer."""
        colors = {
            IgnitionAura.VITE: "#06b6d4",  # Cyan
            IgnitionAura.FASTAPI: "#10b981",  # Emerald
            IgnitionAura.CARGO: "#f97316",  # Orange
            IgnitionAura.NEXT: "#ffffff",  # White
            IgnitionAura.STATIC: "#f472b6",  # Pink
        }
        return colors.get(self.aura, "#94a3b8")

    @field_validator('cwd', mode='before')
    @classmethod
    def _normalize_cwd(cls, v: Any) -> Path:
        """[ASCENSION 10]: Isomorphic Path Purification."""
        return Path(v).resolve()


class DivinationResult(BaseModel):
    """
    =================================================================================
    == THE BAYESIAN DIVINATION DOSSIER                                             ==
    =================================================================================
    The final output of the Diviner Engine.
    Carries the winning prophecy and the probability cloud.
    """
    # The winner of the Bayesian competition
    winning_plan: ExecutionPlan

    # [ASCENSION 1]: The Probability Distribution
    alternative_realities: List[HeuristicResonance] = Field(default_factory=list)

    # [ASCENSION 12]: Socratic Feedback Loop
    requires_architect_intervention: bool = False
    inquiry_hooks: List[str] = Field(default_factory=list)

    # Telemetry
    total_divination_ms: float = 0.0
    logic_heart_path: Path

    @computed_field
    @property
    def is_highly_certain(self) -> bool:
        return self.winning_plan.confidence > 0.85


# =================================================================================
# == SECTION IV: FUSION CORE (POLYGLOT BINDINGS)                                 ==
# =================================================================================

class FusionBinding(BaseModel):
    """[ASCENSION 11]: Definitions for cross-runtime logic fusion (e.g., Rust in Py)."""
    source_lang: str  # rust, go, c
    binary_path: Path
    bridge_type: str  # pyo3, maturin, cffi, node-gyp
    exported_symbols: List[str] = Field(default_factory=list)
    compilation_flags: Dict[str, Any] = Field(default_factory=dict)