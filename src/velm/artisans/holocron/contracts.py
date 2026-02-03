from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional


@dataclass
class HolocronCandidate:
    """A file or symbol proposed for inclusion."""
    path: str
    reason: str  # e.g. "Vector Hit", "Called by main.py"
    score: float
    summary: str  # Brief description for the AI Curator


@dataclass
class VirtualContext:
    """The Final Distilled Reality."""
    intent: str
    files: Dict[str, str]  # Path -> Sliced Content
    token_count: int
    rationale: str  # Why the AI chose this set

