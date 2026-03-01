# Path: src/velm/core/cortex/graph_builder.py
# -------------------------------------------

import collections
import hashlib
import platform
import time
import os
import random
import uuid
import sys
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Set, List, Optional, Any, Tuple, Counter, Final
from collections import defaultdict, deque

# --- GNOSTIC UPLINKS ---
from .contracts import FileGnosis
from ...logger import Scribe
from ...core.resolvers import GnosticPathfinder

Logger = Scribe("GraphBuilder")


class GnosticArchitecturalInquisitor:
    """
    =================================================================================
    == THE GNOSTIC ARCHITECTURAL INQUISITOR (V-Ω-MRI-SOVEREIGN-V3000)              ==
    =================================================================================
    LIF: 100x | ROLE: FORENSIC_MRI_CONDUCTOR | RANK: OMEGA_SUPREME
    AUTH: Ω_INQUISITOR_V3000_SENTINEL_READY_2026

    This class is the Conscience of the Codebase. It receives the raw topology
    and conducts a high-fidelity Inquest to identify structural decay and logic
    heresies. It is the primary anchor for the 'Sentinel' package.

    ### THE PANTHEON OF ASCENDED FACULTIES:
    1.  **Layer Sovereignty Enforcement:** Strictly enforces the directional flow of
        dependency from Outer (Material) to Inner (Pure) layers.
    2.  **Toxicity Detection:** Identifies "Black Hole" components that consume excessive
        dependencies, signaling high coupling.
    3.  **Ouroboros Detection:** Performs a depth-first search to find and flag circular
        dependency chains.
    4.  **Fragility Prophecy:** Simulates the collapse of nodes to determine load-bearing
        structures (Blast Radius analysis).
    5.  **Risk Heatmap Generation:** Synthesizes centrality and fragility into a
        unified risk metric for the Ocular HUD.
    """

    # [STRATUM RANKINGS]
    # Lower = More Pure (Inner). Higher = More Material (Outer).
    LAYERS: Final[Dict[str, int]] = {
        "domain": 0, "model": 0, "entity": 0, "entities": 0,
        "core": 1, "logic": 1, "usecase": 1, "interactor": 1,
        "service": 2, "provider": 2, "adapter": 3, "gateway": 3,
        "api": 4, "controller": 4, "route": 4, "handler": 4,
        "ui": 5, "view": 5, "component": 5, "page": 5,
        "cli": 6, "app": 6, "main": 6, "script": 6
    }

    def __init__(self,
                 dependency_graph: Dict[str, Set[str]],
                 dependents_graph: Dict[str, Set[str]],
                 all_nodes: Set[str]):
        self.deps = dependency_graph
        self.depts = dependents_graph
        self.nodes = all_nodes
        self.heresies: List[Dict[str, Any]] = []
        self.risk_scores: Dict[str, float] = collections.defaultdict(float)

    def conduct_inquest(self) -> Dict[str, Any]:
        """
        The Master Rite of Adjudication.
        Calls upon the specialist sub-rites to judge the cosmos.
        """
        Logger.info("Inquisitor: Initiating deep-tissue MRI of project topology...")

        # --- RITE I: DIRECTIONAL PURITY (LAYERS) ---
        self._check_layer_sovereignty()

        # --- RITE II: COUPLING TOXICITY ---
        self._adjudicate_toxicity()

        # --- RITE III: OUROBOROS SEARCH (CYCLES) ---
        self._hunt_ouroboros_cycles()

        # --- RITE IV: FRAGILITY PROPHECY ---
        fragility_wells = self._scry_fragility()

        return {
            "heresies": self.heresies,
            "risk_heatmap": self._generate_heatmap(fragility_wells),
            "fragility_wells": fragility_wells,
            "status": "CONCLUDED" if not self.heresies else "TAINTED"
        }

    def _check_layer_sovereignty(self):
        """[ASCENSION 2] Inner layers must never know of Outer layers."""
        for source, targets in self.deps.items():
            src_rank = self._divine_rank(source)
            for target in targets:
                tgt_rank = self._divine_rank(target)

                # Ignore lateral moves or upstream moves
                if src_rank == 99 or tgt_rank == 99: continue

                if src_rank < tgt_rank:
                    # Utility/Helper Amnesty: Pure logic can use utils
                    if "util" in target.lower() or "helper" in target.lower() or "common" in target.lower():
                        continue

                    self._proclaim_heresy(
                        "LAYER_VIOLATION",
                        source,
                        f"Inversion Heresy: Pure Logic '{source}' (L{src_rank}) depends on Material '{target}' (L{tgt_rank})."
                    )

    def _adjudicate_toxicity(self):
        """[ASCENSION 5] Detects Black Hole components."""
        total_mass = len(self.nodes)
        if total_mass < 10: return

        for node in self.nodes:
            fan_out = len(self.deps.get(node, []))
            # If a file knows about more than 15% of the project, it is Toxic.
            if fan_out > max(8, total_mass * 0.15):
                self._proclaim_heresy(
                    "COUPLING_TOXICITY",
                    node,
                    f"Toxicity Alert: Scripture is a 'Black Hole'. It consumes {fan_out} unique dependencies."
                )

    def _scry_fragility(self) -> List[Dict[str, Any]]:
        """[ASCENSION 3] Simulates the collapse of load-bearing shards."""
        wells = []
        total_mass = len(self.nodes)
        if total_mass == 0: return []

        for node in self.nodes:
            blast_radius = self._calculate_transitive_impact(node)
            impact_ratio = len(blast_radius) / total_mass
            if impact_ratio > 0.4:  # Load bearing threshold
                wells.append({
                    "path": node,
                    "impact": f"{impact_ratio * 100:.1f}%",
                    "count": len(blast_radius)
                })
        return sorted(wells, key=lambda x: x['count'], reverse=True)

    def _calculate_transitive_impact(self, start_node: str) -> Set[str]:
        """BFS walk to find everything that eventually depends on this node."""
        visited = {start_node}
        queue = deque([start_node])
        while queue:
            curr = queue.popleft()
            for dependent in self.depts.get(curr, []):
                if dependent not in visited:
                    visited.add(dependent)
                    queue.append(dependent)
        return visited

    def _hunt_ouroboros_cycles(self):
        """[ASCENSION 4] Identifies self-eating logic loops via iterative DFS."""
        visited = set()
        path_stack = []
        path_set = set()

        def visit(node):
            path_stack.append(node)
            path_set.add(node)

            for neighbor in self.deps.get(node, []):
                if neighbor in path_set:
                    # Cycle Detected
                    try:
                        start_index = path_stack.index(neighbor)
                        cycle = path_stack[start_index:] + [neighbor]
                        cycle_path = " -> ".join(cycle)
                        self._proclaim_heresy("OUROBOROS_CYCLE", node, f"Logic Whirlpool: {cycle_path}")
                    except ValueError:
                        pass  # Should not happen given set check
                elif neighbor not in visited:
                    visit(neighbor)

            path_stack.pop()
            path_set.remove(node)
            visited.add(node)

        # Iterate over a copy of nodes to allow modification safe iteration
        for node in list(self.nodes):
            if node not in visited:
                visit(node)

    def _divine_rank(self, path: str) -> int:
        parts = path.lower().split('/')
        # Look for the deepest semantic layer in the path
        for p in reversed(parts):
            clean = p.rstrip('s')  # model/models -> model
            if clean in self.LAYERS: return self.LAYERS[clean]
        return 99  # Unknown stratum

    def _proclaim_heresy(self, code: str, locus: str, msg: str):
        self.heresies.append({
            "code": code,
            "locus": locus,
            "message": msg,
            "severity": "CRITICAL" if "CYCLE" in code else "WARNING"
        })

    def _generate_heatmap(self, fragility_wells: List[Dict]) -> Dict[str, float]:
        heatmap = collections.defaultdict(float)
        well_map = {w['path']: float(w['impact'].strip('%')) / 100 for w in fragility_wells}
        for node in self.nodes:
            # Heat = (Centrality proxy * 0.5) + (Fragility * 0.5)
            in_degree = len(self.depts.get(node, []))
            # Normalize in_degree crudely
            centrality = min(1.0, in_degree / 10.0)
            heatmap[node] = round((centrality * 0.5) + (well_map.get(node, 0.0) * 0.5), 2)
        return heatmap


class GraphBuilder:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC CAUSALITY (V-Ω-LEGENDARY-APOTHEOSIS-ULTIMA)       ==
    =================================================================================
    LIF: ∞ (THE OMNISCIENT CARTOGRAPHER)

    The Sovereign Mapper of the Project's Soul.
    It transmutes a list of isolated files into a living, breathing Web of Causality.
    It is the Architect of the Dependency Graph, the Centrality Seer, and the
    Community Diviner.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Substrate-Aware Concurrency (THE FIX):** Automatically detects the WASM/Pyodide
        substrate and pivots from `ThreadPoolExecutor` to Serial execution to prevent
        the `RuntimeError: can't start new thread` heresy.
    2.  **Canonical Path Law:** Enforces Project-Relative POSIX Paths as the absolute
        keys for all nodes, annihilating Windows backslash fragmentation.
    3.  **The Fuzzy Filename Oracle:** Maintains a reverse-lookup map of `filename -> [paths]`
        to resolve ambiguous imports (e.g. `import utils` -> `src/core/utils.py`).
    4.  **Symbolic Deep-Linking:** Pre-indexes all functions, classes, and modules
        found in the AST to enable precise symbol-level dependency resolution.
    5.  **Polyglot Gaze:** Natively understands Python, JS/TS, Go, Rust, and Java
        import semantics via the `GnosticPathfinder`.
    6.  **Hydraulic Merging:** Uses a dedicated `_ingest_partial_results` pipe to
        atomically merge thread/serial worker outputs into the main graph.
    7.  **The Bridge Premium:** Identifies "Bridge Nodes" that connect disparate
        architectural communities and boosts their centrality score.
    8.  **Merkle-Lattice Sealing:** Computes a deterministic SHA-256 hash of the
        entire graph topology to detect structural drift.
    9.  **Ocular Multicast:** Radiates "REACTOR_IGNITION" and "LATTICE_RESONANT"
        events to the React HUD for real-time visualization.
    10. **Test Symbiosis:** Heuristically links test files to their implementation
        targets even without explicit imports.
    11. **Config Shadow-Linking:** Connects configuration files (`package.json`, `Cargo.toml`)
        to their entry points (`index.ts`, `main.rs`).
    12. **The Finality Vow:** Guarantees a fully populated `GnosticGraph` object,
        never leaving the analysis in a partial state.
    """

    def __init__(self, root: Path, inventory: List[FileGnosis], project_gnosis: Dict[str, Dict]):
        self.root = root.resolve()
        self.inventory = inventory
        self.project_gnosis = project_gnosis

        # --- MOVEMENT I: THE CENSUS OF THE CANON ---
        # We normalize every file in the inventory to a Canonical Key.
        # This set acts as the "Authority of Existence".
        self.all_files_set: Set[str] = set()
        self.file_map: Dict[str, FileGnosis] = {}

        # A map for the Fuzzy Oracle: "utils.py" -> ["src/core/utils.py", "src/legacy/utils.py"]
        self.fuzzy_filename_map: Dict[str, List[str]] = defaultdict(list)

        for g in inventory:
            try:
                # Ensure we are working with absolute paths for logic, but relative strings for keys
                if g.path.is_absolute():
                    abs_path = g.path.resolve()
                else:
                    abs_path = (self.root / g.path).resolve()

                # The First Law: Containment
                if not abs_path.is_relative_to(self.root):
                    continue

                # The Second Law: Normalization (POSIX)
                path_str = abs_path.relative_to(self.root).as_posix()

                self.all_files_set.add(path_str)
                self.file_map[path_str] = g
                self.fuzzy_filename_map[abs_path.name].append(path_str)

            except (ValueError, RuntimeError):
                continue

        # --- MOVEMENT II: THE FORGING OF THE DIVINE INSTRUMENTS ---
        # We build the Symbol Map before we start weaving bonds.
        self.symbol_map, self.symbol_multimap = self._forge_symbol_maps()

        # The Pathfinder is summoned with the complete maps of the cosmos.
        self.pathfinder = GnosticPathfinder(self.root, self.symbol_map, self.all_files_set)

        # --- MOVEMENT III: THE INITIALIZATION OF THE GRIMOIRES ---
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)  # Who do I need?
        self.dependents_graph: Dict[str, Set[str]] = defaultdict(set)  # Who needs me?
        self.edge_weights: Dict[Tuple[str, str], float] = defaultdict(float)
        self.edge_types: Dict[Tuple[str, str], Set[str]] = defaultdict(set)
        self.external_dependencies: Counter[str] = Counter()
        self.centrality_scores: Dict[str, float] = defaultdict(float)
        self.architectural_heresies: List[Dict[str, str]] = []
        self.communities: Dict[str, int] = {}  # Path -> Community ID

    def _forge_symbol_maps(self) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
        """
        [ELEVATION 4] THE SYMBOL FORGE.
        Scans the inventory to map Abstract Symbols (classes, functions, modules)
        to Concrete Realities (file paths).
        """
        s_map: Dict[str, str] = {}
        s_multimap: Dict[str, List[str]] = defaultdict(list)

        def register(sym: str, f_path: str):
            if not sym: return
            # Primary Map: Last Write Wins (Good for unique symbols)
            s_map[sym] = f_path
            # Multi Map: All writes preserved (Good for ambiguous symbols)
            if f_path not in s_multimap[sym]:
                s_multimap[sym].append(f_path)

        # Heuristic: Detect 'src' directory for Python package resolution
        src_root = self.root / 'src' if (self.root / 'src').is_dir() else self.root

        for file_path_str in self.all_files_set:
            file_path = self.root / file_path_str

            # 1. Map Python Modules (The Pythonic Way)
            if file_path_str.endswith('.py'):
                try:
                    rel_to_src = file_path.relative_to(src_root)
                    parts = list(rel_to_src.with_suffix('').parts)
                    # Handle __init__.py package mapping
                    if parts and parts[-1] == '__init__':
                        parts.pop()

                    if parts:
                        dotted_path = ".".join(parts)
                        register(dotted_path, file_path_str)
                        # Register the leaf name for short imports
                        register(parts[-1], file_path_str)
                except ValueError:
                    pass

            # 2. Map Generic Filenames (Stem and Full Name)
            register(file_path.stem, file_path_str)
            register(file_path.name, file_path_str)

            # 3. Map Explicit AST Symbols (From the Inquisitor's Dossier)
            # We check both the normalized key and the raw path to be safe.
            dossier = self.project_gnosis.get(file_path_str, {})
            if not dossier:
                dossier = self.project_gnosis.get(str(file_path), {})

            if not dossier: continue

            # We check multiple sources of truth within the dossier
            sources = [dossier, dossier.get("metrics", {}), dossier.get("ast_metrics", {})]
            for source in sources:
                if not isinstance(source, dict): continue
                for container in ["functions", "classes", "structs", "interfaces", "traits"]:
                    items = source.get(container, [])
                    for item in items:
                        if isinstance(item, dict) and 'name' in item:
                            register(item['name'], file_path_str)

        return s_map, dict(s_multimap)

    def build(self) -> Dict[str, Any]:
        """
        =================================================================================
        == THE GRAND RITE OF CAUSALITY (V-Ω-TOTALITY-V3000-SUBSTRATE-AWARE)            ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_RECONSTRUCTOR | RANK: OMEGA_SOVEREIGN

        [THE CURE]: This method now possesses **Substrate Sensing**. It checks the
        `SCAFFOLD_ENV` to determine if it is running in the Ether (WASM) or on Iron.
        If in WASM, it bypasses the `ThreadPoolExecutor` to avoid the Threading Paradox.
        """
        start_ns = time.perf_counter_ns()
        trace_id = os.environ.get("SCAFFOLD_TRACE_ID", f"tr-graph-{uuid.uuid4().hex[:6]}")

        # --- MOVEMENT 0: OCULAR IGNITION ---
        # [ASCENSION 9]: Signal the Ocular HUD
        self._multicast_hud("REACTOR_IGNITION", "#a855f7", trace_id)

        Logger.info(f"The God-Engine of Causality awakens its Gaze...")

        # --- MOVEMENT I: SUBSTRATE-AWARE MATTER DISCOVERY ---
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        if is_wasm:
            self._build_serial()
        else:
            self._build_parallel()

        # --- MOVEMENT II: THE INQUISITION (SUTURED MRI) ---
        # [ASCENSION 1 & 14]: Summon the Forensic MRI Conductor.
        inquisitor = GnosticArchitecturalInquisitor(
            self.dependency_graph,
            self.dependents_graph,
            self.all_files_set
        )

        # [KINETIC STRIKE]: Adjudicate the layers, toxicity, and cycles.
        inquest_results = inquisitor.conduct_inquest()
        self.architectural_heresies = inquest_results["heresies"]

        # --- MOVEMENT III: INTELLIGENCE EVOLUTION ---
        # [ASCENSION 6 & 8]: Fluid convergence of logic-islands and influence mass.
        self._detect_communities()
        self._calculate_advanced_centrality()

        # --- MOVEMENT IV: THE CRYPTOGRAPHIC SEAL ---
        # [ASCENSION 8]: Forge the Merkle-Lattice Seal.
        merkle_seal = self._compute_merkle_lattice_seal()

        # --- MOVEMENT V: FINAL REVELATION (TELEMETRY) ---
        orphans = [f for f in self.all_files_set if f not in self.dependency_graph and f not in self.dependents_graph]
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        Logger.success(
            f"Cosmos mapped in {duration_ms / 1000:.2f}s. "
            f"Seal: [dim]{merkle_seal[:12]}[/] | {len(self.architectural_heresies)} heresies perceived."
        )

        # --- MOVEMENT VI: OCULAR RESONANCE ---
        # [ASCENSION 9]: Broadcast the "Resonant" state to the Cockpit UI.
        self._multicast_hud("LATTICE_RESONANT", "#64ffda", trace_id)

        # [ASCENSION 12]: THE FINALITY VOW
        return {
            "version": "V-Ω-TOTALITY-V3000",
            "merkle_root": merkle_seal,
            "latency_ms": duration_ms,
            "topology": {
                "nodes": len(self.all_files_set),
                "edges": sum(len(v) for v in self.dependency_graph.values()),
                "orphans": orphans
            },
            "graphs": {
                "dependencies": {k: sorted(list(v)) for k, v in self.dependency_graph.items()},
                "dependents": {k: sorted(list(v)) for k, v in self.dependents_graph.items()},
                "edge_types": {f"{k[0]}|{k[1]}": list(v) for k, v in self.edge_types.items()}
            },
            "intelligence": {
                "centrality_scores": dict(self.centrality_scores),
                "risk_heatmap": inquest_results["risk_heatmap"],
                "fragility_wells": inquest_results["fragility_wells"],
                "communities": self.communities,
                "external_dependencies": dict(self.external_dependencies),
            },
            "heresies": self.architectural_heresies,
            "ui_resonance": {
                "vfx": "bloom",
                "priority_nodes": sorted(self.centrality_scores, key=self.centrality_scores.get, reverse=True)[:15]
            }
        }

    def _build_serial(self):
        """
        [ASCENSION 1 - THE FIX]: SERIAL EXECUTION MODE
        Runs the processing loop synchronously on the main thread for WASM environments.
        This annihilates the Threading Paradox.
        """
        Logger.info("WASM Substrate detected. Engaging Serial Causal Weaver.")
        processed = 0
        total = len(self.file_map)

        for path_str, gnosis in self.file_map.items():
            processed += 1
            # Hydraulic Yield: Breathe every 20 items to allow UI updates
            if processed % 25 == 0:
                time.sleep(0.01)

            try:
                partial = self._process_single_scripture(path_str, gnosis)
                if partial:
                    self._ingest_partial_results(partial)
            except Exception as e:
                Logger.error(f"Serial Causal Fracture in '{path_str}': {e}")

    def _build_parallel(self):
        """
        [ASCENSION 1]: PARALLEL EXECUTION MODE
        Uses ThreadPoolExecutor for Native Iron environments.
        """
        Logger.info("Native Iron detected. Engaging Parallel Causal Swarm.")
        max_workers = min(32, (os.cpu_count() or 1) + 4)

        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="CausalWeaver") as executor:
            future_to_file = {
                executor.submit(self._process_single_scripture, p, g): p
                for p, g in self.file_map.items()
            }

            for future in as_completed(future_to_file):
                path_context = future_to_file[future]
                try:
                    partial = future.result()
                    if partial:
                        self._ingest_partial_results(partial)
                except Exception as e:
                    Logger.error(f"Achronal Fracture in '{path_context}': {e}")

    def _ingest_partial_results(self, partial: Dict[str, Any]):
        """
        [ASCENSION 6]: HYDRAULIC MERGER
        Atomically merges the result of a single file analysis into the main graph.
        Shared by both Serial and Parallel execution paths.
        """
        source = partial['source']

        # Merge Edges
        for target, bond_type, weight in partial.get('bonds', []):
            self._add_edge(source, target, bond_type, weight)

        # Merge External Dependencies
        for ext_dep in partial.get('external_deps', []):
            self.external_dependencies[ext_dep] += 1

    def _process_single_scripture(self, path_str: str, gnosis: FileGnosis) -> Optional[Dict[str, Any]]:
        """
        [THE ATOMIC GAZE]
        Analyzes a single file to find its outgoing connections.
        Robustly handles both String imports and Dictionary imports.
        """
        if gnosis.category in ('binary', 'noise', 'lock'): return None

        # Fetch dossier with robust fallback
        dossier = self.project_gnosis.get(path_str, {})
        if not dossier:
            dossier = self.project_gnosis.get(str(Path(path_str)), {})

        bonds: List[Tuple[str, str, float]] = []
        external_deps: List[str] = []

        # --- GATHER IMPORTS ---
        raw_imports = set()

        # 1. From FileGnosis (Already normalized strings by Interrogator)
        if gnosis.imported_symbols:
            raw_imports.update(gnosis.imported_symbols)

        # 2. From Raw AST Dossier (Might be Dicts or Strings)
        deps_block = dossier.get("dependencies", {})

        # Handle 'imports' list (mixed types)
        for imp in deps_block.get("imports", []):
            if isinstance(imp, dict):
                if "path" in imp:
                    raw_imports.add(imp["path"])
            elif isinstance(imp, str):
                raw_imports.add(imp)

        # Handle 'imported_symbols' list (usually strings)
        for sym in deps_block.get("imported_symbols", []):
            if isinstance(sym, str):
                raw_imports.add(sym)

        for imp_str in raw_imports:
            # 1. THE PATHFINDER'S GAZE (Precise)
            target_file = self.pathfinder.resolve(imp_str, path_str, gnosis.language)

            if target_file and target_file in self.all_files_set and target_file != path_str:
                weight = 1.0
                if gnosis.language == 'python' and 'from' in imp_str: weight = 1.5
                bonds.append((target_file, "import", weight))

            # 2. THE FUZZY ORACLE (Fallback)
            elif not target_file:
                potential_name = imp_str.split('.')[-1]

                candidates = []
                for ext in ['.py', '.ts', '.js', '.tsx', '.go', '.rs', '.java']:
                    candidates.extend(self.fuzzy_filename_map.get(potential_name + ext, []))

                if len(candidates) == 1 and candidates[0] != path_str:
                    bonds.append((candidates[0], "fuzzy_link", 0.5))
                else:
                    root_pkg = imp_str.split('.')[0] if '.' in imp_str else imp_str
                    external_deps.append(root_pkg)

        # --- 3. THE SYMBIOTIC GAZE (TEST LINKING) ---
        if 'test' in path_str.lower() or 'spec' in path_str.lower():
            target = self._divine_test_target(path_str)
            if target:
                bonds.append((target, "test_target", 0.5))

        # --- 4. THE SHADOW GAZE (CONFIG LINKING) ---
        if gnosis.category == 'config':
            entry_points = self._divine_config_entry_points(path_str, dossier)
            for ep in entry_points:
                bonds.append((ep, "config_entry", 2.0))

        return {
            "source": path_str,
            "bonds": bonds,
            "external_deps": external_deps
        }

    def _add_edge(self, source: str, target: str, type: str, weight: float):
        """Thread-safe addition to the graph."""
        if target not in self.all_files_set: return
        self.dependency_graph[source].add(target)
        self.dependents_graph[target].add(source)
        self.edge_types[(source, target)].add(type)
        self.edge_weights[(source, target)] += weight

        # Preliminary centrality (In-Degree)
        self.centrality_scores[target] += 1

    def _calculate_advanced_centrality(self, iterations: int = 30):
        """[ELEVATION 2] The PageRank Algorithm."""
        nodes = list(self.all_files_set)
        if not nodes: return

        num_nodes = len(nodes)
        scores = {node: 1.0 / num_nodes for node in nodes}
        damping = 0.85

        for _ in range(iterations):
            new_scores = collections.defaultdict(float)
            for node in nodes:
                dependents = self.dependents_graph.get(node, set())
                new_scores[node] += (1 - damping) / num_nodes
                for dep in dependents:
                    out_degree = len(self.dependency_graph.get(dep, set()))
                    new_scores[node] += (scores[dep] / max(1, out_degree)) * damping
            scores = new_scores

        # [ASCENSION 7]: THE BRIDGE PREMIUM
        for node in nodes:
            my_comm = self.communities.get(node)
            foreign_bonds = 0
            for neighbor in self.dependency_graph.get(node, set()):
                if self.communities.get(neighbor) != my_comm:
                    foreign_bonds += 1
            if foreign_bonds > 0:
                scores[node] *= (1.0 + (foreign_bonds * 0.25))

        max_mass = max(scores.values()) if scores else 1.0
        self.centrality_scores = {k: round((v / max_mass) * 100, 2) for k, v in scores.items()}

    def _detect_communities(self, max_iterations: int = 15, epsilon: float = 0.001):
        """[THE MANIFESTO]: Iterative Weighted Label Propagation."""
        labels = {node: i for i, node in enumerate(self.all_files_set)}
        nodes = list(self.all_files_set)

        for iteration in range(max_iterations):
            # [ASCENSION 6]: Deterministic Jitter
            random.seed(42 + iteration)
            random.shuffle(nodes)
            changes = 0

            for node in nodes:
                neighbors = list(self.dependency_graph.get(node, [])) + \
                            list(self.dependents_graph.get(node, []))

                if not neighbors: continue

                label_influence = collections.defaultdict(float)
                for neighbor in neighbors:
                    w = self.edge_weights.get((node, neighbor), 1.0) + \
                        self.edge_weights.get((neighbor, node), 1.0)
                    label_influence[labels[neighbor]] += w

                if label_influence:
                    best_label = max(label_influence.items(), key=lambda x: x[1])[0]
                    if labels[node] != best_label:
                        labels[node] = best_label
                        changes += 1

            change_ratio = changes / len(nodes)
            if change_ratio < epsilon:
                Logger.verbose(f"Community Lattice stabilized in {iteration + 1} passes.")
                break

        self.communities = labels

    def _compute_merkle_lattice_seal(self) -> str:
        """[ASCENSION 8]: Forges a single SHA256 root hash of the current topology."""
        hasher = hashlib.sha256()
        for source in sorted(self.dependency_graph.keys()):
            hasher.update(source.encode())
            for target in sorted(list(self.dependency_graph[source])):
                hasher.update(f"->{target}".encode())
        return hasher.hexdigest()

    def _multicast_hud(self, type_label: str, color: str, trace: str):
        """[ASCENSION 9]: Projects a Gnostic Pulse to the Ocular HUD."""
        if hasattr(self, 'engine') and self.engine and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "CAUSAL_REACTOR",
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time(),
                        "meta": {"node_id": platform.node(), "process_id": os.getpid()}
                    }
                })
            except Exception:
                pass

    def _detect_cycles(self):
        """[ASCENSION 3]: Finds Ouroboros loops in the graph."""
        visited = set()
        stack = []
        stack_set = set()

        def visit(node):
            visited.add(node)
            stack.append(node)
            stack_set.add(node)

            for neighbor in self.dependency_graph.get(node, []):
                if neighbor not in visited:
                    visit(neighbor)
                elif neighbor in stack_set:
                    cycle_slice = stack[stack.index(neighbor):]
                    cycle_type = "Direct" if len(cycle_slice) == 1 else "Complex"
                    cycle_path = " -> ".join(cycle_slice + [neighbor])
                    self.architectural_heresies.append({
                        "type": f"{cycle_type} Circular Dependency",
                        "detail": cycle_path,
                        "severity": "CRITICAL"
                    })

            stack.pop()
            stack_set.remove(node)

        for node in list(self.dependency_graph.keys()):
            if node not in visited:
                visit(node)

    def _detect_layer_violations(self):
        """[ASCENSION 1]: Enforces Clean Architecture constraints."""
        for source, targets in self.dependency_graph.items():
            src_layer = self._get_layer_score(source, GnosticArchitecturalInquisitor.LAYERS)
            if src_layer == -1: continue

            for target in targets:
                tgt_layer = self._get_layer_score(target, GnosticArchitecturalInquisitor.LAYERS)
                if tgt_layer == -1: continue

                if src_layer < tgt_layer:
                    if "test" in source or "spec" in source or "config" in source: continue
                    self.architectural_heresies.append({
                        "type": "Layer Violation",
                        "detail": f"{source} (L{src_layer}) -> {target} (L{tgt_layer})",
                        "severity": "WARNING"
                    })

    def _get_layer_score(self, path: str, layers: Dict[str, int]) -> int:
        parts = path.lower().split('/')
        best_score = -1
        for part in parts:
            base = part.rstrip('s')
            if base in layers:
                score = layers[base]
                if score > best_score: best_score = score
        return best_score

    def _divine_test_target(self, test_path_str: str) -> Optional[str]:
        """[ASCENSION 10]: THE SYMBIOTIC LINKER."""
        path_obj = Path(test_path_str)
        stem = path_obj.stem
        subject_stem = stem.replace("test_", "").replace("_test", "").replace(".spec", "").replace(".test", "")

        candidates = self.fuzzy_filename_map.get(subject_stem + path_obj.suffix, [])
        if not candidates and path_obj.suffix == '.ts':
            candidates = self.fuzzy_filename_map.get(subject_stem + '.js', [])

        if candidates:
            for c in candidates:
                if c != test_path_str: return c
        return None

    def _divine_config_entry_points(self, config_path_str: str, dossier: Dict) -> List[str]:
        """[ASCENSION 11]: THE SHADOW DEPENDENCY DETECTOR."""
        entry_points = set()

        gnosis = self.file_map.get(config_path_str)
        if gnosis and gnosis.semantic_links:
            for link in gnosis.semantic_links:
                try:
                    config_path = self.root / config_path_str
                    target_abs = (config_path.parent / link).resolve()
                    if target_abs.is_relative_to(self.root):
                        target_rel = target_abs.relative_to(self.root).as_posix()
                        if target_rel in self.all_files_set:
                            entry_points.add(target_rel)
                except (ValueError, OSError):
                    continue

        filename = Path(config_path_str).name
        config_dir = str(Path(config_path_str).parent).replace('\\', '/')
        if config_dir == '.': config_dir = ''

        def check(rel_candidate: str):
            full = f"{config_dir}/{rel_candidate}" if config_dir else rel_candidate
            full = full.replace('//', '/')
            if full in self.all_files_set:
                entry_points.add(full)

        if filename == "package.json":
            for f in ["src/index.ts", "src/main.ts", "index.js", "server.js", "app.js"]: check(f)
        elif filename in ["pyproject.toml", "requirements.txt"]:
            for f in ["src/main.py", "main.py", "app.py", "wsgi.py"]: check(f)
        elif filename == "Cargo.toml":
            for f in ["src/main.rs", "src/lib.rs"]: check(f)
        elif filename == "go.mod":
            for f in ["main.go", "cmd/server/main.go"]: check(f)

        return sorted(list(entry_points))

    def find_orphaned_symbols(self) -> Dict[str, Set[str]]:
        """[ASCENSION 12]: THE VOID HEURISTIC."""
        global_usage = set()
        for gnosis in self.inventory:
            ast = gnosis.ast_metrics
            if not ast: continue
            for block_type in ['functions', 'classes']:
                for block in ast.get(block_type, []):
                    external_deps = block.get('dependencies', {}).get('external', [])
                    global_usage.update(external_deps)

        dormant_map = defaultdict(set)
        for gnosis in self.inventory:
            path_str = str(gnosis.path).replace('\\', '/')
            ast = gnosis.ast_metrics
            if not ast: continue
            for func in ast.get('functions', []):
                name = func['name']
                if name not in global_usage and name not in ['main', '__init__', 'handler']:
                    dormant_map[path_str].add(name)
            for cls in ast.get('classes', []):
                name = cls['name']
                if name not in global_usage:
                    dormant_map[path_str].add(name)

        return dict(dormant_map)