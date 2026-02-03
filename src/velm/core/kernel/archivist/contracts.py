# Path: scaffold/core/kernel/archivist/contracts.py
# -------------------------------------------------

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Literal, Any
import time

@dataclass
class ArchiveConfig:
    """
    The Will of Preservation.
    """
    compression: Literal["gz", "bz2", "xz"] = "gz"
    compression_level: int = 9
    include_git: bool = False
    max_file_size_mb: int = 100
    retention_count: int = 10  # Keep last 10 snapshots
    follow_symlinks: bool = False
    verify_integrity: bool = True
    # If True, generates a 'light' snapshot (structure only, no content) for huge repos
    structure_only: bool = False

@dataclass
class ArchiveResult:
    """
    The Chronicle of the Archival Rite.
    """
    success: bool
    path: Path
    size_bytes: int
    file_count: int
    duration_ms: float
    manifest_hash: str
    skipped_files: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RestoreConfig:
    """
    The Will of Resurrection.
    """
    wipe_destination: bool = False  # Dangerous: Clean directory before restore
    force: bool = False             # Bypass safety checks
    strategy: Literal["overlay", "clean"] = "overlay"

@dataclass
class RestoreResult:
    """
    The Chronicle of the Resurrection.
    """
    success: bool
    files_restored: int
    bytes_restored: int
    duration_ms: float
    heresies: List[str] = field(default_factory=list)