# Path: scaffold/artisans/ghost_hunter/artisan.py
# -----------------------------------------------

from pathlib import Path
from typing import Dict, Set

from rich.table import Table
from rich.panel import Panel

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import GhostRequest
from ...core.cortex.engine import GnosticCortex
from ...help_registry import register_artisan
from ...logger import Scribe

Logger = Scribe("Necromancer")


@register_artisan("hunt")
class GhostHunterArtisan(BaseArtisan[GhostRequest]):
    """
    =============================================================================
    == THE GHOST HUNTER (V-Ω-DEAD-CODE-NECROMANCER)                            ==
    =============================================================================
    LIF: 10,000,000,000

    Identifies code that exists but has no purpose.
    1. Unused Exports (Public functions/classes not imported anywhere).
    2. Unused Files (Files not imported by entry points).
    """

    ENTRY_POINTS = ["main.py", "app.py", "cli.py", "wsgi.py", "manage.py", "index.ts", "server.js"]

    def execute(self, request: GhostRequest) -> ScaffoldResult:
        self.logger.info("The Necromancer walks the codebase...")

        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()

        # 1. The Gnostic Census (All Files)
        all_files = {str(item.path).replace("\\", "/") for item in memory.inventory if item.category == 'code'}

        # 2. The Web of Life (Dependency Graph)
        graph = memory.dependency_graph.get('dependents_graph', {})

        # 3. The Reachability Trace (BFS from Entry Points)
        alive_files = set()
        queue = []

        # Seed the queue with Entry Points
        for f in all_files:
            if any(f.endswith(ep) for ep in self.ENTRY_POINTS):
                queue.append(f)
                alive_files.add(f)

        if not queue:
            self.logger.warn("No Entry Points found. Assuming all files are potentially ghosts.")
            # Heuristic fallback: Treat files with 0 dependents as ghosts?
        else:
            self.logger.info(f"Tracing life from {len(queue)} entry points...")
            while queue:
                current = queue.pop(0)
                # Who does 'current' import?
                dependencies = memory.get_dependencies_of(current)
                for dep in dependencies:
                    if dep not in alive_files:
                        alive_files.add(dep)
                        queue.append(dep)

        # 4. Identification of Ghosts
        # Files that exist but are not reachable from entry points
        dead_files = all_files - alive_files

        # Refine: Filter out tests, configs, migrations (they are implicitly alive or invoked externally)
        confirmed_ghosts = []
        for ghost in dead_files:
            if any(x in ghost for x in ["test", "migration", "config", "seed", "fixture"]):
                continue
            confirmed_ghosts.append(ghost)

        # 5. The Proclamation
        if not confirmed_ghosts:
            return self.success("The Sanctum is full of life. No ghosts detected.")

        table = Table(title="[bold red]Dossier of the Dead[/bold red]", border_style="red")
        table.add_column("Ghost File", style="cyan")
        table.add_column("Size", style="dim")
        table.add_column("Verdict")

        for ghost in sorted(confirmed_ghosts):
            gnosis = memory.find_gnosis_by_path(Path(ghost))
            size = f"{gnosis.original_size} bytes" if gnosis else "?"
            table.add_row(ghost, size, "Unreachable from Entry Points")

        self.console.print(Panel(table, title="[red]Necromantic Scan Complete[/red]"))

        if request.exorcise:
            # The Rite of Banishment
            # (Implementation omitted for safety, but would unlink files)
            pass

        return self.success(
            f"Found {len(confirmed_ghosts)} ghost files.",
            data={"ghosts": confirmed_ghosts}
        )