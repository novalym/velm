# Path: scaffold/artisans/lint/artisan.py
# ---------------------------------------
import json
from pathlib import Path
from typing import List

from rich.panel import Panel
from rich.table import Table
from rich.console import Group
from rich.text import Text

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import LintRequest
from ...core.state.gnostic_db import GnosticDatabase, SQL_AVAILABLE
from ...core.cortex.engine import GnosticCortex
from .engine import GnosticLintEngine
from .contracts import LintContext, HeresySeverity


class LintArtisan(BaseArtisan[LintRequest]):
    """
    =================================================================================
    == THE GNOSTIC MENTOR (V-Ω-PLUGGABLE-INTELLIGENCE)                             ==
    =================================================================================
    The High Priest of Architectural Purity. It summons the GnosticLintEngine to
    adjudicate the reality of the project against the Eternal Laws.
    """

    def execute(self, request: LintRequest) -> ScaffoldResult:
        self.console.rule("[bold magenta]The Gnostic Mentor's Gaze[/bold magenta]")

        # 1. Forge the Context
        db_session = None
        if SQL_AVAILABLE:
            db = GnosticDatabase(self.project_root)
            db_session = db.session

        # We need the Cortex to perceive the file inventory
        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()  # Fast if cached

        context = LintContext(
            project_root=self.project_root,
            db_session=db_session,
            cortex_memory=memory,
            fix_mode=request.fix
        )

        # 2. Summon the Engine
        engine = GnosticLintEngine()

        # 3. Conduct the Inquest
        with self.console.status("[yellow]Consulting the Grimoires...[/yellow]"):
            issues = engine.conduct_inquest(context)

        # 4. Cleanup
        if db_session:
            db_session.close()

        # 5. Proclaim Results
        if request.json_output:
            return self._proclaim_json(issues)

        return self._proclaim_luminous(issues)

    def _proclaim_json(self, issues: List) -> ScaffoldResult:
        data = [
            {
                "rule": i.rule_id,
                "severity": i.severity.value,
                "path": str(i.path),
                "message": i.message
            }
            for i in issues
        ]
        import json
        print(json.dumps(data, indent=2))
        return self.success("Linting complete.", data=data)

    def _proclaim_luminous(self, issues: List) -> ScaffoldResult:
        if not issues:
            self.console.print(Panel(
                "[bold green]The Gaze is serene. The architecture is pure.[/bold green]",
                title="[green]Gnostic Purity Achieved[/green]",
                border_style="green"
            ))
            return self.success("No heresies found.")

        # Group by Category
        by_category = {}
        for i in issues:
            rule_cat = i.rule_id.split('.')[0].title()
            by_category.setdefault(rule_cat, []).append(i)

        for cat, cat_issues in by_category.items():
            table = Table(box=None, padding=(0, 1), show_header=True)
            table.add_column("Severity", width=10)
            table.add_column("Location", style="cyan")
            table.add_column("Heresy", style="white")

            for i in cat_issues:
                sev_color = "red" if i.severity == HeresySeverity.CRITICAL else "yellow"
                loc = str(i.path.relative_to(self.project_root)) if i.path else "Project Root"
                msg = Text(i.message)
                if i.suggestion:
                    msg.append(f"\n💡 {i.suggestion}", style="dim italic")

                table.add_row(f"[{sev_color}]{i.severity.value}[/{sev_color}]", loc, msg)

            self.console.print(Panel(
                table,
                title=f"[bold]{cat} Heresies[/bold]",
                border_style="red" if any(i.severity == HeresySeverity.CRITICAL for i in cat_issues) else "yellow"
            ))

        return self.failure(f"The Mentor perceived {len(issues)} heresies.")