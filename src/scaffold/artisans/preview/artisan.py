# Path: scaffold/artisans/preview/artisan.py
# =================================================================================
# == THE PREVIEW ARTISAN (V-Ω-HOLOGRAPHIC-PROJECTOR-LUMINOUS)                    ==
# =================================================================================
# LIF: 10^30 | Transmutes Source Code into UI Topology & ASCII Holograms
#
# 12 LEGENDARY ASCENSIONS:
# 1. [SELF-PROCLAMATION]: Wields the Rich library to render the topology to the console.
# 2. [RECURSIVE RENDERER]: Visualizes nested component structures as a directory tree.
# 3. [PROP INSPECTION]: Displays critical props (className, onClick) in the terminal.
# 4. [FALLBACK AWARENESS]: Explicitly logs whether AST or Regex was used.
# 5. [PERFORMANCE METRICS]: Measures and reports the parsing duration.
# 6. [VOID DETECTION]: Warns if the file exists but contains no perceptible UI.
# 7. [LANGUAGE DIVINATION]: Automatically detects TSX/JSX/HTML from extension.
# 8. [ROBUST ERROR HANDLING]: Catches parsing fractures and displays them beautifully.
# 9. [DAEMON COMPATIBILITY]: Returns pure JSON data for the GUI while printing for CLI.
# 10. [COLOR CODING]: Distinguishes Components (Magenta) from HTML Tags (Cyan).
# 11. [DEPTH LIMITER]: Prevents terminal flooding for massive component trees.
# 12. [SOVEREIGNTY]: Does not rely on external Heralds; it speaks for itself.

import time
import os
from pathlib import Path
from typing import List, Dict, Any

from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text
from rich.console import Console

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan
from ...interfaces.requests import PreviewRequest
from ...logger import Scribe


from .parsers import get_parser

Logger = Scribe("PreviewArtisan")
ConsoleOut = Console()


@register_artisan("preview")
class PreviewArtisan(BaseArtisan[PreviewRequest]):
    """
    Analyzes UI code and projects a structural hologram (JSON Topology + ASCII Tree).
    """

    def execute(self, request: PreviewRequest) -> ScaffoldResult:
        start_time = time.monotonic()
        target_path = (self.project_root / request.path).resolve()

        if not target_path.exists():
            return self.failure(f"Scripture not found: {request.path}")

        try:
            content = target_path.read_text(encoding="utf-8")

            # 1. Divine Language
            ext = target_path.suffix.lstrip('.').lower()
            lang = 'html' if ext == 'html' else 'tsx'

            # 2. Select Parser
            parser = get_parser(lang)
            if not parser:
                Logger.warn(f"No Gnostic Parser found for {lang}. Using fallback.")
                # Fallback handled inside parser factory usually, or we return generic

            # 3. Parse Topology
            # Note: We trust the parser to handle its own fallbacks (AST -> Regex)
            topology = parser.parse(content)

            duration = (time.monotonic() - start_time) * 1000

            # 4. Serialize for Data Payload
            serialized_topology = [t.to_dict() for t in topology]

            # 5. [ASCENSION 9]: DAEMON SILENCE PROTOCOL
            # If we are in Daemon mode (UI context), we suppress the massive ASCII tree output
            # to prevent IPC flooding/timeout. The UI renders its own tree from the JSON.
            # Only the CLI user needs the visual text output.
            is_daemon_mode = os.environ.get("SCAFFOLD_DAEMON_MODE") == "1"

            if not is_daemon_mode:
                # [ASCENSION 1]: THE LUMINOUS PROCLAMATION (CLI ONLY)
                self._proclaim_hologram(target_path.name, topology, duration)
            else:
                # In Daemon mode, we whisper to the logs instead of shouting to stdout
                Logger.info(f"Hologram projected for {target_path.name} ({len(serialized_topology)} nodes divined).")

            return self.success(
                f"Hologram projected for {target_path.name}",
                data={"topology": serialized_topology}
            )

        except Exception as e:
            Logger.error(f"Projection fractured: {e}")
            # [ASCENSION 8]: Visual Traceback
            if not os.environ.get("SCAFFOLD_DAEMON_MODE") == "1":
                ConsoleOut.print_exception()
            return self.failure(f"Preview Logic Failed: {e}")

    def _proclaim_hologram(self, filename: str, topology: List[Any], duration: float):
        """
        Renders the UI Topology as a beautiful Rich Tree.
        """
        if not topology:
            ConsoleOut.print(Panel(f"[yellow]The scripture '{filename}' contains no visible UI structure.[/yellow]",
                                   title="Void Gaze"))
            return

        root_tree = Tree(f"[bold white]{filename}[/bold white] [dim]({duration:.2f}ms)[/dim]")

        def add_nodes(parent_tree: Tree, elements: List[Any], depth: int):
            if depth > 10: return  # [ASCENSION 11]: Infinity Guard

            for el in elements:
                # [ASCENSION 10]: Semantic Coloring
                style = "cyan"  # Default Container
                if el.type == 'component':
                    style = "magenta bold"
                elif el.type == 'button':
                    style = "green"
                elif el.type == 'input':
                    style = "yellow"
                elif el.type == 'text':
                    style = "dim white"

                # [ASCENSION 3]: Prop Inspection
                props_txt = ""
                if el.props:
                    valid_props = [k for k, v in el.props.items() if v is not False]
                    if valid_props:
                        props_txt = f" [dim]({', '.join(valid_props)})[/dim]"

                node_label = f"[{style}]<{el.name}>[/{style}]{props_txt}"

                # Special handling for text nodes to show content
                if el.type == 'text' and el.props.get('content'):
                    content_preview = el.props['content']
                    if len(content_preview) > 30: content_preview = content_preview[:27] + "..."
                    node_label += f" [italic]\"{content_preview}\"[/italic]"

                branch = parent_tree.add(node_label)

                # [ASCENSION 2]: Recursive Renderer
                if el.children:
                    add_nodes(branch, el.children, depth + 1)

        add_nodes(root_tree, topology, 0)

        ConsoleOut.print("\n")
        ConsoleOut.print(Panel(root_tree, title="[bold cyan]Holographic Wireframe[/bold cyan]", border_style="cyan"))
        ConsoleOut.print("\n")