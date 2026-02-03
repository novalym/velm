# Path: scaffold/core/kernel/transaction/staging.py
import shutil
import time
from pathlib import Path
from typing import Union

from ....logger import Scribe

Logger = Scribe("StagingManager")


class StagingManager:
    """
    =================================================================================
    == THE ARCHITECT OF EPHEMERAL REALITIES (V-Ω-APOTHEOSIS-ULTIMA)                ==
    =================================================================================
    This divine artisan forges, manages, and purifies the parallel universes
    (staging and backup directories) required for an unbreakable, atomic transaction.
    Its Gaze is one of foresight, its hand one of absolute purity.
    =================================================================================
    """

    def __init__(self, project_root: Path, tx_id: str):
        self.project_root = project_root
        self.tx_id = tx_id

        # --- The Sacred Sanctums ---
        self.scaffold_dir = self.project_root / ".scaffold"
        self.staging_root = self.scaffold_dir / "staging" / self.tx_id
        self.backup_root = self.scaffold_dir / "backups" / self.tx_id

        # Ascension VII: The Chronocache of Resolution
        self._path_cache: dict[Union[str, Path], Path] = {}

    def initialize_sanctums(self):
        """
        Ascension I & II: The Gnostic Triage & Disk Space Ward.
        Forges the required ephemeral directories with foresight.
        """
        start_time = time.monotonic()
        Logger.verbose(f"[{self.tx_id[:8]}] Initializing transactional sanctums...")

        # Ascension II: The Disk Space Ward (Heuristic Gaze)
        # A full recursive size check is too slow. We use a heuristic. If the .scaffold
        # dir exists, we assume we have enough space for a small transaction.
        # A future ascension could perform this gaze in a background thread.
        try:
            usage = shutil.disk_usage(self.project_root)
            if usage.free < 100 * 1024 * 1024:  # 100MB buffer
                Logger.warn(f"Disk space is low ({usage.free / 1024 ** 2:.0f}MB free). A large transaction may fail.")
        except FileNotFoundError:
            pass  # We may be creating the project root itself.

        self.scaffold_dir.mkdir(parents=True, exist_ok=True)
        self.staging_root.mkdir(parents=True, exist_ok=True)
        self.backup_root.mkdir(parents=True, exist_ok=True)

        duration = (time.monotonic() - start_time) * 1000
        Logger.verbose(f"[{self.tx_id[:8]}] Sanctums forged in {duration:.2f}ms.")

    def cleanup(self):
        """
        Ascension IV, XI & XII: The Unbreakable Ward, Telemetric Heartbeat, & Sentinel of the Void.
        Annihilates all ephemeral realities forged for this transaction.
        """
        start_time = time.monotonic()
        Logger.verbose(f"[{self.tx_id[:8]}] Purifying ephemeral realities...")

        for sanctum in [self.staging_root, self.backup_root]:
            # Ascension XII: The Sentinel of the Void
            if sanctum.exists() and self.scaffold_dir in sanctum.parents:
                try:
                    shutil.rmtree(sanctum, ignore_errors=True)
                except Exception as e:
                    # Ascension IV: The Unbreakable Ward
                    Logger.error(
                        f"A paradox occurred during cleanup of '{sanctum.name}': {e}. Manual cleanup may be required.")

        duration = (time.monotonic() - start_time) * 1000
        Logger.verbose(f"[{self.tx_id[:8]}] Purification complete in {duration:.2f}ms.")

    def get_staging_path(self, logical_path: Union[str, Path]) -> Path:
        """
        Ascension VI: The On-Demand Sanctum Forge.
        Returns the absolute path to a file within the staging area.
        """
        if logical_path in self._path_cache:
            return self._path_cache[logical_path]

        physical_path = self.staging_root / logical_path

        # Ensure the parent directory for the item exists within the staging area.
        physical_path.parent.mkdir(parents=True, exist_ok=True)

        self._path_cache[logical_path] = physical_path
        return physical_path

    def triangulate_relative_path(self, path: Path) -> Path:
        """
        Ascension V: The Hierophant of Relativity.
        Perceives a path's true, relative soul from any known reality.
        """
        if path.is_absolute():
            try:
                # Is it a path within our staging area?
                return path.relative_to(self.staging_root)
            except ValueError:
                try:
                    # Is it a path within the main project?
                    return path.relative_to(self.project_root)
                except ValueError:
                    # It's an external absolute path. We can only preserve its name.
                    return Path(path.name)

        # If it's already relative, check if it has staging components to strip
        parts = path.parts
        if ".scaffold" in parts and "staging" in parts:
            try:
                idx = parts.index(self.tx_id)
                return Path(*parts[idx + 1:])
            except ValueError:
                pass  # tx_id not in path, it's a clean relative path.

        return path

    def __repr__(self) -> str:
        """Ascension XI: The Forensic Dossier."""
        return (
            f"<StagingManager tx_id='{self.tx_id[:8]}' "
            f"staging='{self.staging_root.relative_to(self.project_root)}' "
            f"backup='{self.backup_root.relative_to(self.project_root)}'>"
        )