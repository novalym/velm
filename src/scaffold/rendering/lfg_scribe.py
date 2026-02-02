# Path: scaffold/rendering/lfg_scribe.py
# --------------------------------------

"""
=================================================================================
== THE SCRIBE OF WILL (V-Ω-LOGIC-FLOW-GRAPH-RENDERER)                          ==
=================================================================================
LIF: 100,000,000,000

This divine artisan is the Gnostic Cartographer of Logic. It receives the pure
Logic Flow Graph from the Parser's dossier and transmutes it into a luminous,
Mermaid.js scripture, revealing the branching paths and potential realities
of the blueprint's intent.
=================================================================================
"""
from typing import List, Dict, Any, Set

from ..contracts.data_contracts import LogicNode, LogicNodeType, ConditionNode, LoopNode, SequenceNode
from ..logger import Scribe

Logger = Scribe("LFG_Scribe")


class LogicFlowGraphScribe:
    """The Scribe that forges Mermaid.js graphs from the Parser's logic tree."""

    def __init__(self, logic_graph: List[LogicNode]):
        self.graph = logic_graph
        self.lines: List[str] = []
        self.nodes_declared: Set[str] = set()

    def render(self) -> str:
        """The Grand Rite of Luminous Proclamation."""
        self.lines = ["graph TD"]

        entry_point_id = "ROOT_ENTRY"
        self.lines.append(f'    {entry_point_id}("🏁 Start")')

        # The graph can be empty if the blueprint has no logic
        if self.graph:
            self._weave_children(self.graph, entry_point_id)

        return "\n".join(self.lines)

    def _weave_node(self, node: LogicNode, parent_id: str, edge_label: str = ""):
        """
        The recursive hand of the Scribe. It weaves a single node and all its
        descendants into the Mermaid scripture.
        """
        label = self._forge_label(node)

        if node.id not in self.nodes_declared:
            shape_start, shape_end = self._get_shape(node)
            self.lines.append(f'    {node.id}{shape_start}"{label}"{shape_end}')
            self.nodes_declared.add(node.id)

        edge = f' -->|{edge_label}| {node.id}' if edge_label else f' --> {node.id}'
        self.lines.append(f'    {parent_id}{edge}')

        if node.node_type == LogicNodeType.CONDITION:
            if node.children:
                self._weave_children(node.children, node.id, "True")

            if node.else_branch:
                self._weave_node(node.else_branch, node.id, "False")
        else:
            self._weave_children(node.children, node.id)

    def _weave_children(self, children: List[LogicNode], parent_id: str, edge_label: str = ""):
        """A helper to weave a list of child nodes from a single parent."""
        current_parent = parent_id
        for i, child in enumerate(children):
            label = edge_label if i == 0 else ""
            self._weave_node(child, current_parent, label)
            current_parent = child.id

    def _forge_label(self, node: LogicNode) -> str:
        """Creates a concise, luminous label for a node."""
        if node.node_type == LogicNodeType.CONDITION:
            condition_text = node.condition.replace('"', "'")
            return f"{condition_text}"

        if node.node_type == LogicNodeType.LOOP:
            return f"for {node.loop_variable} in {node.iterable}"

        if node.node_type == LogicNodeType.SEQUENCE and node.items:
            count = len(node.items)
            item_type = "item" if count == 1 else "items"
            first_item = node.items[0].path.name if node.items[0] and node.items[0].path else "..."
            label = f"Forge {count} {item_type}\\n({first_item}...)"
            return label

        return "Sequence"

    def _get_shape(self, node: LogicNode) -> tuple[str, str]:
        """Returns the Mermaid shape syntax for a node type."""
        if node.node_type == LogicNodeType.CONDITION:
            return ("{", "}")  # Rhombus
        if node.node_type == LogicNodeType.LOOP:
            return ("([", "])")  # Stadium
        return ("[", "]")  # Rectangle