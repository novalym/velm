# Path: scaffold/symphony/renderers/cinematic_renderer/widgets/header.py
# ----------------------------------------------------------------------
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from ..theme import GnosticTheme
from ..state import CinematicState


class HeaderWidget:
    def render(self, state: CinematicState) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right", ratio=1)

        status_color = GnosticTheme.SUCCESS
        status_text = "ACTIVE"
        if state.has_heresy:
            status_color = GnosticTheme.ERROR
            status_text = "HERESY DETECTED"
        elif state.is_paused:
            status_color = GnosticTheme.WARNING
            status_text = "PAUSED"

        elapsed = time.time() - state.start_time

        grid.add_row(
            f"[{GnosticTheme.TEXT_DIM}]Sanctum:[/] [bold white]{state.sanctum}[/]",
            f"[{GnosticTheme.ICON}]Symphony:[/] [bold {GnosticTheme.TEXT_HIGHLIGHT}]{state.title}[/]",
            f"[{status_color}]{status_text}[/]  [dim]⏱ {elapsed:.1f}s[/]"
        )

        return Panel(grid, style=f"on {GnosticTheme.HEADER_BG}", box=None)


import time