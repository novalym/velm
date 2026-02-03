# Path: scaffold/artisans/sgrep/artisan.py
# ----------------------------------------

import re
from typing import List, Dict, Any
from pathlib import Path

from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import SgrepRequest
from ...help_registry import register_artisan
from ...core.cortex.engine import GnosticCortex


@register_artisan("sgrep")
class SgrepArtisan(BaseArtisan[SgrepRequest]):
    """
    =============================================================================
    == THE SEMANTIC EYE (V-Ω-AST-SEARCH)                                       ==
    =============================================================================
    LIF: 10,000,000,000

    Searches the Gnostic Memory (AST) for symbols, not strings.
    """

    def execute(self, request: SgrepRequest) -> ScaffoldResult:
        pattern = re.compile(request.pattern, re.IGNORECASE)
        target_type = request.type  # function, class, any

        self.logger.info(f"The Semantic Eye opens... Searching for {target_type} matching /{request.pattern}/")

        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()

        hits = []

        # Iterate through the Project Gnosis (The AST Dossiers)
        for path_str, dossier in memory.project_gnosis.items():
            if "error" in dossier: continue

            # Search Functions
            if target_type in ("function", "any"):
                for func in dossier.get("functions", []):
                    if pattern.search(func["name"]):
                        hits.append(self._forge_hit(path_str, "Function", func))

            # Search Classes
            if target_type in ("class", "any"):
                for cls in dossier.get("classes", []):
                    if pattern.search(cls["name"]):
                        hits.append(self._forge_hit(path_str, "Class", cls))

        if not hits:
            return self.success("The Gaze returned no reflections.")

        # Proclaim Results
        self.console.rule(f"[bold green]Semantic Search Results ({len(hits)})[/bold green]")

        for hit in hits:
            self._render_hit(hit, request.show_code)

        return self.success(f"Found {len(hits)} semantic matches.")

    def _forge_hit(self, path: str, kind: str, node: Dict[str, Any]) -> Dict:
        return {
            "path": path,
            "kind": kind,
            "name": node["name"],
            "line": node["start_point"][0] + 1,
            "code_start": node["start_point"][0],
            "code_end": node["line_count"] + node["start_point"][0]
        }

    def _render_hit(self, hit: Dict, show_code: bool):
        header = f"[cyan]{hit['path']}[/cyan]:{hit['line']} [bold magenta]({hit['kind']}: {hit['name']})[/bold magenta]"

        if show_code:
            # We need to read the file to get the snippet (Cortex stores metadata, not full content in RAM usually)
            try:
                full_path = self.project_root / hit['path']
                content = full_path.read_text(encoding='utf-8').splitlines()
                # Get snippet
                snippet_lines = content[hit['code_start']:min(hit['code_end'], hit['code_start'] + 10)]
                snippet = "\n".join(snippet_lines)

                syntax = Syntax(snippet, "python", theme="monokai", line_numbers=True, start_line=hit['line'])
                self.console.print(Panel(syntax, title=header, border_style="dim"))
            except Exception:
                self.console.print(header)
        else:
            self.console.print(header)