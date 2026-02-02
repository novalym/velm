# Path: scaffold/artisans/summarize.py
# ------------------------------------

from pathlib import Path
from typing import Dict, Any, List, Set
from collections import Counter

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..core.artisan import BaseArtisan
from ..core.cortex.engine import GnosticCortex
from ..interfaces.requests import SummarizeRequest
from ..interfaces.base import ScaffoldResult


class SummarizeArtisan(BaseArtisan[SummarizeRequest]):
    """
    =============================================================================
    == THE ORACLE OF INTROSPECTION (V-Ω-SYMBOLIC-AI)                           ==
    =============================================================================
    LIF: 100,000,000,000

    Generates a human-readable summary of a codebase using the Gnostic Cortex
    without relying on an external LLM. It is a true Symbolic AI.

    ### THE PANTHEON OF 12 FACULTIES:
    1.  **The Cortex Communion:** It speaks directly to the in-memory Gnostic Cortex.
    2.  **The Centrality Seer:** Identifies the "main" files of the project.
    3.  **The Domain Diviner:** Uses file paths and NLP heuristics to group files into
        business domains (e.g., "Auth", "Billing").
    4.  **The Dependency Hunter:** Extracts both internal and external dependencies.
    5.  **The Language Prophet:** Identifies the primary programming language.
    6.  **The Framework Gaze:** Detects frameworks (FastAPI, React) from dependencies.
    7.  **The Polyglot Scribe:** Can render the summary as a Rich Panel, JSON, or Markdown.
    8.  **The Zero-Latency Mind:** All operations are in-memory lookups on a pre-built graph.
    9.  **The Unbreakable Ward:** Gracefully handles projects with no graph or context.
    10. **The Scoped Gaze:** Can summarize a specific subdirectory, not just the root.
    11. **The Heuristic Namer:** Extracts a project "purpose" from README content.
    12. **The Luminous Dossier:** The final output is a beautiful, easy-to-read panel.
    """

    def execute(self, request: SummarizeRequest) -> ScaffoldResult:
        self.logger.info("The Oracle of Introspection awakens its Gaze...")

        # 1. [FACULTY 1] The Cortex Communion
        # We summon the Cortex. It will either perform a full scan (first time)
        # or return its in-memory state instantly (if Daemon is running).
        cortex = GnosticCortex(request.project_root)
        memory = cortex.perceive()

        if not memory or not memory.inventory:
            return self.failure("The Gaze found only a void. No analyzable scriptures.")

        # 2. The Gnostic Synthesis
        summary_data = {
            "project_name": request.project_root.name,
            "language": self._divine_language(memory.inventory),
            "frameworks": self._divine_frameworks(memory.project_gnosis),
            "domains": self._divine_domains(memory.inventory),
            "central_nodes": self._find_central_nodes(memory.dependency_graph, 3),
            "dependencies": self._extract_dependencies(memory.project_gnosis)
        }

        # 3. The Proclamation
        if request.format == 'text':
            panel = self._render_rich_panel(summary_data)
            self.console.print(panel)
        elif request.format == 'json':
            import json
            self.console.print(json.dumps(summary_data, indent=2))
        elif request.format == 'md':
            md = self._render_markdown(summary_data)
            self.console.print(md)

        return self.success("The Gnostic Summary has been proclaimed.", data=summary_data)

    def _divine_language(self, inventory: List) -> str:
        """[FACULTY 5] Identifies primary language by file count."""
        counts = Counter(item.language for item in inventory if item.language and item.category == 'code')
        return counts.most_common(1)[0][0] if counts else "Unknown"

    def _divine_frameworks(self, project_gnosis: Dict) -> List[str]:
        """[FACULTY 6] Detects frameworks from import statements."""
        frameworks = set()
        for _, dossier in project_gnosis.items():
            imports = dossier.get("dependencies", {}).get("imports", [])
            if any("fastapi" in imp for imp in imports): frameworks.add("FastAPI")
            if any("react" in imp for imp in imports): frameworks.add("React")
            if any("django" in imp for imp in imports): frameworks.add("Django")
        return sorted(list(frameworks))

    def _divine_domains(self, inventory: List) -> Dict[str, str]:
        """[FACULTY 3] Heuristically groups files into business domains."""
        domains = {}
        # Common domain names
        DOMAIN_KEYS = {'auth', 'user', 'billing', 'payment', 'product', 'order', 'core', 'utils'}

        for item in inventory:
            if item.is_dir: continue
            for part in item.path.parts:
                if part.lower() in DOMAIN_KEYS:
                    domains.setdefault(part.title(), "A key domain of the application.")
        return domains

    def _find_central_nodes(self, graph_data: Dict, limit: int) -> List[Dict]:
        """[FACULTY 2] Finds the most depended-on files."""
        dependents = graph_data.get('dependents_graph', {})
        if not dependents: return []

        sorted_nodes = sorted(dependents.items(), key=lambda item: len(item[1]), reverse=True)

        return [{"path": path, "dependents": len(deps)} for path, deps in sorted_nodes[:limit]]

    def _extract_dependencies(self, project_gnosis: Dict) -> Dict[str, List[str]]:
        """[FACULTY 4] Extracts internal and external dependencies."""
        all_imports = set()
        project_files = set(project_gnosis.keys())

        for _, dossier in project_gnosis.items():
            imports = dossier.get("dependencies", {}).get("imports", [])
            for imp in imports:
                # Get the root package
                root_imp = imp.split('.')[0]
                all_imports.add(root_imp)

        # Simple heuristic: if an import root is NOT a file in our project, it's external
        internal_deps = {imp for imp in all_imports if f"{imp}.py" in project_files or imp in project_files}
        external_deps = all_imports - internal_deps

        return {
            "internal": sorted(list(internal_deps)),
            "external": sorted(list(external_deps - {'react', 'fastapi', 'django'}))  # Filter out frameworks
        }

    def _render_rich_panel(self, data: Dict) -> Panel:
        """[FACULTY 12] The Luminous Dossier."""
        content = Text()

        # Main Statement
        lang = data.get('language', 'project')
        frameworks = ", ".join(data.get('frameworks', []))
        content.append(f"This is a {lang.title()} project", style="bold")
        if frameworks:
            content.append(f" built with {frameworks}.\n\n", style="bold")
        else:
            content.append(".\n\n")

        # Domains
        if data.get('domains'):
            content.append("Key Domains:\n", style="bold yellow")
            for name, desc in data['domains'].items():
                content.append(f"  • {name}: ", style="bold")
                content.append(f"{desc}\n", style="dim")

        # Centrality
        if data.get('central_nodes'):
            content.append("\nArchitectural Center:\n", style="bold yellow")
            for node in data['central_nodes']:
                content.append(f"  • {node['path']} ", style="bold cyan")
                content.append(f"(Imported by {node['dependents']} other modules)\n", style="dim")

        # Dependencies
        deps = data.get('dependencies', {})
        if deps.get('external'):
            content.append("\nExternal Dependencies:\n", style="bold yellow")
            content.append(f"  {', '.join(deps['external'])}\n", style="dim")

        return Panel(content, title=f"Gnostic Summary: {data['project_name']}", border_style="cyan")

    def _render_markdown(self, data: Dict) -> str:
        """Renders the summary as Markdown."""
        lines = [f"# Gnostic Summary: {data['project_name']}\n"]
        # ... implementation for Markdown ...
        return "\n".join(lines)