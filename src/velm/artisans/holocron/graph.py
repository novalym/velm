# Path: artisans/holocron/graph.py
# --------------------------------

import re
import math
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict

from ...inquisitor import get_treesitter_gnosis
from ...logger import Scribe

Logger = Scribe("HolocronGraph")


@dataclass
class CallNode:
    """[FACULTY 7] A single, sovereign point in the Holocron's cosmos."""
    id: str
    file_path: str
    symbol_name: str
    type: str
    range: Tuple[int, int]
    weight: float = 1.0
    calls: Set[str] = field(default_factory=set)
    called_by: Set[str] = field(default_factory=set)
    imports: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.id)


class CallGraphOracle:
    """
    =================================================================================
    == THE WEAVER OF THREADS (V-Ω-SYMBOLIC-TRACER-ULTIMA-APOTHEOSIS-HEALED)        ==
    =================================================================================
    @gnosis:title The Holocron's Mind (`CallGraphOracle`)
    @gnosis:summary The divine, self-healing, and hyper-aware God-Engine of Causal Analysis.
    @gnosis:LIF 100,000,000,000,000

    Constructs a detailed, bi-directional Call Graph by performing Deep AST Analysis.
    It has been ascended with the **Unbreakable Gaze of Gnosis**, allowing it to
    perceive both ancient and modern forms of dependency scriptures.
    """

    def __init__(self, root: Path):
        self.root = root
        self.nodes: Dict[str, CallNode] = {}
        self.symbol_table: Dict[str, List[str]] = defaultdict(list)
        self.file_map: Dict[str, List[str]] = defaultdict(list)

    def build_index(self, files: List[Path]):
        """[FACULTY 3 & 4] The Grand Rite of Mapping, now with caching prophecy."""
        Logger.info(f"Building Holocron Graph from {len(files)} scriptures...")
        start_time = time.monotonic()

        valid_files = []
        for path in files:
            try:
                # [FACULTY 2] The Polyglot Path Normalizer
                rel_path = str(path.relative_to(self.root)).replace('\\', '/')
                content = path.read_text(encoding='utf-8', errors='ignore')
                gnosis = get_treesitter_gnosis(path, content)

                if "error" in gnosis: continue

                self._index_definitions(rel_path, gnosis)
                valid_files.append((rel_path, gnosis))
            except Exception as e:
                # [FACULTY 6] The Unbreakable Ward of the Void
                Logger.warn(f"Failed to index '{path.name}': {e}")

        Logger.verbose(f"Indexed {len(self.nodes)} symbols. Commencing Linkage...")

        for rel_path, gnosis in valid_files:
            self._link_references(rel_path, gnosis)

        self._calculate_weights()
        duration = time.monotonic() - start_time
        # [FACULTY 5] The Luminous Telemetry
        Logger.success(f"Holocron constructed in {duration:.2f}s. {len(self.nodes)} nodes linked.")

    def _index_definitions(self, file_path: str, gnosis: Dict):
        """Pass 1: Create Nodes for every function and class."""
        for func in gnosis.get("functions", []):
            node_id = f"{file_path}::{func['name']}"
            n_type = "function"
            if func['name'] == "main" or func['name'].startswith("test_"):
                n_type = "entry_point"
            node = CallNode(
                id=node_id, file_path=file_path, symbol_name=func['name'], type=n_type,
                range=(func["start_point"][0] + 1, func["start_point"][0] + func["line_count"]),
                metadata={"doc": func.get("docstring", "")}
            )
            self.nodes[node_id] = node
            self.symbol_table[func['name']].append(node_id)
            self.file_map[file_path].append(node_id)

        for cls in gnosis.get("classes", []):
            node_id = f"{file_path}::{cls['name']}"
            node = CallNode(
                id=node_id, file_path=file_path, symbol_name=cls['name'], type="class",
                range=(cls["start_point"][0] + 1, cls["start_point"][0] + cls["line_count"])
            )
            self.nodes[node_id] = node
            self.symbol_table[cls['name']].append(node_id)
            self.file_map[file_path].append(node_id)

    def _link_references(self, file_path: str, gnosis: Dict):
        """Pass 2: Connect the dots. The heart of the healing."""
        local_scope = self._resolve_imports(gnosis, file_path)

        for func in gnosis.get("functions", []):
            caller_id = f"{file_path}::{func['name']}"
            caller_node = self.nodes.get(caller_id)
            if not caller_node: continue

            # ★★★ THE DIVINE HEALING: THE UNBREAKABLE GAZE OF GNOSIS (THE CORE FIX) ★★★
            # This is the sacred rite that heals the Gnostic Schism.
            # It gazes upon the dependency scripture, determines its form (ancient dict
            # or modern list), and righteously extracts its soul.
            dependencies_gnosis = func.get("dependencies", {})
            called_symbols = []
            if isinstance(dependencies_gnosis, dict):
                # The Ancient Tongue (Dictionary)
                called_symbols = dependencies_gnosis.get("external", [])
            elif isinstance(dependencies_gnosis, list):
                # The New, Pure Tongue (List)
                called_symbols = dependencies_gnosis
            # ★★★ THE APOTHEOSIS IS COMPLETE. THE GAZE IS UNBREAKABLE. ★★★

            for symbol in called_symbols:
                target_ids = []
                if symbol in local_scope:
                    target_ids = local_scope[symbol]
                elif symbol in self.symbol_table:
                    same_file_matches = [nid for nid in self.symbol_table[symbol] if nid.startswith(file_path)]
                    if same_file_matches:
                        target_ids = same_file_matches
                    elif len(self.symbol_table[symbol]) == 1:
                        target_ids = self.symbol_table[symbol]

                if caller_node.type == "entry_point" and caller_node.symbol_name.startswith("test_"):
                    target_name = caller_node.symbol_name.replace("test_", "")
                    if target_name in self.symbol_table:
                        target_ids.extend(self.symbol_table[target_name])

                for tid in set(target_ids):  # Use set to avoid duplicate linking
                    if tid == caller_id: continue
                    caller_node.calls.add(tid)
                    if tid in self.nodes:
                        self.nodes[tid].called_by.add(caller_id)

    def _resolve_imports(self, gnosis: Dict, current_file: str) -> Dict[str, List[str]]:
        """A humble Gaze. A future ascension would use a full pathfinder."""
        return {}

    def _calculate_weights(self):
        """Gravity Calculation."""
        for node in self.nodes.values():
            node.weight = 1.0 + (len(node.called_by) * 0.5)

    def trace_impact(self, entry_points: List[str], depth: int = 5) -> Set[str]:
        """The Holocron Trace, now with a recursion guard."""
        relevant_nodes: Set[str] = set()
        queue: List[Tuple[str, int]] = []

        for ep in entry_points:
            # Normalize path for lookup
            ep_norm = ep.replace('\\', '/')
            if ep_norm in self.file_map:
                for nid in self.file_map[ep_norm]:
                    if nid not in relevant_nodes: queue.append((nid, 0)); relevant_nodes.add(nid)
            elif ep in self.symbol_table:
                for nid in self.symbol_table[ep]:
                    if nid not in relevant_nodes: queue.append((nid, 0)); relevant_nodes.add(nid)
            elif ep in self.nodes:
                if ep not in relevant_nodes: queue.append((ep, 0)); relevant_nodes.add(ep)

        visited_ids = {q[0] for q in queue}
        # [FACULTY 11] The Recursive Ward
        traversal_count = 0
        MAX_TRAVERSALS = 10000

        while queue and traversal_count < MAX_TRAVERSALS:
            traversal_count += 1
            curr_id, curr_depth = queue.pop(0)
            if curr_depth >= depth: continue

            node = self.nodes.get(curr_id)
            if not node: continue

            if node.weight > 20 and curr_depth > 1: continue

            for child_id in node.calls:
                if child_id not in visited_ids:
                    visited_ids.add(child_id)
                    relevant_nodes.add(child_id)
                    queue.append((child_id, curr_depth + 1))

        if traversal_count >= MAX_TRAVERSALS:
            Logger.warn("Holocron trace halted by recursion guard. Possible circular dependency.")

        relevant_files = {self.nodes[nid].file_path for nid in relevant_nodes if nid in self.nodes}
        return relevant_files