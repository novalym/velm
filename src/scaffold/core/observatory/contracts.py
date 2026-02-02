# Path: scaffold/core/observatory/contracts.py
# --------------------------------------------
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ProjectHealth(str, Enum):
    """The Vitality of a Project."""
    HEALTHY = "HEALTHY"    # Exists, clean git, valid config
    DIRTY = "DIRTY"        # Uncommitted changes
    DRIFT = "DRIFT"        # Config mismatch / Missing dependencies
    GHOST = "GHOST"        # Directory vanished from mortal realm
    UNKNOWN = "UNKNOWN"    # Not yet scanned

class ProjectType(str, Enum):
    """The Soul of the Project."""
    PYTHON = "python"
    NODE = "node"
    RUST = "rust"
    GO = "go"
    POLYGLOT = "polyglot"
    GENERIC = "generic"

class ProjectMetadata(BaseModel):
    """The Deep Gnosis of a specific reality."""
    model_config = ConfigDict(extra='allow')

    language: ProjectType = ProjectType.GENERIC
    frameworks: List[str] = Field(default_factory=list)
    git_branch: Optional[str] = None
    git_remote: Optional[str] = None
    scaffold_version: Optional[str] = None
    last_build_time: Optional[float] = None
    dependencies_hash: Optional[str] = None

class ProjectEntry(BaseModel):
    """
    A single star in the Observatory's sky.
    Represents a managed project on the local filesystem.
    """
    id: str  # Unique hash of the absolute path
    path: Path
    name: str
    created_at: float = Field(default_factory=lambda: datetime.now().timestamp())
    last_accessed: float = Field(default_factory=lambda: datetime.now().timestamp())
    access_count: int = 0
    health: ProjectHealth = ProjectHealth.UNKNOWN
    metadata: ProjectMetadata = Field(default_factory=ProjectMetadata)
    tags: List[str] = Field(default_factory=list)
    is_pinned: bool = False

class ObservatoryState(BaseModel):
    """
    The complete state of the Universe.
    Persisted to ~/.scaffold/observatory.json.
    """
    version: str = "1.0"
    active_project_id: Optional[str] = None
    projects: Dict[str, ProjectEntry] = Field(default_factory=dict)
    global_tags: List[str] = Field(default_factory=list)