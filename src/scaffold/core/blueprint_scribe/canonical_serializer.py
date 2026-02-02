# Path: scaffold/core/blueprint_scribe/canonical_serializer.py
# ------------------------------------------------------------

import re
from typing import Iterator, List, Tuple

from ...contracts.data_contracts import _GnosticNode, ScaffoldItem
from ...core.alchemist import get_alchemist
from .sorting_hat import SortingHat
from .content_renderer import ContentRenderer


class CanonicalSerializer:
    """
    =================================================================================
    == THE CELESTIAL SCRIBE (V-Ω-LIF-10B. AESTHETIC-ALIGNMENT-ULTIMA)               ==
    =================================================================================
    LIF: 10,000,000,000

    This is the final apotheosis of the Scribe. It is a Gnostic AI that writes
    scriptures not just with correctness, but with profound beauty, intelligence,
    and foresight. Its Gaze is two-fold, its hand guided by the Law of Luminous
    Alignment. It is the pinnacle of the Scribe's art.
    """

    def __init__(self):
        self.sorter = SortingHat()
        self.renderer = ContentRenderer()
        # [FACULTY 5] The Path Alchemist
        self.alchemist = get_alchemist()

    def serialize(self, root: _GnosticNode) -> Iterator[str]:
        """The Grand Rite of Serialization."""
        children = self.sorter.sort(root.children)

        # [FACULTY 7] The Hoisting Architect
        if len(children) == 1 and children[0].is_dir:
            hoisted_root = children[0]
            # Serialize the grandchildren at indent 0
            yield from self._serialize_node_group(hoisted_root.children, 0)
        else:
            yield from self._serialize_node_group(children, 0)

    def _serialize_node_group(self, nodes: List[_GnosticNode], indent_level: int) -> Iterator[str]:
        """
        [FACULTY 2] The Altar of Alignment.
        Performs a two-pass Gaze to align all sigils in the current block.
        """
        if not nodes:
            return

        # --- PASS 1: The Gaze of Measurement ---
        # We perceive the geometry of the reality to be inscribed.
        max_path_len = 0
        node_render_data: List[Tuple[_GnosticNode, str]] = []
        for node in nodes:
            path_str = self._forge_path_string(node)
            max_path_len = max(max_path_len, len(path_str))
            node_render_data.append((node, path_str))

        # --- PASS 2: The Rite of Luminous Inscription ---
        # We now proclaim each scripture, its soul perfectly aligned.
        for node, path_str in node_render_data:
            padding = " " * (max_path_len - len(path_str))
            yield from self._serialize_recursive(node, indent_level, path_str, padding)

    def _forge_path_string(self, node: _GnosticNode) -> str:
        """
        [FACULTY 5] The Path Alchemist's Hand.
        Forges the path string, reverse-engineering variables where possible.
        """
        path_str = node.name
        if node.is_dir:
            path_str += "/"

        # This is a humble reverse-gaze. A future ascension could be more intelligent.
        # It looks for exact value matches in the known variables.
        # We sort by value length to replace longer matches first (e.g., 'my-app-api' before 'my-app')
        sorted_vars = sorted(self.alchemist.env.globals.items(), key=lambda item: len(str(item[1])), reverse=True)

        for key, value in sorted_vars:
            if isinstance(value, str) and value and value in path_str:
                path_str = path_str.replace(value, f"{{{{ {key} }}}}")

        return path_str

    def _serialize_recursive(self, node: _GnosticNode, indent_level: int, path_str: str, padding: str) -> Iterator[str]:
        """
        The Stream of Consciousness, now a Master Scribe.
        """
        indent = "    " * indent_level

        # Render the Soul (Content/Seed/Permissions)
        soul_suffix = ""
        block_body = []

        if node.item:
            # [FACULTY 4] The Scribe of Sentient Comments
            # We look for description comments to prepend to the node.
            if node.item.content and node.item.line_type == "COMMENT" and "@description" in node.item.content:
                yield f"{indent}{node.item.content}"

            soul_suffix, block_body = self.renderer.render(node.item, indent_level)

        # Yield the main line
        line = f"{indent}{path_str}"

        if soul_suffix:
            if soul_suffix.startswith(":") and not soul_suffix.startswith("::"):
                line += soul_suffix
            else:
                # Apply the sacred padding for alignment
                line += padding
                line += f"  {soul_suffix}"

        yield line

        # Yield any block content
        for block_line in block_body:
            yield block_line

        # Recurse into children, passing control to the alignment group
        if node.children:
            yield from self._serialize_node_group(self.sorter.sort(node.children), indent_level + 1)