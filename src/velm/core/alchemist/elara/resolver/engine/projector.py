# Path: core/alchemist/elara/resolver/engine/projector.py
# -------------------------------------------------------

from ...contracts.atoms import ASTNode, TokenType


class MermaidAstProjector:
    """
    =============================================================================
    == THE AST PROJECTOR (V-Ω-TOTALITY-VMAX)                                   ==
    =============================================================================[ASCENSION 125 & 130]: VISUAL LOGIC FLOW PROJECTION.
    Transmutes the live AST directly into a Mermaid.js flowchart.
    """

    @classmethod
    def project(cls, root_node: ASTNode, title: str = "Logic Flow") -> str:
        lines = [f"graph TD", f"  %% {title}"]

        def _walk(node: ASTNode, parent_id: str):
            for i, child in enumerate(node.children):
                child_id = f"node_{id(child)}"

                if child.token.type == TokenType.LOGIC_BLOCK:
                    gate = child.metadata.get("gate", "UNKNOWN").upper()
                    expr = child.metadata.get("expression", "")
                    clean_expr = expr.replace('"', "'")[:30]

                    if gate in ("IF", "ELIF"):
                        lines.append(f"  {child_id}{{{{{gate}: {clean_expr}}}}}")
                    elif gate == "FOR":
                        lines.append(f"  {child_id}[/{gate}: {clean_expr}\\]")
                    elif gate in ("MACRO", "CALL", "SLOT"):
                        lines.append(f"  {child_id}(([{gate}: {clean_expr}]]))")
                    else:
                        lines.append(f"  {child_id}({gate})")

                    lines.append(f"  {parent_id} --> {child_id}")
                    _walk(child, child_id)

                elif child.token.type == TokenType.VARIABLE:
                    clean_var = child.token.content.replace('"', "'")[:20]
                    lines.append(f"  {child_id}(($$ {clean_var} ))")
                    lines.append(f"  {parent_id} -.-> {child_id}")

        root_id = "ROOT"
        lines.append(f"  {root_id}((AST_ROOT))")
        _walk(root_node, root_id)

        return "\n".join(lines)
