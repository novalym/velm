# Path: scaffold/shell/widgets/orrery.py
from pathlib import Path
from rich.text import Text
from textual import on
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Tree, Static

# --- THE GRIMOIRE OF ICONS ---
ICON_MAP = {
    ".py": "🐍", ".js": "⚡", ".ts": "📘", ".tsx": "⚛️", ".jsx": "⚛️",
    ".css": "🎨", ".html": "🌐", ".json": "📦", ".md": "📝",
    ".yml": "🔧", ".yaml": "🔧", ".toml": "⚙️", ".git": "🛑",
    ".dockerignore": "🐳", "Dockerfile": "🐳", "Makefile": "🛠️",
    "dir": "📂", "dir_open": "📂", "default": "📄"
}


class Orrery(Vertical):
    """
    =================================================================================
    == THE ORRERY (V-Ω-NAVIGABLE-SIDEBAR)                                          ==
    =================================================================================
    The Sidebar of Reality. It observes the filesystem and emits signals when the
    Architect touches the fabric of the directory structure.
    """

    class DirectorySelected(Message):
        """Proclaimed when the Architect wills a translocation (cd)."""

        def __init__(self, path: Path) -> None:
            self.path = path
            super().__init__()

    def __init__(self, root_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.root_path = root_path

    def compose(self):
        yield Static("FILESYSTEM", classes="orrery-header")
        # Root node matches the directory name
        tree = Tree(f"{self.root_path.name}", data=self.root_path, id="world-tree")
        tree.root.expand()
        self._populate_tree(tree.root, self.root_path)
        yield tree

    def on_mount(self):
        self.update_root(self.root_path)

    def update_root(self, new_path: Path):
        """Refreshes the Gaze upon a new sanctum."""
        self.root_path = new_path.resolve()
        tree = self.query_one("#world-tree", Tree)
        tree.clear()

        # Root Label styling
        tree.root.label = Text(f"{ICON_MAP['dir_open']} {self.root_path.name}/", style="bold blue")
        tree.root.data = self.root_path
        tree.root.expand()

        self._populate_tree(tree.root, self.root_path)

    def _populate_tree(self, node, path: Path):
        try:
            # Sort: Directories first, then files. Hidden files last.
            # Key: (is_file, is_hidden, name)
            children = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.startswith('.'), p.name.lower()))

            for child in children:
                # Skip noisy artifacts
                if child.name in [".git", "__pycache__", ".DS_Store", "node_modules", "venv", ".venv"]:
                    continue

                is_dir = child.is_dir()

                # Determine Icon
                if is_dir:
                    icon = ICON_MAP["dir"]
                    style = "bold cyan"
                else:
                    icon = ICON_MAP.get(child.suffix, ICON_MAP.get(child.name, ICON_MAP["default"]))
                    style = "white"
                    if child.name.startswith("."):
                        style = "dim white"

                label = Text(f"{icon} {child.name}", style=style)

                # We add the node. 
                # Note: In a full file manager, we'd recursively populate on expand. 
                # For the Shell, flat view of current dir is often enough, 
                # but we allow one level deep here.
                new_node = node.add(label, data=child, expand=False)

        except PermissionError:
            pass

    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, event: Tree.NodeSelected):
        """
        Intercepts the raw Tree event and transmutes it into a Gnostic Message.
        """
        event.stop()  # Stop the raw event from bubbling to the App blindly
        path = event.node.data

        if path and path.is_dir():
            # Proclaim the intent to navigate
            self.post_message(self.DirectorySelected(path))
        elif path and path.is_file():
            # Future: Proclaim 'FileInspected' to preview it?
            pass

