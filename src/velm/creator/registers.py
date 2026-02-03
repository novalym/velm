# Path: scaffold/creator/registers.py
# -----------------------------------

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List

from ..core.kernel.transaction import GnosticTransaction
# --- THE SACRED IMPORT ---
from ..core.sanctum.base import SanctumInterface
from ..logger import get_console, Scribe

Logger = Scribe("QuantumRegisters")


@dataclass
class QuantumRegisters:
    """
    =================================================================================
    == THE QUANTUM REGISTERS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                       ==
    =================================================================================
    The divine, sentient, and mutable state of the Quantum Virtual Machine. This is
    the one true, Gnostic heart of the Creator, its contract now whole and eternal.
    """
    # --- System Registers ---
    sanctum: SanctumInterface
    """The sacred reality (Local, SSH, Memory) in which the rite is conducted."""

    # [THE ASCENSION] The Transaction is now optional.
    # This heals the "Missing Argument" heresy for lightweight rites.
    transaction: Optional[GnosticTransaction] = None
    """A telepathic link to the active transaction, the memory of what has been done."""

    project_root: Optional[Path] = None
    """The logical root of the project within the sanctum."""

    # --- Flags of Will & Prophecy ---
    dry_run: bool = False
    """If True, the rite is a pure prophecy; no physical changes are made."""

    preview: bool = False
    """If True, the rite is a luminous prophecy, generating a visual diff."""

    force: bool = False
    """The Vow of Absolute Will, bypassing all safeguards."""

    verbose: bool = False
    """The Vow of Luminosity, enabling hyper-diagnostic proclamation."""

    silent: bool = False
    """The Vow of Silence, suppressing all but the most critical proclamations."""

    no_edicts: bool = False
    """If True, the Maestro's Will (post-run commands) is stayed."""

    # [THE DIVINE HEALING] The Vow of Non-Interaction is now enshrined.
    non_interactive: bool = False
    """If True, all sacred dialogues with the Architect are bypassed."""

    # --- Memory ---
    gnosis: Dict[str, Any] = field(default_factory=dict)
    """The living Gnostic context (variables) for the Alchemist's Gaze."""

    # --- Virtual Filesystem (Simulation) ---
    virtual_fs: List[Path] = field(default_factory=list)
    """A chronicle of scriptures forged in the ephemeral realm of a simulation."""

    # --- Metrics ---
    ops_executed: int = 0
    bytes_written: int = 0
    files_forged: int = 0
    sanctums_forged: int = 0
    start_time: float = field(default_factory=time.monotonic)

    # --- Error State ---
    critical_heresies: int = 0

    # --- IO Hook ---
    console: Any = field(default_factory=get_console)

    def __post_init__(self):
        """
        [THE RITE OF SELF-PURIFICATION]
        Ensures the Gnosis is always a valid dictionary, healing upstream entropy.
        """
        if self.gnosis is None:
            self.gnosis = {}

        if not isinstance(self.gnosis, dict):
            Logger.warn(
                f"QuantumRegisters received profane gnosis type '{type(self.gnosis).__name__}'. Resetting to empty dict.")
            self.gnosis = {}

    # === ASCENDED FACULTIES (PROPERTIES & RITES) ===

    @property
    def is_simulation(self) -> bool:
        """
        [ASCENSION 3] The Singularity of Simulation.
        Proclaims True if the rite is a prophecy, not a materialization.
        """
        return self.dry_run or self.preview

    @property
    def logical_root(self) -> Path:
        """
        [ASCENSION 4] The Gnostic Anchor.
        Guarantees a pure Path for the project's logical root, annihilating the
        Heresy of the Void Path by falling back to the Sanctum's root.
        """
        if self.project_root:
            return self.project_root
        if self.sanctum.is_local:
            return Path(self.sanctum.root)
        # For non-local, return a conceptual root
        return Path(".")

    def get_duration(self) -> float:
        """Perceives the time elapsed since the rite began."""
        return time.monotonic() - self.start_time

    def record_virtual_path(self, path: Path):
        """Inscribes a prophesied scripture into the virtual manifest."""
        self.virtual_fs.append(path)

    def path_exists(self, path: Path) -> bool:
        """Checks existence in Reality (via Sanctum) OR Simulation."""
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
        """
        [ASCENSION 5] The Luminous Soul.
        Proclaims a hyper-diagnostic summary of the VM's state.
        """
        mode = "SIMULATION" if self.is_simulation else "MATERIAL"
        status = "✅ PURE" if self.success else f"💀 HERESY ({self.critical_heresies})"
        return (
            f"<QuantumRegisters id={id(self)} mode={mode} status={status} "
            f"sanctum={self.sanctum.__class__.__name__} files={self.files_forged}>"
        )