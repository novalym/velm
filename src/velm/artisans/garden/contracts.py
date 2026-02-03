# Path: artisans/garden/contracts.py
# ----------------------------------

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional


@dataclass
class WitheredVine:
    """A unit of dead code detected in the Garden."""
    type: Literal["file", "function", "class", "import"]
    path: Path
    name: str
    line_num: int = 0
    confidence: float = 1.0
    reason: str = "Zero In-Degree"

    # Surgical data for removal
    start_byte: Optional[int] = None
    end_byte: Optional[int] = None

