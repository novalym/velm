# Path: scaffold/artisans/graph/architect.py
# ------------------------------------------
import json
import textwrap
from pathlib import Path
from typing import Dict, List, Any

from ...interfaces.requests import CreateRequest
from ...interfaces import ScaffoldResult
from ...core.kernel.transaction import GnosticTransaction
from .layout import LayoutManager
from ...logger import Scribe

Logger = Scribe("GraphArchitect")


class GnosticArchitect:
    """The Hand of Will. Transmutes Graph Intent into physical files."""

    def __init__(self, engine: Any, root: Path):
        self.engine = engine
        self.root = root
        self.layout_manager = LayoutManager(root)

    def manifest(self, graph_data: Dict[str, Any], dry_run: bool) -> Any:
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])

        # [ASCENSION 7]: Atomic Transaction
        with GnosticTransaction(self.root, "Topological Manifestation", simulate=dry_run) as tx:
            # 1. Update Spatial Records
            self.layout_manager.save(nodes)

            # 2. Identify new souls requiring creation
            for node in nodes:
                path = self.root / node['data']['path']
                if not path.exists():
                    # Invoke the Synthesizer
                    content = self._synthesize_content(node, edges, nodes)

                    # [ASCENSION 7]: Dispatch individual creation rites within the transaction
                    create_req = CreateRequest(
                        paths=[str(path)],
                        content=content,
                        force=True
                    )
                    self.engine.dispatch(create_req)

        return ScaffoldResult(success=True, message="Physical reality aligned with Graph.")

    def _synthesize_content(self, node: Dict, edges: List[Dict], all_nodes: List[Dict]) -> str:
        """Generates boilerplate and imports based on graph connections."""
        label = node['label']
        # Find imports by looking at outgoing edges
        imports = []
        for edge in edges:
            if edge['source'] == node['id']:
                target = next((n for n in all_nodes if n['id'] == edge['target']), None)
                if target:
                    imports.append(f"import {{ {target['label']} }} from './{target['label'].lower()}';")

        import_block = "\n".join(imports)
        return textwrap.dedent(f"""
            {import_block}
            // {label}
            // Forged via Gnostic Graph Architecture
            export class {label.replace(' ', '')} {{
                // Logic here
            }}
        """).strip()