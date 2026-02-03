# Path: parser_core/lfg_builder/contracts.py
# ------------------------------------------

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Any

class NodeShape(Enum):
    """The Gnostic Shape of a Node."""
    RECTANGLE = "rect"          # Default / Action
    ROUND_RECT = "round"        # State / Start / End
    DIAMOND = "diamond"         # Decision / Conditional
    CYLINDER = "cylinder"       # Database / Storage
    PARALLELOGRAM = "parallel"  # I/O
    SUBROUTINE = "subroutine"   # Function Call

class LFGNode(dataclass):
    """A single point of logic."""
    id: str
    label: str
    shape: NodeShape = NodeShape.RECTANGLE
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.id)

class LFGEdge(dataclass):
    """The causal link between two points."""
    source_id: str
    target_id: str
    label: Optional[str] = None
    style: str = "solid" # solid, dotted, thick

class LogicFlowGraph(dataclass):
    """The complete map of a logical reality."""
    title: str
    nodes: List[LFGNode] = field(default_factory=list)
    edges: List[LFGEdge] = field(default_factory=list)
    subgraphs: List['LogicFlowGraph'] = field(default_factory=list)

    def add_node(self, id: str, label: str, shape: NodeShape = NodeShape.RECTANGLE) -> str:
        self.nodes.append(LFGNode(id, label, shape))
        return id

    def add_edge(self, source: str, target: str, label: str = None):
        self.edges.append(LFGEdge(source, target, label))