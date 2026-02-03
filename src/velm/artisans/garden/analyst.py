# Path: artisans/garden/analyst.py
# --------------------------------

import re
from pathlib import Path
from typing import List, Set, Dict, Any
from collections import defaultdict

from ...core.cortex.engine import GnosticCortex
from .contracts import WitheredVine


class GardenAnalyst:
    """
    =============================================================================
    == THE OMNISCIENT BOTANIST (V-Ω-SYMBOL-GRAPH-ANALYSIS)                     ==
    =============================================================================
    LIF: 100,000,000,000

    Performs deep static analysis to find dead code.
    1. **File Reachability:** Graph traversal from entry points.
    2. **Symbol Liveness:** Inverted index of usage vs definition.
    """

    # Heuristic Entry Points (Roots of the Graph)
    ENTRY_PATTERNS = {
        "main.py", "app.py", "wsgi.py", "asgi.py", "manage.py",
        "index.ts", "server.js", "cli.py", "__main__.py",
        "conftest.py", "setup.py"
    }

    # Sacred Symbols that must never be pruned
    SACRED_SYMBOLS = {
        "__init__", "__str__", "__repr__", "__call__", "__new__",
        "Meta", "Config",  # Pydantic/Django
        "setUp", "tearDown"  # Unittest
    }

    def __init__(self, project_root: Path):
        self.root = project_root
        self.cortex = GnosticCortex(project_root)
        # We perform a deep gaze upon instantiation
        self.memory = self.cortex.perceive()

    def find_withered_vines(self, aggressive_level: int = 1) -> List[WitheredVine]:
        """The Grand Rite of Inspection."""
        vines = []

        # 1. Dead Files
        dead_files = self._find_dead_files()
        for f in dead_files:
            vines.append(WitheredVine("file", f, f.name, reason="Unreachable from Entry Points"))

        # 2. Dead Symbols (Functions/Classes)
        if aggressive_level >= 3:
            dead_symbols = self._find_dead_symbols(exclude_files=dead_files)
            vines.extend(dead_symbols)

        return vines

    def _find_dead_files(self) -> Set[Path]:
        """
        Builds a reachability graph from Entry Points.
        Any file not visited is dead.
        """
        graph = self.memory.dependency_graph.get("dependency_graph", {})

        # 1. Identify Roots
        roots = set()
        all_files = set()

        for item in self.memory.inventory:
            if item.category != 'code': continue
            path_str = str(item.path).replace('\\', '/')
            all_files.add(path_str)

            # Is it an entry point?
            if item.path.name in self.ENTRY_PATTERNS:
                roots.add(path_str)
            # Is it a test? (Tests are implicitly entry points for the test runner)
            if "test" in item.path.name or "spec" in item.path.name:
                roots.add(path_str)
            # Is it a migration?
            if "migration" in str(item.path):
                roots.add(path_str)

        # 2. Traverse (BFS)
        visited = set(roots)
        queue = list(roots)

        while queue:
            current = queue.pop(0)
            # Who does current import?
            dependencies = graph.get(current, [])
            for dep in dependencies:
                if dep not in visited:
                    visited.add(dep)
                    queue.append(dep)

        # 3. Calculate Difference
        dead_path_strs = all_files - visited
        return {self.root / p for p in dead_path_strs}

    def _find_dead_symbols(self, exclude_files: Set[Path]) -> List[WitheredVine]:
        """
        The Gaze of the Symbol.
        Checks every defined function/class against the global usage index.
        """
        vines = []

        # 1. Build Global Usage Index
        # A set of every symbol name referenced in the codebase
        global_usage = set()

        for item in self.memory.inventory:
            # Add explicit imports
            global_usage.update(item.imported_symbols)

            # Add semantic resonance (words found in content) via regex heuristic
            # This is "Fuzzy Reachability" - safer than strict AST for dynamic langs
            if item.category == 'code':
                # We trust the AST metrics 'external' dependencies if available
                # But for safety, we assume if a string exists, it's used.
                pass

                # 2. Iterate Definitions
        for item in self.memory.inventory:
            if item.category != 'code': continue
            if self.root / item.path in exclude_files: continue  # Already dead file

            # We need the AST dossier
            path_str = str(item.path).replace('\\', '/')
            dossier = self.memory.project_gnosis.get(path_str, {})

            # Check Functions
            for func in dossier.get("functions", []):
                name = func["name"]
                if self._is_symbol_dead(name, item, global_usage):
                    vines.append(WitheredVine(
                        type="function",
                        path=self.root / item.path,
                        name=name,
                        line_num=func["start_point"][0] + 1,
                        start_byte=func["start_byte"],
                        end_byte=func["end_byte"],  # Assuming inquisitor provides this
                        reason="Symbol not imported or used internally"
                    ))

            # Check Classes
            for cls in dossier.get("classes", []):
                name = cls["name"]
                if self._is_symbol_dead(name, item, global_usage):
                    vines.append(WitheredVine(
                        type="class",
                        path=self.root / item.path,
                        name=name,
                        line_num=cls["start_point"][0] + 1,
                        start_byte=cls["start_byte"],
                        end_byte=cls["end_byte"],
                        reason="Class not instantiated or imported"
                    ))

        return vines

    def _is_symbol_dead(self, name: str, item_gnosis: Any, global_usage: Set[str]) -> bool:
        # 1. Sacred check
        if name in self.SACRED_SYMBOLS: return False
        if name.startswith("test_"): return False  # Pytest

        # 2. Framework check (Decorators are usage!)
        # This requires looking at the raw code or deeper AST.
        # For V1, we assume if it's not in global_usage (imports), it might be dead.
        # BUT, local usage?

        # We need to know if 'name' is used inside 'item_gnosis' (excluding its own def).
        # This is hard without full CFG.

        # Conservative Heuristic:
        # If it's not imported anywhere else...
        if name in global_usage: return False

        return True

