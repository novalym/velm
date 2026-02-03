# scaffold/core/simulation/conductor/simulation_mind.py

import os
import time
from pathlib import Path
from contextlib import contextmanager
from typing import Tuple, Optional, Dict, Any, TYPE_CHECKING

from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import BaseRequest
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity

if TYPE_CHECKING:
    from ...runtime import ScaffoldEngine

Logger = Scribe("SimulationMind")


@contextmanager
def _temporal_sanctum(path: Path):
    """
    [THE RITE OF TRANSLOCATION]
    Temporarily shifts the process's center of gravity (CWD) to the simulation root.
    This guarantees that any artisan relying on `Path.cwd()` acts within the simulation.
    """
    original_cwd = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_cwd)


class SimulationMind:
    """
    The Consciousness of the Parallel Reality.
    """

    def __init__(self, parent_engine: 'ScaffoldEngine', sim_root: Path):
        self.parent_engine = parent_engine
        self.sim_root = sim_root.resolve()

    def execute_rite(self, request: BaseRequest) -> Tuple[Optional[ScaffoldResult], Dict[str, Any]]:
        # [THE LAZY SUMMONS]
        from ...runtime import ScaffoldEngine

        # 1. Forge the Inner Engine
        sim_engine = ScaffoldEngine(
            project_root=self.sim_root,
            log_level="INFO",
            silent=True,
            auto_register=False
        )

        # 2. The Rite of Knowledge Transference
        for req_type, artisan_instance in self.parent_engine.registry._map.items():
            sim_engine.register_artisan(req_type, artisan_instance.__class__)

        # 3. Enforce Simulation Laws
        sim_request = request.model_copy(update={
            "project_root": self.sim_root,
            "preview": False,  # Disable preview so it actually writes to sandbox
            "dry_run": False,  # Disable dry_run so it actually writes to sandbox
            "silent": True,  # Silence the output
            "no_edicts": True,  # Do not run post-run scripts
            "force": True,  # Bypass confirmations
            "non_interactive": True  # Ensure no prompts
        })

        # 4. Inject Context
        if not sim_request.variables:
            sim_request.variables = {}

        sim_request.variables.update({
            'SCAFFOLD_SIMULATION': True,
            'SCAFFOLD_SIM_ROOT': str(self.sim_root),
            'SCAFFOLD_TIMESTAMP': str(time.time())
        })

        # [THE GRAVITATIONAL ANCHOR]
        # We shift reality before dispatching.
        try:
            with _temporal_sanctum(self.sim_root):
                Logger.debug(f"Dispatching {type(request).__name__} to Inner Engine (CWD: {Path.cwd()})...")

                # 5. Dispatch
                result = sim_engine.dispatch(sim_request)

                final_vars = {}
                if result.data and isinstance(result.data, dict):
                    if "variables" in result.data:
                        final_vars = result.data["variables"]
                    elif "gnosis" in result.data:
                        final_vars = result.data["gnosis"]
                    else:
                        final_vars = sim_request.variables

                return result, final_vars

        except Exception as e:
            Logger.warn(f"Simulation Mind encountered a paradox: {e}")
            failure_result = ScaffoldResult(
                success=False,
                message=f"Simulation Crash: {str(e)}",
                heresies=[
                    Heresy(
                        message="Inner Reality Collapse",
                        severity=HeresySeverity.CRITICAL,
                        details=str(e),
                        suggestion="Check for infinite loops or resource exhaustion in the blueprint."
                    )
                ]
            )
            return failure_result, sim_request.variables