# Path: scaffold/core/kernel/transaction/rollback.py
import json
import shutil
import tempfile
import traceback
from pathlib import Path
from typing import TYPE_CHECKING, Tuple, Any

from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

if TYPE_CHECKING:
    from .staging import StagingManager
    from .contracts import TransactionalGnosis

Logger = Scribe("RollbackChronomancer")


class RollbackChronomancer:
    """
    =================================================================================
    == THE CHRONOMANCER OF TEMPORAL INVERSION (V-Ω-APOTHEOSIS-ULTIMA)              ==
    =================================================================================
    This divine artisan is the ultimate guardian of reality. When a paradox shatters
    a transaction, it awakens to perform a perfect, surgical, and forensically-aware
    restoration of the cosmos to its original, pure state.
    =================================================================================
    """

    def __init__(self, staging_manager: "StagingManager", project_root: Path, logger: Scribe):
        self.staging_manager = staging_manager
        self.project_root = project_root
        self.logger = logger

    def perform_emergency_rollback(self):
        """
        Ascension I: The Gnostic Triage of Reality.
        Restores reality from the backup sanctum.
        This is the rite of absolute reversal.
        """
        self.logger.warn("A paradox was perceived. The Chronomancer awakens to reverse time...")

        # We only need to restore from backup if files were actually moved to the project root.
        # If the transaction failed before the commit phase, we only need to clean up staging.
        # This is a conceptual check; the physical check is whether the backup dir has content.

        if not self.staging_manager.backup_root.exists() or not any(self.staging_manager.backup_root.iterdir()):
            self.logger.info("No temporal echo found. The paradox occurred before reality was altered.")
            return

        self.logger.info("Restoring reality from the sacred temporal echo...")
        restored_count = 0
        try:
            # Ascension VI: The Intelligent Restorer
            for backup_artifact in self.staging_manager.backup_root.rglob("*"):
                try:
                    rel_path = backup_artifact.relative_to(self.staging_manager.backup_root)
                    live_path = self.project_root / rel_path

                    if backup_artifact.is_dir():
                        live_path.mkdir(parents=True, exist_ok=True)
                    else:
                        live_path.parent.mkdir(parents=True, exist_ok=True)
                        # We use move for efficiency and atomicity
                        shutil.move(str(backup_artifact), str(live_path))
                        restored_count += 1
                except Exception as e:
                    # Ascension IV: The Unbreakable Ward
                    self.logger.error(f"A minor paradox occurred restoring '{backup_artifact.name}': {e}")

            self.logger.success(
                f"Temporal Inversion complete. {restored_count} scripture(s) have been restored to their pure state.")

        except Exception as e:
            raise ArtisanHeresy("A catastrophic meta-heresy shattered the Rollback Chronomancer.",
                                child_heresy=e) from e

    def archive_failed_rite(self, gnosis: "TransactionalGnosis", exc_type: Any, exc_val: Any, exc_tb: Any):
        """
        Ascension II: The Forensic Archivist.
        Forges a complete, self-contained dossier of the fallen rite for post-mortem inquest.
        """
        if not self.staging_manager.staging_root.exists() and not self.staging_manager.backup_root.exists():
            return

        try:
            failed_rites_dir = self.staging_manager.scaffold_dir / "failed_rites"
            failed_rites_dir.mkdir(parents=True, exist_ok=True)

            rite_name_safe = gnosis.rite_name.replace(" ", "_").replace(":", "")
            archive_name = f"{rite_name_safe}_{gnosis.tx_id[:8]}"
            archive_path_base = failed_rites_dir / archive_name

            with tempfile.TemporaryDirectory() as tmpdir:
                dossier_root = Path(tmpdir)

                # Copy the state of the transaction into the archive
                if self.staging_manager.staging_root.exists():
                    shutil.copytree(self.staging_manager.staging_root, dossier_root / "staged_reality_(after)")
                if self.staging_manager.backup_root.exists():
                    shutil.copytree(self.staging_manager.backup_root, dossier_root / "backup_snapshot_(before)")

                # Forge the heresy dossier
                heresy_content = {
                    "gnosis": gnosis.model_dump(),
                    "heresy": {
                        "type": str(exc_type.__name__ if exc_type else "Unknown"),
                        "message": str(exc_val),
                        "traceback": traceback.format_exc(),
                    }
                }
                (dossier_root / "__heresy__.json").write_text(json.dumps(heresy_content, indent=2))

                # Create the final zip archive
                final_archive_path = shutil.make_archive(str(archive_path_base), 'zip', str(dossier_root))

                self.logger.warn(
                    f"A forensic dossier of the fallen rite has been archived at: [cyan]{Path(final_archive_path).name}[/cyan]")

        except Exception as archive_heresy:
            # The Unbreakable Ward must protect even the archivist.
            self.logger.error(f"A meta-heresy occurred during the Rite of Archival: {archive_heresy}")