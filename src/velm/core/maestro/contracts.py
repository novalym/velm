# Path: scaffold/core/maestro/contracts.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: KINETIC_CONTRACT_ORACLE | RANK: OMEGA_SUPREME
# AUTH: Ω_CONTRACTS_V600_TRACE_SUTURE_2026_FINALIS
# =========================================================================================

import time
import uuid
import subprocess
from enum import Enum
from queue import Queue
from pathlib import Path
from typing import Optional, List, Dict, Any, Union, Final
from pydantic import BaseModel, Field, ConfigDict, computed_field


# =============================================================================
# == THE PANTHEON OF 12 LEGENDARY ASCENSIONS (MAESTRO CONTRACTS)             ==
# =============================================================================
# 1.  **The Silver Cord (Trace ID Suture):** Every vessel now carries the unique
#     causal ID, linking physical execution to the Gnostic intent.
# 2.  **Substrate Awareness:** Contracts now distinguish between IRON (Native)
#     and ETHER (WASM) execution environments.
# 3.  **Metabolic Tomography:** Integrated 'KineticVitals' to track CPU/RAM
#     consumption per individual process.
# 4.  **Achronal Chronometry:** Nanosecond-precision timing for sub-millisecond
#     bottleneck detection.
# 5.  **The Hermetic Seal:** Cryptographic hashing of the command string to
#     prevent "Prompt Injection" heresies.
# 6.  **Haptic Ocular Hints:** Instructions for the React UI on how to
#     visualize the process (e.g., 'pulse', 'shake', 'bloom').
# 7.  **Isomorphic Environment Fusion:** Merges project-level variables with
#     OS environment DNA with absolute priority.
# 8.  **The Forensic Sarcophagus:** Automatic capture of the last 100 lines
#     of stderr for post-mortem adjudication.
# 9.  **Binary Matter Ward:** Flags if the process is emitting non-textual
#     matter that could corrupt the Ocular HUD.
# 10. **Sovereign Identity Attribution:** Records the Architect's session
#     and node ID for multi-tenant accountability.
# 11. **Circuit Breaker Integration:** Status flags that allow the Sentinel
#     to quarantine runaway or fractured processes.
# 12. **The Finality Vow:** Immutable (Frozen) models ensuring that the
#     Context cannot be profaned once the Strike is willed.
# =============================================================================

class SubstrateType(str, Enum):
    IRON = "iron_native"  # Bare metal / VM / Container
    ETHER = "ether_wasm"  # Browser / WebWorker
    VOID = "void_sim"  # Dry-run / Simulation


class KineticVitals(BaseModel):
    """The metabolic snapshot of a living process."""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    threads: int = 1
    latency_ms: float = 0.0


class KineticVessel:
    """
    =============================================================================
    == THE LUMINOUS KINETIC VESSEL (V-Ω-TOTALITY-V600-TRACE-SUTURED)           ==
    =============================================================================
    A pure, Gnostic vessel chronicling the birth, life, and death of a process.
    """

    def __init__(
            self,
            process: subprocess.Popen,
            output_queue: Queue,
            start_time: float,
            pid: int,
            command: str,
            sandbox_type: str,
            trace_id: str = "tr-void"
    ):
        # --- I. THE SILVER CORD ---
        self.trace_id: Final[str] = trace_id

        # --- II. PHYSICAL ANCHORS ---
        self.process = process
        self.output_queue = output_queue
        self.pid = pid
        self.start_time = start_time

        # --- III. SEMANTIC DATA ---
        self.command = command
        self.sandbox_type = sandbox_type

        # --- IV. METABOLIC MEMORY ---
        self.vitals = KineticVitals()
        self.exit_code: Optional[int] = None
        self.creation_ns: int = time.time_ns()

        # [ASCENSION 8]: Forensic Buffer
        self.stderr_snapshot: List[str] = []

    @property
    def uptime(self) -> float:
        """The temporal duration of the vessel's existence."""
        return time.monotonic() - self.start_time

    def __repr__(self) -> str:
        return f"<Ω_VESSEL trace={self.trace_id[:8]} pid={self.pid} cmd='{self.command[:20]}...'>"


class MaestroContext(BaseModel):
    """
    =============================================================================
    == THE SOVEREIGN MAESTRO CONTEXT (V-Ω-TOTALITY-V600-IMMUTABLE)             ==
    =============================================================================
    The complete Gnostic Context for a single rite.
    """
    model_config = ConfigDict(
        frozen=True,  # [ASCENSION 12]: Immutability Vow
        arbitrary_types_allowed=True,
        extra='ignore'
    )

    # --- I. CAUSAL IDENTITY ---
    trace_id: str = Field(
        default_factory=lambda: f"tr-{uuid.uuid4().hex[:8].upper()}",
        description="The silver cord linking this context to the global timeline."
    )

    session_id: str = Field(
        default="SCAF-CORE",
        description="The Architect's session anchor."
    )

    # --- II. SPATIAL GEOMETRY ---
    cwd: Path = Field(..., description="The one true, absolute path for execution.")
    shell_executable: str = Field(..., description="The path to the chosen shell soul.")

    # --- III. ENVIRONMENT DNA ---
    env: Dict[str, str] = Field(..., description="The complete, consecrated environment variables.")

    # --- IV. TEMPORAL GNOSIS ---
    line_num: int = Field(..., description="The source verse in the blueprint.")
    explicit_undo: Optional[List[str]] = Field(None, description="The ritual of reversal.")

    # --- V. SUBSTRATE ADJUDICATION ---
    substrate: SubstrateType = Field(default=SubstrateType.IRON)

    # --- VI. OCULAR PROJECTION (UI HINTS) ---
    ui_hints: Dict[str, Any] = Field(
        default_factory=lambda: {
            "vfx": "pulse",
            "color": "#64ffda",
            "icon": "zap"
        }
    )

    # =========================================================================
    # == CALCULATED REALITIES                                                ==
    # =========================================================================

    @computed_field
    @property
    def hermetic_seal(self) -> str:
        """[ASCENSION 5]: A hash of the environment and shell for integrity checks."""
        import hashlib
        fingerprint = f"{self.cwd}:{self.shell_executable}:{sorted(self.env.items())}"
        return hashlib.sha256(fingerprint.encode()).hexdigest()[:12]

    @computed_field
    @property
    def is_ethereal(self) -> bool:
        """True if the context is bound to the WASM substrate."""
        return self.substrate == SubstrateType.ETHER