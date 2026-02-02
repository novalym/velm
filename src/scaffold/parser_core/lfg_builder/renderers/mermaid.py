# Path: parser_core/lfg_builder/renderers/mermaid.py
# --------------------------------------------------

from ..contracts import LogicFlowGraph, NodeShape


class MermaidRenderer:
    """
    Transmutes the Gnostic Graph into Mermaid JS syntax.
    """

    SHAPE_MAP = {
        NodeShape.RECTANGLE: ('[', ']'),
        NodeShape.ROUND_RECT: ('(', ')'),
        NodeShape.DIAMOND: ('{', '}'),
        NodeShape.CYLINDER: ('[(', ')]'),
        NodeShape.PARALLELOGRAM: ('[/', '/]'),
        NodeShape.SUBROUTINE: ('[[', ']]')
    }

    @classmethod
    def render(cls, graph: LogicFlowGraph, orientation="TD") -> str:
        lines = [f"graph {orientation}"]

        # Render Nodes
        for node in graph.nodes:
            open_s, close_s = cls.SHAPE_MAP.get(node.shape, ('[', ']'))
            # Sanitize label
            safe_label = node.label.replace('"', "'")
            lines.append(f'    {node.id}{open_s}"{safe_label}"{close_s}')

        # Render Edges
        for edge in graph.edges:
            arrow = "-->"
            if edge.style == "dotted":
                arrow = "-.->"
            elif edge.style == "thick":
                arrow = "==>"

            label_part = f"|{edge.label}|" if edge.label else ""
            lines.append(f'    {edge.source_id} {arrow}{label_part} {edge.target_id}')

        # Recursion for Subgraphs (Future Ascension)
        for sub in graph.subgraphs:
            lines.append(f"\n    subgraph {sub.title}")
            sub_content = cls.render(sub, orientation).split("\n")[1:]  # Skip header
            lines.extend(sub_content)
            lines.append("    end")

        return "\n".join(lines)