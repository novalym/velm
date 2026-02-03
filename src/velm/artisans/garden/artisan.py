# Path: artisans/garden/artisan.py
# --------------------------------
from typing import List, Optional, Set
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import GardenRequest
from ...help_registry import register_artisan
from .analyst import GardenAnalyst
from .pruner import GardenPruner
from .contracts import WitheredVine


@register_artisan("garden")
class GardenArtisan(BaseArtisan[GardenRequest]):
    """
    =================================================================================
    == THE ENTROPY GARDEN (V-Ω-AUTONOMOUS-PRUNER-ASCENDED)                         ==
    =================================================================================
    LIF: INFINITY

    The Autonomous Maintenance System.
    1. Scans the graph for dead files.
    2. Scans the AST for dead functions/classes (Aggressive Mode).
    3. Performs surgical removal.
    """

    def execute(self, request: GardenRequest) -> ScaffoldResult:
        self.logger.info("The Gardener walks the codebase...")

        analyst = GardenAnalyst(self.project_root)

        with self.console.status("[bold green]Analyzing Gnostic Graph...[/bold green]"):
            vines = analyst.find_withered_vines(aggressive_level=request.aggressiveness)

        if not vines:
            return self.success("The Garden is lush. No withered vines found.")

        # Display Report
        self._proclaim_weeds(vines)

        if request.garden_command == "report":
            return self.success(f"Found {len(vines)} candidates.", data=[v.__dict__ for v in vines])

        elif request.garden_command == "prune":
            if not request.force:
                if not Confirm.ask(f"\n[bold red]Prune these {len(vines)} items?[/bold red]"):
                    return self.success("The shears are stayed.")

            pruner = GardenPruner(self.project_root)

            # Guardian's Offer
            self.guarded_execution([v.path for v in vines], request, context="garden_prune")

            count = pruner.prune(vines)
            return self.success(f"Pruning complete. {count} items removed.")

        # Default scan behavior
        return self.success(f"Scan complete. Found {len(vines)} candidates.")

    def _proclaim_weeds(self, vines: List[WitheredVine]):
        table = Table(title="[bold red]Withered Vines (Dead Code)[/bold red]", border_style="red")
        table.add_column("Type", style="magenta")
        table.add_column("Name", style="yellow")
        table.add_column("Location", style="cyan")
        table.add_column("Reason", style="dim")

        for v in vines:
            loc = v.path.relative_to(self.project_root)
            if v.line_num > 0:
                loc = f"{loc}:{v.line_num}"
            table.add_row(v.type.title(), v.name, str(loc), v.reason)

        self.console.print(Panel(table, border_style="red"))