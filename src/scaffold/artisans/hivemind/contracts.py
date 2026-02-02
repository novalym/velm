# Path: artisans/hivemind/contracts.py
# ------------------------------------

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class PersonaProfile:
    """The Soul of a Council Member."""
    name: str
    role: str
    system_prompt: str
    color: str
    icon: str
    # Tech Stack Overrides (The Polyglot Power)
    provider: Optional[str] = None  # e.g. "anthropic"
    model: Optional[str] = None  # e.g. "claude-3-opus"


@dataclass
class Argument:
    """A single utterance in the debate."""
    speaker: str
    content: str
    round: int
    timestamp: float


@dataclass
class Consensus:
    """The Final Verdict."""
    summary: str
    resolution: str
    minority_report: Optional[str] = None

