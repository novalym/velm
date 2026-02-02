# Path: artisans/analyze/graph_generator.py
# ----------------------------------------
# LIF: INFINITY | The Topological Cartographer

import os
import re
from pathlib import Path
from typing import List, Dict, Any


class TopologicalMapper:
    """
    =============================================================================
    == THE TOPOLOGICAL MAPPER (V-Ω-LATTICE-GENERATOR)                          ==
    =============================================================================
    Transmutes the project's Gnostic Bonds into a Physics-Ready JSON Vessel.
    """

    def generate_lattice(self, project_root: Path, symbol_map: Dict) -> Dict[str, Any]:
        """
        Processes the Symbol Map and File Tree to create Nodes and Edges.
        """
        nodes = []
        links = []

        # 1. Harvest Nodes (Files)
        for rel_path, gnosis in symbol_map.items():
            # Determine "Mass" based on number of symbols defined
            mass = len(gnosis.get('symbols', [])) + 1

            nodes.append({
                "id": rel_path,
                "name": os.path.basename(rel_path),
                "group": self._divine_group(rel_path),
                "mass": mass,
                "type": "scripture"
            })

        # 2. Harvest Links (Bonds)
        # We scan for imports/requires to forge edges
        for rel_path, gnosis in symbol_map.items():
            for bond in gnosis.get('bonds', []):
                links.append({
                    "source": rel_path,
                    "target": bond['target_path'],
                    "strength": 1.0
                })

        return {"nodes": nodes, "links": links}

    def _divine_group(self, path: str) -> str:
        """Categorizes files into functional gravity wells."""
        if "component" in path: return "UI"
        if "service" in path: return "Logic"
        if "model" in path: return "Data"
        return "Core"

