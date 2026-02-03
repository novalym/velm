# Path: core/cortex/call_graph.py
# -------------------------------

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

from ...inquisitor import get_treesitter_gnosis
from ...logger import Scribe

Logger = Scribe("CallGraphAnalyzer")


class CallNode:
    """A Node in the Holocron."""

    def __init__(self, file_path: str, symbol_name: str, symbol_type: str, code_range: Tuple[int, int]):
        self.id = f"{file_path}::{symbol_name}"
        self.file_path = file_path
        self.symbol_name = symbol_name
        self.symbol_type = symbol_type  # 'function', 'class', 'method'
        self.range = code_range  # (start_line, end_line)
        self.calls: Set[str] = set()  # IDs of nodes this node calls


class CallGraphAnalyzer:
    """
    =============================================================================
    == THE WEAVER OF THREADS (V-Ω-SYMBOLIC-TRACER)                             ==
    =============================================================================
    LIF: 100,000,000,000

    Constructs a detailed Call Graph by analyzing ASTs.
    Unlike the Dependency Graph (File -> File), this maps Symbol -> Symbol.
    """

    def __init__(self, project_root: Path, inventory: List[Any]):
        self.root = project_root
        self.nodes: Dict[str, CallNode] = {}
        self.inventory = inventory
        self.symbol_table: Dict[str, str] = {}  # symbol_name -> node_id (Simple lookup)

    def build(self):
        """The Rite of Mapping."""
        Logger.info("Building the Holocron Call Graph...")

        # Pass 1: Index all definitions
        for item in self.inventory:
            if item.category != 'code': continue
            self._index_file(item.path)

        # Pass 2: Link calls
        for item in self.inventory:
            if item.category != 'code': continue
            self._link_calls(item.path)

        Logger.success(f"Holocron constructed. {len(self.nodes)} symbols mapped.")

    def _index_file(self, path: Path):
        """Extracts definitions."""
        try:
            abs_path = self.root / path
            content = abs_path.read_text(encoding='utf-8')
            gnosis = get_treesitter_gnosis(abs_path, content)

            if "error" in gnosis: return

            rel_path = str(path)

            # Index Functions
            for func in gnosis.get("functions", []):
                name = func["name"]
                start = func["start_point"][0] + 1
                end = start + func["line_count"]
                node = CallNode(rel_path, name, "function", (start, end))
                self.nodes[node.id] = node
                self.symbol_table[name] = node.id  # Ambiguity handled by last-win (Basic) or FQN in V2

            # Index Classes
            for cls in gnosis.get("classes", []):
                name = cls["name"]
                start = cls["start_point"][0] + 1
                end = start + cls["line_count"]  # Approximation
                node = CallNode(rel_path, name, "class", (start, end))
                self.nodes[node.id] = node
                self.symbol_table[name] = node.id

        except Exception as e:
            Logger.warn(f"Failed to index {path}: {e}")

    def _link_calls(self, path: Path):
        """Finds calls within files and links them to definitions."""
        try:
            abs_path = self.root / path
            content = abs_path.read_text(encoding='utf-8')
            gnosis = get_treesitter_gnosis(abs_path, content)

            rel_path = str(path)

            # Analyze each function body to see what it calls
            for func in gnosis.get("functions", []):
                caller_id = f"{rel_path}::{func['name']}"
                if caller_id not in self.nodes: continue

                # Retrieve dependencies (calls) from the AST metrics
                # Assuming 'dependencies.external' contains called function names
                calls = func.get("dependencies", {}).get("external", [])

                for callee_name in calls:
                    # Resolve callee
                    if callee_name in self.symbol_table:
                        callee_id = self.symbol_table[callee_name]
                        self.nodes[caller_id].calls.add(callee_id)

        except Exception:
            pass

    def trace_causality(self, entry_symbol: str, depth: int = 5) -> List[CallNode]:
        """
        [THE HOLOCRON TRACE]
        Returns the specific list of Nodes required to execute the entry symbol.
        """
        # Resolve entry
        start_node_id = None

        # Try exact ID match
        if entry_symbol in self.nodes:
            start_node_id = entry_symbol
        # Try symbol name lookup
        elif entry_symbol in self.symbol_table:
            start_node_id = self.symbol_table[entry_symbol]
        # Try fuzzy file match
        else:
            for nid in self.nodes:
                if entry_symbol in nid:
                    start_node_id = nid
                    break

        if not start_node_id:
            return []

        # BFS Traversal
        visited = set()
        queue = [(start_node_id, 0)]
        trace_result = []

        while queue:
            current_id, current_depth = queue.pop(0)
            if current_id in visited or current_depth > depth:
                continue

            visited.add(current_id)
            node = self.nodes[current_id]
            trace_result.append(node)

            for child_id in node.calls:
                queue.append((child_id, current_depth + 1))

        return trace_result