# Path: scaffold/artisans/risk/artisan.py
# ---------------------------------------

from typing import List, Dict, Any
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import BusFactorRequest
from ...core.cortex.engine import GnosticCortex
from ...help_registry import register_artisan


@register_artisan("risk")
class BusFactorArtisan(BaseArtisan[BusFactorRequest]):
    """
    =============================================================================
    == THE ORACLE OF FRAGILITY (V-Ω-BUS-FACTOR-CALCULATOR)                     ==
    =============================================================================
    Calculates the 'Bus Factor' of the codebase.
    Identifies high-complexity scriptures maintained by a single soul.
    """

    def execute(self, request: BusFactorRequest) -> ScaffoldResult:
        self.logger.info("The Oracle of Fragility gazes upon the contributors...")

        # 1. Summon the Cortex (Structure & History)
        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()
        cortex.git_historian.inquire_all()

        risk_ledger = []

        # 2. The Rite of Correlation
        for item in memory.inventory:
            if item.category != 'code': continue

            # Get Structural Complexity
            complexity = item.ast_metrics.get("cyclomatic_complexity", 1)

            # Get Temporal Authorship
            history = cortex.git_historian.inquire(item.path)
            author_count = max(1, history.author_count)
            primary_author = history.primary_author or "Unknown"

            # The Formula of Fragility
            # We normalize complexity (log scale) to avoid skewing by massive files
            import math
            normalized_complexity = math.log1p(complexity)

            # Risk increases with complexity, decreases with author count
            risk_score = normalized_complexity / author_count

            if risk_score > (1.0 - request.threshold):
                risk_ledger.append({
                    "path": item.path,
                    "score": risk_score,
                    "complexity": complexity,
                    "authors": author_count,
                    "owner": primary_author
                })

        # 3. Sort by Risk
        risk_ledger.sort(key=lambda x: x['score'], reverse=True)
        top_risks = risk_ledger[:request.limit]

        if not top_risks:
            return self.success("The Knowledge is well-distributed. No critical fragility detected.")

        # 4. The Luminous Proclamation
        table = Table(title="[bold red]The Bus Factor Heatmap[/bold red]", border_style="red")
        table.add_column("Risk", justify="right", style="bold red")
        table.add_column("Scripture", style="cyan")
        table.add_column("Complexity", justify="right")
        table.add_column("Authors", justify="right")
        table.add_column("Sole Keeper (The Hero/Victim)", style="yellow")

        for entry in top_risks:
            table.add_row(
                f"{entry['score']:.2f}",
                str(entry['path']),
                str(entry['complexity']),
                str(entry['authors']),
                entry['owner']
            )

        self.console.print(table)

        # 5. The Mentor's Advice
        suggestion = Text.from_markup(
            "\n[bold]Mentor's Guidance:[/bold] The files above are complex but understood by few. "
            f"Conduct a [bold green]Code Review[/bold green] with {top_risks[0]['owner']} to diffuse this risk."
        )
        self.console.print(Panel(suggestion, border_style="yellow"))

        return self.success(f"Identified {len(risk_ledger)} fragile zones.", data=risk_ledger)