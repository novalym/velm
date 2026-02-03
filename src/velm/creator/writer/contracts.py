# Path: scaffold/creator/writer/contracts.py
# ------------------------------------------
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any
from ...contracts.data_contracts import InscriptionAction

class WriteMode(str, Enum):
    CREATE = "CREATE"
    OVERWRITE = "OVERWRITE"
    APPEND = "APPEND"
    PREPEND = "PREPEND"
    SKIP = "SKIP"

@dataclass
class WriterResult:
    """The immutable chronicle of a writing event."""
    path: Path
    success: bool
    action: InscriptionAction
    bytes_written: int = 0
    fingerprint: Optional[str] = None
    diff: Optional[str] = None
    security_alerts: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0