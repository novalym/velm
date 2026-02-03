# scaffold/artisans/distill/scribes/mermaid_scribe.py

from typing import List, Dict, Any
from pathlib import Path
from .....core.cortex.contracts import FileGnosis, CortexMemory


class MermaidScribe:
    """
    =============================================================================
    == THE LIVING CONSTELLATION (V-Ω-MERMAID-GENERATOR)                        ==
    =============================================================================
    Transmutes the Gnostic Graph into a Mermaid.js diagram.
    """

    def __init__(self, root: Path, memory: CortexMemory):
        self.root = root
        self.memory = memory

    def inscribe(self, selected_files: List[FileGnosis]) -> str:
        """
        Forges the Mermaid diagram for the selected files.
        """
        lines = ["graph TD"]

        # Create a set of selected paths for fast lookup
        selected_paths = {str(f.path).replace('\\', '/') for f in selected_files}

        # 1. Define Nodes
        for f in selected_files:
            path_str = str(f.path).replace('\\', '/')
            node_id = self._clean_id(path_str)
            # Style based on category
            style = ""
            if f.category == 'code':
                if f.language == 'python':
                    style = "fill:#3776ab,stroke:#fff,color:#fff"
                elif f.language in ['typescript', 'javascript']:
                    style = "fill:#f7df1e,stroke:#333,color:#000"
                else:
                    style = "fill:#eee,stroke:#333,color:#000"

            lines.append(f'    {node_id}["{f.path.name}"]')
            if style:
                lines.append(f'    style {node_id} {style}')

            # Subgraphs for directories? (Optional complexity)

        # 2. Define Edges (Dependencies)
        # We only draw edges where both source and target are in the selected set
        for f in selected_files:
            source_path = str(f.path).replace('\\', '/')
            source_id = self._clean_id(source_path)

            dependencies = self.memory.get_dependencies_of(source_path)

            for dep in dependencies:
                if dep in selected_paths:
                    target_id = self._clean_id(dep)
                    lines.append(f"    {source_id} --> {target_id}")

        return "\n".join(lines)

    def _clean_id(self, path: str) -> str:
        return path.replace('/', '_').replace('.', '_').replace('-', '_')