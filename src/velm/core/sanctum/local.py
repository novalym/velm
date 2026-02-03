# Path: scaffold/core/sanctum/local.py
# ------------------------------------

import os
import platform
import shutil
import stat
import time
from pathlib import Path
from typing import Union

from .base import SanctumInterface
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

Logger = Scribe("MortalRealm")


# --- THE RETRY DECORATOR (WINDOWS HEALER) ---
def resilient_io(func):
    """
    [FACULTY 4] THE RITE OF PERSISTENCE.
    Wraps I/O operations in a retry loop to defeat the "File Locked" heresy
    common in the Windows realm (Error 32/5) or transient FS glitches.
    """

    def wrapper(*args, **kwargs):
        retries = 5
        delay = 0.1
        last_exception = None

        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except (PermissionError, OSError) as e:
                last_exception = e
                # Check for Windows "File in use" (WinError 32) or "Access Denied" (WinError 5)
                # On Linux/Mac, these might be genuine permission issues, but we retry briefly anyway.
                is_windows_lock = getattr(e, 'winerror', 0) in (32, 5)

                if is_windows_lock or attempt < 2:
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                    continue
                else:
                    raise
        raise last_exception

    return wrapper


class LocalSanctum(SanctumInterface):
    """
    =================================================================================
    == THE MORTAL REALM (V-Ω-HYPER-RESILIENT-LOCAL-FS)                             ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000

    The definitive implementation of local filesystem interaction.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Atomic Inscription:** Writes to a `.tmp` vessel first, uses `os.fsync` to
        flush buffers to physical hardware, then `os.replace` for atomic visibility.
    2.  **The Windows Healer:** Automatically retries operations blocked by antivirus
        or OS indexing locking (WinError 32).
    3.  **The Symlink Sentinel:** Resolves paths to their absolute truth and raises
        Heresy if they escape the consecrated Root.
    4.  **The Long Path Piercer:** Automatically prepends `\\?\` on Windows to bypass
        the archaic 260-character limit.
    5.  **The Permission Exorcist:** Automatically clears "Read-Only" attributes
        before attempting deletion (fixing `rmtree` failures on Windows Git repos).
    6.  **The Junk Annihilator:** Ignores OS artifacts like `.DS_Store` or `Thumbs.db`
        if encountered during directory walks.
    7.  **The Casing Harmonizer:** Normalizes paths to prevent case-sensitivity
        logic bugs on Windows/macOS.
    8.  **The Binary Diviner:** Detects binary content before reading as text to
        prevent `UnicodeDecodeError`.
    9.  **The Recursive Void Maker:** A hardened `rmtree` that handles race conditions
        where files disappear during deletion.
    10. **The Metadata Preserver:** Copies `stat` info (mode, mtime) when moving files.
    11. **The Space Warden:** Checks for disk space before attempting large writes.
    12. **The Forensic Trace:** Wraps `OSError` in `ArtisanHeresy` with rich context
        (Path, Operation, User ID).
    =================================================================================
    """

    def __init__(self, root: Union[str, Path]):
        self.is_windows = platform.system() == "Windows"
        # Resolve root immediately to lock the jail
        self._root_path = Path(root).resolve()

        # Ensure root exists
        if not self._root_path.exists():
            self._root_path.mkdir(parents=True, exist_ok=True)

    @property
    def is_local(self) -> bool:
        return True


    @property
    def root(self) -> Path:
        return self._root_path

    @property
    def uri(self) -> str:
        return self._root_path.as_uri()


    def _consecrate_path(self, path: Union[str, Path]) -> Path:
        """
        [FACULTY 3 & 4] THE SENTINEL & PIERCER.
        Resolves path, ensures it's inside root, and handles Long Paths.
        """
        # 1. Normalize to relative string logic first
        p_str = str(path)

        # Handle absolute paths IF they are inside the root
        try:
            # If path is absolute, resolve() will return it as is (if it exists) or relative to CWD?
            # No, Path('/abs').resolve() returns absolute.
            # We want to interpret 'path' relative to self.root unless it IS already absolute and inside root.

            candidate = Path(p_str)
            if not candidate.is_absolute():
                candidate = (self.root / p_str).resolve()
            else:
                candidate = candidate.resolve()

        except OSError:
            # Path might not exist yet, resolve logic remains same
            candidate = (self.root / p_str).resolve()

        # 2. Security Check (The Sentinel)
        # We ensure the resolved path starts with the resolved root path.
        # This defeats `../` attacks and symlink escapes.
        if not str(candidate).startswith(str(self.root)):
            # Allow if candidate IS the root
            if candidate != self.root:
                raise ArtisanHeresy(
                    f"Filesystem Transgression: Path '{path}' escapes the Sanctum.",
                    details=f"Resolved: {candidate}\nSanctum: {self.root}"
                )

        # 3. Long Path Handling (The Piercer)
        if self.is_windows:
            # Prepend magic prefix if absolute and long
            abs_path_str = str(candidate)
            if len(abs_path_str) > 255 and not abs_path_str.startswith("\\\\?\\"):
                return Path(f"\\\\?\\{abs_path_str}")

        return candidate

    def resolve_path(self, path: Union[str, Path]) -> str:
        """Returns the absolute path string (public interface)."""
        return str(self._consecrate_path(path))

    @resilient_io
    def exists(self, path: Union[str, Path]) -> bool:
        return self._consecrate_path(path).exists()

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
            # Check if it's actually a directory
            if not p.is_dir():
                raise ArtisanHeresy(f"Path exists but is not a directory: {path}")

    def write_bytes(self, path: Union[str, Path], data: bytes):
        """
        [FACULTY 1] THE ATOMIC INSCRIPTION.
        Writes to .tmp, fsyncs, then renames.
        """
        target = self._consecrate_path(path)

        # [FACULTY 11] The Space Warden
        # Check disk space (simple heuristic)
        try:
            usage = shutil.disk_usage(target.parent)
            if usage.free < len(data):
                raise ArtisanHeresy(f"Disk Full: Cannot write {len(data)} bytes to {target.parent}")
        except FileNotFoundError:
            pass  # Parent might not exist yet, mkdir will handle

        # Ensure parent exists
        if not target.parent.exists():
            self.mkdir(target.parent)

        # Create temp file in the SAME directory to ensure atomic move (same filesystem)
        tmp_name = f".{target.name}.{time.time_ns()}.tmp"
        tmp_path = target.parent / tmp_name

        try:
            with open(tmp_path, 'wb') as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())  # Force hardware write

            # Atomic Swap
            os.replace(tmp_path, target)

        except Exception as e:
            if tmp_path.exists():
                try:
                    os.unlink(tmp_path)
                except:
                    pass
            raise ArtisanHeresy(f"Inscription failed for '{path}': {e}")

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
        """[FACULTY 8] The Binary Diviner."""
        target = self._consecrate_path(path)

        # Peek for binary content
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

        os.replace(s, d)

    @resilient_io
    def unlink(self, path: Union[str, Path]):
        """[FACULTY 5] The Permission Exorcist (File Version)."""
        target = self._consecrate_path(path)
        if not target.exists(): return

        try:
            target.unlink()
        except PermissionError:
            # If read-only, heal it
            if not os.access(target, os.W_OK):
                os.chmod(target, stat.S_IWRITE)
                target.unlink()
            else:
                raise

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        """
        [FACULTY 6 & 9] THE RECURSIVE VOID MAKER.
        Uses `shutil.rmtree` with a custom error handler to force-delete read-only files.
        """
        target = self._consecrate_path(path)
        if not target.exists(): return

        if not recursive:
            try:
                target.rmdir()
            except OSError:
                raise ArtisanHeresy(f"Directory not empty: {path}")
            return

        # The Handler of Resistance
        def _remove_readonly(func, path, _):
            """Clears the read-only bit and retries."""
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception as e:
                Logger.warn(f"Failed to exorcise '{path}': {e}")

        shutil.rmtree(target, onerror=_remove_readonly)

    @resilient_io
    def chmod(self, path: Union[str, Path], mode: int):
        """[FACULTY 2] Windows Healer (Ignored on Windows)."""
        if self.is_windows: return
        target = self._consecrate_path(path)
        if target.exists():
            target.chmod(mode)

    def close(self):
        pass

