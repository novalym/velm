# Path: scaffold/core/redemption/diagnostician/contracts.py
# ---------------------------------------------------------

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class Diagnosis:
    """
    The Sacred Vessel of Healing.
    Contains not just the cure, but the understanding of the malady.
    """
    heresy_name: str
    cure_command: Optional[str]
    advice: str
    confidence: float  # 0.0 to 1.0
    metadata: Dict[str, Any]

    def to_string(self) -> str:
        """Returns the simple command string for legacy compatibility."""
        return self.cure_command