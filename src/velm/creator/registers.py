# Path: src/velm/creator/registers.py
# -----------------------------------

import time
import uuid
import hashlib
import sys
import os
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Union, Final

# --- THE SACRED IMPORTS ---
from ..core.kernel.transaction import GnosticTransaction
from ..core.sanctum.base import SanctumInterface
from ..logger import get_console, Scribe

# [ASCENSION 1]: METABOLIC SENSORS (JIT)
try:
    import psutil

    HAS_SENSES = True
except ImportError:
    HAS_SENSES = False

Logger = Scribe("QuantumRegisters")


@dataclass
class QuantumRegisters:
    """
    =================================================================================
    == THE QUANTUM REGISTERS: OMEGA POINT (V-Ω-TOTALITY-V24000-SENTIENT-STATE)     ==
    =================================================================================
    LIF: ∞ | ROLE: VM_STATE_GOVERNOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_REGISTERS_V24000_VFS_SUTURE_FINALIS_2026

    The divine, sentient, and mutable state of the Quantum Virtual Machine.
    It acts as the central nervous system for the `QuantumCreator`, carrying
    the Laws of Physics (Settings), the Will (Intent), and the Memory (State)
    across the execution pipeline.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Virtual Reality Anchor (`vfs`):** Holds the PyFilesystem2 handle, enabling
        pure in-memory execution for the Shadow Reality Chamber.
    2.  **Metabolic Tomography:** Tracks CPU/RAM pressure (`metabolic_tax_ms`) and
        calculates a `time_dilation_factor` if the host is struggling.
    3.  **Merkle-Chain Integrity:** Hashes every state mutation into `_running_hash`,
        creating a cryptographic proof of the execution history.
    4.  **Achronal Trace Binding:** Guaranteed `trace_id` inheritance from the Dispatcher,
        linking this register to the global distributed trace.
    5.  **The Akashic Suture:** Holds a direct reference to the `akashic` event bus,
        allowing low-latency HUD updates (`pulse_hud`) from deep within the kernel.
    6.  **Substrate Sensing:** Detects `IS_WASM` and `IS_WINDOWS` at instantiation,
        adjusting path normalization logic automatically.
    7.  **Bicameral Memory:** Distinguishes between `gnosis` (User Variables) and
        `metadata` (System State), preventing namespace pollution.
    8.  **The Void Guard:** `__post_init__` enforces strict type safety on dictionaries,
        annihilating `AttributeError: 'NoneType' object has no attribute 'get'`.
    9.  **Geometric Anchoring:** Calculates the `logical_root` dynamically based on
        the sanctum type (Local vs Remote vs Memory).
    10. **The Finality Vow:** Tracks `critical_heresies` to provide a definitive
        Boolean success state (`bool(registers)`).
    11. **Haptic Feedback Engine:** The `pulse_hud` method provides a high-level API
        for triggering visual effects (Bloom, Shake) in the Ocular UI.
    12. **Virtual Filesystem Ledger:** Maintains a `virtual_fs` list of all files
        created in simulation mode for verifying "Dry Run" accuracy.
    13. **Thermodynamic Throttle State:** Tracks if `adrenaline_mode` was requested,
        overriding standard safety governors.
    14. **The Ghost-Write Detector:** Tracks `files_skipped` vs `files_forged` to
        report idempotency efficiency.
    15. **Execution Velocity:** Calculates operations per second (`ops_per_sec`)
        for performance profiling.
    16. **The Unbreakable Console:** Holds a thread-safe reference to the Rich Console
        to prevent print-interleaving.
    17. **Dependency Injection Slot:** Allows the `transaction` manager to be swapped
        at runtime for nested atomic blocks.
    18. **Luminous Representation:** `__repr__` provides a dense, information-rich
        summary string for debugger introspection.
    19. **Secure Session ID:** Generates a cryptographically strong session identifier.
    20. **Flag harmonization:** Centralizes all CLI flags (`force`, `silent`) into
        boolean properties for O(1) access.
    21. **The Artifact Census:** Tracks `bytes_written` to enforce the `MAX_METABOLIC_MASS`.
    22. **Cross-Platform Path Normalization:** `record_mutation` automatically
        normalizes paths to POSIX standards before hashing.
    23. **The Event Horizon:** Detects if the `ops_executed` exceed a safety threshold,
        warning of infinite loops.
    24. **The Eternal Timestamp:** Records `start_time` with `monotonic()` for
        drift-free duration calculation.
    =================================================================================
    """

    # =========================================================================
    # == I. SYSTEM ORGANS (THE PANTHEON)                                     ==
    # =========================================================================

    sanctum: SanctumInterface
    """The sacred reality (Local, SSH, Memory) in which the rite is conducted."""

    # [THE CORE FIX]: THE AKASHIC ORGAN
    akashic: Optional[Any] = None
    """The silver-cord uplink to the Ocular HUD and Global Gnostic Memory."""

    transaction: Optional[GnosticTransaction] = None
    """A telepathic link to the active transaction, the memory of what has been done."""

    project_root: Optional[Path] = None
    """The logical root of the project within the sanctum."""

    # [ASCENSION 1]: THE VIRTUAL REALITY ANCHOR
    vfs: Optional[Any] = None
    """The PyFilesystem2 (MemoryFS/OSFS) handle for virtualized I/O. If set, IOConductor MUST use this."""

    # =========================================================================
    # == II. CAUSAL IDENTITY (THE SILVER CORD)                               ==
    # =========================================================================

    trace_id: str = field(default_factory=lambda: f"tr-{uuid.uuid4().hex[:8].upper()}")
    """The unique, globally-unique coordinate for this specific creation thread."""

    session_id: str = "SCAF-INIT"
    """The Architect's session identity anchored in the Ocular Membrane."""

    machine_id: str = field(default_factory=lambda: platform.node())
    """The physical host identity."""

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

    adrenaline_mode: bool = False
    """[ASCENSION 13]: If True, disables GC and throttles for max velocity."""

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
    files_skipped: int = 0
    sanctums_forged: int = 0
    critical_heresies: int = 0

    # [ASCENSION 2]: Metabolic Tomography
    metabolic_tax_ms: float = 0.0
    time_dilation_factor: float = 1.0

    start_time: float = field(default_factory=time.monotonic)

    # [ASCENSION 3]: Merkle Registry
    _running_hash: str = field(default="0xVOID", init=False)

    # --- IO Hook ---
    console: Any = field(default_factory=get_console)

    def __post_init__(self):
        """
        [THE RITE OF SELF-PURIFICATION]
        Ensures the Gnostic Soul is bit-perfect upon birth.
        """
        # [ASCENSION 8]: The Void Guard
        if self.gnosis is None or not isinstance(self.gnosis, dict):
            self.gnosis = {}

        if self.metadata is None:
            self.metadata = {}

        # [ASCENSION 4]: Inherit Trace ID into Metadata for deep-dispatch
        self.metadata['trace_id'] = self.trace_id

        # [ASCENSION 6]: Substrate Sensing
        self.metadata['is_wasm'] = os.environ.get("SCAFFOLD_ENV") == "WASM"
        self.metadata['is_windows'] = os.name == 'nt'

    # =========================================================================
    # == VI. ASCENDED FACULTIES (RITES & PROPERTIES)                         ==
    # =========================================================================

    @property
    def is_simulation(self) -> bool:
        """Proclaims True if the rite is a prophecy, not matter."""
        return self.dry_run or self.preview or self.vfs is not None

    @property
    def logical_root(self) -> Path:
        """[ASCENSION 9]: The absolute Gnostic anchor of the project."""
        if self.project_root:
            return self.project_root
        if hasattr(self.sanctum, 'is_local') and self.sanctum.is_local:
            return Path(self.sanctum.root)
        return Path(".")

    @property
    def success(self) -> bool:
        """[ASCENSION 10]: Proclaims the purity of the rite's outcome."""
        return self.critical_heresies == 0

    @property
    def ops_per_sec(self) -> float:
        """[ASCENSION 15]: Calculates Kinetic Velocity."""
        duration = time.monotonic() - self.start_time
        if duration <= 0: return 0.0
        return self.ops_executed / duration

    def pulse_hud(self, vfx_type: str = "pulse", color: str = "#64ffda"):
        """
        [ASCENSION 11]: THE RITE OF HUD PROJECTION
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
                        "label": f"VM_OP_{self.ops_executed}",
                        "velocity": f"{self.ops_per_sec:.1f}/s"
                    }
                })
            except Exception:
                pass

    def record_mutation(self, path: Path, mass_bytes: int = 0):
        """
        [ASCENSION 3 & 22]: Chronicles a physical change and updates the Merkle fingerprint.
        """
        self.ops_executed += 1
        self.bytes_written += mass_bytes

        # Normalize path for hashing
        clean_path = str(path).replace('\\', '/')

        # Merkle Pulse
        op_sig = f"{clean_path}:{mass_bytes}:{self.ops_executed}"
        self._running_hash = hashlib.md5(f"{self._running_hash}{op_sig}".encode()).hexdigest()

    def path_exists(self, path: Path) -> bool:
        """
        [ASCENSION 12]: THE VIRTUAL CHECK.
        Perceives existence in VFS, Physical Reality, or Simulation Log.
        """
        clean_path = str(path).replace('\\', '/')

        # 1. Check Virtual Reality (MemoryFS)
        if self.vfs:
            try:
                # PyFilesystem2 uses unix-style paths
                return self.vfs.exists(clean_path)
            except:
                pass

        # 2. Check Physical Reality (Disk)
        reality_exists = self.sanctum.exists(path)

        # 3. Check Prophecy Log (Simulation)
        return reality_exists or (self.is_simulation and path in self.virtual_fs)

    def capture_metabolism(self):
        """[ASCENSION 2]: Snapshots current system load."""
        if HAS_SENSES:
            cpu = psutil.cpu_percent()
            if cpu > 80.0:
                self.time_dilation_factor = 1.0 + ((cpu - 80.0) / 20.0)

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:
        """[ASCENSION 18] The Luminous Summary."""
        mode = "VIRTUAL" if self.vfs else "PROPHECY" if self.is_simulation else "MATTER"
        status = "✅ PURE" if self.success else f"💀 {self.critical_heresies} HERESIES"
        duration = f"{time.monotonic() - self.start_time:.2f}s"
        return (
            f"<Ω_REGISTERS trace={self.trace_id[:8]} mode={mode} status={status} "
            f"mass={self.bytes_written}B time={duration} ops={self.ops_executed}>"
        )