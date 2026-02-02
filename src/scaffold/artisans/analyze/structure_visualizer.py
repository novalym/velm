# Path: artisans/analyze/structure_visualizer.py
# ----------------------------------------------

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.symphony_contracts import Edict, EdictType

Logger = logging.getLogger("StructureVisualizer")


class StructureVisualizer:
    """
    =============================================================================
    == THE STRUCTURE VISUALIZER (V-Ω-HOLOGRAPHIC-LATTICE-ULTIMA)               ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: TOPOLOGY_ARCHITECT | RANK: SOVEREIGN

    Transmutes flat Gnostic Atoms into a deeply nested, hierarchically correct
    Holographic Tree for the Ocular UI.

    [CAPABILITIES]:
    1. **Indentation Reconstruction:** Rebuilds parent-child bonds from whitespace.
    2. **Path Polymerization:** Fuses relative names into absolute IDs.
    3. **Hybrid Topology:** Handles both nested blocks and inline path definitions.
    """

    def __init__(self, grammar: str):
        self.grammar = grammar

    def visualize(self, items: List[ScaffoldItem], edicts: List[Edict], content: str = "") -> List[Dict[str, Any]]:
        """
        The Grand Rite of Visualization.
        Dispatches to the specific geometer based on the grammar.
        """
        if self.grammar == "symphony":
            return self._visualize_symphony(edicts)

        return self._visualize_scaffold(items, content)

    def _visualize_scaffold(self, items: List[ScaffoldItem], content: str) -> List[Dict[str, Any]]:
        """
        [THE SCAFFOLD GEOMETER]
        Reconstructs the file tree using a Stack Machine that respects indentation.
        """
        # 1. CALCULATE GEOMETRY (INDENTATION MAP)
        lines = content.splitlines()

        def get_indent(line_num: int) -> int:
            if 0 < line_num <= len(lines):
                line = lines[line_num - 1]
                # We measure raw leading whitespace.
                # 1 tab or 4 spaces = 1 Level, but relative difference is what matters.
                return len(line) - len(line.lstrip())
            return 0

        # 2. TRANSMUTE ATOMS TO NODES
        nodes: List[Dict[str, Any]] = []

        for item in items:
            # [ASCENSION 1]: FILTER NOISE
            # We skip variable definitions ($$) in the tree view to reduce clutter,
            # unless they are structural (which they aren't usually).
            if str(item.path).startswith('$$'): continue

            clean_path = str(item.path).replace('\\', '/').rstrip('/')
            if not clean_path: continue

            # Determine Nature
            is_logic = item.line_type == GnosticLineType.LOGIC
            is_dir = item.is_dir or is_logic

            # [ASCENSION 8]: KIND DIVINATION
            # 19=Folder, 1=File, 5=Class (Logic), 2=Module
            kind = 19 if is_dir else 1
            if is_logic: kind = 5

            indent = get_indent(item.line_num)

            node = {
                "id": clean_path,  # Initial ID (Relative to block)
                "name": os.path.basename(clean_path),
                "path": clean_path,  # Source of Truth
                "is_dir": is_dir,
                "kind": kind,
                "line": item.line_num,
                "indent": indent,  # Spatial Coordinate
                "detail": "Logic" if is_logic else ("Sanctum" if is_dir else "Scripture"),
                "has_content": bool(item.content or item.seed_path),
                "children": []
            }
            nodes.append(node)

        # 3. TOPOLOGICAL RECONSTRUCTION (STACK MACHINE)
        # We process nodes in linear order. The stack tracks the current open parents.

        root_nodes = []
        stack: List[Dict[str, Any]] = []

        for node in nodes:
            current_indent = node['indent']

            # [ASCENSION 11]: STACK UNWIND
            # Pop items from the stack until we find a parent with strictly LESS indentation.
            # This closes sibling blocks and returns to the parent scope.
            while stack and stack[-1]['indent'] >= current_indent:
                stack.pop()

            if stack:
                # We have a parent!
                parent = stack[-1]

                # [ASCENSION 2]: PATH POLYMERIZATION
                # We must update the child's ID to include the parent's path prefix.
                # BUT we must check if it's already included (explicit full path vs relative).

                # e.g. Parent "src/", Child "main.py" -> "src/main.py"
                # e.g. Parent "src/", Child "src/main.py" -> "src/main.py" (No change)

                parent_prefix = parent['path']
                # Strip trailing slash for joining
                if parent_prefix.endswith('/'): parent_prefix = parent_prefix[:-1]

                if not node['path'].startswith(parent_prefix + '/'):
                    # It's relative. Polymerize.
                    node['path'] = f"{parent_prefix}/{node['name']}"
                    node['id'] = node['path']  # Update ID

                parent['children'].append(node)

                # [ASCENSION 4]: CONTAINER FORCE
                # If a node accepts children, it becomes a container visually.
                if not parent['is_dir']:
                    parent['is_dir'] = True
                    parent['kind'] = 19
                    parent['detail'] = "Sanctum (Implicit)"

            else:
                # No parent in stack -> Root Node
                root_nodes.append(node)

            # [ASCENSION 3]: HYBRID TOPOLOGY
            # If this node is a directory (or logic block), push it to stack
            # so subsequent indented items become its children.
            if node['is_dir']:
                stack.append(node)

        # 4. GHOST FOLDER RESOLUTION (Post-Process)
        # Some paths might be "a/b/c.py" at root level. We need to create "a/" and "b/".
        # This handles explicit full paths that weren't indented.
        final_roots = self._resolve_ghosts(root_nodes)

        # 5. GEOMETRIC SORTING
        return self._sort_tree(final_roots)

    def _resolve_ghosts(self, roots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        [ASCENSION 5]: THE GHOST FORGE
        Iterates root nodes. If a node is `a/b/c`, it ensures `a` and `b` exist as parents.
        """
        node_map = {n['path']: n for n in roots}  # Only map current roots
        new_roots = []

        # We need a robust map of ALL nodes created to link them
        # Actually, reconstructing the whole tree from paths is safer for the "Flat" items.
        # But we want to preserve the indentation hierarchy we just built.
        # So we only apply this logic to the top-level roots of the indentation tree.

        # Strategy:
        # 1. Take all current roots.
        # 2. For each root, check if it needs a ghost parent.
        # 3. If so, create/find ghost parent, link, and remove from roots list (it's now a child).

        # We iterate a copy because we might move nodes.
        processing_list = list(roots)
        path_map: Dict[str, Dict[str, Any]] = {n['path']: n for n in processing_list}  # Map of known roots

        for node in processing_list:
            path = node['path']
            if '/' in path:
                parent_path = os.path.dirname(path)

                # Recursive ascent to find or create parents
                current_child = node
                current_parent_path = parent_path

                while current_parent_path:
                    # Do we have this parent?
                    parent_node = path_map.get(current_parent_path)

                    if not parent_node:
                        # Forge Ghost
                        parent_node = {
                            "id": current_parent_path,
                            "name": os.path.basename(current_parent_path),
                            "path": current_parent_path,
                            "is_dir": True,
                            "kind": 19,
                            "line": 0,  # Virtual
                            "detail": "Sanctum (Implicit)",
                            "children": []
                        }
                        path_map[current_parent_path] = parent_node
                        # It's a new root for now
                        new_roots.append(parent_node)

                        # Link Child to Parent
                    if current_child not in parent_node['children']:
                        parent_node['children'].append(current_child)

                    # Determine next step up
                    if '/' in current_parent_path:
                        current_child = parent_node
                        current_parent_path = os.path.dirname(current_parent_path)
                    else:
                        break

        # Filter out nodes that are now children
        # Any node that is in someone else's children list is no longer a root.
        all_children = set()
        for p in path_map.values():
            for c in p['children']:
                all_children.add(c['path'])

        final_roots = [n for n in path_map.values() if n['path'] not in all_children]
        return final_roots

    def _sort_tree(self, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        [ASCENSION 6]: THE LAW OF ORDER
        Sorts nodes: Folders first, then Files. Alphabetical within groups.
        Recursively sorts children.
        """

        def sort_key(n):
            # Sort by: (Not Directory, Name)
            # This puts Directories (False) before Files (True)
            return (not n['is_dir'], n['name'].lower())

        sorted_nodes = sorted(nodes, key=sort_key)

        for node in sorted_nodes:
            # Clean up internal metadata before sending to UI
            if 'indent' in node: del node['indent']

            if node['children']:
                node['children'] = self._sort_tree(node['children'])

        return sorted_nodes

    def _visualize_symphony(self, edicts: List[Edict]) -> List[Dict[str, Any]]:
        """
        [ASCENSION 7]: SYMPHONY DECODER
        Flattens Symphony edicts into a visual list (Symphonies are usually linear).
        """
        tree_nodes = []
        for edict in edicts:
            label = self._forge_label(edict)
            type_tag = self._determine_type(edict)

            node = {
                "id": f"line_{edict.line_num}",
                "name": label,
                "path": f"line_{edict.line_num}",  # Virtual path
                "is_dir": bool(edict.body or edict.parallel_edicts),
                "line": edict.line_num,
                "kind": 12,  # Function/Method like
                "detail": type_tag.upper(),
                "children": []  # Nested blocks could go here in V2
            }
            tree_nodes.append(node)
        return tree_nodes

    def _forge_label(self, edict: Edict) -> str:
        cmd = edict.command or edict.vow_type or "..."
        if len(cmd) > 30: cmd = cmd[:27] + "..."

        if edict.type == EdictType.ACTION: return f"🚀 {cmd}"
        if edict.type == EdictType.VOW: return f"⚖️ {cmd} {', '.join(edict.vow_args)}"
        if edict.type == EdictType.STATE: return f"💾 {edict.state_key}: {edict.state_value}"
        if edict.type == EdictType.CONDITIONAL: return f"🔀 @{edict.conditional_type.name}"
        if edict.type == EdictType.POLYGLOT_ACTION: return f"🔮 {edict.language}"
        if edict.type == EdictType.DIRECTIVE: return f"✨ @{edict.directive_type}"
        return f"📄 {cmd}"

    def _determine_type(self, edict: Edict) -> str:
        if edict.type == EdictType.ACTION: return "action"
        if edict.type == EdictType.VOW: return "vow"
        if edict.type == EdictType.STATE: return "state"
        if edict.type == EdictType.CONDITIONAL: return "logic"
        return "info"