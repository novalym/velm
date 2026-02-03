# // scaffold/artisans/translocate_core/resolvers/cpp/contracts.py
# ----------------------------------------------------------------

from dataclasses import dataclass


@dataclass
class CppDetectedInclude:
    line_num: int
    path: str
    kind: str  # 'local' ("...") or 'system' (<...>)
    start_byte: int
    end_byte: int


@dataclass
class CppHealingEdict:
    line_num: int
    original_path: str
    new_path: str
    start_byte: int
    end_byte: int

