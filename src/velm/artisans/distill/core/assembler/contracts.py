# Path: scaffold/artisans/distillation/assembler/contracts.py
# -----------------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union


@dataclass
class AssemblyStats:
    """The Ledger of the Build."""
    total_tokens: int = 0
    files_included: int = 0
    files_omitted: int = 0
    breakdown: Dict[str, int] = field(default_factory=lambda: {
        'full': 0, 'skeleton': 0, 'summary': 0, 'path_only': 0
    })


@dataclass
class AssemblyContext:
    """The Configuration of the Loom."""
    token_budget: int
    focus_keywords: List[str]
    active_symbols_map: Dict[str, Any]  # Path -> Set[symbols]

