# Path: artisans/translocate_core/conductor/engine.py
# --------------------------------------------------

from __future__ import annotations
import time
import os
import sys
from pathlib import Path
from typing import Optional, Dict, List, TYPE_CHECKING, Tuple, Any, Final

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe
from ..contracts import TranslocationMap
from ..will_parser import GnosticWillParser
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# --- THE DIVINE SUMMONS OF THE STRUCTURE SENTINEL ---
# The missing link. Ensures that no file is ever moved into a structural void.
from ....core.structure_sentinel import StructureSentinel

# --- THE DIVINE INHERITANCE OF FACULTIES (MIXINS) ---
from .perception import PerceptionMixin
from .proclamation import ProclamationMixin
from .snapshot import SnapshotMixin
from .execution import ExecutionMixin

if TYPE_CHECKING:
    from ....core.cortex.engine import GnosticCortex
    from ....core.kernel.transaction import GnosticTransaction
    from ....creator.io_controller.facade import IOConductor

Logger = Scribe("TranslocationConductor")


class TranslocationConductor(PerceptionMixin, ProclamationMixin, SnapshotMixin, ExecutionMixin):
    """
    =================================================================================
    == THE OMEGA EVOLUTIONARY CONDUCTOR (V-Ω-TOTALITY-V1100-FINALIS)               ==
    =================================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_EVOLUTION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_TRANSLOCATE_V1100_SUTURE_2026_FINALIS

    The supreme orchestrator of architectural evolution. It unifies the faculties
    of Perception, Proclamation, Snapshotting, and Execution into a single,
    transaction-aware God-Engine. Sutured to the IOConductor for atomic materialization.
    =================================================================================
    """

    def __init__(
            self,
            project_root: Path,
            non_interactive: bool = False,
            preview: bool = False,
            backup_path: Optional[str] = None,
            cortex: Optional["GnosticCortex"] = None,
            transaction: Optional["GnosticTransaction"] = None,
            io_conductor: Optional["IOConductor"] = None  # [ASCENSION 1]: The Suture
    ):
        """
        =================================================================================
        == THE RITE OF GNOSTIC INCEPTION (V-Ω-TOTALITY-SUTURED)                        ==
        =================================================================================
        The Conductor is born. It now possesses the sovereign ability to manipulate
        reality through the IOConductor, while the Cortex provides the eyes to see.
        """
        self.project_root = project_root.resolve()
        self.non_interactive = non_interactive
        self.preview = preview
        self.backup_root_path = Path(backup_path).resolve() if backup_path else None

        # --- THE KERNEL SUTURES ---
        self.transaction = transaction

        # =========================================================================
        # == [ASCENSION 1]: THE SOVEREIGN HAND SUTURE (THE CURE)                 ==
        # =========================================================================
        # We prioritize the provided IOConductor (usually from the Artisan).
        # If unmanifest, we forge a local one to ensure kinetic resonance.
        if io_conductor:
            self.io = io_conductor
        else:
            from ....creator.io_controller.facade import IOConductor
            from ....creator.registers import QuantumRegisters

            # [ASCENSION 11]: Registers Suture
            # Forge ephemeral registers to anchor the local hand.
            regs = QuantumRegisters(
                sanctum=None,  # Defaults to LocalIron
                project_root=self.project_root,
                transaction=self.transaction,
                dry_run=self.preview,
                trace_id=getattr(transaction, 'trace_id', f"tr-local-{os.getpid()}")
            )
            self.io = IOConductor(regs)

        # --- THE MEMORY LATTICE ---
        self.translocation_map: Optional[TranslocationMap] = None
        self.all_healing_plans: Dict[Path, List[Dict]] = {}
        self.logger = Logger
        self._start_ts = time.perf_counter_ns()

        # [FACULTY 1: THE STRUCTURE SENTINEL]
        # Consecrates new directories (creating __init__.py/mod.rs) transactionally.
        self.structure_sentinel = StructureSentinel(self.project_root, self.transaction)

        # [ASCENSION 6]: THE CORTEX SUTURE (THE MIND)
        if cortex:
            self.cortex = cortex
        else:
            # [THE FALLBACK RITE]: Summon a local cortex if the Engine is cold.
            from ....core.cortex.engine import GnosticCortex
            self.cortex = GnosticCortex(self.project_root)

        # [ASCENSION 13]: INTENT ALCHEMY
        # The WillParser translates Architect pleas (globs/scripts) into the Map.
        self.will_parser = GnosticWillParser(self.project_root)

        if self.logger.is_verbose:
            self.logger.debug(
                f"Evolutionary Conductor manifest. "
                f"Anchor: [cyan]{self.project_root.name}[/] | "
                f"Shadow_Volume: {'ACTIVE' if self.io.router.transaction else 'NONE'}"
            )

    def conduct(self) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EVOLUTION (V-Ω-TOTALITY-V1100-HEALED)             ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_DISPATCHER | RANK: OMEGA_SOVEREIGN

        [THE CURE]: This method is now the absolute orchestrator. It delegages
        to the ExecutionMixin's conduct() and righteously returns the 4-fold
        ScaffoldResult to the calling Artisan.
        """
        self._start_ts = time.perf_counter_ns()

        # --- MOVEMENT 0: THE VOID WARD ---
        if not self.translocation_map or not self.translocation_map.moves:
            self.logger.verbose("Kinetic Void: No translocations perceived. Rite stayed.")
            return ScaffoldResult.forge_success("No translocation required.")

        # --- THE SYMPHONY MOVEMENTS (I-V) ---
        # Movement I: Prophecy (Cortex)
        # Movement II: Archival (Snapshot)
        # Movement III: Translocation (IO Strike)
        # Movement IV: Healing (Import Mend)
        # Movement V: Consecration (Structure)

        # [STRIKE]: Delegate to the Mixin logic which is now ascended.
        # This prevents the "Redundant Move" paradox.
        result = super().conduct()

        # --- MOVEMENT VI: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - self._start_ts) / 1_000_000

        if result.success:
            self.logger.success(f"Evolutionary Rite concluded purely in {duration_ms:.2f}ms.")
        else:
            self.logger.error(f"Evolutionary Symphony fractured after {duration_ms:.2f}ms.")

        return result

    @property
    def trace_id(self) -> str:
        """[ASCENSION 4]: Distributed Trace ID."""
        return getattr(self.transaction, 'trace_id', 'tr-unbound')

    def __repr__(self) -> str:
        status = "PREVIEW" if self.preview else "LIVE"
        return f"<Ω_EVOLUTION_CONDUCTOR state={status} root={self.project_root.name} trace={self.trace_id[:8]}>"
