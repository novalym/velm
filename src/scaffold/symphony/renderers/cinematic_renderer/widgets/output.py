# Path: scaffold/symphony/renderers/cinematic_renderer/widgets/output.py
# ----------------------------------------------------------------------
from rich.panel import Panel
from rich.text import Text
from rich.ansi import AnsiDecoder
from ..theme import GnosticTheme
from ..state import CinematicState


class OutputWidget:
    def __init__(self):
        self.decoder = AnsiDecoder()

    def render(self, state: CinematicState) -> Panel:
        content = Text()
        for line in state.log_buffer:
            decoded = self.decoder.decode_line(line)
            content.append(decoded)
            content.append("\n")

        title = "Celestial Stream"
        if state.active_edict_index >= 0:
            active = state.edicts[state.active_edict_index]
            title = f"Stream: {active.name}"

        return Panel(
            content,
            title=f"[bold]{title}[/]",
            border_style=GnosticTheme.TEXT_DIM,
            padding=(0, 1)
        )