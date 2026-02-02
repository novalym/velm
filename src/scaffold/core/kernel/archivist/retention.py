# Path: scaffold/core/kernel/archivist/retention.py
# -------------------------------------------------

from pathlib import Path
from typing import List
from ....logger import Scribe

Logger = Scribe("TheReaper")


class GnosticReaper:
    """
    =============================================================================
    == THE REAPER OF OLD SOULS (V-Ω-RETENTION-POLICY)                          ==
    =============================================================================
    Ensures the Sanctum does not overflow with echoes of the past.
    """

    @staticmethod
    def reap(backup_dir: Path, retention_count: int):
        if not backup_dir.exists(): return

        # Gather all archives
        archives = sorted(
            list(backup_dir.glob("*.tar.*")),
            key=lambda f: f.stat().st_mtime,
            reverse=True  # Newest first
        )

        if len(archives) <= retention_count:
            return

        # Identify the condemned
        condemned = archives[retention_count:]

        if condemned:
            Logger.info(f"Reaping {len(condemned)} ancient snapshot(s)...")

        for spirit in condemned:
            try:
                spirit.unlink()
                Logger.verbose(f"   -> Returned to Void: {spirit.name}")
            except Exception as e:
                Logger.warn(f"Failed to reap '{spirit.name}': {e}")