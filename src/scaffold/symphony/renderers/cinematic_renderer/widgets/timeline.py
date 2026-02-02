# Path: scaffold/symphony/renderers/cinematic_renderer/widgets/timeline.py
# ------------------------------------------------------------------------
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from ..theme import GnosticTheme
from ..state import CinematicState


class TimelineWidget:
    def render(self, state: CinematicState) -> Panel:
        table = Table(box=None, expand=True, padding=(0, 1), show_header=False)
        table.add_column("Icon", width=3)
        table.add_column("Name", ratio=1)
        table.add_column("Time", width=8, justify="right")

        # Scroll logic: Show window around active index
        window_size = 10
        start = max(0, state.active_edict_index - (window_size // 2))
        end = start + window_size
        visible_edicts = state.edicts[start:end]

        for edict in visible_edicts:
            style = "dim"
            icon = GnosticTheme.ICON_PENDING

            if edict.status == "RUNNING":
                style = "bold white"
                icon = GnosticTheme.ICON_RUNNING
            elif edict.status == "SUCCESS":
                style = GnosticTheme.SUCCESS
                icon = GnosticTheme.ICON_SUCCESS
            elif edict.status == "FAILURE":
                style = GnosticTheme.ERROR
                icon = GnosticTheme.ICON_FAILURE

            duration = f"{edict.duration:.1f}s" if edict.duration > 0 else ""

            # Highlight active row background? Rich doesn't support row-bg easily in tables without Text styles
            # We use bold/color to highlight

            name_text = Text(edict.name, style=style)
            if edict.status == "RUNNING":
                name_text = Text("➤ ", style=GnosticTheme.INFO) + name_text

            table.add_row(icon, name_text, duration)

        border = GnosticTheme.PANEL_BORDER_ACTIVE if state.active_edict_index >= 0 else GnosticTheme.PANEL_BORDER
        return Panel(table, title="[bold]The Timeline[/]", border_style=border)