# Path: scaffold/artisans/vector/artisan.py
# -----------------------------------------


from pathlib import Path
from typing import Optional

from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Group
from rich.text import Text

from ...core.artisan import BaseArtisan
from ...interfaces.requests import VectorRequest
from ...interfaces.base import ScaffoldResult
from ...core.cortex.vector import VectorCortex


class VectorArtisan(BaseArtisan[VectorRequest]):
    """
    =============================================================================
    == THE VECTOR LIBRARIAN (V-Ω-LUMINOUS-INTERFACE-CORRECTED)                 ==
    =============================================================================
    LIF: 10,000,000,000

    The Sovereign Interface to the Semantic Index.
    It now speaks in Luminous Panels, revealing the code it finds.

    [ASCENSION]: The Resonance Calculation has been healed. It now uses
    Inverse Distance Weighting to translate Euclidean distance into a
    valid 0-100% confidence score.
    """

    def execute(self, request: VectorRequest) -> ScaffoldResult:
        cortex = VectorCortex(self.project_root)

        if request.vector_command == "index":
            cortex.index_project()
            return self.success("The codebase has been assimilated into the Vector Space.")

        elif request.vector_command == "query":
            if not request.query_text:
                return self.failure("The Oracle requires a query string.")

            self.logger.info(f"Resonating with: '[cyan]{request.query_text}[/cyan]'")

            # The Cortex will auto-index if empty.
            hits = cortex.search(request.query_text, limit=request.limit or 3)

            if not hits:
                return self.success("The Void returned no echoes. (Try indexing more code or a different query).")

            # --- THE LUMINOUS PROCLAMATION ---
            self.console.rule(f"[bold magenta]Semantic Resonance ({len(hits)} hits)[/bold magenta]")

            for hit in hits:
                source = hit['metadata']['source']
                distance = hit['distance']
                content = hit['content']

                # [THE FIX] Inverse Distance Weighting
                # Chroma returns L2 distance (0 to Infinity).
                # 0.0 = Identical
                # 1.0 = Moderate drift
                # > 1.5 = Distant
                # Formula: 1 / (1 + distance) normalizes this to 0.0 - 1.0
                similarity = 1 / (1 + distance)
                confidence = similarity * 100

                # Determine language for syntax highlighting
                lang = "python"
                if source.endswith(('.ts', '.tsx')):
                    lang = "typescript"
                elif source.endswith(('.js', '.jsx')):
                    lang = "javascript"
                elif source.endswith('.rs'):
                    lang = "rust"
                elif source.endswith('.go'):
                    lang = "go"
                elif source.endswith('.md'):
                    lang = "markdown"

                # Colorize based on new confidence
                resonance_style = "dim green"
                if confidence > 60:
                    resonance_style = "bold green"
                elif confidence > 40:
                    resonance_style = "yellow"
                elif confidence < 20:
                    resonance_style = "dim red"

                header = Text.assemble(
                    (f"{source} ", "bold cyan"),
                    (f"(Resonance: {confidence:.1f}%)", resonance_style),
                    (f" [Dist: {distance:.3f}]", "dim")
                )

                self.console.print(Panel(
                    Syntax(content, lang, theme="monokai", line_numbers=True, start_line=1),
                    title=header,
                    border_style="blue",
                    padding=(0, 1)
                ))

            return self.success(f"Found {len(hits)} resonance points.", data={"hits": hits})

        elif request.vector_command == "clear":
            cortex.clear()
            return self.success("The Vector Store is empty.")

        return self.failure("Unknown vector rite.")