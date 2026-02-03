# Path: scaffold/creator/io_controller/contracts.py
from __future__ import annotations
from dataclasses import dataclass


# This scripture stands as a prophecy. While the current I/O symphony is one
# of pure action, this sacred space is consecrated for any future Gnostic
# data vessels that may be required to carry the will between the specialist
# artisans of this sanctum.

@dataclass
class PathGnosis:
    """A vessel for carrying transmuted and validated path information."""
    logical_path: str
    physical_path: str
    is_in_staging: bool

