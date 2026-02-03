# Path: scaffold/symphony/conductor_core/resilience/contracts.py
# --------------------------------------------------------------

import time
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, Any, Dict

# --- THE DIVINE SUMMONS ---
# We must know the shape of an Edict to enshrine it.
from ....contracts.symphony_contracts import Edict

class IntercessionChoice(Enum):
    """
    The Sacred Alphabet of Redemption. Each value corresponds to the Architect's
    plea at the Altar of Intercession.
    """
    RETRY = "r"
    SKIP = "s"
    EDIT = "e"
    SHELL = "!"
    DIAGNOSE = "d"
    GOOGLE = "g"
    ABORT = "q"


@dataclass
class IntercessionOutcome:
    """
    =============================================================================
    == THE VESSEL OF WILL (V-Ω-ETERNAL-APOTHEOSIS)                             ==
    =============================================================================
    A humble, mutable vessel forged at the beginning of a `rite_boundary`. It is
    destined to carry the one true, final will of the Architect (`choice`) back
    to the Symphony Engine if a paradox occurs. Its soul is pure potential.
    """
    choice: Optional[IntercessionChoice] = None


@dataclass(frozen=True)
class FailureContext:
    """
    =============================================================================
    == THE FORENSIC DOSSIER (V-Ω-IMMUTABLE-TRUTH)                              ==
    =============================================================================
    A sacred, immutable vessel forged only at the moment of paradox. It contains
    the complete, Gnostic truth of a fallen rite—the Edict, the heresy, and the
    state of the cosmos at the moment of its death. It is the black box recorder
    of the Symphony.
    """
    edict: Edict
    heresy: Exception
    traceback: str
    variables: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)