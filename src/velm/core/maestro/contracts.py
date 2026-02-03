# Path: scaffold/core/maestro/contracts.py
# ----------------------------------------
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import subprocess
from queue import Queue

from pydantic import BaseModel, Field


@dataclass
class KineticVessel:
    """
    [ASCENSION 9] The Luminous Vessel of Kinetic Will. A pure, Gnostic vessel
    chronicling the birth of a process.
    """
    process: subprocess.Popen
    output_queue: Queue
    start_time: float
    pid: int
    command: str
    sandbox_type: str


class MaestroContext(BaseModel):
    """
    The complete Gnostic Context for a single rite. It is the memory and the
    environment of the Maestro's Hand at one moment in time.
    """
    line_num: int
    explicit_undo: Optional[List[str]] = None
    cwd: Path = Field(..., description="The one true, absolute path for execution.")
    env: Dict[str, str] = Field(..., description="The complete, consecrated environment variables.")
    shell_executable: str = Field(..., description="The path to the chosen shell soul (bash, cmd.exe).")

    class Config:
        arbitrary_types_allowed = True

