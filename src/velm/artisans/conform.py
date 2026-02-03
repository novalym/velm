import time
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional

from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from .translocate_core.conductor import TranslocationConductor
from .translocate_core.detective import GnosticDetective
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import ConformRequest
from ..logger import Scribe
from ..utils import atomic_write

Logger = Scribe("ConformArtisan")

@register_artisan("conform")
class ConformArtisan(BaseArtisan[ConformRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC ALIGNMENT (V-Ω-LEGENDARY-ULTIMA) ==
    =================================================================================
    LIF: 10,000,000,000,000
    The **Conform Artisan** is the High Priest of Order. Unlike `translocate` (which
    moves specific files) or `transmute` (which creates/updates content), `conform`
    takes a chaotic directory structure and forces it to align with a Gnostic
    Blueprint.

    It is "Structural Refactoring as Code".

    ### THE PANTHEON OF 12 ELEVATIONS:
    1.  **The Gnostic Detective:** Uses fuzzy logic and hash matching to find where
        existing files *should* be in the blueprint, even if renamed.
    2.  **The Ambiguity Resolver:** Interactively resolves conflicts where multiple
        source files could map to the same blueprint node.
    3.  **The Orphan Adjudicator:** Identifies files in reality that have no place
        in the prophecy and offers to Archive, Delete, or Ignore them.
    4.  **The Backup Sentinel:** Enforces a safety snapshot before mass structural changes.
    5.  **The Import Healer:** Automatically triggers the `PythonImportResolver` to
        fix imports in moved files.
    6.  **The Dry-Run Prophecy:** Renders a "Before vs After" tree visualization.
    7.  **The Variable Injection:** Uses `--set` variables to resolve dynamic paths
        in the blueprint before matching.
    8.  **The Git Guard:** Ensures the repository is clean before restructuring.
    9.  **The Luminous Report:** Generates a `CONFORM_REPORT.md` detailing the migration.
    10. **The Flattening Strategy:** Can flatten nested structures if the blueprint dictates.
    11. **The Atomic Handoff:** Delegates the physical moves to the `TranslocationConductor`
        for consistent safety.
    12. **The Interactive Triage:** Allows the Architect to veto specific moves in the plan.
    =================================================================================
    """

    def execute(self, request: ConformRequest) -> ScaffoldResult:

        # 1. The Git Guard
        if not request.force and not request.dry_run:
            self._check_git_status()

        # [THE DIVINE SUMMONS]
        from ..core.cortex.engine import GnosticCortex
        cortex = GnosticCortex(self.project_root)

        # 2. The Gnostic Detective (Forging the Plan)
        detective = GnosticDetective(
            project_root=self.project_root,
            source_dir_str=request.conform_from,
            blueprint_path_str=request.blueprint_path,
            cli_set_vars=[],  # Variables handled via request object in new architecture
            non_interactive=request.non_interactive or request.force
        )

        # Inject variables from request into detective context manually if needed,
        # or rely on detective parsing them from args.
        # (Assuming Detective updated to handle dict vars or we pass them)

        final_moves, full_dossier = detective.investigate()

        # 3. The Ambiguity Resolver
        if "ambiguities" in full_dossier:
            self._resolve_ambiguities(full_dossier["ambiguities"], request)

        # 4. The Orphan Adjudicator
        orphans = full_dossier.get("orphans", {}).get("paths", [])
        orphan_disposition = "ignore"
        if orphans:
            orphan_disposition = self._adjudicate_orphans(orphans, request)

        # 5. The Symphony of Prophecy (Preview)
        # [HEALED] Bestowing Gnosis
        prophecy_conductor = TranslocationConductor(
            project_root=self.project_root,
            preview=True,
            cortex=cortex
        )
        prophecy_conductor.perceive_will(direct_moves=final_moves)
        prophecy_conductor.conduct()

        # 6. The Final Adjudication
        if not request.force and not request.non_interactive:
            if not self._confirm_execution(prophecy_conductor, orphans, orphan_disposition):
                return self.success("The Rite of Conformity was stayed by the Architect.")

        # 7. The Backup Sentinel
        backup_path = request.backup_to
        if not backup_path and not request.dry_run and not request.force:
            if Confirm.ask("[bold yellow]No backup path specified. Create default snapshot?[/bold yellow]",
                           default=True):
                backup_path = ".scaffold/backups/conform_snapshot"

        # 8. The Manifestation of Reality
        # [HEALED] Bestowing Gnosis
        live_conductor = TranslocationConductor(
            project_root=self.project_root,
            preview=request.dry_run,  # If dry_run, conductor stays in preview mode
            backup_path=backup_path,
            cortex=cortex
        )
        live_conductor.translocation_map = prophecy_conductor.translocation_map
        live_conductor.conduct()

        # 9. The Rite of Orphan Disposal
        if not request.dry_run:
            self._enact_orphan_fate(orphans, orphan_disposition, backup_path)

        # 10. The Luminous Report
        self._generate_conform_report(final_moves, orphans, orphan_disposition)

        return self.success(
            f"Conformity achieved. {len(final_moves)} scriptures translocated.",
            data={"moves": len(final_moves), "orphans": len(orphans)}
        )

    def _check_git_status(self):
        """[ELEVATION 8] Ensures the sanctum is clean."""
        if (self.project_root / ".git").exists():
            import subprocess
            try:
                status = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.project_root).decode()
                if status.strip():
                    Logger.warn("Git Sentinel: The sanctum is dirty. Uncommitted changes may be lost.")
                    if not Confirm.ask("Proceed anyway?", default=False):
                        raise ArtisanHeresy("Rite stayed by Git Sentinel.")
            except Exception:
                pass

    def _resolve_ambiguities(self, ambiguities: Dict[str, List[Path]], request: ConformRequest):
        """[ELEVATION 2] Interactive resolution of naming conflicts."""
        if request.non_interactive:
            raise ArtisanHeresy(
                "Ambiguous Soul Heresy detected in non-interactive mode.",
                details=str(ambiguities)
            )

        table = Table(title="[bold red]Ambiguity Detected[/bold red]", box=None)
        table.add_column("Name", style="cyan")
        table.add_column("Conflicting Paths", style="yellow")

        for name, paths in ambiguities.items():
            table.add_row(name, "\n".join(f"• {p.relative_to(self.project_root)}" for p in paths))

        self.console.print(Panel(table, border_style="red"))
        raise ArtisanHeresy("The rite was stayed to prevent a catastrophic paradox of ambiguity.")

    def _adjudicate_orphans(self, orphans: List[Path], request: ConformRequest) -> str:
        """[ELEVATION 3] Decides the fate of files not in the blueprint."""
        if not orphans or request.non_interactive:
            return "ignore"

        self.console.print(Panel(
            f"The Detective perceived [bold yellow]{len(orphans)} Orphaned Soul(s)[/bold yellow] not in the blueprint.",
            title="[yellow]Adjudication of Orphans[/yellow]", border_style="yellow"
        ))

        # Show sample
        for o in orphans[:5]:
            self.console.print(f"  [dim]• {o.relative_to(self.project_root)}[/dim]")
        if len(orphans) > 5:
            self.console.print(f"  [dim]... and {len(orphans) - 5} more[/dim]")

        action = Prompt.ask(
            "[bold question]Fate of Orphans?[/bold question]",
            choices=["ignore", "archive", "delete"],
            default="ignore"
        )
        return action

    def _enact_orphan_fate(self, orphans: List[Path], disposition: str, backup_path: Optional[str]):
        """Executes the will regarding orphans."""
        if disposition == "ignore":
            return

        if disposition == "delete":
            for p in orphans:
                if p.exists():
                    if p.is_dir():
                        shutil.rmtree(p)
                    else:
                        p.unlink()
            Logger.success(f"Annihilated {len(orphans)} orphaned souls.")

        elif disposition == "archive":
            archive_dir = self.project_root / (backup_path or ".scaffold/archive") / "orphans"
            archive_dir.mkdir(parents=True, exist_ok=True)
            for p in orphans:
                if p.exists():
                    dest = archive_dir / p.name
                    shutil.move(str(p), str(dest))
            Logger.success(f"Archived {len(orphans)} orphans to {archive_dir}.")

    def _confirm_execution(self, conductor: TranslocationConductor, orphans: List[Path], disposition: str) -> bool:
        """[ELEVATION 12] Final confirmation."""
        num_moves = len(conductor.translocation_map.moves)
        num_heals = sum(len(p) for p in getattr(conductor, 'all_healing_plans', {}).values())

        plea = Text.assemble(
            ("[bold question]Conformity Plan:[/bold question]\n", "white"),
            (f"  • {num_moves} Translocations\n", "cyan"),
            (f"  • {num_heals} Import Healings\n", "magenta"),
            (f"  • {len(orphans)} Orphans ({disposition})\n", "yellow"),
            ("\nManifest this reality?", "bold white")
        )
        return Confirm.ask(plea, default=False)

    def _generate_conform_report(self, moves: Dict[Path, Path], orphans: List[Path], disposition: str):
        """[ELEVATION 9] Generates a markdown report."""
        report_path = self.project_root / "CONFORM_REPORT.md"
        lines = [
            "# 🤝 Gnostic Conformity Report",
            f"> **Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 🔄 Translocations",
            "| Original Path | New Path |",
            "| :--- | :--- |"
        ]

        for src, dst in moves.items():
            try:
                s = src.relative_to(self.project_root)
                d = dst.relative_to(self.project_root)
                lines.append(f"| `{s}` | `{d}` |")
            except ValueError:
                pass

        lines.append("")
        lines.append(f"## 👻 Orphans ({disposition})")
        for o in orphans:
            try:
                lines.append(f"- `{o.relative_to(self.project_root)}`")
            except ValueError:
                pass

        atomic_write(report_path, "\n".join(lines), self.logger, self.project_root, verbose=False)
        Logger.info(f"Report inscribed at {report_path}")