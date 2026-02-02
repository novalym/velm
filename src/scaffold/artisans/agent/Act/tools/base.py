# artisans/agent/Act/tools/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class BaseTool(ABC):
    """
    The Abstract Soul of an Agentic Tool.
    """
    name: str
    description: str
    args_schema: Dict[str, Any]

    def __init__(self, project_root: Path, engine: Any):
        self.project_root = project_root
        self.engine = engine

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        Performs the tool's rite. Returns a string observation.
        """
        pass

