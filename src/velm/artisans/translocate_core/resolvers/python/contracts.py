# // scaffold/artisans/translocate_core/resolvers/python/contracts.py
# -------------------------------------------------------------------

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

@dataclass
class DetectedImport:
    """
    A raw import statement perceived by the Inquisitor.
    """
    line_num: int
    module: Optional[str]      # e.g. "core.utils"
    name: str                  # e.g. "get_gnosis" or "*"
    alias: Optional[str]       # e.g. "gg" in "as gg"
    level: int                 # e.g. 2 for ".."
    is_wildcard: bool

@dataclass
class HealingEdict:
    """
    A specific instruction to transfigure an import statement.
    """
    line_num: int
    symbol_name: str           # The symbol being imported
    original_module: str       # What it currently says
    new_module_path: str       # What it MUST say to be pure
    confidence: float = 1.0    # For future probabilistic healing