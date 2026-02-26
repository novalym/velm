# Path: src/velm/core/kernel/transaction/volume_shifter/shadow_forge/replicator.py
# --------------------------------------------------------------------------------

import os
import shutil
import stat
from pathlib import Path
from typing import Final

from ......logger import Scribe
from .contracts import ForgeMetrics
from .sieve import EntropySieve


class AtomicReplicator:
    """
    =============================================================================
    == THE ATOMIC REPLICATION UNIT: OMEGA (V-Ω-TOTALITY-V21-SCRIPTURE-AWARE)   ==
    =============================================================================
    LIF: ∞ | ROLE: MATTER_FISSION_CONDUCTOR | RANK: OMEGA_SUPREME

    The supreme physical hand of the Shadow Forge. It attempts O(1) Inode Hardlinks
    first, seamlessly degrading to OS-optimized Block-Copies if boundaries are crossed.
    """

    COPY_BUFFER_SIZE: Final[int] = 1024 * 1024  # 1MB

    def __init__(self, logger: Scribe, metrics: ForgeMetrics, cross_device: bool):
        self.Logger = logger
        self.metrics = metrics
        self.cross_device = cross_device

    def replicate(self, src: Path, dst: Path):
        """
        The precise physical manifestation of a single atomic shard.
        Wraps the operation in a Titanium Sarcophagus to quarantine OS-level panics.
        """
        try:
            # 1. THE SCRIPTURE WARD
            if src.is_file() and EntropySieve.is_holy_scripture(src):
                return

            # 2. ACHRONAL LSTAT BIOPSY
            st = src.lstat()

            # 3. THE POINTER RITE (SYMLINK)
            if stat.S_ISLNK(st.st_mode):
                self._forge_symlink(src, dst)
                return

            # 4. THE IDENTITY RITE (HARDLINK)
            if not self.cross_device:
                if self._forge_hardlink(src, dst, st.st_size):
                    return

            # 5. THE MATTER RITE (BLOCK COPY)
            self._forge_copy(src, dst, st.st_size)

        except Exception as fracture:
            self.metrics.record_error()
            raise fracture

    def _forge_symlink(self, src: Path, dst: Path):
        """Isomorphic Link Mirroring."""
        link_target = os.readlink(str(src))
        if os.path.exists(str(dst)):
            os.unlink(str(dst))
        os.symlink(link_target, str(dst))

    def _forge_hardlink(self, src: Path, dst: Path, mass: int) -> bool:
        """O(1) Physical Inode Sharing."""
        try:
            if os.path.exists(str(dst)):
                os.unlink(str(dst))
            os.link(str(src), str(dst))

            # Verification of physical parity
            if src.stat().st_ino != dst.stat().st_ino:
                raise OSError("Lattice Schism: Inode Mismatch after link strike.")

            self.metrics.record_link(mass)
            return True
        except OSError:
            return False

    def _forge_copy(self, src: Path, dst: Path, mass: int):
        """The Hydraulic Fallback (Bit-for-Bit Copy)."""
        # First attempt high-speed native copy
        try:
            shutil.copy2(src, dst, follow_symlinks=False)
            self.metrics.record_copy(mass)
            return
        except Exception:
            pass

        # Ultimate Fallback: Manual 1MB Buffered Streaming
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            while True:
                buf = fsrc.read(self.COPY_BUFFER_SIZE)
                if not buf: break
                fdst.write(buf)

        shutil.copystat(src, dst)
        self.metrics.record_copy(mass)