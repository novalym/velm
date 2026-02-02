# Path: scaffold/core/kernel/chronicle/archivist.py
import json
import shutil
from pathlib import Path
from typing import Dict

from ....logger import Scribe

Logger = Scribe("ChronicleArchivist")


class GnosticArchivist:
    """
    =================================================================================
    == THE KEEPER OF ECHOES (V-Ω-ETERNAL-APOTHEOSIS)                               ==
    =================================================================================
    This divine artisan is the guardian of the Gnostic Timeline. Its one true purpose
    is to take the scripture of the immediate past (`scaffold.lock`) and enshrine it
    in the eternal library (`.scaffold/chronicles/`) with a new, luminous name,
    preserving it as an echo for all time.
    =================================================================================
    """

    def __init__(self, lock_path: Path, project_root: Path):
        self.lock_path = lock_path
        self.chronicles_dir = project_root / ".scaffold" / "chronicles"

    def archive_previous_chronicle(self, old_lock_data: Dict) -> Dict:
        """
        Performs the Rite of Archival.
        Returns the manifest from the archived data for the Federator.
        """
        # Ascension IV: The Gaze of the Void
        if not self.lock_path.exists():
            return {}

        try:
            # The Gaze is now upon the pre-loaded data, not the file system.
            # This makes the artisan purer and more testable.
            if not old_lock_data:
                old_lock_data = json.loads(self.lock_path.read_text(encoding='utf-8'))

            # Ascension IX: The Sentinel of Existence
            self.chronicles_dir.mkdir(parents=True, exist_ok=True)

            # Ascension VI: The Rite Namer
            prov = old_lock_data.get("provenance", {})
            rite_id = prov.get("rite_id", "unknown")[:8]
            rite_name = prov.get("rite_name", "rite").replace(" ", "_").lower()
            archive_name = f"{rite_name}_{rite_id}.lock"

            archive_path = self.chronicles_dir / archive_name

            # Ascension X: The Rite of Pure Transmutation
            shutil.copy2(self.lock_path, archive_path)

            Logger.verbose(f"Archived previous chronicle as '[cyan]{archive_name}[/cyan]'.")
            return old_lock_data.get("manifest", {})

        except (json.JSONDecodeError, IOError, OSError) as e:
            # Ascension V: The Unbreakable Ward of Paradox
            Logger.warn(f"The Rite of Archival was stayed by a paradox: {e}. The old chronicle may not be preserved.")
            return {}
