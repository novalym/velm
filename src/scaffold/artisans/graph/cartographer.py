# Path: artisans/graph/cartographer.py
# ------------------------------------

import time
import hashlib
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from ...core.cortex.engine import GnosticCortex
from .layout import LayoutManager
from ...logger import Scribe
from ...interfaces.base import ScaffoldResult

Logger = Scribe("Cartographer")


class GnosticCartographer:
    """
    =================================================================================
    == THE OMNISCIENT CARTOGRAPHER (V-Ω-TOTALITY-FINAL-V502-ARGUMENT-HEALED)        ==
    =================================================================================
    @gnosis:title The Gnostic Cartographer
    @gnosis:summary The divine artisan that projects the physical file lattice into
                     a visual node-graph for the Genesis View.
    @gnosis:LIF 10,000,000,000

    [HEALED]:
    1. Path Relativity Paradox Annihilated (Absolute/Relative checks).
    2. Signature Harmonization: Now accepts 'format' to satisfy the GraphArtisan's plea.
    """

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.layout_manager = LayoutManager(self.root)

    def gaze(self,
             focus: Optional[str] = None,
             format: str = "json",
             include_orphans: bool = True) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND RITE OF TOPOLOGICAL PERCEPTION (V-Ω-TOTALITY)                 ==
        =============================================================================
        LIF: INFINITY | ROLE: REALITY_CARTOGRAPHER | RANK: SOVEREIGN

        Transmutes the project's internal Gnosis into a Physics-Ready Causal Lattice.
        [THE CURE]: Implements high-order path-equivalence and JIT shadow-merging.
        """
        import time
        import math
        import uuid
        from pathlib import Path

        start_time = time.perf_counter()
        trace_id = f"gaze-{uuid.uuid4().hex[:6].upper()}"

        try:
            # --- MOVEMENT I: SUMMON THE CORE MENTAL STATE ---
            # [ASCENSION 7]: Check for warm Cortex
            cortex = getattr(self.engine, 'cortex', GnosticCortex(self.root))
            memory = cortex.perceive()  # Utilizes the Iron Core (Rust)

            # --- MOVEMENT II: RESURRECT SPATIAL MEMORY ---
            layout = self.layout_manager.load() if hasattr(self, 'layout_manager') else {}

            nodes = []
            node_ids = set()

            # [ASCENSION 1]: CAUSAL SLICING PREP
            # If focus is requested, we perform a neighbor-search
            focus_norm = focus.replace("\\", "/") if focus else None
            reachable_ids = set()
            if focus_norm:
                reachable_ids = self._scry_neighborhood(memory, focus_norm, depth=2)

            # --- MOVEMENT III: TRANSMUTE INVENTORY (MATTER) ---
            for idx, file_gnosis in enumerate(memory.inventory):
                # 1. PATH PURIFICATION
                raw_path = file_gnosis.path
                try:
                    # [THE FIX]: Resolve absolute/relative schism
                    if raw_path.is_absolute():
                        rel_path = raw_path.relative_to(self.root).as_posix()
                    else:
                        rel_path = raw_path.as_posix()
                except ValueError:
                    continue  # Escape the sanctum

                # 2. THE ABYSSAL SIEVE [ASCENSION 8]
                if any(abyss in rel_path for abyss in ABYSS):
                    continue

                # 3. SLICING VETO [ASCENSION 1]
                if focus_norm and rel_path not in reachable_ids:
                    continue

                # 4. MOLECULAR ARCHETYPING
                node_type = self._divine_archetype(file_gnosis)

                # 5. DETERMINISTIC SPATIAL HASHING [ASCENSION 5]
                # Calculate Spiral-Radial coordinates if no layout exists
                angle = idx * (2 * math.pi / 13)
                radius = 400 + (idx * 50)
                default_x = 1000 + (radius * math.cos(angle))
                default_y = 1000 + (radius * math.sin(angle))

                pos = layout.get(rel_path, {"x": default_x, "y": default_y})

                # 6. MOLECULAR METADATA SIPHONING [ASCENSION 2 & 9]
                complexity = file_gnosis.ast_metrics.get("cyclomatic_complexity", 0)
                churn = getattr(file_gnosis, 'author_count', 1)
                heat_score = min(1.0, (complexity / 20.0) + (churn / 10.0))

                nodes.append({
                    "id": rel_path,
                    "type": node_type,
                    "label": file_gnosis.name,
                    "x": pos["x"],
                    "y": pos["y"],
                    "data": {
                        "path": rel_path,
                        "heat": heat_score,
                        "complexity": complexity,
                        "lines": file_gnosis.original_size // 45,
                        "author_count": churn,
                        "hash": file_gnosis.hash_signature[:8] if file_gnosis.hash_signature else "0xVOID"
                    }
                })
                node_ids.add(rel_path)

            # --- MOVEMENT IV: SHADOW PROJECTION [ASCENSION 3] ---
            # We merge files that exist only in the AI Staging Area
            shadow_nodes = self._scry_shadow_realities(node_ids)
            nodes.extend(shadow_nodes)
            for sn in shadow_nodes: node_ids.add(sn['id'])

            # --- MOVEMENT V: WEAVE THE CABLES (BONDS) ---
            edges = []
            dep_graph = memory.dependency_graph.get('dependency_graph', {})

            for source, targets in dep_graph.items():
                src_id = source.replace("\\", "/")
                if src_id not in node_ids: continue

                for target in targets:
                    tgt_id = target.replace("\\", "/")
                    if tgt_id not in node_ids: continue
                    if src_id == tgt_id: continue

                    # [ASCENSION 4]: HERESY TOMOGRAPHY
                    # Adjudicate Layer Violation
                    is_heresy = self._is_heretical(src_id, tgt_id)

                    # [ASCENSION 6]: CAUSAL ANIMATION
                    # Animate if it's a critical path or a violation
                    is_animated = is_heresy or any(k in src_id.lower() for k in ('service', 'daemon', 'transporter'))

                    edges.append({
                        "id": f"{src_id}->{tgt_id}",
                        "source": src_id,
                        "target": tgt_id,
                        "type": "Import",
                        "isHeresy": is_heresy,
                        "animated": is_animated,
                        "data": {"strength": 1.0 if not is_heresy else 2.0}
                    })

            # --- MOVEMENT VI: METABOLIC TELEMETRY [ASCENSION 12] ---
            duration_ms = (time.perf_counter() - start_time) * 1000
            Logger.info(f"Lattice Synchronized: {len(nodes)} Atoms, {len(edges)} Bonds. [{duration_ms:.2f}ms]")

            return ScaffoldResult(
                success=True,
                message=f"Reality Projected in {duration_ms:.2f}ms.",
                data={
                    "nodes": nodes,
                    "edges": edges,
                    "fingerprint": memory.gnostic_hash,
                    "trace_id": trace_id
                }
            )

        except Exception as catastrophic_fracture:
            # [ASCENSION 11]: THE FORENSIC SARCOPHAGUS
            import traceback
            tb = traceback.format_exc()
            self.logger.error(f"Cartographer shattered during gaze: {catastrophic_fracture}\n{tb}")

            # Return partial truth if we managed to harvest any nodes
            if 'nodes' in locals() and nodes:
                return ScaffoldResult(
                    success=True,
                    message="Perception Fractured: Returning Partial Reality.",
                    data={"nodes": nodes, "edges": edges if 'edges' in locals() else []}
                )

            # Nuclear Failure
            return ScaffoldResult.forge_failure(
                message=f"Total Perception Collapse: {str(catastrophic_fracture)}",
                details=tb
            )

    def _scry_neighborhood(self, memory: Any, focus_id: str, depth: int = 2) -> Set[str]:
        """[ASCENSION 1]: Breadth-First Causal Slicing."""
        reachable = {focus_id}
        graph = memory.dependency_graph.get('dependency_graph', {})

        # Simple BFS
        current_layer = [focus_id]
        for _ in range(depth):
            next_layer = []
            for node in current_layer:
                # Add children
                children = graph.get(node, [])
                for c in children:
                    if c not in reachable:
                        reachable.add(c)
                        next_layer.append(c)
                # Add parents (reverse lookup)
                for potential_parent, children in graph.items():
                    if node in children and potential_parent not in reachable:
                        reachable.add(potential_parent)
                        next_layer.append(potential_parent)
            current_layer = next_layer
        return reachable

    def _scry_shadow_realities(self, existing_ids: Set[str]) -> List[Dict]:
        """[ASCENSION 3]: GHOST NODE PROJECTION."""
        ghosts = []
        staging = self.root / ".scaffold" / "staging"
        if not staging.exists(): return []

        for root, _, files in os.walk(staging):
            for f in files:
                abs_p = Path(root) / f
                rel_p = abs_p.relative_to(staging).as_posix()
                if rel_p not in existing_ids:
                    ghosts.append({
                        "id": rel_p,
                        "type": "ghost",
                        "label": f,
                        "x": 2000, "y": 2000,  # Push to Ethereal Quadrant
                        "data": {"path": rel_p, "status": "dreaming"}
                    })
        return ghosts

    def _divine_archetype(self, gnosis: Any) -> str:
        """Determines the visual node type based on filename heuristics."""
        path = str(gnosis.path).lower()
        if "service" in path: return "Service"
        if "controller" in path or "route" in path: return "Controller"
        if "model" in path or "schema" in path or "entity" in path: return "Model"
        if "view" in path or ".tsx" in path or "page" in path: return "View"
        if "main" in path or "app" in path or "index" in path: return "Gateway"
        return "Utility"

    def _is_heretical(self, src: str, tgt: str) -> bool:
        """
        Enforces Layered Sovereignty.
        Domain (High) cannot depend on API (Low).
        """
        s = src.lower()
        t = tgt.lower()

        # 1. Domain -> API/UI Violation
        if "domain" in s and ("api" in t or "ui" in t or "components" in t):
            return True

        # 2. Model -> Controller Violation
        if "model" in s and "controller" in t:
            return True

        return False

