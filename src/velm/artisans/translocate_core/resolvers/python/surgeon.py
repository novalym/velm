# Path: scaffold/artisans/translocate_core/resolvers/python/surgeon.py
# --------------------------------------------------------------------


import ast
from collections import defaultdict
from typing import List, Dict, Any, Tuple, Optional
from .contracts import HealingEdict
from .....logger import Scribe

Logger = Scribe("PythonSurgeon")


class GnosticImportTransformer(ast.NodeTransformer):
    """
    =================================================================================
    == THE GNOSTIC IMPORT TRANSFORMER (V-Ω-MULTI-VECTOR-SURGEON)                   ==
    =================================================================================
    LIF: 10,000,000,000

    A divine AST manipulator that performs surgical extractions and grafts on Python
    import statements. It is capable of splitting a single atomic import line into
    multiple distinct realities based on the Translocation Plan.
    """

    def __init__(self, plan: List[HealingEdict]):
        # Map: Line Number -> List[Edict]
        # We allow multiple mutations per line (e.g. splitting `from x import A, B`)
        self.plan_map: Dict[int, List[HealingEdict]] = defaultdict(list)
        for item in plan:
            self.plan_map[item.line_num].append(item)

        self.healed_count = 0

    def _parse_module_and_level(self, import_string: str) -> Tuple[Optional[str], int]:
        """
        Transmutes a raw import string (e.g. '..core.utils') into AST components.
        Returns (module_name, level).
        """
        if not import_string:
            return None, 0

        level = 0
        # Count leading dots for relative imports
        for char in import_string:
            if char == '.':
                level += 1
            else:
                break

        module_name = import_string[level:] if level < len(import_string) else None
        return module_name, level

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """
        The Rite of Separation.
        Splits a `from ... import ...` statement into kept and moved components,
        regrouping the moved components by their new destinations.
        """
        if node.lineno not in self.plan_map:
            return self.generic_visit(node)

        edicts = self.plan_map[node.lineno]

        # Map symbol name to its specific edict for O(1) lookup
        # If multiple edicts target the same symbol (rare redundancy), last wins.
        symbol_edict_map = {e.symbol_name: e for e in edicts}

        kept_aliases = []
        # Group moved aliases by their NEW destination string to consolidate imports
        # Dict[new_module_path_str, List[ast.alias]]
        moves_by_destination: Dict[str, List[ast.alias]] = defaultdict(list)

        for alias in node.names:
            if alias.name in symbol_edict_map:
                # This symbol is destined for a new reality
                edict = symbol_edict_map[alias.name]
                moves_by_destination[edict.new_module_path].append(alias)
                # self.healed_count += 1 (Counted later per group or per symbol? Per symbol is accurate)
                self.healed_count += 1
                Logger.verbose(f"   -> Surgically removing '{alias.name}' from L{node.lineno}")
            else:
                # This symbol remains in the old reality
                kept_aliases.append(alias)

        new_nodes = []

        # 1. Forge the nodes for the Moved Souls
        for new_path, aliases in moves_by_destination.items():
            module_name, level = self._parse_module_and_level(new_path)

            new_import_node = ast.ImportFrom(
                module=module_name,
                names=aliases,
                level=level
            )
            # We copy location to preserve comments/formatting affinity as much as possible,
            # though ast.unparse will generate fresh code.
            ast.copy_location(new_import_node, node)
            new_nodes.append(new_import_node)
            Logger.verbose(f"   -> Grafted new import to '{new_path}' for {len(aliases)} symbol(s).")

        # 2. Forge the node for the Remaining Souls (if any)
        if kept_aliases:
            old_node = ast.ImportFrom(
                module=node.module,
                names=kept_aliases,
                level=node.level
            )
            ast.copy_location(old_node, node)
            # We place the original (reduced) import FIRST to minimize diff noise
            new_nodes.insert(0, old_node)

        # If we emptied the import entirely and created no new ones (deletion?), return None (remove node).
        # But here we moved symbols, so we return the list of new nodes.
        if not new_nodes:
            return None

            # If it's a single node, return it directly. If multiple, return the list (AST supports this for statements).
        return new_nodes if len(new_nodes) > 1 else new_nodes[0]

    def visit_Import(self, node: ast.Import) -> Any:
        """
        The Rite of Renaming.
        Handles `import x, y`.
        """
        if node.lineno not in self.plan_map:
            return self.generic_visit(node)

        edicts = self.plan_map[node.lineno]
        symbol_edict_map = {e.symbol_name: e for e in edicts}

        new_aliases = []

        for alias in node.names:
            if alias.name in symbol_edict_map:
                edict = symbol_edict_map[alias.name]
                # We replace the name with the new module path
                # Note: `import x.y.z` -> alias.name is "x.y.z"
                # Edict contains the FULL new path.

                # Logic: If we rename `import A` to `import B`, we lose `A` in the namespace.
                # To be safe, if there was no 'asname', we might need to add one to preserve code references?
                # BUT, the Resolver's 'pathfinder' usually maps files.
                # If `src/utils.py` moves to `src/core/utils.py`, `import src.utils` becomes `import src.core.utils`.
                # Code using `src.utils.foo()` will break unless we alias `import src.core.utils as utils`?
                # Or we assume the user will fix usages.
                # For this Surgeon, we follow the Edict strictly.

                new_aliases.append(ast.alias(name=edict.new_module_path, asname=alias.asname))
                self.healed_count += 1
            else:
                new_aliases.append(alias)

        if not new_aliases:
            return None

        new_node = ast.Import(names=new_aliases)
        ast.copy_location(new_node, node)
        return new_node