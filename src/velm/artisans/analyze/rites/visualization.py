# Path: artisans/analyze/rites/visualization.py
# ---------------------------------------------

import time
import logging
from io import StringIO
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from rich.console import Console
from ....rendering import render_gnostic_tree
from ..structure_visualizer import StructureVisualizer

# [ASCENSION 1]: FORENSIC LOGGER
Logger = logging.getLogger("RiteOfVisualization")


class RiteOfVisualization:
    """
    =============================================================================
    == THE RITE OF VISUALIZATION (V-Ω-HOLOGRAPHIC-PROJECTION-V32)              ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: REALITY_RENDERER

    The Bridge between Abstract Data and Human Perception.
    It transmutes the parsed Atoms into:
    1. A JSON Topology for the Ocular UI (React).
    2. An ASCII Hologram for the Console/Logs.

    [CAPABILITIES]:
    - Content-Aware Nesting (Indentation Analysis).
    - Fault-Tolerant Rendering.
    - Polyglot Visualization (Scaffold vs Symphony).
    """

    @staticmethod
    def conduct(
            items: List,
            edicts: List,
            grammar: str,
            project_root: Optional[Path],
            content: str = "",  # [ASCENSION 2]: INJECTED CONTENT
            trace_id: str = "0xVOID"
    ) -> Tuple[List[Dict[str, Any]], str]:
        """
        Executes the Grand Projection.
        Returns: (JSON_Structure, ASCII_String)
        """
        start_time = time.perf_counter()

        # --- PHASE I: TOPOLOGICAL RECONSTRUCTION ---
        # We summon the StructureVisualizer to perform the heavy lifting of
        # Indentation Analysis and Parent Linking.
        visualizer = StructureVisualizer(grammar)

        # [THE FIX]: PASS CONTENT FOR DEEP RECONSTRUCTION
        structure = visualizer.visualize(items, edicts, content)

        # [ASCENSION 9]: NODE CENSUS
        node_count = len(structure)

        # --- PHASE II: ASCII HOLOGRAPHY ---
        ascii_tree = ""

        try:
            if not items and not edicts:
                # [ASCENSION 4]: VOID STATE HANDLING
                ascii_tree = RiteOfVisualization._render_void_state(grammar)

            elif grammar == "symphony" and edicts:
                # [ASCENSION 3]: SYMPHONY HIGH-FIDELITY
                ascii_tree = RiteOfVisualization._render_symphony_ascii(edicts)

            else:
                # [ASCENSION 6]: ROOT FALLBACK
                safe_root = project_root or Path.cwd()

                # [ASCENSION 2]: FAULT-TOLERANT SARCOPHAGUS
                ascii_tree = RiteOfVisualization._render_scaffold_ascii(items, safe_root)

        except Exception as e:
            Logger.error(f"[{trace_id}] Visualization Fracture: {e}")
            ascii_tree = f"!! HOLOGRAPHIC FAILURE: {str(e)} !!"

        # --- PHASE III: TELEMETRY ---
        duration_ms = (time.perf_counter() - start_time) * 1000

        # [ASCENSION 5]: CHRONOMETRIC LOGGING
        if duration_ms > 10:
            Logger.debug(f"[{trace_id}] Visualization generated ({node_count} nodes) in {duration_ms:.2f}ms")

        return structure, ascii_tree

    @staticmethod
    def _render_scaffold_ascii(items: List, root: Path) -> str:
        """
        Renders the classic Gnostic Tree using Rich.
        """
        try:
            # We use the shared rendering utility
            renderable = render_gnostic_tree(
                items,
                output_format='text',
                use_markup=True,
                project_root=root
            )

            # [ASCENSION 10]: MEMORY OPTIMIZATION
            f = StringIO()
            # [ASCENSION 7]: WIDTH CONSTRAINT (Prevent wrapping in logs)
            Console(file=f, force_terminal=False, width=120).print(renderable)
            return f.getvalue()

        except ImportError:
            # Fallback if Rich is missing (rare)
            return "\n".join([f"- {i.path}" for i in items])

    @staticmethod
    def _render_symphony_ascii(edicts: List) -> str:
        """
        Renders the Symphony of Will.
        """
        lines = ["🎼 SYMPHONY WORKFLOW"]
        lines.append("─────────────────────")

        for e in edicts:
            # [ASCENSION 12]: THEMATIC ICONS
            icon = "📄"
            if e.type == "ACTION":
                icon = "🚀"  # >>
            elif e.type == "VOW":
                icon = "⚖️"  # ??
            elif e.type == "STATE":
                icon = "💾"  # %%
            elif e.type == "CONDITIONAL":
                icon = "🔀"  # @if

            cmd = e.command or e.vow_type or e.state_key or "Unknown"
            lines.append(f"{icon} {cmd}")

        return "\n".join(lines)

    @staticmethod
    def _render_void_state(grammar: str) -> str:
        """Returns a visual representation of emptiness."""
        return f"∅ VOID SANCTUM ({grammar.upper()})\nNo artifacts manifest."