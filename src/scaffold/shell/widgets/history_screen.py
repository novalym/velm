# Path: scaffold/shell/widgets/history_screen.py
from textual.screen import ModalScreen
from textual.widgets import Input, OptionList
from textual.containers import Vertical
from textual.binding import Binding
from textual import on


class HistorySearchScreen(ModalScreen[str]):
    """
    The Chronomancer's Dial.
    Fuzzy search through command history.
    """

    CSS = """
    HistorySearchScreen {
        align: center middle;
        background: rgba(0,0,0,0.8);
    }
    #history-box {
        width: 60;
        height: 20;
        background: #16161e;
        border: thick #7aa2f7;
        padding: 1;
    }
    #history-input {
        dock: top;
        border: none;
        background: #24283b;
        color: #c0caf5;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        Binding("escape", "dismiss_screen", "Cancel"),
    ]

    def __init__(self, history: list[str]):
        super().__init__()
        self.full_history = list(reversed(history))  # Newest first

    def compose(self):
        with Vertical(id="history-box"):
            yield Input(placeholder="Search the Annals of Time...", id="history-input")
            yield OptionList(*self.full_history, id="history-list")

    def on_mount(self):
        self.query_one("#history-input").focus()

    @on(Input.Changed)
    def filter_history(self, event: Input.Changed):
        term = event.value.lower()
        filtered = [cmd for cmd in self.full_history if term in cmd.lower()]
        ol = self.query_one(OptionList)
        ol.clear_options()
        ol.add_options(filtered)

    @on(OptionList.OptionSelected)
    def select_command(self, event: OptionList.OptionSelected):
        self.dismiss(str(event.option.prompt))

    def action_dismiss_screen(self):
        self.dismiss(None)