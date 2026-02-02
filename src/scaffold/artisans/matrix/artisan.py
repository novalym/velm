# Path: scaffold/artisans/matrix/artisan.py
# -----------------------------------------

import json
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict

try:
    import toml

    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import MatrixRequest
from ...help_registry import register_artisan
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree


@register_artisan("matrix")
class MatrixArtisan(BaseArtisan[MatrixRequest]):
    """
    =============================================================================
    == THE DEPENDENCY MATRIX (V-Ω-VERSION-SEER)                                ==
    =============================================================================
    LIF: 10,000,000,000

    Analyses lockfiles to reveal the true state of the supply chain.
    Highlights duplicate versions (dependency hell).
    """

    def execute(self, request: MatrixRequest) -> ScaffoldResult:
        self.logger.info("The Matrix Seer awakens...")

        # 1. Harvest Gnosis
        npm_graph = self._analyze_npm()
        poetry_graph = self._analyze_poetry()

        full_graph = {**npm_graph, **poetry_graph}

        if not full_graph:
            return self.failure("No lockfiles (package-lock.json, poetry.lock) found.")

        # 2. Analyze Conflicts
        conflicts = {}
        for pkg, versions in full_graph.items():
            if len(versions) > 1:
                conflicts[pkg] = versions

        # 3. Proclaim
        if request.format == "json":
            return self.success("Matrix calculated.", data={"dependencies": full_graph, "conflicts": conflicts})

        self._render_tui(full_graph, conflicts)
        return self.success(f"Matrix analyzed. {len(conflicts)} conflict(s) detected.")

    def _analyze_npm(self) -> Dict[str, Set[str]]:
        """Parses package-lock.json for installed versions."""
        lock_path = self.project_root / "package-lock.json"
        graph = defaultdict(set)

        if not lock_path.exists(): return {}

        try:
            data = json.loads(lock_path.read_text(encoding='utf-8'))

            # Modern NPM (v2/v3 lockfile) - Flattened 'packages'
            if "packages" in data:
                for path, info in data["packages"].items():
                    if not path: continue  # Skip root
                    name = path.split("node_modules/")[-1]
                    version = info.get("version")
                    if name and version:
                        graph[name].add(version)

            # Legacy NPM (v1) - Nested 'dependencies'
            elif "dependencies" in data:
                self._recurse_npm_v1(data["dependencies"], graph)

        except Exception as e:
            self.logger.warn(f"Failed to parse NPM matrix: {e}")

        return graph

    def _recurse_npm_v1(self, deps: Dict, graph: Dict):
        for name, info in deps.items():
            graph[name].add(info.get("version"))
            if "dependencies" in info:
                self._recurse_npm_v1(info["dependencies"], graph)

    def _analyze_poetry(self) -> Dict[str, Set[str]]:
        """Parses poetry.lock."""
        if not TOML_AVAILABLE: return {}
        lock_path = self.project_root / "poetry.lock"
        graph = defaultdict(set)

        if not lock_path.exists(): return {}

        try:
            data = toml.loads(lock_path.read_text(encoding='utf-8'))
            for pkg in data.get("package", []):
                graph[pkg["name"]].add(pkg["version"])
        except Exception as e:
            self.logger.warn(f"Failed to parse Poetry matrix: {e}")

        return graph

    def _render_tui(self, graph: Dict[str, Set[str]], conflicts: Dict[str, Set[str]]):
        if conflicts:
            conflict_table = Table(title="[bold red]Dependency Conflicts (Multiple Versions)[/bold red]",
                                   border_style="red")
            conflict_table.add_column("Package", style="cyan")
            conflict_table.add_column("Versions Installed", style="yellow")

            for pkg, versions in sorted(conflicts.items()):
                conflict_table.add_row(pkg, ", ".join(sorted(list(versions))))

            self.console.print(conflict_table)
            self.console.print()

        # Summary Tree
        tree = Tree(f"[bold]Dependency Matrix ({len(graph)} packages)[/bold]")

        # Sort by status (conflicted first) then name
        sorted_keys = sorted(graph.keys(), key=lambda k: (0 if k in conflicts else 1, k))

        for pkg in sorted_keys:
            versions = sorted(list(graph[pkg]))
            if pkg in conflicts:
                label = f"[red]{pkg}[/red] -> {', '.join(versions)}"
            else:
                label = f"[green]{pkg}[/green] {versions[0]}"
            tree.add(label)

        self.console.print(Panel(tree, border_style="blue"))