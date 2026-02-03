# === [scaffold/artisans/distill/core/oracle/scribe/topology.py] ===
from pathlib import Path
from typing import Iterator
from ...governance.contracts import RepresentationTier


class TopologyHerald:
    """
    =============================================================================
    == THE MAP MAKER (V-Ω-MERMAID-SCRIBE)                                      ==
    =============================================================================
    Renders the Logic Flow Graph.
    """

    def __init__(self, root: Path):
        self.root = root

    def proclaim(self, ctx) -> Iterator[str]:
        if not ctx.memory: return

        active_paths = {str(p).replace('\\', '/') for p, t in ctx.governance_plan.items() if
                        t != RepresentationTier.EXCLUDED.value}
        deps = ctx.memory.dependency_graph.get('dependency_graph', {})

        yield "#\n# ## 🕸️ Logic Flow Graph (LFG)\n# ```mermaid\n# graph TD;\n"

        # Cluster by directory
        clusters = {}
        for path in active_paths:
            parent = str(Path(path).parent).replace('\\', '/')
            if parent == '.': parent = 'Root'
            clusters.setdefault(parent, []).append(path)

        for folder, files in clusters.items():
            folder_id = self._slugify(folder)
            yield f"#   subgraph {folder_id} [{folder}]\n"
            for f in files:
                node_id = self._slugify(f)
                yield f"#     {node_id}[{Path(f).name}]\n"
            yield "#   end\n"

        # Edges
        for source, targets in deps.items():
            if source not in active_paths: continue
            src_id = self._slugify(source)
            for target in targets:
                if target not in active_paths: continue
                tgt_id = self._slugify(target)
                yield f"#     {src_id} --> {tgt_id}\n"

        yield "# ```\n#\n"

    def _slugify(self, path: str) -> str:
        return path.replace('/', '_').replace('.', '_').replace('-', '_')