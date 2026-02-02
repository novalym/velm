
# Path: scaffold/artisans/astrolabe/tui.py
# ----------------------------------------
from pathlib import Path
from typing import List, Tuple

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input, Tree, Label
from textual.reactive import reactive
from textual.message import Message

from ...inquisitor import get_treesitter_gnosis
from ...inquisitor.core import LANGUAGES, is_grammar_available

# Try to import tree_sitter directly for query construction
try:
    from tree_sitter import Query, Node

    TREE_SITTER_LIB_AVAILABLE = True
except ImportError:
    TREE_SITTER_LIB_AVAILABLE = False


class CodeView(Static):
    """Displays the source code."""
    content: reactive[str] = reactive("")

    def render(self) -> str:
        return self.content


class ResultTree(Tree):
    """Displays query captures."""
    pass


class AstrolabeApp(App):
    CSS = """
    Screen { layout: vertical; }
    #main_view { layout: horizontal; height: 1fr; }
    #code_pane { width: 50%; border-right: solid $accent; height: 100%; overflow: auto; }
    #sidebar { width: 50%; layout: vertical; height: 100%; }
    #query_input { dock: top; }
    #results_tree { height: 1fr; border-top: solid $accent; }
    .highlight { background: $accent; color: $text; }
    """

    BINDINGS = [("q", "quit", "Quit"), ("r", "run_query", "Run Query")]

    def __init__(self, file_path: Path, project_root: Path):
        super().__init__()
        self.file_path = file_path
        self.project_root = project_root
        self.source_code = file_path.read_text(encoding="utf-8")
        self.language_name = self._divine_language()

    def _divine_language(self) -> str:
        # Simple extension mapping
        ext = self.file_path.suffix.lower()
        mapping = {'.py': 'python', '.js': 'javascript', '.ts': 'typescript', '.go': 'go', '.rs': 'rust', '.rb': 'ruby'}
        return mapping.get(ext, 'python')  # Default

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Astrolabe: {self.file_path.name} ({self.language_name})", classes="header")
        with Horizontal(id="main_view"):
            yield CodeView(id="code_pane")
            with Vertical(id="sidebar"):
                yield Input(placeholder="(function_definition) @func", id="query_input")
                yield ResultTree("Captures", id="results_tree")
        yield Footer()

    def on_mount(self):
        self.query_one(CodeView).content = self.source_code
        self.query_one("#query_input").focus()

    def on_input_submitted(self, event: Input.Submitted):
        self.run_query(event.value)

    def run_query(self, query_str: str):
        if not TREE_SITTER_LIB_AVAILABLE:
            self.notify("Tree-sitter library not found.", severity="error")
            return

        tree_view = self.query_one(ResultTree)
        tree_view.clear()
        tree_view.root.expand()

        if not is_grammar_available(f"tree_sitter_{self.language_name}", self.language_name):
            self.notify(f"Grammar for {self.language_name} not available.", severity="error")
            return

        lang = LANGUAGES[self.language_name]
        try:
            query = lang.query(query_str)
            from tree_sitter import Parser
            parser = Parser()
            parser.set_language(lang)
            tree = parser.parse(bytes(self.source_code, "utf8"))

            captures = query.captures(tree.root_node)

            # Group by capture name
            results = []
            if isinstance(captures, list):  # Modern bindings
                for node, name in captures:
                    results.append((name, node))
            elif isinstance(captures, dict):  # Older bindings
                for name, nodes in captures.items():
                    for node in nodes:
                        results.append((name, node))

            for name, node in results:
                line_start = node.start_point[0] + 1
                text_preview = node.text.decode('utf-8').splitlines()[0][:50]
                label = f"@{name} [L{line_start}]: {text_preview}..."
                tree_view.root.add(label)

            self.notify(f"Found {len(results)} matches.")

        except Exception as e:
            self.notify(f"Query Error: {e}", severity="error")

