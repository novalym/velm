# Path: artisans/akasha/artisan.py
# --------------------------------

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import AkashaRequest
from ...help_registry import register_artisan
from ...core.ai.akasha import AkashicRecord
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax


@register_artisan("akasha")
class AkashaArtisan(BaseArtisan[AkashaRequest]):
    """
    =============================================================================
    == THE KEEPER OF THE AKASHA (V-Ω-GLOBAL-MEMORY-CLI)                        ==
    =============================================================================
    LIF: 10,000,000,000

    Manages the persistent, cross-project memory of the God-Engine.
    """

    def execute(self, request: AkashaRequest) -> ScaffoldResult:
        akasha = AkashicRecord()

        if request.akasha_command == "stats":
            stats = akasha.get_stats()
            self.console.print(Panel(
                f"Memories: [bold green]{stats['total_memories']}[/bold green]\n"
                f"Storage:  [cyan]{stats['storage_size_bytes'] / 1024 / 1024:.2f} MB[/cyan]\n"
                f"Sanctum:  [dim]{stats['location']}[/dim]",
                title="[bold magenta]Akashic Record Status[/bold magenta]"
            ))
            return self.success("Stats proclaimed.")

        elif request.akasha_command == "query":
            if not request.query:
                return self.failure("A query is required to gaze into the Akasha.")

            hits = akasha.recall_wisdom(request.query, limit=3)
            if not hits:
                return self.success("The Akasha is silent on this matter.")

            for hit in hits:
                meta = hit['metadata']
                self.console.print(Panel(
                    Syntax(hit['content'][:500] + "...", "python", theme="monokai"),
                    title=f"[bold cyan]{meta.get('rite', 'Unknown Rite')}[/bold cyan] ({meta.get('project', 'Unknown Project')})",
                    subtitle=f"Distance: {hit['distance']:.3f}"
                ))
            return self.success(f"Recalled {len(hits)} memories.")

        elif request.akasha_command == "purge":
            akasha.purge()
            return self.success("The Akasha has been returned to the Void.")

        elif request.akasha_command == "learn":
            # Manual ingestion of a file into global memory
            if not request.source_path:
                return self.failure("Source path required for manual learning.")

            # Implementation logic for manual ingestion would go here
            # using akasha.enshrine(...)
            return self.success("Manual learning logic is a future prophecy.")

        return self.failure("Unknown Akasha rite.")