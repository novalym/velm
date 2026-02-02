# Path: scaffold/core/guardian/contracts.py
# -----------------------------------------

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional


class ThreatLevel(Enum):
    """The Gnostic measure of danger."""
    SAFE = 0  # Pure intent
    LOW = 10  # Minor risk (e.g., read operations)
    MEDIUM = 50  # Significant state change
    HIGH = 80  # Dangerous (e.g., chmod, network)
    CRITICAL = 100  # Existential threat (e.g., rm -rf /, secrets)


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