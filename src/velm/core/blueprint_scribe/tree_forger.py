# Path: scaffold/core/blueprint_scribe/tree_forger.py
# ---------------------------------------------------
import re
from typing import List
from ...contracts.data_contracts import ScaffoldItem, _GnosticNode


class TreeForger:
    """
    =================================================================================
    == THE STRUCTURAL ARCHITECT (V-Ω-TREE-BUILDER)                                 ==
    =================================================================================
    Responsible for transmuting a flat list of items into a hierarchical Gnostic Tree.
    """

    def forge(self, items: List[ScaffoldItem]) -> _GnosticNode:
        """
        [EVOLUTION 10] The Path Normalizer: Enforces hierarchy logic.
        """
        root = _GnosticNode(name="__ROOT__", is_dir=True)

        for item in items:
            current_node = root
            # Normalize path separators
            path_parts = item.path.as_posix().strip('/').split('/')

            for i, part in enumerate(path_parts):
                if not part: continue

                # Clean artifacts from visual tree representations if present
                clean_part = re.sub(r'[│├──└──`\s]', '', part).strip()
                if not clean_part: continue

                child_node = current_node.find_child(clean_part)

                if not child_node:
                    # Is this the leaf node?
                    is_leaf_of_path = (i == len(path_parts) - 1)

                    # It is a directory if it's an intermediate node OR if the item itself is a dir
                    is_dir = (not is_leaf_of_path) or item.is_dir

                    new_node = _GnosticNode(name=clean_part, is_dir=is_dir)
                    current_node.children.append(new_node)
                    current_node = new_node
                else:
                    current_node = child_node

            # Attach the Soul (Item) to the final node
            current_node.item = item

        return root