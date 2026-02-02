# Path: artisans/analyze/reporting/console.py
# -------------------------------------------

from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich import box


class ConsoleScribe:
    """
    =============================================================================
    == THE CONSOLE SCRIBE (V-Ω-VISUAL-FEEDBACK)                                ==
    =============================================================================
    Renders human-readable reports to stdout using Rich.
    """

    @staticmethod
    def render_report(result):
        console = Console()

        # 1. Failure State
        if not result.success:
            console.print(Panel(
                f"[bold red]Analysis Fractured[/]\n\n{result.message}",
                border_style="red",
                title="HERESY DETECTED"
            ))
            return

        data = result.data or {}
        diagnostics = result.diagnostics or data.get("diagnostics", [])

        # 2. Purity State
        if not diagnostics:
            console.print(Panel(
                "[bold green]The Lattice is Pure.[/]\nNo structural or syntactic heresies detected.",
                border_style="green",
                title="GNOSTIC INTEGRITY VERIFIED"
            ))
            return

        # 3. Heresy Table
        # Determine Title
        target = data.get('path', 'Scripture')
        title = f"Gnostic Inquisition: {target}"

        table = Table(
            title=title,
            expand=True,
            border_style="cyan",
            box=box.ROUNDED
        )

        table.add_column("Sev", justify="center", style="bold", width=8)
        table.add_column("Location", style="cyan", width=20)
        table.add_column("Heresy", style="white")
        table.add_column("Code", style="dim", width=12)

        for d in diagnostics:
            # Extract fields safely
            sev_raw = d.get('severity', 2)

            # Map Severity to Color/Label
            if sev_raw == 1:
                sev_display = "[bold red]CRIT[/]"
            elif sev_raw == 2:
                sev_display = "[yellow]WARN[/]"
            elif sev_raw == 3:
                sev_display = "[blue]INFO[/]"
            else:
                sev_display = "[dim]HINT[/]"

            # Format Location
            rng = d.get('range', {})
            start = rng.get('start', {})
            line = start.get('line', 0) + 1  # Convert 0-indexed to 1-indexed for humans
            loc_display = f"Ln {line}"

            # Format Message
            msg = d.get('message', '').strip()

            # Format Code
            code = str(d.get('code', 'UNK'))

            table.add_row(sev_display, loc_display, msg, code)

        console.print(table)

        # 4. Summary Footer
        crit_count = sum(1 for d in diagnostics if d.get('severity') == 1)
        if crit_count > 0:
            console.print(f"\n[bold red]✖ {crit_count} Critical Fractures Detected.[/]")
        else:
            console.print(f"\n[bold yellow]⚠ {len(diagnostics)} Warnings Detected.[/]")