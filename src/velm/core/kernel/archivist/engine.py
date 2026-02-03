# Path: scaffold/core/kernel/archivist/engine.py
# ----------------------------------------------

import shutil
import time
from pathlib import Path
from typing import List, Optional, Union

from .contracts import ArchiveConfig, ArchiveResult, RestoreConfig, RestoreResult
from .storage import GnosticStorage
from .restorer import GnosticRestorer
from .retention import GnosticReaper
from ....logger import Scribe
from ....utils import get_human_readable_size

Logger = Scribe("GnosticArchivist")


class GnosticArchivist:
    """
    =================================================================================
    == THE KEEPER OF ECHOES (V-Ω-MODULAR-ENGINE)                                   ==
    =================================================================================
    The Sovereign Conductor of the Archival Symphony. It coordinates the Filter,
    The Scribe, The Storage, and The Reaper to perform the perfect snapshot.
    """

    def __init__(self, project_root: Path, config: Optional[ArchiveConfig] = None):
        self.project_root = project_root.resolve()
        self.backup_root = self.project_root / ".scaffold" / "backups"
        self.config = config or ArchiveConfig()

        # Ensure sanctum exists
        if not self.backup_root.exists():
            self.backup_root.mkdir(parents=True, exist_ok=True)

    def _check_disk_space(self, estimated_bytes: int):
        """[FACULTY 10] The Space Ward."""
        try:
            usage = shutil.disk_usage(self.backup_root)
            if usage.free < estimated_bytes * 2:  # Require 2x buffer
                Logger.warn(f"Disk space is low. Snapshot may fail. Free: {get_human_readable_size(usage.free)}")
        except Exception:
            pass

    def create_snapshot(self, targets: List[Path], reason: str = "manual") -> Optional[Path]:
        """
        The Grand Rite of Archival.
        Creates a compressed, manifest-enriched snapshot of the target files.
        """
        start_time = time.monotonic()

        # 1. Existence Check
        valid_targets = [p.resolve() for p in targets if p.exists()]
        if not valid_targets:
            Logger.verbose("No material souls to preserve.")
            return None

        # 2. Forge Name
        timestamp = int(time.time())
        ext = "tar.gz" if self.config.compression == "gz" else f"tar.{self.config.compression}"
        # Sanitize reason for filename
        safe_reason = "".join(c for c in reason if c.isalnum() or c in ('_', '-'))
        archive_name = f"{timestamp}_{safe_reason}.{ext}"
        dest_path = self.backup_root / archive_name

        # 3. Space Check (Heuristic: 50MB buffer)
        self._check_disk_space(50 * 1024 * 1024)

        Logger.info(f"Forging Snapshot: [cyan]{archive_name}[/cyan] ({len(valid_targets)} sources)...")

        try:
            # 4. Summon Storage Artisan
            storage = GnosticStorage(self.project_root, self.config)

            # 5. Inscribe
            size, digest, skipped = storage.inscribe(valid_targets, dest_path, reason)

            # 6. Verify (Optional)
            if self.config.verify_integrity:
                from ....utils import hash_file
                if hash_file(dest_path) != digest:
                    raise RuntimeError("Cryptographic Verification Failed after write.")

            # 7. Reap Old Souls
            GnosticReaper.reap(self.backup_root, self.config.retention_count)

            duration = (time.monotonic() - start_time) * 1000
            size_str = get_human_readable_size(size)

            Logger.success(f"Snapshot Secured: {archive_name} ({size_str}) in {duration:.0f}ms")

            if skipped:
                Logger.verbose(f"   -> {len(skipped)} heavy/profane items filtered from archive.")

            return dest_path

        except Exception as e:
            Logger.error(f"Archival Paradox: {e}", exc_info=True)
            # We cleanse the partial artifact
            if dest_path.exists():
                try:
                    dest_path.unlink()
                except OSError:
                    pass
            return None

    def restore_snapshot(self, snapshot_path: Union[str, Path],
                         config: Optional[RestoreConfig] = None) -> RestoreResult:
        """
        The Rite of Resurrection.
        Restores a previous state from a snapshot.
        """
        snap_path = Path(snapshot_path).resolve()
        if not snap_path.exists():
            Logger.error(f"Snapshot not found: {snap_path}")
            return RestoreResult(False, 0, 0, 0.0, ["Snapshot missing"])

        Logger.warn(f"Initiating Resurrection from: [yellow]{snap_path.name}[/yellow]")

        restore_config = config or RestoreConfig()
        restorer = GnosticRestorer(self.project_root, restore_config)

        return restorer.resurrect(snap_path)