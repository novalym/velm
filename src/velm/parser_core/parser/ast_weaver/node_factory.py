from pathlib import Path
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType


class NodeFactory:
    """
    =============================================================================
    == THE NODE FORGE (V-Ω-FACTORY)                                            ==
    =============================================================================
    A pure artisan dedicated to forging Gnostic Nodes from raw Scaffold Items.
    """

    @staticmethod
    def forge_root() -> _GnosticNode:
        return _GnosticNode(name="__ROOT__", is_dir=True)

    @staticmethod
    def forge_logic_node(item: ScaffoldItem) -> _GnosticNode:
        """Forges a node representing a logic gate or Jinja construct."""
        # Determine the True Name of the logic block
        if item.path:
            name = str(item.path)
        elif item.sgf_expression:
            name = item.sgf_expression
        else:
            name = f"@{item.condition_type}"

        return _GnosticNode(name=name, is_dir=False, item=item)

    @staticmethod
    def forge_form_node(name: str, is_dir: bool, item: ScaffoldItem = None) -> _GnosticNode:
        """
        [ASCENSION 1]: GHOST-NODE ANCHORING.
        Ensures implicit directories like 'nova' are not prefixed with metadata tags.
        """
        return _GnosticNode(name=name, is_dir=is_dir, item=item)