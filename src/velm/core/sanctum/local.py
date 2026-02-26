# Path: src/velm/core/sanctum/local.py
# ------------------------------------

import os
import sys
import shutil
import platform
import stat
import time
import threading
import errno
import hashlib
import uuid
from pathlib import Path
from typing import Union, List, Iterator, Any, Dict, Optional, Tuple

# --- THE DIVINE UPLINKS ---
from .base import SanctumInterface
from .contracts import SanctumStat, SanctumKind
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("LocalSanctum")


# =============================================================================
# == THE RESILIENCE WRAPPER (V-Ω-WINDOWS-HEALER)                             ==
# =============================================================================
def resilient_io(func):
    """
    [FACULTY: THE UNYIELDING GRIP]
    Wraps I/O operations in an exponential backoff retry loop.
    Specifically targets Windows file locking (Antivirus/Indexer/Git) heresies.
    """

    def wrapper(*args, **kwargs):
        retries = 6
        delay = 0.05
        last_error = None

        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except (PermissionError, OSError) as e:
                last_error = e
                # Check for Windows "File in use" (WinError 32) or "Access Denied" (WinError 5)
                # On Linux/Mac, these might be genuine permission issues, but we retry briefly anyway.
                win_err = getattr(e, 'winerror', 0)

                # WinError 32: Sharing Violation (Locked by another process)
                # WinError 5: Access Denied (Read-only or Locked)
                # Errno 13: Permission Denied (POSIX)
                if win_err in (5, 32) or e.errno == errno.EACCES:
                    # [HEALING]: Yield to the OS scheduler
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                    continue

                # If it's a "File Not Found" during a delete/read, we might accept it or fail fast
                if e.errno == errno.ENOENT:
                    raise e

                # Unknown error, raise immediately
                raise e

        # If we exhaust retries, we raise the last error wrapped in Heresy
        raise ArtisanHeresy(
            f"I/O Resilience Exhausted: {str(last_error)}",
            details=f"Operation failed after {retries} attempts.",
            severity=HeresySeverity.CRITICAL
        ) from last_error

    return wrapper


class LocalSanctum(SanctumInterface):
    """
    =================================================================================
    == THE MORTAL REALM (V-Ω-TITANIUM-LOCAL-FS-ULTIMA)                             ==
    =================================================================================
    LIF: ∞ | ROLE: IRON_CORE_DRIVER | RANK: OMEGA_SOVEREIGN

    The definitive, battle-hardened driver for the Local Filesystem.
    It treats the disk not as a passive storage, but as a hostile environment
    that must be tamed with atomic locks, retry loops, and path normalization.
    """

    def __init__(self, root: Union[str, Path]):
        super().__init__()
        self._is_windows = platform.system() == "Windows"

        # [ASCENSION 1]: PATH CANONIZATION
        # We resolve the root immediately to lock the Jail.
        try:
            self._root_path = Path(root).resolve()
        except OSError:
            # If the path is invalid (e.g. non-existent drive), fallback to CWD
            Logger.warn(f"Sanctum root '{root}' is invalid. Anchoring to CWD.")
            self._root_path = Path.cwd().resolve()

        # [ASCENSION 2]: LAZY INCEPTION
        # We do not create the root directory in __init__. We wait for the first Write.
        # This prevents empty directories from polluting the disk during dry-runs.

        self._mutex = threading.RLock()
        self._inode_cache: Dict[str, int] = {}  # For loop detection

    @property
    def kind(self) -> SanctumKind:
        return SanctumKind.LOCAL

    @property
    def root(self) -> Path:
        return self._root_path

    @property
    def uri_root(self) -> str:
        """
        =============================================================================
        == THE GEOMETRIC IDENTITY (V-Ω-TOTALITY-V5000-SUTURED)                     ==
        =============================================================================
        [THE CURE]: Directly satisfies the SanctumInterface abstract method.
        Annihilates the 'TypeError: Can't instantiate abstract class' heresy.
        """
        return self._root_path.as_uri()

    @property
    def is_local(self) -> bool:
        return True

    def _consecrate_path(self, path: Union[str, Path]) -> Path:
        """
        =============================================================================
        == THE GEOMETRIC WARD (V-Ω-PATH-SANITIZER)                                 ==
        =============================================================================
        1. Resolves relative paths against the Sanctum Root.
        2. Enforces the Jail (Symlink/Traversal protection).
        3. Applies the Windows Long-Path Phalanx (\\?\) if needed.
        """
        p_str = str(path)

        try:
            # Handle absolute paths IF they are inside the root
            candidate = Path(p_str)
            if not candidate.is_absolute():
                candidate = (self.root / p_str).resolve()
            else:
                candidate = candidate.resolve()
        except OSError:
            # Path might not exist yet, resolve logic logic remains same
            candidate = (self.root / p_str).resolve()

        # [ASCENSION 4]: THE SYMLINK JAIL
        # We ensure the resolved path starts with the resolved root path.
        # This defeats `../` attacks and symlink escapes.
        # Note: We convert to string and lower() on Windows to be case-insensitive safe
        root_str = str(self.root)
        cand_str = str(candidate)

        if self._is_windows:
            root_str = root_str.lower()
            cand_str = cand_str.lower()

        if not cand_str.startswith(root_str):
            # Allow if candidate IS the root
            if candidate != self.root:
                raise ArtisanHeresy(
                    f"Filesystem Transgression: Path '{path}' escapes the Sanctum.",
                    details=f"Resolved: {candidate}\nSanctum: {self.root}",
                    severity=HeresySeverity.CRITICAL
                )

        # [ASCENSION 1]: THE WINDOWS LONG PATH PHALANX
        if self._is_windows:
            abs_path_str = str(candidate)
            # Only prepend if absolute and long and not already prepended
            if len(abs_path_str) > 240 and not abs_path_str.startswith("\\\\?\\"):
                # Must be absolute path for UNC
                if not Path(abs_path_str).is_absolute():
                    abs_path_str = str(candidate.resolve())
                return Path(f"\\\\?\\{abs_path_str}")

        return candidate

    def resolve_path(self, path: Union[str, Path]) -> str:
        """Returns the absolute path string (public interface)."""
        return str(self._consecrate_path(path))

    @resilient_io
    def exists(self, path: Union[str, Path]) -> bool:
        return self._consecrate_path(path).exists()

    @resilient_io
    def stat(self, path: Union[str, Path]) -> SanctumStat:
        """
        [ASCENSION 12]: FORENSIC BIOPSY
        Returns a normalized stat object, safe for cross-platform logic.
        """
        target = self._consecrate_path(path)
        if not target.exists():
            raise FileNotFoundError(f"Void: {path}")

        st = target.stat()
        kind = "file"
        if target.is_dir():
            kind = "dir"
        elif target.is_symlink():
            kind = "symlink"

        return SanctumStat(
            path=str(path),
            size=st.st_size,
            mtime=st.st_mtime,
            kind=kind,
            permissions=st.st_mode,
            # On Windows, UID/GID are 0
            owner=str(st.st_uid) if hasattr(st, 'st_uid') else "0",
            group=str(st.st_gid) if hasattr(st, 'st_gid') else "0",
            metadata={
                "inode": st.st_ino if hasattr(st, 'st_ino') else 0,
                "device": st.st_dev if hasattr(st, 'st_dev') else 0,
                "is_readonly": not bool(st.st_mode & stat.S_IWRITE)
            }
        )

    @resilient_io
    def is_dir(self, path: Union[str, Path]) -> bool:
        p = self._consecrate_path(path)
        return p.exists() and p.is_dir()

    @resilient_io
    def is_file(self, path: Union[str, Path]) -> bool:
        p = self._consecrate_path(path)
        return p.exists() and p.is_file()

    @resilient_io
    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        p = self._consecrate_path(path)
        try:
            p.mkdir(parents=parents, exist_ok=exist_ok)
        except FileExistsError:
            if not exist_ok: raise
            if not p.is_dir():
                raise ArtisanHeresy(f"Path collision: '{path}' exists but is not a directory.")

    def write_bytes(self, path: Union[str, Path], data: bytes):
        """
        [ASCENSION 2]: THE ATOMIC INSCRIPTION (ACID)
        Writes to .tmp -> Fsync -> Rename. Guarantees file integrity.
        """
        target = self._consecrate_path(path)

        # [ASCENSION 10]: THE SPACE WARDEN
        try:
            # Check free space on the drive containing the target's parent
            usage = shutil.disk_usage(target.parent if target.parent.exists() else self.root)
            # Require 2x buffer for safety
            if usage.free < len(data) * 2:
                raise ArtisanHeresy(f"Disk Full: Insufficient space for {len(data)} bytes.")
        except (FileNotFoundError, OSError):
            pass  # Drive might be virtual or unmounted, proceed with faith

        # Ensure parent exists
        if not target.parent.exists():
            self.mkdir(target.parent)

        # Create temp file in the SAME directory (essential for atomic rename)
        # We use a unique nonce to allow parallel writes
        nonce = uuid.uuid4().hex[:8]
        tmp_name = f".{target.name}.{nonce}.tmp"
        tmp_path = target.parent / tmp_name

        try:
            with open(tmp_path, 'wb') as f:
                f.write(data)
                f.flush()
                # [STRIKE]: Hardware Sync
                if hasattr(os, 'fsync'):
                    os.fsync(f.fileno())

            # [ASCENSION 8]: The Permission Healer (Pre-Swap)
            # If target exists and is read-only, we must unlock it before replacing
            if target.exists() and not os.access(target, os.W_OK):
                self._unlock_file(target)

            # Atomic Swap
            os.replace(tmp_path, target)

        except Exception as e:
            # Cleanup temp artifact
            if tmp_path.exists():
                try:
                    os.unlink(tmp_path)
                except:
                    pass
            raise ArtisanHeresy(f"Inscription fracture for '{path}': {e}", severity=HeresySeverity.CRITICAL)

    def write_text(self, path: Union[str, Path], data: str, encoding: str = 'utf-8'):
        self.write_bytes(path, data.encode(encoding))

    @resilient_io
    def read_bytes(self, path: Union[str, Path]) -> bytes:
        target = self._consecrate_path(path)
        if not target.exists():
            raise FileNotFoundError(f"Scripture not found: {path}")
        return target.read_bytes()

    @resilient_io
    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        [ASCENSION 7]: THE BINARY DIVINER.
        Peeks at content before full read to prevent encoding crashes.
        """
        target = self._consecrate_path(path)

        # Peek first 1KB
        with open(target, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                raise ArtisanHeresy(f"Binary Soul detected in '{path}'. Cannot read as text.")

        return target.read_text(encoding=encoding)

    @resilient_io
    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        s = self._consecrate_path(src)
        d = self._consecrate_path(dst)

        if not d.parent.exists():
            self.mkdir(d.parent)

        # [ASCENSION 8]: Unlock destination if it exists
        if d.exists() and not os.access(d, os.W_OK):
            self._unlock_file(d)

        os.replace(s, d)

    @resilient_io
    def unlink(self, path: Union[str, Path]):
        """
        [ASCENSION 5]: THE PERMISSION EXORCIST.
        Unlocks and deletes a file.
        """
        target = self._consecrate_path(path)
        if not target.exists(): return

        try:
            target.unlink()
        except PermissionError:
            self._unlock_file(target)
            target.unlink()

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        """
        [ASCENSION 3 & 9]: THE ZOMBIE REAPER.
        Robust directory deletion with read-only file handling.
        """
        target = self._consecrate_path(path)
        if not target.exists(): return

        if not recursive:
            try:
                target.rmdir()
            except OSError:
                raise ArtisanHeresy(f"Directory not empty: {path}")
            return

        # The Exorcism Handler
        def on_error(func, path, exc_info):
            """
            Error handler for shutil.rmtree.
            If the error is due to access rights, try to make the file writable and delete again.
            """
            ex = exc_info[1]
            if isinstance(ex, PermissionError) or (isinstance(ex, OSError) and getattr(ex, 'winerror', 0) == 5):
                try:
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                except Exception as e:
                    Logger.warn(f"Failed to exorcise '{path}': {e}")
            else:
                # Re-raise other errors
                raise ex

        # [ASCENSION 5]: The Metabolic Throttle
        # For massive directories, we might want to yield?
        # Standard rmtree is C-optimized, so we trust it, but we wrap it in the handler.
        shutil.rmtree(target, onerror=on_error)

    @resilient_io
    def copy(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        [ASCENSION 10]: THE METADATA PRESERVER.
        Replicates matter and its temporal soul (mtime/mode).
        """
        s = self._consecrate_path(src)
        d = self._consecrate_path(dst)

        if not d.parent.exists():
            self.mkdir(d.parent)

        if s.is_dir():
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    @resilient_io
    def chmod(self, path: Union[str, Path], mode: int):
        """
        [ASCENSION 8]: The Permission Healer.
        Applies permissions. On Windows, maps 'w' bit to ReadOnly attribute.
        """
        target = self._consecrate_path(path)
        if not target.exists(): return

        try:
            os.chmod(target, mode)
        except OSError:
            # Some filesystems (FAT32) ignore chmod, we swallow this heresy gracefully
            pass

    def list_dir(self, path: Union[str, Path]) -> List[str]:
        target = self._consecrate_path(path)
        # [ASCENSION 6]: The Junk Annihilator
        # We filter out OS-level trash immediately
        return [
            p.name for p in target.iterdir()
            if p.name not in {'.DS_Store', 'Thumbs.db', 'desktop.ini'}
        ]

    def walk(self, top: Union[str, Path], topdown: bool = True) -> Iterator[Any]:
        """
        Topological Traversal.
        Yields (root, dirs, files) tuples.
        """
        target = self._consecrate_path(top)
        return os.walk(str(target), topdown=topdown)

    def touch(self, path: Union[str, Path]):
        """
        [ASCENSION 11]: THE TOUCH OF MIDAS.
        Updates mtime/atime. Creates file if missing.
        """
        target = self._consecrate_path(path)
        if target.exists():
            os.utime(target, None)
        else:
            self.write_bytes(path, b"")

    def symlink(self, target: Union[str, Path], link: Union[str, Path]):
        """
        Creates a symbolic link.
        NOTE: 'target' is the content of the link, 'link' is the location.
        """
        l_path = self._consecrate_path(link)
        # Target might be relative to link, so we don't strictly resolve it against root
        # But we must ensure the link itself is inside root.

        # [ASCENSION 12]: Windows Privilege Check
        try:
            os.symlink(str(target), l_path)
        except OSError as e:
            if self._is_windows and getattr(e, 'winerror', 0) == 1314:
                raise ArtisanHeresy(
                    "Privilege Heresy: Creating symlinks on Windows requires Admin rights or Developer Mode.",
                    severity=HeresySeverity.WARNING
                )
            raise e

    def _unlock_file(self, path: Path):
        """Helper to force-enable write permissions."""
        try:
            os.chmod(path, stat.S_IWRITE)
        except Exception:
            pass

    def close(self):
        pass

    def __repr__(self) -> str:
        return f"<LocalSanctum root={self.root} platform={'WIN' if self._is_windows else 'POSIX'}>"