# Path: src/velm/core/kernel/transaction/volume_shifter/contracts.py
# ------------------------------------------------------------------

from enum import Enum, auto
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path


class VolumeState(str, Enum):
    VOID = "VOID"  # No shadow exists
    FORGING = "FORGING"  # Data is being cloned
    RESONANT = "RESONANT"  # Shadow is ready for the Flip
    FLIPPING = "FLIPPING"  # The microsecond swap is in progress
    ACTIVE = "ACTIVE"  # Shadow has become Reality
    FRACTURED = "FRACTURED"  # Collision or OS-level failure


class FlipStrategy(str, Enum):
    RENAME = "RENAME"  # Physical directory rename (Most Atomic)
    SYMLINK = "SYMLINK"  # Pointer swap (Best for massive mass)
    COW = "COW"  # Copy-on-Write (Substrate dependent)


class VolumeManifest(BaseModel):
    """The Gnostic Dossier of a Shifter operation."""
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    tx_id: str
    start_time: float
    strategy: FlipStrategy
    source_path: Path
    shadow_path: Path
    legacy_path: Path
    merkle_root: str = "0xVOID"