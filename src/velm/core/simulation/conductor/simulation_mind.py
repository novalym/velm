# Path: src/velm/core/simulation/conductor/simulation_mind.py
# -----------------------------------------------------------

import os
import time
import traceback
from pathlib import Path
from contextlib import contextmanager
from typing import Tuple, Optional, Dict, Any, TYPE_CHECKING

from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity

if TYPE_CHECKING:
    from ...runtime import VelmEngine

Logger = Scribe("SimulationMind")


@contextmanager
def _temporal_sanctum(path: Path):
    original_cwd = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_cwd)


class SimulationMind:
    """
    =================================================================================
    == THE CONSCIOUSNESS OF THE PARALLEL REALITY (V-Ω-SILENT-KERNEL-ASCENDED)      ==
    =================================================================================
    """

    def __init__(self, parent_engine: 'VelmEngine', sim_root: Path):
        self.parent_engine = parent_engine
        self.sim_root = sim_root.resolve()

    def execute_rite(self, request: BaseRequest) -> Tuple[Optional[ScaffoldResult], Dict[str, Any]]:
        # [THE LAZY SUMMONS]
        from ...runtime import VelmEngine

        # 1. Forge the Inner Engine
        sim_engine = VelmEngine(
            project_root=self.sim_root,
            log_level="INFO",
            silent=True,
            auto_register=True
        )

        # Autonomic Severance
        if hasattr(sim_engine, 'watchdog') and sim_engine.watchdog:
            sim_engine.watchdog.stop_vigil()
        if hasattr(sim_engine, 'vitality') and sim_engine.vitality:
            sim_engine.vitality.stop_vigil()

        # 3. Enforce Simulation Laws
        sim_request = request.model_copy(update={
            "project_root": self.sim_root,
            "preview": False,
            "dry_run": False,
            "silent": True,
            "no_edicts": True,
            "force": True,
            "non_interactive": True
        })

        # 4. Inject Context
        if not sim_request.variables:
            sim_request.variables = {}

        # [ASCENSION]: Inject Real Root for JIT Teleportation
        real_root = self.parent_engine.project_root.resolve()

        sim_request.variables.update({
            'SCAFFOLD_SIMULATION': True,
            'SCAFFOLD_SIM_ROOT': str(self.sim_root),
            'SCAFFOLD_REAL_ROOT': str(real_root),  # <--- THE FIX
            'SCAFFOLD_TIMESTAMP': str(time.time())
        })

        try:
            with _temporal_sanctum(self.sim_root):
                Logger.debug(f"Dispatching {type(request).__name__} to Inner Engine (CWD: {Path.cwd()})...")
                os.environ.pop("SCAFFOLD_ADRENALINE", None)

                # Inject Env Var for ImportManager to see
                os.environ["SCAFFOLD_REAL_ROOT"] = str(real_root)

                # 5. Dispatch
                result = sim_engine.dispatch(sim_request)

                if result is None:
                    Logger.critical("Inner Engine returned None! Forging emergency failure.")
                    result = ScaffoldResult(
                        success=False,
                        message="Inner Engine Dispatch returned Void (None).",
                        heresies=[Heresy(
                            message="Void Return from Inner Engine",
                            severity=HeresySeverity.CRITICAL,
                            details="The dispatch call returned None, which is mathematically impossible in the ascended kernel."
                        )]
                    )

                final_vars = {}
                if result and result.data and isinstance(result.data, dict):
                    if "variables" in result.data:
                        final_vars = result.data["variables"]
                    elif "gnosis" in result.data:
                        final_vars = result.data["gnosis"]
                    else:
                        final_vars = sim_request.variables
                else:
                    final_vars = sim_request.variables

                return result, final_vars

        except Exception as e:
            Logger.warn(f"Simulated Mind encountered a paradox: {e}")
            failure_result = ScaffoldResult(
                success=False,
                message=f"Simulation Crash: {str(e)}",
                heresies=[
                    Heresy(
                        message="Inner Reality Collapse",
                        severity=HeresySeverity.CRITICAL,
                        details=traceback.format_exc(),
                        suggestion="Check for infinite loops or resource exhaustion in the blueprint."
                    )
                ]
            )
            return failure_result, sim_request.variables
        finally:
            if sim_engine:
                sim_engine.shutdown()
            os.environ.pop("SCAFFOLD_REAL_ROOT", None)