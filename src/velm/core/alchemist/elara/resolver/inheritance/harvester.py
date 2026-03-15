# Path: core/alchemist/elara/resolver/inheritance/harvester.py
# -----------------------------------------------------------

from typing import Dict, TYPE_CHECKING
from ...contracts.atoms import ASTNode, TokenType


class BlockHarvester:
    """
    =============================================================================
    == THE BLOCK HARVESTER (V-Ω-TOTALITY)                                      ==
    =============================================================================
    ROLE: SEMANTIC_SOUL_EXTRACTOR
    Recursively mines the child AST for block overrides.
    """

    @classmethod
    def harvest(cls, node: ASTNode) -> Dict[str, ASTNode]:
        """
        [ASCENSION 9]: Recursive Block Mining.
        Walks the tree to find all {% block name %} nodes.
        """
        blocks = {}
        for child in node.children:
            if child.token.type == TokenType.LOGIC_BLOCK:
                gate = child.metadata.get("gate")
                if gate == "block":
                    name = child.metadata.get("expression", "").strip()
                    blocks[name] = child

            # Recurse: Blocks can be nested inside if/for gates
            if child.children:
                blocks.update(cls.harvest(child))
        return blocks