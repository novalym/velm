# Path: scaffold/artisans/distill/core/oracle/forensics/contracts.py
# ------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path


@dataclass
class Indictment:
    """
    A formal accusation against a specific file.
    """
    path: Path
    score: int
    reason: str
    line_number: Optional[int] = None
    context_snippet: Optional[str] = None

    def __hash__(self):
        return hash((self.path, self.line_number))


@dataclass
class ForensicReport:
    """
    The final dossier of the investigation.
    """
    primary_error: Optional[str] = None
    indictments: List[Indictment] = field(default_factory=list)
    raw_evidence_size: int = 0

    @property
    def most_guilty(self) -> List[Indictment]:
        """Returns indictments sorted by score (highest first)."""
        return sorted(self.indictments, key=lambda x: x.score, reverse=True)