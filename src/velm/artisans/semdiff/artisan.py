# Path: scaffold/artisans/semdiff/artisan.py
# ------------------------------------------

import subprocess
from pathlib import Path

from rich.table import Table
from rich.panel import Panel

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import SemDiffRequest
from ...help_registry import register_artisan
from ...inquisitor import get_treesitter_gnosis
from ...core.cortex.semantic_comparator import SemanticComparator


@register_artisan("semdiff")
class SemDiffArtisan(BaseArtisan[SemDiffRequest]):
    """
    =============================================================================
    == THE SEMANTIC DIFF (V-Ω-ARCHITECTURAL-REVIEW)                            ==
    =============================================================================
    LIF: 10,000,000,000

    Compares the current reality against a Git reference (HEAD).
    Instead of lines, it reports on Symbols (Functions, Classes).
    """

    def execute(self, request: SemDiffRequest) -> ScaffoldResult:
        target_path = (self.project_root / request.target).resolve()

        if not target_path.exists():
            return self.failure(f"Target '{request.target}' not found.")

        if target_path.is_dir():
            # Future: Recurse directories
            return self.failure("Semantic Diff currently supports single files only.")

        self.logger.info(f"Comparing '{target_path.name}' against reference '[cyan]{request.reference}[/cyan]'...")

        # 1. Get Current Gnosis
        try:
            current_content = target_path.read_text(encoding='utf-8')
            current_gnosis = get_treesitter_gnosis(target_path, current_content)
        except Exception as e:
            return self.failure(f"Failed to read current reality: {e}")

        # 2. Get Reference Gnosis (via Git)
        try:
            rel_path = target_path.relative_to(self.project_root).as_posix()
            # git show HEAD:src/main.py
            old_content = subprocess.check_output(
                ["git", "show", f"{request.reference}:{rel_path}"],
                cwd=self.project_root, text=True, stderr=subprocess.DEVNULL
            )
            old_gnosis = get_treesitter_gnosis(target_path, old_content)  # Pass path for language detection
        except subprocess.CalledProcessError:
            return self.failure(f"Could not retrieve reference '{request.reference}' for this file.")

        # 3. The Comparator
        comparator = SemanticComparator()
        changes = comparator.compare(old_gnosis, current_gnosis)

        if not changes:
            return self.success("No semantic changes detected. The structure is stable.")

        # 4. The Proclamation
        table = Table(title=f"Semantic Diff: {target_path.name}", border_style="blue")
        table.add_column("Type", style="dim", width=8)
        table.add_column("Symbol", style="bold white")
        table.add_column("Change", justify="center", width=10)
        table.add_column("Details", style="cyan")

        for c in changes:
            style = "green" if c.change_type == "ADDED" else "red" if c.change_type == "REMOVED" else "yellow"
            table.add_row(
                c.symbol_type,
                c.symbol_name,
                f"[{style}]{c.change_type}[/{style}]",
                c.details
            )

        self.console.print(table)

        return self.success(f"Identified {len(changes)} semantic shifts.")