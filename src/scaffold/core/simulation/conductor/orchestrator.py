# scaffold/core/simulation/conductor/orchestrator.py

import time
import uuid
from typing import TYPE_CHECKING

from .reality_forge import RealityForge
from .simulation_mind import SimulationMind
from .gnostic_comparator import GnosticComparator
from ..prophecy import Prophecy
from ....contracts.heresy_contracts import Heresy
from ....interfaces.requests import (
    BaseRequest, CreateRequest, GenesisRequest, InitRequest, RunRequest
)
from ....logger import Scribe

if TYPE_CHECKING:
    from ...runtime import ScaffoldEngine

Logger = Scribe("SimulationOrchestrator")


class SimulationConductor:
    """
    =================================================================================
    == THE QUANTUM ORCHESTRATOR (V-Ω-MODULAR-GOD-ENGINE)                           ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Master of Prophecy. It coordinates the creation of parallel realities, the
    execution of simulated will, and the extraction of truth from the delta.

    It delegates to:
    1.  **RealityForge:** To build the sandbox (Mirror or Void).
    2.  **SimulationMind:** To execute the rite within the sandbox.
    3.  **GnosticComparator:** To perceive the difference between Reality and Simulation.
    """

    def __init__(self, engine: 'ScaffoldEngine'):
        self.engine = engine
        self.real_root = self.engine.project_root.resolve()
        self.sim_id = str(uuid.uuid4())[:8]
        self.sim_root = self.real_root / ".scaffold" / "simulation" / self.sim_id

        # The Sub-Artisans
        self.forge = RealityForge(self.real_root, self.sim_root)
        self.mind = SimulationMind(self.engine, self.sim_root)
        self.comparator = GnosticComparator(self.real_root, self.sim_root)

    def conduct(self, request: BaseRequest) -> Prophecy:
        Logger.info(f"Initiating Quantum Simulation (ID: {self.sim_id}) for {type(request).__name__}...")

        setup_start = time.time()
        needs_mirror = self._does_rite_need_mirror(request)

        # --- MOVEMENT I: THE FORGING OF REALITY ---
        try:
            if needs_mirror:
                self.forge.materialize_mirror()
            else:
                self.forge.materialize_void()
        except Exception as e:
            Logger.error(f"Reality Forge shattered: {e}", exc_info=True)
            self.forge.annihilate()
            return Prophecy(
                rite_name=type(request).__name__,
                is_pure=False,
                summary=f"Simulation Aborted: {e}",
                heresies=[
                    Heresy(message="Reality Forge Paradox", line_num=0, line_content="System", severity="CRITICAL",
                           details=str(e))]
            )
        setup_duration = time.time() - setup_start

        # --- MOVEMENT II: THE SIMULATION OF WILL ---
        run_start = time.time()
        try:
            result, final_vars = self.mind.execute_rite(request)
        except Exception as e:
            Logger.warn(f"Simulated Mind encountered a paradox: {e}")
            result = None
            final_vars = {}
        run_duration = time.time() - run_start

        # --- MOVEMENT III: THE GNOSTIC DIFFERENTIAL ---
        diff_start = time.time()
        try:
            diffs = self.comparator.perceive_divergence()
        except Exception as e:
            Logger.error(f"Differential Gaze failed: {e}")
            diffs = []
        diff_duration = time.time() - diff_start

        # --- MOVEMENT IV: THE CLEANUP ---
        self.forge.annihilate()

        is_success = result.success if result else False
        heresies = result.heresies if result else []

        summary = (
            f"Prophecy Generated.\n"
            f"• Forge: {setup_duration:.2f}s {'(Mirrored)' if needs_mirror else '(Void)'}\n"
            f"• Rite:  {run_duration:.2f}s\n"
            f"• Gaze:  {diff_duration:.2f}s"
        )

        return Prophecy(
            rite_name=type(request).__name__,
            is_pure=is_success,
            summary=summary,
            diffs=diffs,
            heresies=heresies,
            final_variables=final_vars
        )

    def _does_rite_need_mirror(self, request: BaseRequest) -> bool:
        """[THE GAZE OF INTENT] Adjudicates if the simulation requires history."""
        # Generative rites start from a clean slate.
        if isinstance(request, (CreateRequest, GenesisRequest, InitRequest)):
            return False
        # RunRequest logic: If running a .scaffold file and no lockfile exists, it's a genesis rite.
        if isinstance(request, RunRequest):
            target = getattr(request, 'target', '')
            if str(target).endswith('.scaffold') and not (self.real_root / "scaffold.lock").exists():
                return False
        # All other rites (transmute, patch, heal, etc.) are mutations and need the mirror.
        return True