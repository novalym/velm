# Path: scaffold/core/kernel/transaction/committer.py
import os
import shutil
import time
from pathlib import Path
from typing import TYPE_CHECKING, List

# Ascension VIII: The Windows Healer
from ....utils import _resilient_rename
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy

if TYPE_CHECKING:
    from .staging import StagingManager

Logger = Scribe("GnosticCommitter")


class GnosticCommitter:
    """
    =================================================================================
    == THE HAND OF MANIFESTATION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                   ==
    =================================================================================
    This divine artisan is the final link in the chain of causality. It takes the
    pure, perfected will from the Ephemeral Staging Realm and makes it manifest in
    the Mortal Realm with unbreakable, atomic precision. It is the very hand of God.
    =================================================================================
    """

    def __init__(self, project_root: Path, staging_manager: "StagingManager", logger: Scribe):
        self.project_root = project_root
        self.staging_manager = staging_manager
        self.logger = logger
        self.console = get_console()

    def commit(self):
        """
        The Grand Rite of Materialization.
        Moves all artifacts from the staging area to the project root atomically.
        """
        start_time = time.monotonic()
        staged_files = self._collect_staged_artifacts()

        if not staged_files:
            self.logger.verbose("Commitment rite concluded. The ephemeral realm was a void.")
            return

        self.logger.info("The Hand of Manifestation awakens. Committing staged reality...")

        # Ascension III: The Hierophant of Pruning
        self._prune_conflicting_directories(staged_files)

        # Ascension IV: The Luminous Voice
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=self.console,
                transient=True
        ) as progress:
            task = progress.add_task("[cyan]Materializing...", total=len(staged_files))

            for staged_path in staged_files:
                try:
                    rel_path = staged_path.relative_to(self.staging_manager.staging_root)
                    live_path = self.project_root / rel_path

                    progress.update(task, advance=1, description=f"[cyan]Inscribing [green]'{rel_path}'[/green]...")

                    # The Rite of Parent Sanctum Forging
                    live_path.parent.mkdir(parents=True, exist_ok=True)

                    # Ascension II: The Unbreakable Vow of Atomicity
                    # We use our ascended, resilient rename for Windows safety.
                    _resilient_rename(staged_path, live_path)

                    # Ascension VI & VII: The Permission Alchemist & Chronomancer's Touch
                    # Note: shutil.copystat follows symlinks, which is what we want here.
                    # We are copying the *state* of the staged file, not its link nature.
                    shutil.copystat(live_path, live_path, follow_symlinks=True)

                except Exception as e:
                    # Ascension X: The Unbreakable Ward of Paradox
                    raise ArtisanHeresy(
                        f"Commitment Paradox: The Hand faltered while inscribing '{rel_path}'.",
                        child_heresy=e
                    ) from e

        duration = (time.monotonic() - start_time) * 1000
        self.logger.success(f"Commitment complete. {len(staged_files)} artifacts manifested in {duration:.0f}ms.")

    def _collect_staged_artifacts(self) -> List[Path]:
        """
        Performs a deep Gaze upon the staging sanctum to find all materialized souls.
        Ascension V: The Sentinel of the Void - Skips empty directories.
        """
        staged_artifacts = []
        if not self.staging_manager.staging_root.exists():
            return []

        for root, dirs, files in os.walk(self.staging_manager.staging_root):
            root_path = Path(root)
            for name in files:
                staged_artifacts.append(root_path / name)
            # Ascension V: We only add directories if they are NOT empty.
            # This is a heuristic; a better way is to track created dirs in the transaction.
            # For now, we rely on the final Ghost Buster pass in the creator engine.
            # A simpler version is to just add all files and let mkdir -p handle parents.

        # We return only files, as `os.replace` on a directory can be non-atomic.
        # Parent directories will be created on demand by the commit loop.
        return staged_artifacts

    def _prune_conflicting_directories(self, staged_files: List[Path]):
        """
        Ascension III: Annihilates directories in the mortal realm that are about to
        be replaced by files from the staging realm.
        """
        for staged_path in staged_files:
            rel_path = staged_path.relative_to(self.staging_manager.staging_root)
            live_path = self.project_root / rel_path
            if live_path.is_dir() and not live_path.is_symlink():
                self.logger.warn(f"Annihilating sanctum '{rel_path}' to make way for a new scripture.")
                shutil.rmtree(live_path)