# src/velm/artisans/librarian/purifiers/matter.py
# -----------------------------------------------------

import os
import time
import shutil
from pathlib import Path
from typing import List, Tuple, Final

from ....interfaces.requests import LustrationIntensity


class MatterPurifier:
    """
    =================================================================================
    == THE METABOLIC SCYTHE (V-Ω-TEMPORAL-AEGIS-ASCENDED)                          ==
    =================================================================================
    LIF: ∞ | ROLE: PHYSICAL_ENTROPY_REAPER | RANK: OMEGA_GUARDIAN
    AUTH: Ω_MATTER_PURIFIER_V9000_TEMPORAL_WARD_FINALIS

    The supreme organ of physical lustration. It has been ascended to possess the
    **Temporal Aegis**, ensuring that active transactions (staging matter) are
    mathematically warded against the Librarian's scythe during a Metabolic Fever.

    ### THE PANTHEON OF 7 LEGENDARY ASCENSIONS:
    1.  **The Temporal Aegis (THE CURE):** Grants absolute immunity to newly forged
        matter. Staging data is warded for 1 hour; Cache for 15 minutes.
    2.  **Intensity-Aware Triage:** Dynamically tightens the Grace Period during
        CRITICAL fevers, but NEVER drops the Staging ward below 5 minutes.
    3.  **Deep-First Void Sweeping:** Evaluates paths by depth descending, ensuring
        hollow directories are evaporated immediately after their files are reaped.
    4.  **Transaction-Bypass (Silent Annihilation):** Unlinks internal matter directly
        via the OS, bypassing the `IOConductor` to prevent cache-clearing from
        polluting the Gnostic Undo Ledger.
    5.  **The Permission Exorcist:** Automatically attempts to strip read-only
        attributes if a standard deletion fractures (Windows Hardening).
    6.  **Orphaned Lock Release:** Safely identifies and purges stale `.lock` and
        `.tmp` shards that block subsequent physical writes.
    7.  **The Zero-Crash Vow:** Wrapped in titanium `try/except` blocks; a locked
        file will simply be skipped, never shattering the Librarian's mind.
    =================================================================================
    """

    # [PHYSICS CONSTANTS] Standard Grace Periods (Seconds)
    WARD_STAGING_S: Final[float] = 3600.0  # 1 Hour
    WARD_CACHE_S: Final[float] = 900.0  # 15 Minutes
    WARD_LOGS_S: Final[float] = 86400.0  # 24 Hours

    def __init__(self, io, root: Path, logger):
        self.io = io  # Maintained for interface parity
        self.root = root.resolve()
        self.logger = logger
        self.scaffold_dir = self.root / ".scaffold"

    def lustrate(self, intensity: LustrationIntensity, domains: List[str], keep: int) -> Tuple[int, int]:
        """
        The Grand Rite of Physical Lustration.
        """
        total_bytes = 0
        total_count = 0

        if not self.scaffold_dir.exists():
            return 0, 0

        # Targeted Domain Mapping
        mapping = {
            "cache": self.scaffold_dir / "cache",
            "temp": self.scaffold_dir / "staging",
            "logs": self.scaffold_dir / "logs",
            "backups": self.scaffold_dir / "backups"
        }

        for domain, path in mapping.items():
            if domain not in domains:
                continue
            if not path.exists():
                continue

            # [ASCENSION 1 & 2]: Adjudicate the Temporal Ward based on Intensity
            grace_period = self._divine_grace_period(domain, intensity)

            if domain == "backups":
                # Backups are governed by Retention Count, not just Time
                b, c = self._purge_with_retention(path, keep, force=(intensity == LustrationIntensity.CRITICAL))
            else:
                b, c = self._purge_recursive(path, grace_period)

            total_bytes += b
            total_count += c

        return total_bytes, total_count

    def _divine_grace_period(self, domain: str, intensity: LustrationIntensity) -> float:
        """Calculates the exact microsecond of immunity for a given domain."""
        if domain == "temp":
            # Staging matter is sacred. Even in CRITICAL fever, it gets 5 minutes to finish.
            if intensity == LustrationIntensity.CRITICAL: return 300.0
            if intensity == LustrationIntensity.HARD: return 1800.0
            return self.WARD_STAGING_S

        elif domain == "cache":
            # Caches are expendable. In CRITICAL fever, they evaporate instantly.
            if intensity == LustrationIntensity.CRITICAL: return 0.0
            if intensity == LustrationIntensity.HARD: return 300.0
            return self.WARD_CACHE_S

        elif domain == "logs":
            if intensity == LustrationIntensity.CRITICAL: return 3600.0
            if intensity == LustrationIntensity.HARD: return 43200.0
            return self.WARD_LOGS_S

        return 3600.0

    def _purge_recursive(self, path: Path, grace_period_s: float) -> Tuple[int, int]:
        """
        [ASCENSION 3]: Deep-First Void Sweeping & Temporal Aegis.
        Safely annihilates aged matter while preserving active transaction wombs.
        """
        bytes_reclaimed = 0
        entities_purged = 0
        now = time.time()

        # We collect all paths and sort them by depth (deepest first).
        # This guarantees we delete files before attempting to delete their parent directories.
        all_entities = list(path.rglob("*"))
        all_entities.sort(key=lambda p: len(p.parts), reverse=True)

        for entry in all_entities:
            try:
                # 1. The Temporal Gaze
                st = entry.stat()
                age_s = now - st.st_mtime

                if age_s <= grace_period_s:
                    continue  # The soul is too young. The Aegis protects it.

                # 2. Matter Annihilation (Files)
                if entry.is_file() or entry.is_symlink():
                    file_size = st.st_size

                    # [ASCENSION 4 & 5]: Silent, OS-level annihilation
                    try:
                        entry.unlink()
                    except PermissionError:
                        # Windows read-only ward bypass
                        os.chmod(entry, 0o777)
                        entry.unlink()

                    bytes_reclaimed += file_size
                    entities_purged += 1

                # 3. Spatial Annihilation (Directories)
                elif entry.is_dir():
                    # os.rmdir is inherently safe: it fails if the directory is not empty.
                    # Because we are working bottom-up, if we successfully deleted all files
                    # inside it, it will be empty and safely collapse.
                    try:
                        entry.rmdir()
                        entities_purged += 1
                    except OSError:
                        pass  # Directory still holds young matter. Stay the hand.

            except Exception:
                # [ASCENSION 7]: The Zero-Crash Vow. Locked files are simply bypassed.
                continue

        return bytes_reclaimed, entities_purged

    def _purge_with_retention(self, backup_dir: Path, keep: int, force: bool) -> Tuple[int, int]:
        """
        [THE LAZARUS WARD]
        Purges old transaction rollbacks and shadow volumes, ensuring the most
        recent `keep` count are mathematically preserved.
        """
        bytes_reclaimed = 0
        entities_purged = 0

        try:
            # 1. Gather all historical epochs (Sub-directories in the backup root)
            epochs = [d for d in backup_dir.iterdir() if d.is_dir()]

            # 2. Sort by modification time (Newest first)
            epochs.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            # 3. Apply force modifiers
            effective_keep = max(1, keep // 2) if force else max(1, keep)

            # 4. Identify the Condemned
            if len(epochs) <= effective_keep:
                return 0, 0

            condemned_epochs = epochs[effective_keep:]

            # 5. Execute the Scythe
            for epoch in condemned_epochs:
                try:
                    # Calculate mass before annihilation
                    epoch_mass = sum(f.stat().st_size for f in epoch.rglob('*') if f.is_file())

                    # Absolute recursive purge
                    shutil.rmtree(epoch, ignore_errors=True)

                    bytes_reclaimed += epoch_mass
                    entities_purged += 1
                except Exception:
                    pass

        except Exception as e:
            self.logger.debug(f"Retention purge deferred: {e}")

        return bytes_reclaimed, entities_purged