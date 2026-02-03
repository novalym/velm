# // scaffold/artisans/translocate_core/resolvers/rust/contracts.py
# -----------------------------------------------------------------

from dataclasses import dataclass


@dataclass
class RustDetectedUse:
    line_num: int
    path: str  # e.g., "crate::utils::helper"
    start_byte: int  # Byte offset of the path string in the use stmt
    end_byte: int


@dataclass
class RustHealingEdict:
    line_num: int
    original_path: str
    new_path: str
    start_byte: int
    end_byte: int

