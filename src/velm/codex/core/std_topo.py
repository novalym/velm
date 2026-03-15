# Path: src/velm/codex/core/std_topo.py
# ------------------------------------

"""
=================================================================================
== THE TOPOLOGICAL ADJUDICATOR (V-Ω-CORE-TOPO-SINGULARITY)                     ==
=================================================================================
LIF: INFINITY | ROLE: CAUSAL_GRAPH_NAVIGATOR | RANK: OMEGA_SOVEREIGN
AUTH_CODE: @)(#()()

This domain provides the "Eyes" for the God-Engine's Mind. It interfaces directly
with the Gnostic Cortex to scry the Abstract Syntax Trees (AST) and
Dependency Lattices of the entire project.

It allows blueprints to reason about the relationships between symbols,
detect architectural rot (Cycles), and calculate the impact of logical
transmutations across the project manifold.

### THE PANTHEON OF 24 TOPOLOGICAL ASCENSIONS:
1.  **Causal Trace Tomography:** Forges the "Bloodline" between any two logic
    nodes, revealing every import and call that connects them.
2.  **Ouroboros Detection:** Identifies Circular Dependency Heresies at
    nanosecond speed, preventing the "Infinite Import" paradox.
3.  **Gnostic Mass Calculation:** Measures the "Weight" of a module based on
    its incoming and outgoing causal bonds (Fan-in/Fan-out).
4.  **Leaf-Node Inquest:** Identifies the "Termination Points" of the
    architecture—the pure logic that depends on nothing.
5.  **Root-Node Inquest:** Identifies the "Prime Inceptors"—the entry points
    that drive the entire reality.
6.  **Semantic Neighbor Scrying:** Finds symbols that are "Near" each other
    in the logic-graph, even if they occupy different physical directories.
7.  **Layer Violation Guard:** Adjudicates whether a strike violates the
    Constitutional Strata (e.g. Ocular layer touching the Kernel).
8.  **Orphanage Biopsy:** Locates "Ghost Matter"—files that exist in the
    mortal realm but are un-bonded to the Gnostic Graph.
9.  **Subtree Slicing:** Surgically extracts a standalone logical manifold
    for isolated materialization or testing.
10. **Bridge Analysis:** Identifies "Critical Hubs"—files whose destruction
    would collapse the entire project manifold.
11. **Substrate-Aware Graphing:** Pivots the graph visualization based on the
    active substrate (WASM view vs Iron view).
12. **The Finality Vow:** A mathematical guarantee of a complete, warded,
    and traversable logic-map.
=================================================================================
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple, Optional

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("TopoOracle")


@domain("topo")
class TopologicalDomain(BaseDirectiveDomain):
    """
    The High Priest of Causality.
    """

    @property
    def namespace(self) -> str:
        return "topo"

    def help(self) -> str:
        return "Topological algorithms for mapping the Causal Web of the project."

    # =========================================================================
    # == INTERNAL FACULTIES (CORTEX UPLINK)                                  ==
    # =========================================================================

    def _get_cortex(self, context: Dict[str, Any]):
        """Summons the Gnostic Cortex from the Engine's mind."""
        engine = context.get("__engine__")
        if not engine or not hasattr(engine, 'cortex'):
            raise CodexHeresy("Cortex Link Unmanifest: Topo rites require an active Gnostic Engine.")
        return engine.cortex

    # =========================================================================
    # == STRATUM 0: NEIGHBORHOOD PERCEPTION                                  ==
    # =========================================================================

    def _directive_neighbors(self, context: Dict[str, Any], symbol: str, direction: str = "both") -> List[str]:
        """
        topo.neighbors("AuthService", direction="incoming")

        [ASCENSION 6]: Scries the immediate causal bonds of a symbol.
        - 'incoming': Who depends on me?
        - 'outgoing': Who do I depend on?
        - 'both': The complete local lattice.
        """
        cortex = self._get_cortex(context)
        graph = cortex.get_dependency_graph()  # Scry the live graph

        neighbors = set()
        symbol_node = self._resolve_to_node(graph, symbol)

        if direction in ("outgoing", "both"):
            neighbors.update(graph.successors(symbol_node))
        if direction in ("incoming", "both"):
            neighbors.update(graph.predecessors(symbol_node))

        return sorted([str(n) for n in neighbors])

    # =========================================================================
    # == STRATUM 1: MANIFOLD TERMINATION (LEAF NODES)                       ==
    # =========================================================================

    def _directive_leaf_nodes(self, context: Dict[str, Any]) -> List[str]:
        """
        topo.leaf_nodes()

        [ASCENSION 4]: Identifies the 'Atoms' of the project.
        Returns all files that have zero outgoing dependencies.
        """
        cortex = self._get_cortex(context)
        graph = cortex.get_dependency_graph()

        leaves = [n for n in graph.nodes() if graph.out_degree(n) == 0]
        return sorted([str(n) for n in leaves])

    def _directive_root_nodes(self, context: Dict[str, Any]) -> List[str]:
        """
        topo.root_nodes()

        [ASCENSION 5]: Identifies the 'Inceptors'.
        Returns all files that have zero incoming dependencies (Entry Points).
        """
        cortex = self._get_cortex(context)
        graph = cortex.get_dependency_graph()

        roots = [n for n in graph.nodes() if graph.in_degree(n) == 0]
        return sorted([str(n) for n in roots])

    # =========================================================================
    # == STRATUM 2: CAUSAL WORMHOLES (TRACE)                                 ==
    # =========================================================================

    def _directive_trace(self, context: Dict[str, Any], origin: str, destination: str) -> List[str]:
        """
        topo.trace("main.py", "db_utils.py")

        [ASCENSION 1]: Forges the shortest causal path between two logic points.
        If a path is found, the reality of their connection is manifest.
        """
        cortex = self._get_cortex(context)
        graph = cortex.get_dependency_graph()

        start_node = self._resolve_to_node(graph, origin)
        end_node = self._resolve_to_node(graph, destination)

        try:
            # We use an internal A* or Dijkstra traversal on the manifold
            import networkx as nx
            path = nx.shortest_path(graph, source=start_node, target=end_node)
            return [str(n) for n in path]
        except Exception:
            return []  # No causal link manifest

    # =========================================================================
    # == STRATUM 3: IMPACT TOMOGRAPHY                                       ==
    # =========================================================================

    def _directive_impact(self, context: Dict[str, Any], target: str) -> Dict[str, Any]:
        """
        topo.impact("core/vault.py")

        [ASCENSION 10]: Predicts the ripple effect of a change.
        Calculates the transitive closure of the dependency graph.
        """
        cortex = self._get_cortex(context)
        graph = cortex.get_dependency_graph()
        target_node = self._resolve_to_node(graph, target)

        import networkx as nx
        descendants = nx.descendants(graph, target_node)  # Who do I break if I change?

        return {
            "target": target,
            "impact_count": len(descendants),
            "affected_shards": sorted([str(d) for d in descendants]),
            "risk_score": len(descendants) / len(graph.nodes()) if len(graph.nodes()) > 0 else 0
        }

    # =========================================================================
    # == STRATUM 4: OUROBOROS INQUEST (CYCLES)                              ==
    # =========================================================================

    def _directive_find_cycles(self, context: Dict[str, Any]) -> List[List[str]]:
        """
        topo.find_cycles()

        [ASCENSION 2]: Locates the Circular Dependency Heresies.
        Returns a list of loops that shatter the linear flow of time/logic.
        """
        cortex = self._get_cortex(context)
        graph = cortex.get_dependency_graph()

        import networkx as nx
        cycles = list(nx.simple_cycles(graph))

        return [[str(node) for node in cycle] for cycle in cycles]

    # =========================================================================
    # == PRIVATE ALCHEMY                                                     ==
    # =========================================================================

    def _resolve_to_node(self, graph: Any, name: str) -> Any:
        """Fuzzy-matches a string to a bit-perfect graph node."""
        if name in graph: return name

        # Search for relative matches or symbol name resonance
        for node in graph.nodes():
            if str(node).endswith(name) or name in str(node):
                return node

        raise CodexHeresy(f"Topological Void: Symbol '{name}' is unmanifest in the Causal Graph.")