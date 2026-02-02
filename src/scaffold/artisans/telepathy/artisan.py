# Path: scaffold/artisans/telepathy/artisan.py
# --------------------------------------------

import time
import pyperclip
from pathlib import Path
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Group
from rich.text import Text

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import TelepathyRequest
from ...help_registry import register_artisan

# We use Textual for the TUI if available, else a simple loop
try:
    from textual.app import App, ComposeResult
    from textual.widgets import Header, Footer, Static, Button, ListView, ListItem, Label
    from textual.containers import Container, Vertical

    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False


@register_artisan("telepathy")
class TelepathyArtisan(BaseArtisan[TelepathyRequest]):
    """
    =============================================================================
    == THE TELEPATHIC CLIPBOARD (V-Ω-CLIPBOARD-SENTINEL)                       ==
    =============================================================================
    LIF: 10,000,000,000

    Watches the system clipboard. When code is detected, it captures it,
    sanitizes it, and offers it to the Architect.
    """

    def execute(self, request: TelepathyRequest) -> ScaffoldResult:
        if not TEXTUAL_AVAILABLE:
            return self.failure("The Telepathic Interface requires 'textual'. pip install textual")

        app = TelepathyApp(self.project_root, request.save_dir)
        app.run()
        return self.success("Telepathic session ended.")


if TEXTUAL_AVAILABLE:
    class TelepathyApp(App):
        CSS = """
        Screen { layout: horizontal; }
        #sidebar { width: 30%; border-right: solid green; background: $surface; }
        #main { width: 70%; padding: 1; }
        .snippet-item { padding: 1; border: solid $accent; margin-bottom: 1; }
        """

        def __init__(self, root: Path, save_dir: str):
            super().__init__()
            self.root = root
            self.save_dir = root / save_dir
            self.save_dir.mkdir(exist_ok=True)
            self.last_clip = ""
            self.snippets = []

        def compose(self) -> ComposeResult:
            yield Header()
            with Container(id="sidebar"):
                yield Label("Captured Thoughts")
                yield ListView(id="snippet-list")
            with Container(id="main"):
                yield Static(id="preview-pane")
                yield Button("Inscribe (Save)", id="save-btn", variant="success")
            yield Footer()

        def on_mount(self):
            self.set_interval(0.5, self.check_clipboard)

        def check_clipboard(self):
            try:
                content = pyperclip.paste()
                if content != self.last_clip and content.strip():
                    self.last_clip = content
                    # Heuristic: Is it code?
                    if self._is_code(content):
                        self._add_snippet(content)
            except:
                pass

        def _is_code(self, text: str) -> bool:
            # Simple heuristic
            indicators = ["def ", "class ", "import ", "{", "}", "function", "const ", "var ", "return"]
            return any(i in text for i in indicators) or "\n" in text and " " in text

        def _add_snippet(self, content: str):
            timestamp = time.strftime("%H:%M:%S")
            preview = content[:30].replace("\n", " ") + "..."
            self.snippets.append(content)

            list_view = self.query_one("#snippet-list", ListView)
            list_view.append(ListItem(Label(f"[{timestamp}] {preview}")))

            # Auto-select newest
            # list_view.index = len(self.snippets) - 1
            self._show_preview(content)

        def _show_preview(self, content: str):
            pane = self.query_one("#preview-pane", Static)
            # Detect lang roughly
            lang = "python" if "def " in content else "javascript" if "function" in content else "text"
            pane.update(Syntax(content, lang, theme="monokai", line_numbers=True))

        def on_button_pressed(self, event: Button.Pressed):
            if event.button.id == "save-btn":
                if not self.snippets: return
                # Save the last captured
                content = self.snippets[-1]
                timestamp = int(time.time())
                filename = f"snippet_{timestamp}.txt"
                (self.save_dir / filename).write_text(content, encoding='utf-8')
                self.notify(f"Inscribed to {self.save_dir / filename}")