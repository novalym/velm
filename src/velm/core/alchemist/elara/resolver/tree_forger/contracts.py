# Path: core/alchemist/elara/resolver/tree_forger/contracts.py
# -----------------------------------------------------------

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from ...contracts.atoms import ASTNode




@dataclass
class GnosticFrame:
    """
    =============================================================================
    == THE TOPOLOGICAL FRAME (V-Ω-MEMORY-CELL)                                 ==
    =============================================================================
    Represents a level of depth in the Dimensional Stack.
    """
    node: ASTNode
    indent_floor: int