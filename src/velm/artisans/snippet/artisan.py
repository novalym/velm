# Path: scaffold/artisans/snippet/artisan.py
# ------------------------------------------

import sys
from pathlib import Path
from rich.table import Table
from rich.syntax import Syntax
from rich.panel import Panel

try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import SnippetRequest
from ...help_registry import register_artisan


@register_artisan("snippet")
class SnippetArtisan(BaseArtisan[SnippetRequest]):
    """
    =============================================================================
    == THE FRAGMENT KEEPER (V-Ω-LOCAL-LIBRARY)                                 ==
    =============================================================================
    LIF: 10,000,000,000

    Manages a library of code snippets in .scaffold/snippets.
    """

    def execute(self, request: SnippetRequest) -> ScaffoldResult:
        snippet_dir = self.project_root / ".scaffold" / "snippets"
        snippet_dir.mkdir(parents=True, exist_ok=True)

        cmd = request.snippet_command
        name = request.name

        if cmd == "list":
            return self._list_snippets(snippet_dir)

        if not name:
            return self.failure("A snippet name is required for save/load/delete.")

        snippet_path = snippet_dir / name
        # Allow saving without extension, but prefer one if known

        if cmd == "save":
            content = ""
            if request.source_file:
                src = (self.project_root / request.source_file).resolve()
                if not src.exists(): return self.failure(f"Source file {src} not found.")
                content = src.read_text(encoding="utf-8")
            elif request.clipboard:
                if not CLIPBOARD_AVAILABLE: return self.failure("pyperclip missing.")
                content = pyperclip.paste()
            else:
                # Read from stdin
                if not sys.stdin.isatty():
                    content = sys.stdin.read()
                else:
                    return self.failure("Provide source: --file, --clip, or pipe.")

            if not content.strip():
                return self.failure("Snippet content is void.")

            snippet_path.write_text(content, encoding="utf-8")
            return self.success(f"Snippet '{name}' enshrined.")

        elif cmd == "load":
            if not snippet_path.exists():
                return self.failure(f"Snippet '{name}' not found.")

            content = snippet_path.read_text(encoding="utf-8")

            if request.clipboard:
                if not CLIPBOARD_AVAILABLE: return self.failure("pyperclip missing.")
                pyperclip.copy(content)
                return self.success(f"Snippet '{name}' copied to clipboard.")
            else:
                # Proclaim to stdout (cleanly, for piping)
                print(content)
                return self.success(f"Snippet '{name}' proclaimed.")

        elif cmd == "delete":
            if snippet_path.exists():
                snippet_path.unlink()
                return self.success(f"Snippet '{name}' returned to the void.")
            return self.failure(f"Snippet '{name}' not found.")

        return self.failure(f"Unknown rite: {cmd}")

    def _list_snippets(self, directory: Path) -> ScaffoldResult:
        snippets = sorted(list(directory.glob("*")))
        if not snippets:
            return self.success("The Snippet Library is empty.")

        table = Table(title="[bold cyan]Gnostic Fragments[/bold cyan]")
        table.add_column("Name", style="green")
        table.add_column("Size", style="dim")

        for s in snippets:
            table.add_row(s.name, f"{s.stat().st_size} bytes")

        self.console.print(table)
        return self.success(f"Found {len(snippets)} snippets.")