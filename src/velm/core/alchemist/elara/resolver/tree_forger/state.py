# Path: core/alchemist/elara/resolver/tree_forger/state.py
# -----------------------------------------------------------

from typing import List
from .contracts import GnosticFrame, ASTNode
from ......logger import Scribe

Logger = Scribe("TopologicalStack")

class TopologicalStack:
    """
    =============================================================================
    == THE DIMENSIONAL STACK (V-Ω-GEOMETRIC-MEMORY)                            ==
    =============================================================================
    ROLE: DEPTH_WARDEN | RANK: MASTER
    """

    def __init__(self, root: ASTNode):
        self.frames: List[GnosticFrame] = [GnosticFrame(node=root, indent_floor=-1)]

    @property
    def current_node(self) -> ASTNode:
        return self.frames[-1].node

    @property
    def current_indent(self) -> int:
        return self.frames[-1].indent_floor

    def push(self, node: ASTNode, indent: int):
        """Descends into a new logical stratum."""
        self.frames.append(GnosticFrame(node=node, indent_floor=indent))

    def pop(self) -> GnosticFrame:
        """Ascends from the current logic branch."""
        if len(self.frames) > 1:
            return self.frames.pop()
        return self.frames[0]

    def __len__(self):
        return len(self.frames)