from dataclasses import dataclass
from enum import Enum, auto


# --- THE NEW SACRED SCRIPTURE: THE LANGUAGE OF ARCHITECTURAL INTENT ---
class GnosticArchetype(Enum):
    """The divine, Gnostic soul of a single path segment's purpose."""
    ROOT = auto()       # The source root (e.g., 'src', 'app')
    DOMAIN = auto()     # An architectural domain (e.g., 'components', 'services')
    ENTITY = auto()     # The name of a specific thing (e.g., 'UserProfile')
    RITUAL = auto()     # A file with a special framework meaning (e.g., 'index.tsx')
    UTILITY = auto()    # A supporting directory (e.g., 'utils', 'helpers')
    UNKNOWN = auto()    # A segment whose soul has not yet been perceived.

@dataclass
class SemanticSegment:
    """A sacred vessel for a single, semantically understood path segment."""
    segment: str
    archetype: GnosticArchetype