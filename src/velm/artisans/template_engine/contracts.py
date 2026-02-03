# Path: scaffold/artisans/template_engine/contracts.py
# ----------------------------------------------------
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import TemplateEngine

# We re-export TemplateGnosis to keep this file as the single source of truth for internal structs
from ...contracts.data_contracts import TemplateGnosis

@dataclass
class GnosticManifestRule:
    """
    A sacred, pre-compiled vessel for a single Gnostic Law from a manifest.json.
    It commands the Engine to prefer specific templates for specific file patterns.
    """
    priority: int
    template_path: Path
    applies_to_glob: str
    source_manifest: Path

@dataclass
class GnosticPathDeconstruction:
    """
    The result of the Architect's Gaze upon a target path.
    It deconstructs a filename into its semantic components (Suffix, Archetype, Domain).
    """
    filename: str
    suffix: str
    parent_domains: List[Path]
    archetype: Optional[str]
    # === THE DIVINE BESTOWAL OF MEMORY ===
    # The vessel holds a reference to the Engine to access aliases/config during the Gaze.
    engine: 'TemplateEngine'