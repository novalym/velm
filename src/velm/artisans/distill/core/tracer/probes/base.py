# Path: scaffold/artisans/distill/core/oracle/tracer/probes/base.py
# -----------------------------------------------------------------

from abc import ABC, abstractmethod
from pathlib import Path
from ..contracts import RuntimeState


class BaseProbe(ABC):
    """
    The Sacred Contract for all Live Tracers.
    """

    def __init__(self, project_root: Path):
        self.root = project_root

    @abstractmethod
    def conduct(self, command: str) -> RuntimeState:
        """Executes the command under observation."""
        pass

