# Path: scaffold/creator/registers.py
# =========================================================================================
# == THE QUANTUM REGISTERS: OMEGA POINT (V-Ω-TOTALITY-V12.0-FINALIS)                    ==
# =========================================================================================
# LIF: INFINITY | ROLE: VM_STATE_GOVERNOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_REGISTERS_V12_AKASHIC_SUTURE_2026_FINALIS
# =========================================================================================

import time
import uuid
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

# --- THE SACRED IMPORTS ---
from ..core.kernel.transaction import GnosticTransaction
from ..core.sanctum.base import SanctumInterface
from ..logger import get_console, Scribe

Logger = Scribe("QuantumRegisters")


@dataclass
class QuantumRegisters:
    """
    The divine, sentient, and mutable state of the Quantum Virtual Machine.
    This is the one true, Gnostic heart of the Creator, its contract now
    sutured to the Akashic Record for universal transparency.
    """

    # =========================================================================
    # == I. SYSTEM ORGANS (THE PANTHEON)                                     ==
    # =========================================================================

    sanctum: SanctumInterface
    """The sacred reality (Local, SSH, Memory) in which the rite is conducted."""

    # [THE CORE FIX]: THE AKASHIC ORGAN
    # This attribute annihilates the 'QuantumRegisters object has no attribute akashic' heresy.
    akashic: Optional[Any] = None
    """The silver-cord uplink to the Ocular HUD and Global Gnostic Memory."""

    transaction: Optional[GnosticTransaction] = None
    """A telepathic link to the active transaction, the memory of what has been done."""

    project_root: Optional[Path] = None
    """The logical root of the project within the sanctum."""

    # =========================================================================
    # == II. CAUSAL IDENTITY (THE SILVER CORD)                               ==
    # =========================================================================

    trace_id: str = field(default_factory=lambda: f"tr-{uuid.uuid4().hex[:8].upper()}")
    """The unique, globally-unique coordinate for this specific creation thread."""

    session_id: str = "SCAF-INIT"
    """The Architect's session identity anchored in the Ocular Membrane."""

    # =========================================================================
    # == III. FLAGS OF WILL & PROPHECY                                       ==
    # =========================================================================

    dry_run: bool = False
    """If True, the rite is a pure prophecy; no physical changes are made."""

    preview: bool = False
    """If True, the rite generates a luminous visual hologram for the UI."""

    force: bool = False
    """The Vow of Absolute Will, bypassing all physical safeguards."""

    verbose: bool = False
    """The Vow of Luminosity, enabling hyper-diagnostic proclamation."""

    silent: bool = False
    """The Vow of Silence, suppressing all but the most critical signals."""

    no_edicts: bool = False
    """If True, the Maestro's Will (post-run commands) is stayed."""

    non_interactive: bool = False
    """If True, all sacred dialogues with the Architect are bypassed."""

    # =========================================================================
    # == IV. COGNITIVE MEMORY                                                ==
    # =========================================================================

    gnosis: Dict[str, Any] = field(default_factory=dict)
    """The living Gnostic context (variables) for the Alchemist's Gaze."""

    metadata: Dict[str, Any] = field(default_factory=dict)
    """Catch-all vessel for ephemeral Gnosis (timings, persona DNA)."""

    virtual_fs: List[Path] = field(default_factory=list)
    """A chronicle of scriptures forged in the ephemeral realm of simulation."""

    # =========================================================================
    # == V. METABOLIC METRICS                                                ==
    # =========================================================================

    ops_executed: int = 0
    bytes_written: int = 0
    files_forged: int = 0
    sanctums_forged: int = 0
    critical_heresies: int = 0

    start_time: float = field(default_factory=time.monotonic)

    # [ASCENSION 5]: Merkle Registry
    _running_hash: str = field(default="0xVOID", init=False)

    # --- IO Hook ---
    console: Any = field(default_factory=get_console)

    def __post_init__(self):
        """
        [THE RITE OF SELF-PURIFICATION]
        Ensures the Gnostic Soul is bit-perfect upon birth.
        """
        if self.gnosis is None or not isinstance(self.gnosis, dict):
            self.gnosis = {}

        if self.metadata is None:
            self.metadata = {}

        # [ASCENSION 11]: Inherit Trace ID into Metadata for deep-dispatch
        self.metadata['trace_id'] = self.trace_id

    # =========================================================================
    # == VI. ASCENDED FACULTIES (RITES & PROPERTIES)                         ==
    # =========================================================================

    @property
    def is_simulation(self) -> bool:
        """Proclaims True if the rite is a prophecy, not matter."""
        return self.dry_run or self.preview

    @property
    def logical_root(self) -> Path:
        """The absolute Gnostic anchor of the project."""
        if self.project_root:
            return self.project_root
        if hasattr(self.sanctum, 'is_local') and self.sanctum.is_local:
            return Path(self.sanctum.root)
        return Path(".")

    def pulse_hud(self, vfx_type: str = "pulse", color: str = "#64ffda"):
        """
        [ASCENSION 4]: THE RITE OF HUD PROJECTION
        Surgically multicasts a visual signal to the Ocular HUD.
        """
        if self.akashic:
            try:
                self.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": vfx_type,
                        "color": color,
                        "trace": self.trace_id,
                        "label": f"VM_OP_{self.ops_executed}"
                    }
                })
            except Exception:
                pass

    def record_mutation(self, path: Path, mass_bytes: int = 0):
        """Chronicles a physical change and updates the Merkle fingerprint."""
        self.ops_executed += 1
        self.bytes_written += mass_bytes

        # [ASCENSION 5]: Merkle Pulse
        op_sig = f"{path}:{mass_bytes}:{self.ops_executed}"
        self._running_hash = hashlib.md5(f"{self._running_hash}{op_sig}".encode()).hexdigest()

    def path_exists(self, path: Path) -> bool:
        """Checks existence in Reality OR the Virtual Mirror."""
        reality_exists = self.sanctum.exists(path)
        return reality_exists or (self.is_simulation and path in self.virtual_fs)

    @property
    def success(self) -> bool:
        """Proclaims the purity of the rite's outcome."""
        return self.critical_heresies == 0

    @property
    def registers(self) -> 'QuantumRegisters':
        """A luminous alias for self-reference."""
        return self

    def __repr__(self) -> str:
        """[ASCENSION 10] The Luminous Summary."""
        mode = "PROPHECY" if self.is_simulation else "MATTER"
        status = "✅ PURE" if self.success else f"💀 {self.critical_heresies} HERESIES"
        duration = f"{time.monotonic() - self.start_time:.2f}s"
        return (
            f"<QuantumRegisters trace={self.trace_id} mode={mode} status={status} "
            f"mass={self.bytes_written}B time={duration}>"
        )

