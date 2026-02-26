# Path: src/velm/core/sanctum/contracts.py
# ----------------------------------------

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Dict, Any
import time


class SanctumKind(str, Enum):
    """The Ontological Nature of the Sanctum."""
    LOCAL = "local"  # The Mortal Realm (Iron)
    MEMORY = "memory"  # The Ethereal Plane (RAM)
    S3 = "s3"  # The Celestial Archive (Object Storage)
    SSH = "ssh"  # The Wormhole (Remote Execution)


@dataclass
class SanctumStat:
    """
    =============================================================================
    == THE UNIVERSAL ATOM (V-Ω-UNIFIED-STAT-RESULT)                            ==
    =============================================================================
    A normalized forensic biopsy of a file, valid across all dimensions.
    Annihilates the differences between `os.stat`, `s3.head_object`, and `sftp.stat`.
    """
    path: str
    size: int
    mtime: float
    kind: str = "file"  # 'file', 'dir', 'symlink', 'void'
    permissions: int = 0o644
    owner: str = "root"
    group: str = "root"
    content_type: Optional[str] = None
    etag: Optional[str] = None  # For Cloud entities
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_dir(self) -> bool:
        return self.kind == "dir"

    @property
    def is_file(self) -> bool:
        return self.kind == "file"

    @property
    def is_symlink(self) -> bool:
        return self.kind == "symlink"