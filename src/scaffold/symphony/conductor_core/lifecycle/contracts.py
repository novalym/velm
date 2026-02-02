# Path: scaffold/symphony/conductor_core/lifecycle/contracts.py
# -------------------------------------------------------------

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any

class ServiceState(Enum):
    """
    The Living State of a Daemon.
    """
    PENDING = 'PENDING'
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    HEALTHY = 'HEALTHY'
    UNHEALTHY = 'UNHEALTHY'
    STOPPED = 'STOPPED'
    CRASHED = 'CRASHED'
    RESTARTING = 'RESTARTING'


@dataclass
class ServiceConfig:
    """
    The DNA of a Background Service.
    """
    name: str
    command: str
    cwd: Path
    action: str = "start"
    healthcheck_cmd: Optional[str] = None
    initial_delay_s: int = 5
    restart_policy: str = "on-failure"  # 'always', 'on-failure', 'never'
    env: Dict[str, str] = field(default_factory=dict)