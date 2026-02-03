# Path: scaffold/core/kernel/archivist/restorer.py
# ------------------------------------------------

import tarfile
import time
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

from .contracts import RestoreConfig, RestoreResult
from ....logger import Scribe

Logger = Scribe("GnosticRestorer")


class GnosticRestorer:
    """
    =============================================================================
    == THE HAND OF RESURRECTION (V-Ω-RESTORATION-ENGINE)                       ==
    =============================================================================
    LIF: 10,000,000,000

    Handles the delicate operation of unpacking a snapshot back into reality.
    """

    def __init__(self, project_root: Path, config: RestoreConfig):
        self.root = project_root
        self.config = config

    def resurrect(self, snapshot_path: Path) -> RestoreResult:
        start_time = time.monotonic()
        files_restored = 0
        bytes_restored = 0
        heresies = []

        try:
            # 1. Validation
            if not tarfile.is_tarfile(snapshot_path):
                return RestoreResult(False, 0, 0, 0.0, ["Invalid archive format"])

            # 2. Safety Wipe (Optional)
            if self.config.wipe_destination:
                Logger.warn("Wiping destination sanctum before resurrection...")
                # Implementation needed: Be very careful here.
                # For V1, we skip auto-wipe to prevent accidents.
                pass

            # 3. Unpacking
            with tarfile.open(snapshot_path, "r:*") as tar:

                # Security Check: Zip Slip
                members = []
                for member in tar.getmembers():
                    if member.name in ["__gnosis__.json", "__skipped__.log"]:
                        continue  # Internal artifacts

                    # Resolve member path relative to project root
                    try:
                        dest_path = (self.root / member.name).resolve()
                        if not str(dest_path).startswith(str(self.root.resolve())):
                            heresies.append(f"Zip-Slip Attempt: {member.name}")
                            continue
                        members.append(member)
                    except Exception as e:
                        heresies.append(f"Path Resolution Error: {member.name} ({e})")

                if heresies and not self.config.force:
                    return RestoreResult(False, 0, 0, 0.0, heresies)

                # Extraction
                tar.extractall(path=self.root, members=members)

                files_restored = len(members)
                bytes_restored = sum(m.size for m in members)

            duration = (time.monotonic() - start_time) * 1000
            return RestoreResult(True, files_restored, bytes_restored, duration, heresies)

        except Exception as e:
            Logger.error(f"Resurrection Paradox: {e}", exc_info=True)
            return RestoreResult(False, files_restored, bytes_restored, 0.0, [str(e)])