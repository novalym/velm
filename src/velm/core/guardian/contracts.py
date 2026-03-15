# Path: velm/core/guardian/contracts.py
# -----------------------------------------

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional


class ThreatLevel(Enum):
    """
    =============================================================================
    == THE SCALES OF JURISPRUDENCE (V-Ω-TOTALITY)                              ==
    =============================================================================
    Defines the mathematical weight of architectural danger.
    """
    SAFE = 0  # Pure intent: Read-only, idempotent scrying.
    LOW = 10  # Minor risk: Standard file creation, metadata mutation.

    # [ASCENSION]: THE SHADOWED INTENT
    SUSPICIOUS = 30  # Unusual patterns: Unquoted variables, complex pipes, or shadowed symbols.

    MEDIUM = 50  # Significant state change: Tool execution, dependency weaving, environment shifts.
    HIGH = 80  # Dangerous: Physical permission mutation (chmod), celestial network egress.
    CRITICAL = 100  # Existential threat: Annihilation rites (rm -rf), secret exposure, kernel-level overrides.

@dataclass
class SecurityViolation:
    """A specific transgression against the laws of safety."""
    ward: str
    reason: str
    threat_level: ThreatLevel
    context: str


@dataclass
class SentinelVerdict:
    """The Final Judgment of the Citadel."""
    allowed: bool
    score: int
    violations: List[SecurityViolation] = field(default_factory=list)

    @property
    def highest_threat(self) -> ThreatLevel:
        if not self.violations:
            return ThreatLevel.SAFE
        return max((v.threat_level for v in self.violations), key=lambda x: x.value)

    def summary(self) -> str:
        if self.allowed:
            return "Rite Approved."
        return f"Rite Rejected ({self.highest_threat.name}): {self.violations[0].reason}"