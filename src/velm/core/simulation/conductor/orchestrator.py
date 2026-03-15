# Path: src/velm/core/simulation/conductor/orchestrator.py
# --------------------------------------------------------

import time
import uuid
import tempfile
import shutil
import os
import traceback
import sys
from typing import TYPE_CHECKING
from pathlib import Path

from .reality_forge import RealityForge
from .simulation_mind import SimulationMind
from .gnostic_comparator import GnosticComparator
from ..prophecy import Prophecy
from ....contracts.heresy_contracts import Heresy, HeresySeverity
from ....interfaces.requests import (
    BaseRequest, CreateRequest, GenesisRequest, InitRequest, RunRequest
)
from ....logger import Scribe

if TYPE_CHECKING:
    from ...runtime import VelmEngine

Logger = Scribe("SimulationOrchestrator")


class SimulationConductor:
    """
    =================================================================================
    == THE QUANTUM ORCHESTRATOR (V-Ω-MODULAR-GOD-ENGINE-ASCENDED)                  ==
    =================================================================================
    LIF: ∞ | ROLE: PROPHETIC_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    """

    def __init__(self, engine: 'VelmEngine'):
        self.engine = engine
        self.real_root = self.engine.project_root.resolve()
        self.sim_id = str(uuid.uuid4())[:8]

        # [ASCENSION 1]: ABSOLUTE ETHEREAL ISOLATION
        self._temp_sanctum = tempfile.TemporaryDirectory(prefix=f"scaf_sim_{self.sim_id}_")
        self.sim_root = Path(self._temp_sanctum.name).resolve()

        self.forge = RealityForge(self.real_root, self.sim_root)
        self.mind = SimulationMind(self.engine, self.sim_root)
        self.comparator = GnosticComparator(self.real_root, self.sim_root)

    def conduct(self, request: BaseRequest) -> Prophecy:
        Logger.info(f"Initiating Quantum Simulation (ID: {self.sim_id}) for {type(request).__name__}...")

        # =========================================================================
        # == [THE CURE]: SPATIOTEMPORAL ANCHOR INJECTION                         ==
        # =========================================================================
        # We must proclaim the REAL world coordinate to the Ether so the
        # JIT Teleporter can find Ancestral Shards.
        os.environ["SCAFFOLD_REAL_ROOT"] = str(self.real_root)
        os.environ["SCAFFOLD_SIM_ROOT"] = str(self.sim_root)
        os.environ["SCAFFOLD_SIMULATION"] = "True"

        setup_start = time.time()
        needs_mirror = self._does_rite_need_mirror(request)

        blueprint_target = None
        if hasattr(request, 'blueprint_path') and request.blueprint_path:
            blueprint_target = Path(str(request.blueprint_path))
        elif hasattr(request, 'target') and request.target:
            blueprint_target = Path(str(request.target))

        try:
            # --- MOVEMENT I: THE FORGING OF REALITY ---
            try:
                if needs_mirror:
                    self.forge.materialize_mirror(focus_target=blueprint_target)
                else:
                    self.forge.materialize_void()
            except Exception as e:
                Logger.error(f"Reality Forge shattered: {e}", exc_info=True)
                return self._forge_aborted_prophecy(request, e, "Forge Paradox")

            setup_duration = time.time() - setup_start

            # --- MOVEMENT II: THE SIMULATION OF WILL ---
            run_start = time.time()
            crash_error = None
            result = None
            final_vars = {}

            try:
                result, final_vars = self.mind.execute_rite(request)
            except Exception as e:
                crash_error = e
                sys.stderr.write(f"[SIMULATION:CRASH] {e}\n")

            run_duration = time.time() - run_start

            # --- MOVEMENT III: THE GNOSTIC DIFFERENTIAL ---
            diff_start = time.time()
            try:
                diffs = self.comparator.perceive_divergence()
            except Exception as e:
                Logger.error(f"Differential Gaze failed: {e}")
                diffs = []
            diff_duration = time.time() - diff_start

            # --- MOVEMENT IV: PROPHETIC ASSEMBLY ---
            is_success = False
            heresies = []

            if result is not None:
                is_success = result.success
                heresies = result.heresies
                if not is_success and not heresies and result.message:
                    heresies.append(Heresy(
                        message="Inner Engine Failure",
                        severity=HeresySeverity.CRITICAL,
                        details=result.message,
                        line_num=0
                    ))
            elif crash_error:
                heresies.append(Heresy(
                    message=f"Simulation Crash: {str(crash_error)}",
                    severity=HeresySeverity.CRITICAL,
                    details=traceback.format_exc(),
                    line_num=0
                ))
            else:
                heresies.append(Heresy(
                    message="Simulation Silent Failure",
                    severity=HeresySeverity.CRITICAL,
                    details="The Inner Engine returned void (None) without raising an exception.",
                    suggestion=f"Verify that '{blueprint_target}' exists and is valid."
                ))

            sim_cmds = []
            if result and result.data and isinstance(result.data, dict):
                sim_cmds = result.data.get('simulated_commands', [])

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
                simulated_commands=sim_cmds,
                heresies=heresies,
                final_variables=final_vars
            )

        finally:
            self._purge_ethereal_sanctum()
            # Restore Substrate Physics
            os.environ.pop("SCAFFOLD_REAL_ROOT", None)
            os.environ.pop("SCAFFOLD_SIM_ROOT", None)
            os.environ.pop("SCAFFOLD_SIMULATION", None)

    def _forge_aborted_prophecy(self, request, error, title):
        return Prophecy(
            rite_name=type(request).__name__,
            is_pure=False,
            summary=f"Simulation Aborted: {title}",
            heresies=[
                Heresy(message=title, line_num=0, line_content="System", severity=HeresySeverity.CRITICAL,
                       details=str(error))]
        )

    def _purge_ethereal_sanctum(self):
        try:
            self._temp_sanctum.cleanup()
        except Exception:
            if os.name == 'nt':
                try:
                    shutil.rmtree(str(self.sim_root), ignore_errors=True)
                except:
                    pass

    def _does_rite_need_mirror(self, request: BaseRequest) -> bool:
        req_type = type(request).__name__
        if req_type == 'InitRequest':
            return False
        return True