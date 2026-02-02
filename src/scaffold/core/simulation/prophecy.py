# scaffold/core/simulation/prophecy.py

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from ...contracts.heresy_contracts import Heresy

class GnosticDiff(BaseModel):
    """
    A vessel for a single file's transformation.
    Captures the state transition from Reality -> Simulation.
    """
    path: str
    status: str # CREATED, MODIFIED, DELETED
    diff: Optional[str] = None

class SimulatedCommand(BaseModel):
    """A vessel for a simulated shell command (from the Maestro)."""
    command: str
    exit_code: int = 0
    output: str = "[Simulated Execution]"

class Prophecy(BaseModel):
    """
    The final, sacred proclamation of the Simulation Engine.
    It holds the complete dossier of the timeline divergence.
    """
    rite_name: str
    is_pure: bool = True
    summary: str
    diffs: List[GnosticDiff] = Field(default_factory=list)
    simulated_commands: List[SimulatedCommand] = Field(default_factory=list)
    heresies: List[Heresy] = Field(default_factory=list)
    final_variables: Dict[str, Any] = Field(default_factory=dict)