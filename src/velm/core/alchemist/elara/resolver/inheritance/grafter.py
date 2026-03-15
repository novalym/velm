# Path: core/alchemist/elara/resolver/inheritance/grafter.py
# ----------------------------------------------------------


from typing import List, Dict, Any, TYPE_CHECKING
from ...contracts.atoms import ASTNode, TokenType


class TreeGrafter:
    """
    =============================================================================
    == THE TREE GRAFTER (V-Ω-TOTALITY-VMAX-JINJA-INHERITANCE)                  ==
    =============================================================================
    ROLE: TOPOLOGICAL_SUTURE_CONDUCTOR
    The engine of substitution. Replaces parent placeholders with child matter.

    [ASCENSION]: Fully handles `{{ super() }}` integration by attaching parent
    nodes to the child block's metadata prior to AST walking.
    """

    @classmethod
    def suture(cls, parent_node: ASTNode, child_blocks: Dict[str, ASTNode], scope: Any) -> ASTNode:
        """
        =========================================================================
        == THE RITE OF THE SURGICAL GRAFT                                      ==
        =========================================================================
        """
        new_children = []

        for p_child in parent_node.children:
            if p_child.token.type == TokenType.LOGIC_BLOCK and p_child.metadata.get("gate") == "block":
                block_name = p_child.metadata.get("expression", "").strip()

                if block_name in child_blocks:
                    # [GAP 5]: SUPER DISCONNECT CURE
                    # We take the child's replacement block, but we MUST inject the
                    # parent's original nodes into its metadata so that if the child
                    # invokes `{{ super() }}`, the Evaluator knows what the parent was.
                    c_block = child_blocks[block_name]
                    c_block.metadata["parent_block_nodes"] = p_child.children

                    # Child overrides Parent in the AST
                    new_children.append(c_block)
                else:
                    # No override from child: Keep parent default and recurse deeper
                    p_child.children = cls.suture(p_child, child_blocks, scope).children
                    new_children.append(p_child)
            else:
                # Non-block node: Preserve and recurse
                if p_child.children:
                    p_child.children = cls.suture(p_child, child_blocks, scope).children
                new_children.append(p_child)

        parent_node.children = new_children
        return parent_node