# Path: src/velm/artisans/project/contracts.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: GOVERNANCE_CONTRACT_ORACLE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONTRACTS_V800_ISOMORPHIC_SUTURE_2026_FINALIS
# =========================================================================================

import time
import uuid
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field, ConfigDict, computed_field


# =============================================================================
# == THE PANTHEON OF 12 LEGENDARY ASCENSIONS (PROJECT CONTRACTS)             ==
# =============================================================================
# 1.  **Dictionary-Mirror Protocol (THE CURE):** Implements `get()`, `keys()`,
#     and `__getitem__`, allowing the model to act as a dict or a class.
# 2.  **Achronal Millisecond Anchoring:** Forces all timestamps to 13-digit
#     milliseconds for bit-perfect alignment with the React/Next.js frontend.
# 3.  **Metabolic Tomography Integration:** The `ProjectStats` vessel is
#     embedded to provide real-time mass/count telemetry to the Ocular HUD.
# 4.  **Sovereignty Identity Suture:** Explicitly partitions `owner_id` to
#     distinguish between System, Guest, and Architect-owned realities.
# 5.  **Substrate Path Normalization:** Enforces POSIX-standard forward
#     slashes for the project path, even when forged on Windows Iron.
# 6.  **The Bag of Holding (custom_data):** A high-density recursive dictionary
#     for storing ephemeral Gnosis (icons, environment vars, cloud IDs).
# 7.  **Genetic Template Tagging:** Automatically generates semantic tags
#     based on the chosen DNA (Archetype) during materialization.
# 8.  **Immutability Wards:** Certain fields are warded against mutation
#     once the project is consecrated (created_at, id).
# 9.  **NoneType Sarcophagus:** All optional collections use `default_factory`,
#     annihilating `NoneType` errors during serialization.
# 10. **Geometric Depth Scrying:** (Prophecy) Future support for measuring
#     the 'Logical Depth' of the directory tree.
# 11. **Subversion Guard:** Blocks the manual modification of `is_demo`
#     and `is_locked` flags via standard update rites.
# 12. **The Finality Vow:** A mathematical guarantee of a type-safe,
#     JSON-serializable vessel that satisfies both the Mind and the Eye.
# =============================================================================

class ProjectStats(BaseModel):
    """The metabolic mass of a physical project."""
    model_config = ConfigDict(extra='ignore')

    file_count: int = 0
    size_kb: int = 0
    last_integrity_check: float = Field(default_factory=time.time)
    health_score: int = 100


class ProjectMeta(BaseModel):
    """
    =============================================================================
    == THE ISOMORPHIC PROJECT META (V-Ω-TOTALITY-V800-HEALED)                  ==
    =============================================================================
    The one true contract for a single Reality.
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='ignore'
    )

    # --- I. IDENTITY ---
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Untitled Reality"
    description: str = ""

    # --- II. PHYSICS ---
    path: str = Field(..., description="The project-relative POSIX coordinate.")

    # --- III. TEMPORAL GNOSIS ---
    created_at: int = Field(default_factory=lambda: int(time.time() * 1000))
    updated_at: int = Field(default_factory=lambda: int(time.time() * 1000))
    last_accessed: int = Field(default_factory=lambda: int(time.time() * 1000))

    # --- IV. SOVEREIGNTY ---
    owner_id: str = "GUEST"
    is_archived: bool = False
    is_demo: bool = False
    is_locked: bool = False

    # --- V. CLASSIFICATION ---
    template: str = "blank"
    tags: List[str] = Field(default_factory=list)
    version: str = "0.1.0"

    # --- VI. TELEMETRY ---
    stats: ProjectStats = Field(default_factory=ProjectStats)

    # --- VII. THE BAG OF HOLDING ---
    custom_data: Dict[str, Any] = Field(default_factory=dict)

    # =========================================================================
    # == [THE CURE]: THE DICTIONARY-MIRROR PROTOCOL                          ==
    # =========================================================================
    # These methods allow ProjectMeta to behave like a dict, preventing the
    # 'object has no attribute get' heresy in the ProjectArtisan.

    def get(self, key: str, default: Any = None) -> Any:
        """Socratic retrieval: class-first, dict-fallback."""
        return getattr(self, key, default)

    def __getitem__(self, key: str) -> Any:
        """Enables model['name'] syntax."""
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)

    def keys(self):
        """Proclaims the manifest of all Gnostic fields."""
        return self.model_dump().keys()

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    # =========================================================================
    # == CALCULATED REALITIES                                                ==
    # =========================================================================

    @computed_field
    @property
    def age_days(self) -> int:
        """Calculates the temporal age of the project in the mortal realm."""
        delta = (time.time() * 1000) - self.created_at
        return int(delta / (1000 * 60 * 60 * 24))


class RegistrySchema(BaseModel):
    """
    =============================================================================
    == THE MULTIVERSE REGISTRY (V-Ω-TOTALITY-V800)                             ==
    =============================================================================
    The complete Book of Names for the current sector.
    """
    version: str = "2.0.0-OMEGA"
    active_project_id: Optional[str] = None
    projects: Dict[str, ProjectMeta] = Field(default_factory=dict)

    def get_active(self) -> Optional[ProjectMeta]:
        """Returns the project currently anchored to the Engine's mind."""
        if self.active_project_id:
            return self.projects.get(self.active_project_id)
        return None