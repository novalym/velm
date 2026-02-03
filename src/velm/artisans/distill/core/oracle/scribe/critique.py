# === [scaffold/artisans/distill/core/oracle/scribe/critique.py] - SECTION 1 of 1: The Gnostic Critic ===
from pathlib import Path
from typing import Iterator

from ..contracts import OracleContext


class CritiqueHerald:
    """
    =============================================================================
    == THE GNOSTIC CRITIC (V-Ω-ARCHITECTURAL-JUDGE)                            ==
    =============================================================================
    Appends a footer detailing architectural sins found during the graph build.
    It exposes Circular Dependencies and Layer Violations directly to the AI,
    so the AI knows the codebase is fragile before it attempts to modify it.
    """

    def __init__(self, root: Path):
        self.root = root

    def proclaim(self, ctx: OracleContext) -> Iterator[str]:
        if not ctx.memory: return

        # Retrieve Gnosis from the GraphBuilder's labor
        heresies = ctx.memory.dependency_graph.get('architectural_heresies', [])
        # Some GraphBuilders might put cycles in a separate key or within heresies
        # We check both to be safe.
        cycles = ctx.memory.dependency_graph.get('cycles', [])

        # Also check for explicit "Critical" heresies in the list
        critical_issues = [h for h in heresies if h.get('severity') == 'CRITICAL']

        if not heresies and not cycles:
            return

        yield "# ========================================================\n"
        yield "# 🛡️  GNOSTIC CRITIQUE (AUTO-GENERATED WARNINGS)\n"
        yield "#    The GraphBuilder has detected structural anomalies.\n"
        yield "# ========================================================\n"

        if cycles:
            yield "# [CRITICAL] Circular Dependencies Detected:\n"
            for cycle in cycles:
                # Cycle is usually a list of strings
                chain = " -> ".join(cycle) if isinstance(cycle, list) else str(cycle)
                yield f"#    - {chain}\n"
            yield "#\n"

        if heresies:
            yield "# [WARNING] Architectural Violations:\n"
            for h in heresies:
                htype = h.get('type', 'Violation')
                detail = h.get('detail', 'Unknown')
                yield f"#    - {htype}: {detail}\n"

        yield "\n"

