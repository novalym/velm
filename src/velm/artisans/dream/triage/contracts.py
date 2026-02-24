# Path: artisans/dream/triage/contracts.py
# ----------------------------------------

from enum import Enum, auto

class DreamIntent(Enum):
    """
    The Fundamental Classifications of Will.
    """
    GENESIS = auto()       # Creation of new matter (blueprints)
    MUTATION = auto()      # Modification of existing matter (refactor/move)
    TOOLING = auto()       # Execution of utilities (scripts/analysis)
    INQUIRY = auto()       # Requests for knowledge (help/explain)
    VOID = auto()          # Unknowable intent