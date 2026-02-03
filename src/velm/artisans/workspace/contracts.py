# Path: scaffold/artisans/workspace/contracts.py
# ----------------------------------------------
from __future__ import annotations
import time
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict


# =================================================================================
# == THE GNOSTIC CONTRACTS OF THE OBSERVATORY (V-Ω-ETERNAL-SCHEMA)               ==
# =================================================================================
# LIF: 10,000,000,000
#
# These vessels define the structure of the `.scaffold-workspace` scripture and
# the in-memory representation of the Multi-Project Cosmos.
# =================================================================================

class ProjectMetadata(BaseModel):
    """
    The Forensic Soul of a Project.
    Carries deep gnosis about the project's technological makeup, perceived by
    the LanguageOracle and GitHistorian.
    """
    model_config = ConfigDict(extra='allow')

    language: str = Field(default="generic", description="The primary tongue (python, node, rust).")
    frameworks: List[str] = Field(default_factory=list, description="Detected frameworks (react, fastapi).")
    git_branch: Optional[str] = Field(default=None, description="The currently active timeline.")
    last_build_time: Optional[float] = Field(default=None, description="Timestamp of the last successful build.")


class WorkspaceProject(BaseModel):
    """
    A Sovereign Reality within the Gnostic Observatory.
    Represents a single project's anchor, identity, and relationships.
    """
    model_config = ConfigDict(extra='ignore')

    # --- I. The Anchor ---
    path: str = Field(..., description="The relative path to the project root (e.g., './apps/api').")

    # --- II. The Identity ---
    gnosis_name: str = Field(default="", description="The luminous display name (defaults to directory name).")
    gnosis_description: str = Field(default="", description="A one-line summary of the project's purpose.")

    # --- III. The Constellation (Relationships) ---
    tags: List[str] = Field(default_factory=list, description="Taxonomy tags for filtering (e.g., 'backend', 'core').")
    depends_on: List[str] = Field(default_factory=list, description="Paths of other projects this one depends on.")

    # --- IV. The Origin ---
    remote: Optional[str] = Field(default=None, description="The Git remote URL for synchronization.")

    # --- V. The Telemetry (State) ---
    mode: Literal['managed', 'ethereal'] = Field(default='managed',
                                                 description="Whether this project is permanently enshrined or ephemeral.")
    last_accessed: float = Field(default_factory=time.time, description="Timestamp of the last Architect interaction.")

    # --- VI. The Deep Gnosis ---
    metadata: ProjectMetadata = Field(default_factory=ProjectMetadata, description="Auto-discovered characteristics.")

    @property
    def name(self) -> str:
        """Returns the effective name (gnosis_name or directory name)."""
        if self.gnosis_name:
            return self.gnosis_name
        # Fallback to directory name derived from path
        return self.path.replace('\\', '/').split('/')[-1]


class WorkspaceConfig(BaseModel):
    """
    The Scripture of the Cosmos (.scaffold-workspace).
    Defines the totality of the monitored universe.
    """
    model_config = ConfigDict(extra='ignore')

    version: str = Field(default="1.0", description="The schema version of this workspace manifest.")

    global_gnosis: Dict[str, Any] = Field(
        default_factory=dict,
        description="Variables injected into all workspace rites (e.g., shared company constants)."
    )

    projects: List[WorkspaceProject] = Field(
        default_factory=list,
        description="The roster of anchored realities."
    )

    def get_project(self, path_str: str) -> Optional[WorkspaceProject]:
        """Retrieves a project by its path."""
        # Normalize slashes for comparison
        target = path_str.replace('\\', '/')
        for p in self.projects:
            if p.path.replace('\\', '/') == target:
                return p
        return None

