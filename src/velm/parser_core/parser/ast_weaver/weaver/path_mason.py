# Path: parser_core/parser/ast_weaver/weaver/path_mason.py
# ----------------------------------------------------------

from pathlib import Path
from ..node_factory import NodeFactory
from ..stack_manager import StackManager
from .....contracts.data_contracts import _GnosticNode, ScaffoldItem


class PathMason:
    """
    =============================================================================
    == THE PATH MASON (V-Ω-POLYGLOT-NODE-ARCHITECT)                            ==
    =============================================================================
    Handles the iterative construction of intermediate AST nodes for deep paths.
    (e.g., transmuting `src/api/v1/main.py` into 4 distinct nested nodes).
    """

    def __init__(self, factory: NodeFactory):
        self.factory = factory

    def weave_form_item(
            self,
            item: ScaffoldItem,
            parent_node: _GnosticNode,
            parent_phys_path: Path,
            stack_mgr: StackManager
    ):
        """
        [ASCENSION 3 & 4]: The Deep Path Weaver & Atomic Node Forging.
        Handles deep paths (a/b/c) by creating intermediate structural nodes.
        """
        if not item.path:
            return

        rel_path = item.path

        # [ASCENSION 11]: The Phantom Path Exorcist
        if str(parent_phys_path) != ".":
            try:
                rel_path = item.path.relative_to(parent_phys_path)
            except ValueError:
                pass

        # [ASCENSION 13]: Substrate-Aware Normalization
        path_str = str(rel_path).replace('\\', '/')
        path_atoms = [p for p in path_str.split('/') if p and p != '.']

        current_node = parent_node

        for i_atom, atom in enumerate(path_atoms):
            is_last = (i_atom == len(path_atoms) - 1)

            # [ASCENSION 6]: O(1) Child Resolution (Linear scan optimized)
            child = next((c for c in current_node.children if c.name == atom), None)

            if not child:
                child_item = item if is_last else None
                is_dir_node = (not is_last) or (is_last and item.is_dir)

                child = self.factory.forge_form_node(atom, is_dir_node, child_item)
                current_node.children.append(child)

            current_node = child

        # [ASCENSION 20]: Temporal Order Suture (Push only if it's a structural boundary)
        if item.is_dir:
            stack_mgr.push(current_node, item.original_indent, item.path)