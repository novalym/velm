# Path: scaffold/symphony/renderers/cinematic_renderer/widgets/footer.py
# ----------------------------------------------------------------------
from rich.text import Text
from ..theme import GnosticTheme
from ..state import CinematicState

class FooterWidget:
    def render(self, state: CinematicState) -> Text:
        return Text.assemble(
            (" [p] ", "bold black on cyan"), (" Pause ", "dim white"),
            (" [q] ", "bold black on red"), (" Abort ", "dim white"),
            (" [d] ", "bold black on yellow"), (" Debug ", "dim white"),
            justify="center",
            style=f"on {GnosticTheme.FOOTER_BG}"
        )