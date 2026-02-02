# Path: scaffold/artisans/distill/core/skeletonizer/contracts.py
# --------------------------------------------------------------

from dataclasses import dataclass, field
from typing import List, Set, Optional, Dict, Any

@dataclass
class SkeletonStats:
    """The Vital Signs of the Surgery."""
    active_count: int = 0
    dormant_count: int = 0
    hidden_lines: int = 0
    bytes_saved: int = 0

@dataclass
class SurgicalContext:
    """
    The Context of the Operation.
    Carries the file's Gnosis and the Architect's Intent into the operating theatre.
    """
    content: str
    dossier: Dict[str, Any]
    active_symbols: Optional[Set[str]]
    focus_keywords: List[str]
    stats: SkeletonStats = field(default_factory=SkeletonStats)
    is_stub_mode: bool = False  # The Apophatic Filter

    @property
    def lines(self) -> List[str]:
        return self.content.splitlines()