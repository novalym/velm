# Path: scaffold/artisans/simulacrum/contracts.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path

@dataclass
class VoidContext:
    """The metaphysical state of a simulation."""
    id: str
    root: Path
    project_root: Path
    language: str
    env_vars: Dict[str, str]
    created_at: float

@dataclass
class RuntimeConfig:
    """Configuration for a specific language runtime."""
    binary: str
    args: List[str] = field(default_factory=list)
    extension: str = "txt"
    env_inject: Dict[str, str] = field(default_factory=dict)