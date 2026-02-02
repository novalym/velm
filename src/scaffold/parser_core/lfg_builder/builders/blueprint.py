# Path: parser_core/lfg_builder/builders/blueprint.py
# ---------------------------------------------------

from typing import List
from ...lexer_core.contracts import GnosticLineType
from ...contracts.data_contracts import ScaffoldItem
from ..contracts import LogicFlowGraph, NodeShape


class BlueprintLFGBuilder:
    """
    Analyzes Scaffold/Symphony parsed items to build a control flow graph.
    Handles @if, @for, and sequential execution.
    """

    def build(self, items: List[ScaffoldItem], title: str) -> LogicFlowGraph:
        graph = LogicFlowGraph(title=title)

        start_id = graph.add_node("start", "Start", NodeShape.ROUND_RECT)
        last_id = start_id

        # Stack for tracking parent contexts (for nesting)
        # (id, type)
        stack = []

        for i, item in enumerate(items):
            node_id = f"node_{i}"

            # 1. Logic Gates (@if)
            if "@if" in item.raw_scripture:
                label = item.raw_scripture.replace("@if", "").strip()
                graph.add_node(node_id, f"If {label}?", NodeShape.DIAMOND)
                graph.add_edge(last_id, node_id)

                stack.append((node_id, "IF"))
                last_id = node_id  # We step INTO the if block
                continue

            # 2. Logic Branches (@else/elif)
            if "@else" in item.raw_scripture or "@elif" in item.raw_scripture:
                # Close the 'True' path of the previous block visually?
                # Complex flow. For simplicity in V1:
                # We connect the PARENT of the IF to this node (Parallel path)
                if stack:
                    parent_if_id, _ = stack[-1]
                    label = "Else"
                    graph.add_node(node_id, label, NodeShape.DIAMOND)
                    graph.add_edge(parent_if_id, node_id, label="False")
                    last_id = node_id
                continue

            # 3. Loops (@for)
            if "@for" in item.raw_scripture:
                label = item.raw_scripture.replace("@for", "").strip()
                graph.add_node(node_id, f"Loop {label}", NodeShape.PARALLELOGRAM)
                graph.add_edge(last_id, node_id)
                stack.append((node_id, "FOR"))
                last_id = node_id
                continue

            # 4. Closers (@endif, @endfor)
            if "@end" in item.raw_scripture:
                if stack:
                    # We 'close' the loop/if visually by converging?
                    # For now, we just pop the stack.
                    # Ideally we create a convergence node.
                    converge_id = f"end_block_{i}"
                    graph.add_node(converge_id, "Merge", NodeShape.ROUND_RECT)
                    graph.add_edge(last_id, converge_id)
                    stack.pop()
                    last_id = converge_id
                continue

            # 5. Standard Items (Files/Commands)
            label = item.path.name if item.path else (item.raw_scripture[:30] + "...")
            shape = NodeShape.RECTANGLE
            if item.is_dir: shape = NodeShape.CYLINDER
            if ">>" in item.raw_scripture: shape = NodeShape.SUBROUTINE

            graph.add_node(node_id, label, shape)

            # Connect
            # If we are inside an IF block, the edge label might be 'True' if it's the first child
            edge_label = None
            if stack and last_id == stack[-1][0]:
                edge_label = "True/Inside"

            graph.add_edge(last_id, node_id, edge_label)
            last_id = node_id

        end_id = graph.add_node("end", "End", NodeShape.ROUND_RECT)
        graph.add_edge(last_id, end_id)

        return graph