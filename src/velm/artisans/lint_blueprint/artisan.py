# Path: scaffold/artisans/lint_blueprint/artisan.py
# -------------------------------------------------

from pathlib import Path
from rich.table import Table
from rich.panel import Panel

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import LintBlueprintRequest
from ...help_registry import register_artisan
from ...parser_core.parser import ApotheosisParser


@register_artisan("lint-blueprint")
class BlueprintLinterArtisan(BaseArtisan[LintBlueprintRequest]):
    """
    =============================================================================
    == THE ARCHITECT'S LEVEL (V-Ω-STATIC-ANALYZER)                             ==
    =============================================================================
    LIF: 10,000,000,000

    Parses a .scaffold blueprint without executing it.
    Checks for syntax errors, unclosed blocks, and logic heresies.
    """

    def execute(self, request: LintBlueprintRequest) -> ScaffoldResult:
        target = (self.project_root / request.target).resolve()

        if not target.exists():
            return self.failure(f"Blueprint '{request.target}' not found.")

        self.logger.info(f"Leveling the foundation of [cyan]{target.name}[/cyan]...")

        # 1. Summon the Parser
        parser = ApotheosisParser(grammar_key="scaffold")
        content = target.read_text(encoding='utf-8')

        # 2. Conduct the Inquest (Parse String)
        # We don't need resolved vars for linting syntax
        _, items, _, _, _, dossier = parser.parse_string(content, file_path_context=target)

        # 3. Adjudicate
        if not parser.heresies:
            self.console.print(Panel(
                "[bold green]The Blueprint is plumb and level.[/bold green]\n"
                f"Parsed {len(items)} structural items.",
                title="[green]Purity Confirmed[/green]",
                border_style="green"
            ))
            return self.success("No syntax heresies found.")

        # 4. Proclaim Heresies
        table = Table(title="[bold red]Blueprint Heresies[/bold red]", border_style="red")
        table.add_column("Line", style="magenta", width=6)
        table.add_column("Severity", style="yellow", width=10)
        table.add_column("Message", style="white")

        for heresy in parser.heresies:
            table.add_row(
                str(heresy.line_num),
                heresy.severity.name,
                heresy.message
            )

        self.console.print(table)

        return self.failure(
            f"Found {len(parser.heresies)} heresies in blueprint.",
            data={"heresies": [h.model_dump() for h in parser.heresies]}
        )