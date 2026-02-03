# Path: scaffold/artisans/resonate/artisan.py
# -------------------------------------------

from pathlib import Path
from typing import List, Dict, Any

from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ResonateRequest  # Assume created
from ...core.cortex.semantic_indexer import SemanticIndexer
from ...help_registry import register_artisan
from ...logger import Scribe

Logger = Scribe("SemanticResonator")


@register_artisan("resonate")
class ResonateArtisan(BaseArtisan[ResonateRequest]):
    """
    =============================================================================
    == THE SEMANTIC RESONATOR (V-Ω-CODE-TO-CONCEPT)                            ==
    =============================================================================
    LIF: 10,000,000,000,000

    Stop searching for strings. Search for *intent*.
    This artisan embeds the AST of the project into a vector space and performs
    cosine similarity searches to find code that matches a *concept*.
    """

    def execute(self, request: ResonateRequest) -> ScaffoldResult:
        self.logger.info(f"The Resonator awakens. Tuning to frequency: '[cyan]{request.query}[/cyan]'...")

        # 1. The Rite of Indexing (Lazy)
        # We summon the Indexer. It checks if the Vector Store is fresh.
        indexer = SemanticIndexer(self.project_root)

        if request.reindex or not indexer.is_index_valid():
            self.console.print("[yellow]The Vector Space is stale or void. Commencing Gnostic Embedding...[/yellow]")
            with self.console.status("[bold magenta]Reading AST & Embedding Vectors...[/bold magenta]"):
                indexer.index_reality()

        # 2. The Rite of Resonance
        results = indexer.search(request.query, limit=request.limit)

        if not results:
            return self.failure("The Void returned no echoes. Try a different query.")

        # 3. The Luminous Proclamation
        self.console.rule(f"[bold cyan]Resonance Detected: {len(results)} Echoes[/bold cyan]")

        for hit in results:
            score = hit['distance']  # Lower is better in some metrics, Higher in Cosine. Assume Similarity (0-1).
            meta = hit['metadata']

            # Color code confidence
            color = "green" if score > 0.8 else "yellow" if score > 0.6 else "dim"

            header = f"[{color}]Confidence: {score:.2f}[/{color}] | [bold]{meta['type']}: {meta['name']}[/bold]"
            subtitle = f"[dim]{meta['file_path']}:{meta['line_number']}[/dim]"

            # Syntax highlight the code snippet
            code_view = Syntax(
                hit['content'],
                "python",  # Prophecy: Auto-detect language
                theme="monokai",
                line_numbers=True,
                start_line=meta['line_number']
            )

            self.console.print(Panel(
                code_view,
                title=header,
                subtitle=subtitle,
                border_style=color,
                padding=(0, 1)
            ))

        return self.success(f"Found {len(results)} semantic matches.")