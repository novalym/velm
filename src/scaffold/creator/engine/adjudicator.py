# Path: scaffold/creator/engine/adjudicator.py
# --------------------------------------------


from pathlib import Path
from typing import Set, TYPE_CHECKING, Any, Union
from rich.panel import Panel
from ...contracts.data_contracts import GnosticWriteResult
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...utils import atomic_write
from ...logger import Scribe, get_console

if TYPE_CHECKING:
    from .facade import QuantumCreator
    from ...genesis.genesis_engine.engine import GenesisEngine

Logger = Scribe("GnosticAdjudicator")


class GnosticAdjudicator:
    """
    =============================================================================
    == THE CONSCIENCE OF THE ENGINE (V-Ω-JUDGE-POLYMORPHIC)                    ==
    =============================================================================
    Handles the Sentinel Inquest and Dynamic Ignore updates.
    Now accepts any Gnostic Engine (QuantumCreator or GenesisEngine) that holds
    state, sanctum, and transaction.
    """

    def __init__(self, creator: Union['QuantumCreator', 'GenesisEngine', Any]):
        self.creator = creator
        self.console = get_console()

    def conduct_sentinel_inquest(self):
        """Summons the Sentinel to judge newly-born souls."""
        # [FACULTY 1] The Gnostic Check for Capability
        # We ensure the creator actually has the conduit before accessing it.
        if not hasattr(self.creator, 'sentinel_conduit') or \
           not self.creator.sentinel_conduit or \
           not self.creator.sentinel_conduit.sentinel_path:
            Logger.warn("Adjudication skipped: SentinelConduit is dormant or missing.")
            return

        if not self.creator.transaction: return

        for result in self.creator.transaction.write_dossier.values():
            if result.success and result.action_taken in ("CREATED", "TRANSFIGURED") and result.bytes_written > 0:
                staged_path = result.path
                try:
                    staged_content = self.creator.sanctum.read_text(staged_path)
                    heresies = self.creator.sentinel_conduit.adjudicate(Path(staged_path).name, staged_content)
                    if any(h.severity == HeresySeverity.CRITICAL for h in heresies):
                        from rich.table import Table
                        heresy_table = Table(title=f"[bold]Heresies in '{Path(staged_path).name}'[/bold]", box=None)
                        heresy_table.add_column("L#", style="magenta");
                        heresy_table.add_column("Heresy", style="red")
                        for h in heresies: heresy_table.add_row(str(h.line_num), h.message)
                        self.console.print(Panel(heresy_table, border_style="red"))
                        raise ArtisanHeresy(
                            "The Sentinel's Gaze perceived a CRITICAL heresy. Transaction will be rolled back.")
                except Exception as e:
                    if isinstance(e, ArtisanHeresy): raise e
                    raise ArtisanHeresy(f"A paradox shattered the Gnostic Adjudication: {e}", child_heresy=e)

    def conduct_dynamic_ignore(self):
        """Updates .gitignore with secrets found during creation."""
        if not self.creator.transaction or not self.creator.transaction.write_dossier:
            return

        files_to_ignore: Set[str] = set()

        for path, result in self.creator.transaction.write_dossier.items():
            if not result.success: continue
            if result.security_notes:
                Logger.warn(f"Security Alert: Secrets detected in '{result.name}'. Adding to ignore list.")
                files_to_ignore.add(result.name)

        if files_to_ignore:
            self._update_gitignore(files_to_ignore)

    def _update_gitignore(self, files_to_ignore: Set[str]):
        gitignore_path = self.creator.sanctum.root / ".gitignore"
        existing_ignores = set()

        if gitignore_path.exists():
            try:
                content = gitignore_path.read_text(encoding='utf-8')
                existing_ignores = {line.strip() for line in content.splitlines() if
                                    line.strip() and not line.startswith('#')}
            except Exception:
                pass

        new_ignores = files_to_ignore - existing_ignores

        if new_ignores:
            Logger.info(f"Dynamic Ignorer adding {len(new_ignores)} artifact(s) to .gitignore...")
            append_content = "\n# [Scaffold Dynamic Ignorer] Secrets/Sensitive Artifacts\n" + "\n".join(
                sorted(new_ignores)) + "\n"

            current_content = ""
            if gitignore_path.exists():
                current_content = gitignore_path.read_text(encoding='utf-8')

            final_content = current_content + append_content

            try:
                atomic_write(gitignore_path, final_content, Logger, self.creator.project_root)
                Logger.success("Veil of Ignorance updated.")
            except Exception as e:
                Logger.warn(f"Failed to update .gitignore: {e}")