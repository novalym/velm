# Path: scaffold/symphony/renderers/cinematic_renderer/widgets/context.py
# -----------------------------------------------------------------------
from rich.panel import Panel
from rich.table import Table
from ..theme import GnosticTheme
from ..state import CinematicState


class ContextWidget:
    def render(self, state: CinematicState) -> Panel:
        table = Table(box=None, expand=True, show_header=False)
        table.add_column("Key", style=GnosticTheme.INFO)
        table.add_column("Value", style=GnosticTheme.TEXT_DIM, justify="right")

        # Show last 5 variables
        items = list(state.variables.items())[-5:]
        for k, v in items:
            table.add_row(k, str(v))

        return Panel(table, title="[bold]Gnosis[/]", border_style=GnosticTheme.PANEL_BORDER)