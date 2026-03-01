# Path: src/velm/core/kernel/transaction/volume_shifter/shadow_forge/replicator.py
# --------------------------------------------------------------------------------

import os
import sys
import shutil
import stat
import time
from pathlib import Path
from typing import Final, Optional, Union

# --- THE DIVINE UPLINKS ---
from ......logger import Scribe
from .contracts import ForgeMetrics
from .sieve import EntropySieve


class AtomicReplicator:
    """
    =============================================================================
    == THE ATOMIC REPLICATOR: TOTALITY (V-Ω-TOTALITY-V25.2-WASM-RESILIENT)     ==
    =============================================================================
    LIF: ∞ | ROLE: MATTER_FISSION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_REPLICATOR_V25_WASM_RESONANT_2026_FINALIS

    The supreme physical hand of the Shadow Forge. It is now a Substrate-Aware
    organ, capable of conducting materialization rites across Iron and Ether
    planes with zero friction.
    =============================================================================
    """

    COPY_BUFFER_SIZE: Final[int] = 1024 * 1024  # 1MB Hydraulic Pulse

    def __init__(self, logger: Scribe, metrics: ForgeMetrics, cross_device: bool):
        """[THE RITE OF INCEPTION]"""
        self.Logger = logger
        self.metrics = metrics
        self.cross_device = cross_device

        # [ASCENSION 1]: SUBSTRATE PERCEPTION
        # We divine the nature of our reality once at birth.
        self._is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

    def replicate(self, src: Path, dst: Path):
        """
        =============================================================================
        == THE RITE OF REPLICATION (MATERIALIZATION)                               ==
        =============================================================================
        The precise physical manifestation of a single atomic shard.
        Wraps the operation in a Titanium Sarcophagus to quarantine OS-level panics.
        """
        # [ASCENSION 9]: NoneType Sarcophagus
        if src is None or dst is None:
            return

        try:
            # 1. THE SCRIPTURE WARD
            # Skip replication if the matter is deemed holy (protected configuration).
            if src.is_file() and EntropySieve.is_holy_scripture(src):
                return

            # 2. ACHRONAL LSTAT BIOPSY
            # We use lstat to perceive the pointer (link) rather than the destination.
            st = src.lstat()
            mass = st.st_size

            # [ASCENSION 11]: GEOMETRIC NORMALIZATION
            s_path = str(src).replace('\\', '/')
            d_path = str(dst).replace('\\', '/')

            # 3. THE POINTER RITE (SYMLINK)
            if stat.S_ISLNK(st.st_mode):
                self._forge_symlink(s_path, d_path)
                return

            # 4. [ASCENSION 11]: FAST-FAIL EMPTY SIEVE
            # If the soul is empty, we touch the coordinate and skip the engine.
            if mass == 0 and src.is_file():
                self._forge_void(d_path)
                self.metrics.record_copy(0)
                return

            # 5. THE IDENTITY RITE (HARDLINK)
            # [ASCENSION 1 & 2]: The WASM-Aware Link Guard.
            # We only attempt Hardlinks on Iron substrates where 'os.link' is manifest.
            if not self.cross_device and not self._is_wasm and hasattr(os, 'link'):
                if self._forge_hardlink(s_path, d_path, mass):
                    return

            # 6. THE MATTER RITE (HYDRAULIC BLOCK COPY)
            # Fallback for WASM or cross-device boundaries.
            self._forge_copy(src, dst, mass)

        except Exception as fracture:
            # [ASCENSION 8]: THE SOCRATIC ERROR TRIAGE
            self.Logger.error(f"Replicator Fracture at {src.name}: {str(fracture)}")
            self.metrics.record_error()
            raise fracture

    def _forge_void(self, dst_path: str):
        """Forges an empty scripture instantly."""
        with open(dst_path, 'a'):
            os.utime(dst_path, None)

    def _forge_symlink(self, src_path: str, dst_path: str):
        """Isomorphic Link Mirroring."""
        link_target = os.readlink(src_path)
        if os.path.exists(dst_path):
            os.unlink(dst_path)
        os.symlink(link_target, dst_path)

    def _forge_hardlink(self, src_path: str, dst_path: str, mass: int) -> bool:
        """O(1) Physical Inode Sharing (Iron Only)."""
        try:
            if os.path.exists(dst_path):
                os.unlink(dst_path)

            # [THE CURE]: This call is now warded by the check in .replicate()
            os.link(src_path, dst_path)

            # Verification of physical parity
            if os.stat(src_path).st_ino != os.stat(dst_path).st_ino:
                return False

            self.metrics.record_link(mass)
            return True
        except (OSError, AttributeError):
            return False

    def _forge_copy(self, src: Path, dst: Path, mass: int):
        """
        =============================================================================
        == THE HYDRAULIC FALLBACK (BLOCK-STRATUM COPY)                             ==
        =============================================================================
        [ASCENSION 4]: 1MB Buffered Copy. Optimized for WASM memory constraints.
        """
        # --- MOVEMENT I: THE HIGH PATH (SHUTIL) ---
        try:
            # We attempt shutil.copy2 to preserve metadata soul (mtime/mode).
            shutil.copy2(src, dst, follow_symlinks=False)
            self.metrics.record_copy(mass)
            return
        except Exception:
            # If shutil fails (Permission/Substrate), we move to Movement II.
            pass

        # --- MOVEMENT II: THE HYDRAULIC PULSE (MANUAL STREAM) ---
        # [ASCENSION 5]: Bestow write permissions to the destination locus.
        dst_dir = dst.parent
        if not dst_dir.exists():
            dst_dir.mkdir(parents=True, exist_ok=True)

        # [ASCENSION 11]: Absolute Binary Parity
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            while True:
                buf = fsrc.read(self.COPY_BUFFER_SIZE)
                if not buf:
                    break
                fdst.write(buf)

        # [ASCENSION 6]: Temporal Soul Restoration
        try:
            shutil.copystat(src, dst)
        except Exception:
            pass  # Non-critical metadata failure

        self.metrics.record_copy(mass)

    def __repr__(self) -> str:
        return f"<Ω_ATOMIC_REPLICATOR substrate={'ETHER' if self._is_wasm else 'IRON'}>"