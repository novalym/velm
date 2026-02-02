# // studio/pads/distill_pad/widgets/file_selector.py
# ---------------------------------------------------

from __future__ import annotations

from pathlib import Path
from typing import Set, List, Dict, Optional

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.message import Message
from textual.widgets import Tree, Input, Button, Label, ListView, ListItem
from textual.widgets._tree import TreeNode
from textual.screen import ModalScreen
from textual.events import Click

from ....logger import Scribe
from ..state import FilesSelected


class ContextMenu(ModalScreen):
    """The Floating Hand of Will."""

    def __init__(self, path: Path, x: int, y: int, **kwargs):
        super().__init__(**kwargs)
        self.target_path = path
        self.click_x = x
        self.click_y = y

    def compose(self) -> ComposeResult:
        # We use a centered box but titled with the file name.
        with Vertical(classes="context-menu-box"):
            yield Label(f"Actions: {self.target_path.name}", classes="modal-title")
            yield ListView(
                ListItem(Label("Toggle Selection"), id="toggle"),
                ListItem(Label("Select Only This"), id="only"),
                ListItem(Label("Exclude (Add to Ignore)"), id="exclude"),
                ListItem(Label("Reveal in OS"), id="reveal"),
            )
            yield Button("Cancel", id="cancel", variant="error", classes="modal-btn")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.dismiss((event.item.id, self.target_path))

    @on(Button.Pressed, "#cancel")
    def cancel(self):
        self.dismiss(None)


class FileSelector(Vertical):
    """The Living World Tree."""

    class SelectionChanged(Message):
        """Proclaimed when the Architect alters the selection."""

        def __init__(self, selected_paths: Set[Path]) -> None:
            self.selected_paths = selected_paths
            super().__init__()

    def __init__(self, project_root: Path, **kwargs) -> None:
        super().__init__(**kwargs)
        self.scribe = Scribe("FileSelector")
        self._all_files: List[Path] = []
        self._root_path: Path = project_root
        self._current_selection: Set[Path] = set()
        self._search_term: str = ""

    def compose(self) -> ComposeResult:
        with Horizontal(id="file-selector-header"):
            yield Input(placeholder="Filter files...", id="file-tree-search")
            yield Button("+", id="btn-add-source", classes="icon-btn", variant="success", tooltip="Add Source")
            yield Button("⚙", id="btn-configure", classes="icon-btn", variant="primary", tooltip="Settings")

        yield Tree("Project Root", id="file-tree-main")

    def update_files(self, all_files: List[Path], selected_files: Set[Path]) -> None:
        """Renders the tree from scratch based on the current Gnosis."""
        self._all_files = sorted(list(set(all_files)))  # Ensure uniqueness
        self._current_selection = selected_files
        self._rebuild_tree()

    def _rebuild_tree(self) -> None:
        tree = self.query_one(Tree)
        tree.clear()
        tree.root.set_label(Text(f"{self._root_path.name}/", style="bold cyan"))
        tree.root.data = self._root_path
        tree.root.expand()

        # Filter based on search
        term = self._search_term.lower()
        files_to_show = [
            f for f in self._all_files
            if not term or term in f.name.lower() or term in str(f).lower()
        ]

        # Build Node Map
        nodes: Dict[Path, TreeNode] = {self._root_path: tree.root}

        # Virtual Node for External Files (Defined in local scope)
        external_root_node: Optional[TreeNode] = None

        # Helper to get/create dir node
        def get_dir_node(path: Path) -> TreeNode:
            # Check cache
            if path in nodes: return nodes[path]

            # Determine Parent
            # If path is equal to project root, return tree root
            if path == self._root_path:
                return tree.root

            # Check if path is inside project root
            try:
                path.relative_to(self._root_path)
                # It is inside. Parent is path.parent
                parent = path.parent
                parent_node = get_dir_node(parent)
            except ValueError:
                # It is EXTERNAL.
                # We use nonlocal to access the variable defined in _rebuild_tree
                nonlocal external_root_node

                if external_root_node is None:
                    external_root_node = tree.root.add(Text("External Sources", style="bold magenta"), data=None,
                                                       expand=True)

                # Strategy: Attach direct parent to External Root.
                if path.parent == path:  # Root of drive
                    return external_root_node

                # We treat the directory containing the file as a direct child of "External Sources"
                if path.parent not in nodes:
                    # Just create a node for this specific external directory
                    label = Text(f"📁 {path.name}", style="bold blue")
                    node = external_root_node.add(label, data=path, expand=True)
                    nodes[path] = node
                    return node
                return nodes[path.parent]

            # Standard creation logic
            label = Text(f"📁 {path.name}", style="bold blue")
            node = parent_node.add(label, data=path, expand=True)
            nodes[path] = node
            return node

        for file_path in files_to_show:
            # Get parent node
            try:
                # Check if inside root
                file_path.relative_to(self._root_path)
                parent_node = get_dir_node(file_path.parent)
            except ValueError:
                # External File Logic (Direct access to local variable, NO nonlocal needed here)
                if external_root_node is None:
                    external_root_node = tree.root.add(Text("External Sources", style="bold magenta"), data=None,
                                                       expand=True)

                # We group by immediate parent directory for cleaner display
                parent_dir = file_path.parent
                if parent_dir not in nodes:
                    label = Text(f"📁 {parent_dir.name} ({parent_dir})", style="bold blue")
                    nodes[parent_dir] = external_root_node.add(label, data=parent_dir, expand=True)
                parent_node = nodes[parent_dir]

            is_selected = file_path in self._current_selection

            icon = "✅" if is_selected else "⬜"
            style = "green" if is_selected else "dim white"
            label = Text(f"{icon} {file_path.name}", style=style)

            parent_node.add_leaf(label, data=file_path)

    @on(Input.Changed, "#file-tree-search")
    def on_search(self, event: Input.Changed):
        self._search_term = event.value
        self._rebuild_tree()

    @on(Button.Pressed, "#btn-add-source")
    def on_add(self):
        self.app.action_add_external_source()

    @on(Button.Pressed, "#btn-configure")
    def on_conf(self):
        self.app.action_toggle_config()

    @on(Tree.NodeSelected)
    def on_select(self, event: Tree.NodeSelected):
        """Toggle selection of file or directory."""
        node = event.node
        path = node.data
        if not path: return  # Structural node like "External Sources"

        paths_to_toggle = set()
        if node.is_leaf:
            paths_to_toggle.add(path)
        else:
            # Directory: Select all descendants currently shown/known in this branch
            descendants = [f for f in self._all_files if str(f).startswith(str(path))]
            paths_to_toggle.update(descendants)

        # Determine intent: If any are unchecked, check all. Else uncheck all.
        all_checked = all(p in self._current_selection for p in paths_to_toggle)

        if all_checked:
            self._current_selection.difference_update(paths_to_toggle)
        else:
            self._current_selection.update(paths_to_toggle)

        # Broadcast the change
        self.post_message(self.SelectionChanged(self._current_selection.copy()))

        # Optimistic UI update
        self._rebuild_tree()

    def on_click(self, event: Click) -> None:
        if event.button == 3:  # Right click
            tree = self.query_one(Tree)
            node = tree.cursor_node
            if node and node.data:
                self.app.push_screen(ContextMenu(node.data, event.screen_x, event.screen_y), self._handle_context)

    def _handle_context(self, result):
        if not result: return
        action, path = result

        if action == "toggle":
            if path in self._current_selection:
                self._current_selection.remove(path)
            else:
                self._current_selection.add(path)
        elif action == "only":
            self._current_selection = {path}
        elif action == "exclude":
            # Add to ignore list in config
            self.app.add_ignore_pattern(f"**/{path.name}")
            return  # Early return, config change triggers update

        self.post_message(FilesSelected(self._current_selection.copy()))
        self._rebuild_tree()