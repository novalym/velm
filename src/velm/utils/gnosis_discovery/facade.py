# Path: src/velm/utils/gnosis_discovery/facade.py
# -----------------------------------------------

from typing import List, Dict, Any, Tuple, Optional
from .inquisitor import OmegaInquisitor
from ...contracts.data_contracts import ScaffoldItem
from .contracts import GnosticDossier

def discover_required_gnosis(
        execution_plan: List[ScaffoldItem],
        post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
        blueprint_vars: Dict[str, Any],
        macros: Optional[Dict[str, Any]] = None,
        tasks: Optional[Dict[str, Any]] = None
) -> GnosticDossier:
    """
    =================================================================================
    == THE UNIVERSAL GATEWAY (V-Ω-TOTALITY-V10000-SOVEREIGN-HEALED)                ==
    =================================================================================
    The one true, public rite for discovering required variables.
    It materializes the ascended Omega Inquisitor and righteously delegates the
    Inquest, ensuring all Macro and Task scopes are correctly warded.
    =================================================================================
    """
    inquisitor = OmegaInquisitor()
    return inquisitor.inquire(
        execution_plan=execution_plan,
        post_run_commands=post_run_commands,
        blueprint_vars=blueprint_vars,
        known_macros=macros or {},
        known_tasks=tasks or {}
    )