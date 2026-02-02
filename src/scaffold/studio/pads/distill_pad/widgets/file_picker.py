# Path: studio/pads/distill_pad/widgets/file_picker.py
# ----------------------------------------------------

from pathlib import Path
from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, DirectoryTree


class FilePickerModal(ModalScreen[Optional[Path]]):
    """
    The Eye of Selection.
    """

    CSS = """
    FilePickerModal {
        align: center middle;
        background: rgba(0, 0, 0, 0.7);
    }
    #picker-box {
        width: 70%;
        height: 80%;
        background: $surface;
        border: thick $accent;
        padding: 1;
        layout: vertical;
    }
    #picker-title {
        text-align: center;
        text-style: bold;
        background: $accent-darken-2;
        color: $text;
        padding: 1;
        dock: top;
    }
    #picker-header {
        height: 3;
        background: $surface-darken-1;
        border-bottom: solid $primary;
        layout: horizontal;
        align: left middle;
        padding: 0 1;
        margin-top: 1;
    }
    #current-path-label {
        width: 1fr;
        content-align: left middle;
        text-style: bold;
        color: $accent-lighten-2;
        padding-left: 1;
    }
    #picker-tree {
        height: 1fr;
        border: solid $primary-darken-1;
        margin: 1 0;
        background: $surface-lighten-1;
    }
    #picker-footer {
        height: 3;
        dock: bottom;
        align: right middle;
        padding-top: 1;
    }
    .picker-btn {
        margin-left: 1;
    }
    .nav-btn {
        min-width: 4;
        margin-right: 1;
    }
    #selected-label {
        width: 1fr;
        color: $text-muted;
        content-align: left middle;
    }
    """

    def __init__(self, initial_path: Path = None, **kwargs):
        super().__init__(**kwargs)
        self.current_path = (initial_path or Path.cwd()).resolve()
        # [THE JAIL] We set the hard floor to the drive root or system root
        self.root_boundary = Path(self.current_path.anchor)
        self.selected_node_path: Optional[Path] = None

    def compose(self) -> ComposeResult:
        with Vertical(id="picker-box"):
            yield Label("Select Source (File or Directory)", id="picker-title")

            with Horizontal(id="picker-header"):
                yield Button("⬆️ Up", id="btn-up", variant="default", classes="nav-btn")
                yield Label(str(self.current_path), id="current-path-label")

            yield DirectoryTree(str(self.current_path), id="picker-tree")

            with Horizontal(id="picker-footer"):
                yield Label("No selection", id="selected-label")
                yield Button("Select", variant="primary", id="btn-select", classes="picker-btn")
                yield Button("Cancel", variant="error", id="btn-cancel", classes="picker-btn")

    def on_mount(self):
        self.query_one("#picker-tree").focus()
        self._check_boundary()

    def _check_boundary(self):
        """Disables the Up button if we hit the floor."""
        # If current path is same as anchor, we are at root (C:\ or /)
        # Or if we hit our safety limit (though anchor check is better)
        if self.current_path == self.root_boundary:
            self.query_one("#btn-up").disabled = True
        else:
            self.query_one("#btn-up").disabled = False

    @on(Button.Pressed, "#btn-up")
    def action_navigate_up(self):
        if self.current_path == self.root_boundary:
            self.notify("Root boundary reached. Cannot ascend further.", severity="warning")
            return

        parent = self.current_path.parent
        # Extra safety check against infinite loop at root
        if parent == self.current_path:
            return

        self.current_path = parent
        self._refresh_tree()

    def _refresh_tree(self):
        self.query_one("#current-path-label").update(str(self.current_path))
        tree = self.query_one(DirectoryTree)
        tree.path = str(self.current_path)
        self._check_boundary()
        self.selected_node_path = None
        self.query_one("#selected-label").update("Navigating...")

    @on(DirectoryTree.NodeSelected)
    def on_node_selected(self, event: DirectoryTree.NodeSelected) -> None:
        self.selected_node_path = event.node.data.path
        self.query_one("#selected-label").update(f"Selected: [cyan]{self.selected_node_path.name}[/]")

    @on(DirectoryTree.FileSelected)
    def on_file_double_click(self, event: DirectoryTree.FileSelected) -> None:
        self.dismiss(event.path)

    @on(Button.Pressed, "#btn-select")
    def action_confirm(self) -> None:
        if self.selected_node_path:
            self.dismiss(self.selected_node_path)
        else:
            # Fallback: Select current directory
            self.dismiss(self.current_path)

    @on(Button.Pressed, "#btn-cancel")
    def action_cancel(self) -> None:
        self.dismiss(None)