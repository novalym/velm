# Path: src/velm/artisans/project/contracts.py
# -----------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: GOVERNANCE_CONTRACT_ORACLE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONTRACTS_V1200_MUTABLE_JSON_SUTURE_2026_FINALIS
# =========================================================================================

import time
import uuid
import json
import re
from typing import Dict, List, Any, Optional, Union, Iterator
from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator

# =============================================================================
# == [THE ULTIMATE SUTURE]: THE GLOBAL JSON APOTHEOSIS                      ==
# =============================================================================
# This rite is conducted at the moment of inhalation. It teaches the entire
# Python interpreter how to handle Gnostic Vessels, ensuring json.dump()
# never fractures again.

_original_json_dump = json.dump
_original_json_dumps = json.dumps


def _gnostic_json_serializer(obj):
    """Transmutes complex souls into JSON-safe matter."""
    if hasattr(obj, 'model_dump'):
        return obj.model_dump(mode='json')
    if isinstance(obj, set):
        return list(obj)
    if hasattr(obj, '__dict__'):
        return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
    return str(obj)


def gnostic_dump(obj, fp, *args, **kwargs):
    """A version of json.dump that is aware of Pydantic souls."""
    if 'default' not in kwargs:
        kwargs['default'] = _gnostic_json_serializer
    return _original_json_dump(obj, fp, *args, **kwargs)


def gnostic_dumps(obj, *args, **kwargs):
    """A version of json.dumps that is aware of Pydantic souls."""
    if 'default' not in kwargs:
        kwargs['default'] = _gnostic_json_serializer
    return _original_json_dumps(obj, *args, **kwargs)


# [STRIKE]: Apply the global suture
json.dump = gnostic_dump
json.dumps = gnostic_dumps


# =============================================================================
# == THE POLYMORPHIC BASE: GnosticVessel                                     ==
# =============================================================================
class GnosticVessel(BaseModel):
    """
    =============================================================================
    == THE GNOSTIC VESSEL (V-Ω-TOTALITY-V1200-POLYMORPHIC)                     ==
    =============================================================================
    LIF: ∞ | ROLE: ISOMORPHIC_STATE_VESSEL | RANK: OMEGA_SUPREME

    This vessel implements the Mutable Mapping protocol, allowing it to behave
    exactly like a dictionary while maintaining Pydantic V2 structure.
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='allow'  # [ASCENSION 8]: Pydantic V2 Adrenaline
    )

    # =========================================================================
    # == [THE CURE]: THE MUTABLE MAPPING SUTURE                              ==
    # =========================================================================

    def __getitem__(self, key: str) -> Any:
        """Enables model['name'] resonance."""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(f"Lattice Gap: Field '{key}' is unmanifest in {self.__class__.__name__}.")

    def __setitem__(self, key: str, value: Any):
        """
        [THE CURE]: Enables model['key'] = value.
        Annihilates 'TypeError: RegistrySchema object does not support item assignment'.
        """
        # If the key is a formal field, use the Pydantic setter
        if key in self.model_fields:
            setattr(self, key, value)
        else:
            # [ASCENSION 3]: Overflow Triage
            # If the class has a custom_data 'Bag of Holding', store it there.
            if hasattr(self, 'custom_data') and isinstance(self.custom_data, dict):
                self.custom_data[key] = value
            else:
                # Otherwise, use the Pydantic 'extra' storage
                setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:
        """Socratic retrieval: object-first, dict-fallback."""
        return getattr(self, key, default)

    def keys(self):
        """Proclaims the manifest of all Gnostic fields."""
        return self.model_dump().keys()

    def values(self):
        return self.model_dump().values()

    def items(self):
        return self.model_dump().items()

    def __iter__(self) -> Iterator:
        """[ASCENSION 2]: Mimics a dictionary during JSON serialization."""
        yield from self.model_dump().keys()

    def __contains__(self, key: object) -> bool:
        return hasattr(self, key)


# =============================================================================
# == I. METABOLIC TELEMETRY (ProjectStats)                                   ==
# =============================================================================
class ProjectStats(GnosticVessel):
    """The metabolic mass and vitality of a physical project."""
    file_count: int = 0
    size_kb: int = 0
    health_score: int = 100
    last_integrity_check: int = Field(default_factory=lambda: int(time.time() * 1000))


# =============================================================================
# == II. THE SOVEREIGN IDENTITY (ProjectMeta)                                ==
# =============================================================================
class ProjectMeta(GnosticVessel):
    """
    =============================================================================
    == THE ISOMORPHIC PROJECT META (V-Ω-TOTALITY-V1200-HEALED)                 ==
    =============================================================================
    The one true contract for a single Reality.
    """
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
    version: str = "1.0.0"

    # --- VI. TELEMETRY ---
    stats: ProjectStats = Field(default_factory=ProjectStats)

    # --- VII. THE BAG OF HOLDING ---
    custom_data: Dict[str, Any] = Field(default_factory=dict)

    # =========================================================================
    # == THE ALCHEMICAL NORMALIZERS                                          ==
    # =========================================================================
    @field_validator('path', mode='before')
    @classmethod
    def _normalize_path_geometry(cls, v: Any) -> str:
        """[ASCENSION 6]: Enforces POSIX-slash harmony."""
        if isinstance(v, str):
            return v.replace('\\', '/')
        return str(v)

    @computed_field
    @property
    def age_days(self) -> int:
        """Calculates the temporal age of the project in the mortal realm."""
        delta = (time.time() * 1000) - self.created_at
        return int(delta / (1000 * 60 * 60 * 24))


# =============================================================================
# == III. THE BOOK OF NAMES (RegistrySchema)                                 ==
# =============================================================================
class RegistrySchema(GnosticVessel):
    """
    =============================================================================
    == THE MULTIVERSE REGISTRY (V-Ω-TOTALITY-V1200-SUBSCRIPTABLE)              ==
    =============================================================================
    The complete Book of Names. Healed of the subscriptable heresy.
    """
    version: str = "2.0.0-OMEGA"
    active_project_id: Optional[str] = None
    projects: Dict[str, ProjectMeta] = Field(default_factory=dict)

    def get_active(self) -> Optional[ProjectMeta]:
        """Returns the project currently anchored to the Engine's mind."""
        if self.active_project_id:
            return self.projects.get(self.active_project_id)
        return None

    def __repr__(self) -> str:
        return f"<Ω_REGISTRY v={self.version} projects={len(self.projects)}>"