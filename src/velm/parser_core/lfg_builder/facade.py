# Path: parser_core/lfg_builder/facade.py
# ---------------------------------------

from pathlib import Path
from typing import Optional, List

from .builders.blueprint import BlueprintLFGBuilder
from .builders.codebase_python import PythonFlowBuilder
from .renderers.mermaid import MermaidRenderer
from ..parser import parse_structure


class LFGEngine:
    """
    =================================================================================
    == THE GNOSTIC CARTOGRAPHER FACADE (V-Ω-VISUAL-ENGINE)                         ==
    =================================================================================
    """

    def __init__(self, project_root: Path):
        self.root = project_root

    def generate_blueprint_lfg(self, blueprint_path: Path) -> str:
        """Parses a blueprint and returns Mermaid scripture."""
        # 1. Parse
        _, items, _, _, _, _ = parse_structure(blueprint_path)

        # 2. Build Graph
        builder = BlueprintLFGBuilder()
        graph = builder.build(items, title=blueprint_path.name)

        # 3. Render
        return MermaidRenderer.render(graph)

    def generate_codebase_lfg(self, target_path: Path) -> str:
        """Parses a source file and returns Mermaid scripture."""
        if target_path.suffix == '.py':
            builder = PythonFlowBuilder()
            graph = builder.build(target_path)
            return MermaidRenderer.render(graph)

        return "graph TD\nError[Unsupported Language]"

