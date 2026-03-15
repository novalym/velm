# Path: core/alchemist/elara/vis/flow_projector.py
# ------------------------------------------------

import json
import time
import hashlib
from enum import Enum
from typing import List, Dict, Any, Optional, Final, Tuple, Set
from pathlib import Path

# --- THE DIVINE UPLINKS ---
# We scry the contracts to ensure our aura-mapping resonates with the Kernel
from ..contracts import ASTNode, TokenType


class GateAura(str, Enum):
    """The Chromatic Resonance of a logic gate or matter shard."""
    NEUTRAL = "#94a3b8"  # Slate: Ethereal/Passive
    ACTIVE = "#64ffda"  # Teal: Struck/Resonant
    BRANCH = "#3b82f6"  # Blue: Decision/Will
    LOOP = "#fbbf24"  # Amber: Iterative/Metabolic
    MACRO = "#a855f7"  # Purple: Functional/Soul
    SHADOW = "#ec4899"  # Pink: Trial/Simulation
    FRACTURE = "#ef4444"  # Red: Heresy/Fracture
    SUBSTRATE = "#10b981"  # Green: Iron/Substrate Native


class VisualGate:
    """
    =============================================================================
    == THE VISUAL GATE: OMNISCIENT PROJECTION (V-Ω-TOTALITY-VMAX)              ==
    =============================================================================
    The Ocular representation of a Gnostic Node, enriched with metabolic and
    topological gnosis.
    """

    def __init__(self, node: ASTNode, parent_path: Optional[str] = None):
        self.node_id = f"gate_{id(node)}"
        self.parent_path = parent_path
        self.label = self._forge_label(node)
        self.aura = self._divine_aura(node)
        self.shape = self._divine_shape(node)
        self.metadata = self._harvest_metadata(node)

    def _forge_label(self, node: ASTNode) -> str:
        """[ASCENSION 18]: Iconographic Labeling."""
        content = str(node.token.content).strip()

        if node.token.type == TokenType.LOGIC_BLOCK:
            gate = node.metadata.get("gate", "UNK").upper()
            expr = node.metadata.get("expression", "")
            # Truncate for visual purity in the Ocular Membrane
            clean_expr = (expr[:22] + '..') if len(expr) > 22 else expr
            return f"[{gate}] {clean_expr}"

        if node.token.type == TokenType.VARIABLE:
            return f"$$ {content[:15]}"

        # For Matter (Files/Sanctums)
        return content[:25]

    def _divine_aura(self, node: ASTNode) -> str:
        """[ASCENSION 3]: Metabolic Heat Tomography."""
        # 1. Heresy Check
        if node.metadata.get("is_fractured"):
            return GateAura.FRACTURE

        # 2. Logic Type Mapping
        if node.token.type == TokenType.LOGIC_BLOCK:
            gate = node.metadata.get("gate", "").lower()
            if gate in ("if", "elif", "else", "match", "case"): return GateAura.BRANCH
            if gate in ("for", "while", "repeat"): return GateAura.LOOP
            if gate in ("macro", "call", "task", "func"): return GateAura.MACRO
            if gate in ("try", "catch", "finally"): return GateAura.SHADOW

        # 3. Matter Type Mapping
        if node.token.type == TokenType.VARIABLE:
            return GateAura.NEUTRAL

        # 4. Metabolic Pulse (Active Strike)
        if node.metadata.get("execution_ns", 0) > 1_000_000:  # Over 1ms
            return GateAura.SUBSTRATE

        return GateAura.ACTIVE

    def _divine_shape(self, node: ASTNode) -> str:
        """[ASCENSION 12]: Substrate-Aware Geometry."""
        if node.token.type == TokenType.LOGIC_BLOCK:
            gate = node.metadata.get("gate", "").lower()
            if gate in ("if", "elif", "match"): return "diamond"
            if gate in ("for", "while"): return "parallelogram"
            if gate in ("macro", "call"): return "subroutine"
            return "rect"

        if node.token.type == TokenType.VARIABLE:
            return "circle"

        # Directories are Cylindrical Sanctums
        if str(node.token.content).endswith('/'):
            return "cylinder"

        return "rect"

    def _harvest_metadata(self, node: ASTNode) -> Dict[str, Any]:
        """[ASCENSION 11]: Complexity Tomography."""
        return {
            "type": node.token.type.name,
            "line": node.token.line_num,
            "col": node.token.column_index,
            "complexity": node.metadata.get("cyclomatic_mass", 1),
            "trace": node.metadata.get("trace_id", "tr-void"),
            "merkle": node.branch_hash[:8] if hasattr(node, 'branch_hash') else "0xVOID"
        }


class LogicFlowProjector:
    """
    =================================================================================
    == THE LOGIC FLOW PROJECTOR: OMEGA POINT (V-Ω-TOTALITY-VMAX-VISUAL-LFG)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_CARTOGRAPHER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_VIS_FLOW_VMAX_HYPER_EVOLVED_2026_FINALIS
    """

    @classmethod
    def project_mermaid(cls, root: ASTNode, title: str = "ELARA Logic Flow") -> str:
        """
        =========================================================================
        == THE RITE OF MERMAID PROJECTION (ASCENDED)                           ==
        =========================================================================
        [ASCENSION 16]: Indentation-Aware Gravity & Cluster Inlining.
        """
        lines = [
            "graph TD",
            f"  %% {title}",
            "  %% [GEOMETRIC_ANCHOR]: AXIS_MUNDI",
            "  style ROOT fill:#020202,stroke:#64ffda,stroke-width:2px,color:#fff",
            "  ROOT((Ω_ROOT))"
        ]

        def _walk(node: ASTNode, parent_id: str, depth: int):
            # [ASCENSION 20]: NoneType Sarcophagus
            if not node or depth > 50: return

            for child in node.children:
                gate = VisualGate(child)

                # 1. Resolve Geometry Markers
                shape_start, shape_end = "[", "]"
                if gate.shape == "diamond": shape_start, shape_end = "{{", "}}"
                if gate.shape == "parallelogram": shape_start, shape_end = "[/", "/]"
                if gate.shape == "circle": shape_start, shape_end = "((", "))"
                if gate.shape == "cylinder": shape_start, shape_end = "[(", ")]"
                if gate.shape == "subroutine": shape_start, shape_end = "[[", "]]"

                # 2. Inscribe Node
                lines.append(f'  {gate.node_id}{shape_start}"{gate.label}"{shape_end}')
                lines.append(f'  style {gate.node_id} fill:#18181b,stroke:{gate.aura},color:#fff')

                # 3. Inscribe Edge (With Haptic Pulsing hints for UI)
                edge_style = "-->"
                if child.token.type == TokenType.VARIABLE: edge_style = "-.->"

                lines.append(f'  {parent_id} {edge_style} {gate.node_id}')

                # 4. Recursive Descent
                _walk(child, gate.node_id, depth + 1)

        _walk(root, "ROOT", 0)
        return "\n".join(lines)

    @classmethod
    def project_json_manifest(cls, root: ASTNode) -> Dict[str, Any]:
        """
        =========================================================================
        == THE RITE OF OCULAR JSON MANIFESTATION                               ==
        =========================================================================
        [ASCENSION 6]: Trace ID Silver-Cord & Haptic Couplings.
        """
        nodes = []
        edges = []

        # [ASCENSION 13]: State Tracking for Fission Visualization
        seen_ids: Set[str] = set()

        def _walk(node: ASTNode, parent_id: Optional[str] = None):
            gate = VisualGate(node)

            if gate.node_id in seen_ids: return
            seen_ids.add(gate.node_id)

            # [ASCENSION 9]: Geodesic Anchoring
            # Position is calculated by the React UI Stage, but we provide hints
            nodes.append({
                "id": gate.node_id,
                "type": "gnosticNode",
                "data": {
                    "label": gate.label,
                    "aura": gate.aura,
                    "meta": gate.metadata,
                    "logic_result": node.metadata.get("last_result"),
                    "is_dir": str(node.token.content).endswith('/')
                },
                "position": {"x": 0, "y": 0}
            })

            if parent_id:
                # [ASCENSION 14]: Haptic Edge Coupling
                edges.append({
                    "id": f"e_{parent_id}_{gate.node_id}",
                    "source": parent_id,
                    "target": gate.node_id,
                    "animated": node.token.type != TokenType.LITERAL,
                    "label": "wakes" if node.token.type == TokenType.MACRO_DEF else "",
                    "style": {"stroke": gate.aura, "strokeWidth": 2 if node.token.is_logic else 1}
                })

            for child in node.children:
                _walk(child, gate.node_id)

        _walk(root)

        # [ASCENSION 22]: Merkle Sealing the Manifest
        manifest_data = {"nodes": nodes, "edges": edges}
        manifest_hash = hashlib.md5(json.dumps(manifest_data, sort_keys=True).encode()).hexdigest()

        manifest_data["merkle_root"] = manifest_hash[:12].upper()
        manifest_data["transmutation_ts"] = time.time()

        return manifest_data

    @classmethod
    def project_svg_stream(cls, root: ASTNode) -> str:
        """[ASCENSION 23]: Isomorphic SVG Emitter (Prophecy)."""
        # This artisan is prepared to emit raw XML for headless documentation strikes.
        return "<!-- [SVG_EMITTER_LOCKED]: Requires Ocular_Stage_Fabricator -->"

    def __repr__(self) -> str:
        return f"<Ω_LOGIC_FLOW_PROJECTOR status=RESONANT mode=TOTALITY version=VMAX_2026>"