# Path: scaffold/creator/writer/atomic.py
# ---------------------------------------
import os
import time
import shutil
from pathlib import Path
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("AtomicScribe")


class AtomicScribe:
    """
    =============================================================================
    == THE HAND OF THE ATOM (V-Ω-TRANSACTIONAL-IO)                             ==
    =============================================================================
    Performs the physical write operation using the 'Rename-Over-Temp' pattern.
    """

    def __init__(self, sanctum_root: Path):
        self.sanctum = sanctum_root

    def inscribe(self, target: Path, data: bytes, mode: int = 0o644) -> int:
        """
        Writes data to a temp file, syncs to disk, then atomically renames.
        Returns bytes written.
        """
        # Ensure directory exists
        if not target.parent.exists():
            target.parent.mkdir(parents=True, exist_ok=True)

        temp_name = f".{target.name}.{time.time_ns()}.tmp"
        temp_path = target.parent / temp_name

        try:
            with open(temp_path, 'wb') as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())

            # Apply permissions before rename
            try:
                os.chmod(temp_path, mode)
            except Exception:
                pass  # Windows tolerance

            # Atomic Swap
            os.replace(temp_path, target)
            return len(data)

        except Exception as e:
            if temp_path.exists():
                try:
                    os.unlink(temp_path)
                except:
                    pass
            raise ArtisanHeresy(f"Atomic Inscription Failed for '{target}': {e}")