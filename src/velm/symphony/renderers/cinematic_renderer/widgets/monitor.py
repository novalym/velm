# Path: scaffold/symphony/renderers/cinematic_renderer/widgets/monitor.py
# -----------------------------------------------------------------------
from rich.panel import Panel
from rich.table import Table
from .sparkline import Sparkline  # We'll implement a simple one
from ..theme import GnosticTheme
from ..state import CinematicState


class ResourceMonitorWidget:
    def render(self, state: CinematicState) -> Panel:
        # Simple text for now, Sparkline needs complex logic
        cpu = state.cpu_history[-1] if state.cpu_history else 0
        mem = state.mem_history[-1] if state.mem_history else 0

        grid = Table.grid(expand=True)
        grid.add_column("Label", style="dim")
        grid.add_column("Value", style="bold white", justify="right")

        grid.add_row("CPU Vitality", f"{cpu:.1f}%")
        grid.add_row("Memory Flux", f"{mem:.0f} MB")

        return Panel(grid, title="[bold]Vitals[/]", border_style=GnosticTheme.PANEL_BORDER)