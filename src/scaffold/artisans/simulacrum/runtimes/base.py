import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict


@dataclass
class RuntimeConfig:
    binary: str
    args: List[str] = field(default_factory=list)
    extension: str = "txt"
    env_inject: Dict[str, str] = field(default_factory=dict)
    entry_point_name: str = "main"


class BaseRuntime(ABC):
    def __init__(self, project_root: Path):
        self.project_root = project_root

    @abstractmethod
    def configure(self, void_path: Path) -> RuntimeConfig:
        """Determines the execution command and environment."""
        pass

    def prepare_source(self, content: str, void_path: Path, filename: str) -> Path:
        """Writes the source code to the void."""
        script_path = void_path / filename
        script_path.write_text(content, encoding="utf-8")
        return script_path

    def _inject_path(self, new_paths: List[str]) -> str:
        current = os.environ.get("PATH", "")
        return os.pathsep.join(new_paths) + os.pathsep + current