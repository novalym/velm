# Path: core/lsp/features/workspace/folders/models.py
# ----------------------------------------------------
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Dict
from enum import Enum
import time


class RootAura(str, Enum):
    SCAFFOLD = "scaffold"
    PYTHON = "python"
    NODE = "node"
    SYSTEMS = "systems"
    SHADOW = "shadow"
    UNKNOWN = "unknown"


class FolderMetadata(BaseModel):
    """The physiological record of a sanctum."""
    file_count: int = 0
    total_mass_bytes: int = 0
    aura: RootAura = RootAura.UNKNOWN
    is_ghosted: bool = False
    last_scry_ts: float = Field(default_factory=time.time)


class WorkspaceFolder(BaseModel):
    """
    [LSP 3.17 COMPLIANT]
    The definitive vessel for a project root.
    """
    model_config = ConfigDict(populate_by_name=True)

    uri: str
    name: str

    # [ASCENSION 8]: Gnostic Metadata
    metadata: FolderMetadata = Field(default_factory=FolderMetadata)