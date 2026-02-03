# scaffold/artisans/daemon_artisan/contracts.py

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class DaemonInfo(BaseModel):
    """
    =================================================================================
    == THE GNOSTIC DOSSIER OF THE DAEMON                                           ==
    =================================================================================
    The sacred, immutable contract for the `daemon.json` file. It ensures the
    Daemon's self-awareness is always pure and well-formed.
    =================================================================================
    """
    pid: int
    port: int
    host: str
    token: str
    project_root: str
    mode: str = "Nexus"
    start_time: float
    user_context: Dict[str, Any] = Field(default_factory=dict)
    ssl: bool = False