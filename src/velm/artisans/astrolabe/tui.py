
# Path: scaffold/artisans/astrolabe/tui.py
# ----------------------------------------
import sys
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
    # --- MOVEMENT I: NATIVE COMMUNION (THE HIGH PATH) ---
    # We first attempt to speak with the native C-extension.
    from tree_sitter import Query, Node

    TREE_SITTER_LIB_AVAILABLE = True

except ImportError:
    # --- MOVEMENT II: PROXY RESURRECTION (THE WASM PATH) ---
    # If the native tongue is absent, we scry the Gnostic Registry
    # for the Diamond Proxy forged by the Simulacrum.
    if "tree_sitter" in sys.modules:
        _ts = sys.modules["tree_sitter"]
        Query = _ts.Query
        Node = _ts.Node
        TREE_SITTER_LIB_AVAILABLE = True
    else:
        # --- MOVEMENT III: THE BLIND GAZE (STASIS) ---
        # If no soul is manifest in any realm, we forge hollow vessels.
        TREE_SITTER_LIB_AVAILABLE = False

        # We forge 'Hollow' types to allow code to be imported
        # without crashing, even if the Gaze is blind.
        Query = type("HollowQuery", (object,), {})
        Node = type("HollowNode", (object,), {})


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
        """
        =============================================================================
        == THE RITE OF SYMBOLIC INQUEST (V-Ω-TOTALITY-V200.12-ISOMORPHIC)          ==
        =============================================================================
        LIF: 10x | ROLE: PATTERN_ADJUDICATOR | RANK: OMEGA

        Executes a Gnostic Query against the active scripture. Engineered to mirror
        modern C-bindings while remaining fully compatible with the Diamond Proxy.
        =============================================================================
        """
        # [ASCENSION 1]: Functional Availability Check
        # Now represents functional availability across both Iron and Ether.
        if not TREE_SITTER_LIB_AVAILABLE:
            self.notify("Gaze is Blind: Tree-sitter unmanifested in this stratum.", severity="error")
            return

        # UI Ritual: Preparation of the Result Tree
        try:
            tree_view = self.query_one(ResultTree)
            tree_view.clear()
            tree_view.root.expand()
        except Exception:
            # Fallback for headless or initializing UI states
            pass

        # [ASCENSION 8]: Linguistic Shard Verification
        # We verify against the central registry, which our Diamond Suture populates.
        if not is_grammar_available(f"tree_sitter_{self.language_name}", self.language_name):
            self.notify(f"Linguistic Shard '{self.language_name}' not available.", severity="error")
            return

        lang = LANGUAGES[self.language_name]

        try:
            # [MOVEMENT I]: THE SUMMONS
            # The Diamond Meta-Path Suture guarantees this import resolves correctly.
            from tree_sitter import Parser

            # Pre-compile the pattern via the Language Proxy
            query = lang.query(query_str)

            parser = Parser()
            parser.set_language(lang)

            # [MOVEMENT II]: THE STRIKE
            # Transmute source code to bytes for the engine.
            # Our Proxy handles both 'str' and 'bytes' for maximum resilience.
            source_bytes = self.source_code.encode("utf-8") if isinstance(self.source_code, str) else self.source_code
            tree = parser.parse(source_bytes)

            # [MOVEMENT III]: THE CAPTURE
            # Our Proxy specifically returns a List[Tuple[Node, str]] to mirror modern bindings.
            # We remove the legacy 'dict' check to enforce the new Diamond Standard.
            captures = query.captures(tree.root_node)

            # [MOVEMENT IV]: THE REVELATION
            for node, name in captures:
                # [ASCENSION 1]: Achronal Point Parity
                # node.start_point returns (row, col) in both C and WASM strata.
                line_start = node.start_point[0] + 1

                # [ASCENSION 2]: Gnostic Byte Parity
                # node.text returns bytes. We decode locally to preserve UI strings.
                raw_text = node.text
                text_preview = raw_text.decode('utf-8', errors='replace').splitlines()[0][:50]

                label = f"@{name} [L{line_start}]: {text_preview}..."

                # Inscribe the finding into the Ocular HUD
                if 'tree_view' in locals():
                    tree_view.root.add(label)

            self.notify(f"Resonance Achieved: {len(captures)} matches perceived.")

        except Exception as e:
            # [ASCENSION 11]: Forensic Fracture Capture
            self.notify(f"Query Error: {str(e)}", severity="error")

