# Path: scaffold/artisans/tool/hash_artisan.py
# ----------------------------------------------
from ...core.artisan import BaseArtisan
from ...interfaces.requests import HashRequest
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan
from ...utils import hash_file

@register_artisan("hash")
class HashArtisan(BaseArtisan[HashRequest]):
    """The Cryptographic Sealer. Forges integrity hashes."""
    def execute(self, request: HashRequest) -> ScaffoldResult:
        self.logger.info(f"Forging a [cyan]{request.algo}[/cyan] seal for [yellow]{request.file_path.name}[/yellow]...")
        # ... Implementation logic would reside here.
        # 1. Use `utils.hash_file` with the specified algorithm.
        # 2. Proclaim the final hash to the console.
        # 3. Bonus: Proclaim the full `@hash(sha256:...)` string for easy copy-pasting.
        file_hash = hash_file(request.file_path, algorithm=request.algo)
        self.console.print(f"\n[bold green]Cryptographic Seal Forged:[/bold green]")
        self.console.print(f"  [bold cyan]@{request.algo}:{file_hash}[/bold cyan]\n")
        return self.success("Seal forged.", data={"hash": file_hash})