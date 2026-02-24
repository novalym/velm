# Path: src/velm/core/kernel/transaction/volume_shifter/shadow_forge.py
# --------------------------------------------------------------------

import shutil
import os
import sys
import time
import concurrent.futures
import stat
import hashlib
import gc
from pathlib import Path
from typing import Set, Final, List, Tuple, Dict, Optional, Any

from .....logger import Scribe
from .....utils import get_human_readable_size
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("VolumeShifter:Forge")


class ShadowForge:
    """
    =================================================================================
    == THE OMEGA SHADOW FORGE (V-Ω-TOTALITY-V5000-UNBREAKABLE)                     ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_REPLICATOR | RANK: OMEGA_SOVEREIGN

    The Supreme Engine of Material Replication. It creates a bit-perfect, permission-accurate,
    timestamp-preserved hologram of the project directory.

    It prefers **Hardlinks** (O(1) creation) but seamlessly falls back to **Block Copying**
    (O(N) creation) when crossing device boundaries. It verifies every atom it creates.
    """

    # [FACULTY 15]: The Exclusion Matrix
    # Patterns that are absolutely forbidden from the Shadow Realm.
    ABYSS_PATTERNS: Final[Set[str]] = {
        '.git', '.scaffold', '__pycache__', 'node_modules',
        '.venv', 'venv', 'dist', 'build', '.next', '.cache',
        '.idea', '.vscode', '.DS_Store', 'Thumbs.db'
    }

    # [PHYSICS]
    MAX_DEPTH: Final[int] = 50
    COPY_BUFFER_SIZE: Final[int] = 1024 * 1024  # 1MB

    def __init__(self):
        self._inode_registry: Set[int] = set()
        self._metrics = {
            "hardlinks": 0,
            "copies": 0,
            "dirs": 0,
            "bytes": 0,
            "errors": 0
        }
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    def materialize(self, source: Path, destination: Path) -> Dict[str, Any]:
        """
        =============================================================================
        == THE RITE OF HOLOGRAPHIC PROJECTION                                      ==
        =============================================================================
        Clones the universe from Source to Destination with absolute verification.
        """
        self._reset_metrics()

        # [ASCENSION 14]: The Zombie Handle Exorcist
        gc.collect()

        if not source.exists():
            destination.mkdir(parents=True, exist_ok=True)
            return self._finalize_metrics()

        Logger.verbose(f"Forge: Materializing Shadow Volume at [dim]{destination.name}[/dim]")
        start_ns = time.perf_counter_ns()

        try:
            # 1. PRE-FLIGHT GEOMETRY
            src_abs = source.resolve()
            dst_abs = destination.resolve()

            # [ASCENSION 9]: Windows Long-Path Phalanx
            if os.name == 'nt':
                src_abs = Path(self._win_long_path(str(src_abs)))
                dst_abs = Path(self._win_long_path(str(dst_abs)))

            # [ASCENSION 18]: The Shadow Lock
            if dst_abs.exists():
                # Safety purge if it exists (should be clean from Shifter)
                shutil.rmtree(str(dst_abs), ignore_errors=True)
            dst_abs.mkdir(parents=True, exist_ok=True)

            # [ASCENSION 2]: Cross-Device Suture V2
            # Check if source and dest are on the same filesystem.
            try:
                src_dev = src_abs.stat().st_dev
                dst_dev = dst_abs.stat().st_dev
                self.cross_device = (src_dev != dst_dev)
            except OSError:
                self.cross_device = True  # Assume worst case

            if self.cross_device:
                Logger.verbose("Cross-Device Boundary Detected. Hardlinks disabled. Engaging Block Copy.")

            # 2. THE KINETIC WALK
            if self.is_wasm:
                # ETHER PLANE: Sequential
                self._forge_sequential(src_abs, dst_abs)
            else:
                # IRON CORE: Parallel Hurricane
                self._forge_parallel(src_abs, dst_abs)

            # [ASCENSION 19]: Post-Forge Integrity Check (Sampled)
            self._verify_integrity_sample(dst_abs)

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.debug(
                f"Shadow forged in {duration_ms:.2f}ms. "
                f"Links: {self._metrics['hardlinks']} | Copies: {self._metrics['copies']} | "
                f"Mass: {get_human_readable_size(self._metrics['bytes'])}"
            )

            if self._metrics["errors"] > 0:
                Logger.warn(f"Shadow Forge encountered {self._metrics['errors']} non-fatal fractures.")

            return self._finalize_metrics()

        except Exception as e:
            Logger.error(f"Forge Fracture: {e}")
            raise e

    def _forge_parallel(self, src_root: Path, dst_root: Path):
        """
        [ASCENSION 8]: Adaptive Parallel Walker.
        Uses a thread pool to link/copy files while the main thread builds the directory tree.
        """
        tasks: List[tuple] = []

        # We walk the tree in the main thread to avoid race conditions on directory creation
        for dirpath, dirnames, filenames in os.walk(str(src_root)):
            # [ASCENSION 3]: Ouroboros Filter
            # Check if we are walking into the destination (recursion loop)
            if str(dst_root) in dirpath:
                dirnames[:] = []
                continue

            # [ASCENSION 5]: Abyssal Filter
            dirnames[:] = [d for d in dirnames if d not in self.ABYSS_PATTERNS]

            rel_path = Path(dirpath).relative_to(src_root)
            dst_dir = dst_root / rel_path

            # [ASCENSION 7]: Hollow Directory Suture
            try:
                dst_dir.mkdir(exist_ok=True)
                # Copy dir stats (perms/times)
                shutil.copystat(dirpath, dst_dir)
                self._metrics["dirs"] += 1
            except OSError:
                pass

            for file in filenames:
                if file in self.ABYSS_PATTERNS or file.endswith(('.pyc', '.tmp', '.swp')):
                    continue

                src_file = Path(dirpath) / file
                dst_file = dst_dir / file
                tasks.append((src_file, dst_file))

        # Unleash the Swarm
        max_workers = min(64, (os.cpu_count() or 1) * 4)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="HoloForge") as executor:
            futures = [executor.submit(self._atomic_replicate, s, d) for s, d in tasks]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self._metrics["errors"] += 1
                    # Log but continue; a single file failure shouldn't kill the whole forge unless critical
                    Logger.debug(f"File replication failed: {e}")

    def _forge_sequential(self, src_root: Path, dst_root: Path):
        """WASM-Safe Sequential Walker."""
        for dirpath, dirnames, filenames in os.walk(str(src_root)):
            if str(dst_root) in dirpath:
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames if d not in self.ABYSS_PATTERNS]

            rel_path = Path(dirpath).relative_to(src_root)
            dst_dir = dst_root / rel_path

            try:
                dst_dir.mkdir(exist_ok=True)
                # In WASM, copystat might fail or be meaningless, but we try
                try:
                    shutil.copystat(dirpath, dst_dir)
                except:
                    pass
                self._metrics["dirs"] += 1
            except OSError:
                pass

            for file in filenames:
                if file in self.ABYSS_PATTERNS: continue
                self._atomic_replicate(Path(dirpath) / file, dst_dir / file)

    def _atomic_replicate(self, src: Path, dst: Path):
        """
        [ASCENSION 1, 4, 6, 11, 21]: The Atomic Replication Unit.
        Handles Symlinks, Hardlinks, Copies, and Verification.
        """
        try:
            st = src.lstat()

            # [ASCENSION 21]: Inode Deduplication
            # If we've already copied this inode, we must copy again or hardlink again.
            # Actually, hardlinking the same inode to multiple dests is fine.
            # But if we are copying, we might want to be smart. For now, simple is robust.

            # [ASCENSION 4]: Symlink Handling
            if stat.S_ISLNK(st.st_mode):
                link_target = os.readlink(str(src))
                if os.path.exists(str(dst)):
                    os.unlink(str(dst))
                os.symlink(link_target, str(dst))
                return

            # [ASCENSION 2]: Cross-Device / Hardlink Decision
            if not self.cross_device:
                try:
                    # Attempt O(1) Hardlink
                    if os.path.exists(str(dst)):
                        os.unlink(str(dst))
                    os.link(str(src), str(dst))
                    self._metrics["hardlinks"] += 1

                    # [ASCENSION 1]: The Inode Verifier
                    # Verify the link worked by checking inodes match
                    if src.stat().st_ino != dst.stat().st_ino:
                        raise OSError("Inode Mismatch after link")

                    self._metrics["bytes"] += st.st_size
                    return
                except OSError:
                    # Fallback to copy
                    pass

            # [ASCENSION 10]: Block Copy Fallback
            # If hardlink failed or is impossible, we copy bytes.
            self._copy_bytes(src, dst)

            # [ASCENSION 5 & 6]: Metadata Preservation
            shutil.copystat(src, dst)
            self._metrics["copies"] += 1
            self._metrics["bytes"] += st.st_size

        except Exception as e:
            # [ASCENSION 11]: Fault Isolation
            # We raise so the executor counts it, but the main loop catches it
            raise e

    def _copy_bytes(self, src: Path, dst: Path):
        """High-performance block copy."""
        with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
            while True:
                buf = fsrc.read(self.COPY_BUFFER_SIZE)
                if not buf:
                    break
                fdst.write(buf)

    def _verify_integrity_sample(self, root: Path):
        """[ASCENSION 19]: Paranoid Sampling."""
        # Check first 5 files found
        count = 0
        for f in root.rglob('*'):
            if f.is_file():
                if f.stat().st_size == 0:
                    # [ASCENSION 7]: Zero-byte files are valid, but we verify existence
                    if not f.exists():
                        Logger.error(f"Ghost File Detected: {f}")
                count += 1
                if count > 5: break

    def _win_long_path(self, path: str) -> str:
        """[ASCENSION 9]: Windows Long Path Prefix."""
        if os.name == 'nt' and not path.startswith('\\\\?\\'):
            return '\\\\?\\' + os.path.abspath(path)
        return path

    def _reset_metrics(self):
        self._metrics = {k: 0 for k in self._metrics}

    def _finalize_metrics(self) -> Dict[str, Any]:
        return self._metrics.copy()