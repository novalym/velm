# Path: scaffold/shell/widgets/suggestion_menu.py
from textual.widgets import OptionList
from rich.text import Text


class SuggestionMenu(OptionList):
    """
    The Holographic Projection of Possibility.
    Appears above the prompt to offer Gnostic Completions.
    """

    def update_suggestions(self, suggestions: list[tuple[str, str]]):
        """
        Accepts list of (command, description).
        """
        self.clear_options()
        if not suggestions:
            self.display = False
            return

        for cmd, desc in suggestions:
            # Format: Command (cyan) - Description (dim white)
            label = Text.assemble(
                (cmd.ljust(20), "bold cyan"),
                (" ", ""),
                (desc, "dim white")
            )
            self.add_option(label)

        self.display = True
        # Reset selection to top
        self.highlighted = 0