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
import secrets
from pathlib import Path
from typing import Union, List, Iterator, Any, Dict, Optional

from .base import SanctumInterface
from .contracts import SanctumStat, SanctumKind
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("LocalFS")

# =========================================================================
# == DIAGNOSTIC TELEMETRY GATE                                           ==
# =========================================================================
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


def resilient_io(func):
    """
    Wraps I/O operations in an exponential backoff retry loop.

    This is highly critical for Windows environments where external processes
    (Windows Defender, Search Indexer, Git clients) frequently place transient,
    millisecond-level locks on newly created files, resulting in WinError 32
    (Sharing Violation) or WinError 5 (Access Denied).
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
                win_err = getattr(e, 'winerror', 0)

                # WinError 32: The process cannot access the file because it is being used by another process.
                # WinError 5: Access is denied.
                # EACCES: Permission denied (POSIX fallback).
                if win_err in (5, 32) or e.errno == errno.EACCES:
                    time.sleep(delay)
                    delay *= 2
                    continue

                # Immediately raise if the file simply doesn't exist, as retrying won't create it
                if e.errno == errno.ENOENT:
                    raise e

                raise e

        raise ArtisanHeresy(
            f"I/O Resilience Exhausted: {str(last_error)}",
            details=f"The filesystem operation failed consecutively after {retries} attempts. The file may be permanently locked.",
            severity=HeresySeverity.CRITICAL
        ) from last_error

    return wrapper


class LocalSanctum(SanctumInterface):
    """
    The definitive driver for Local Filesystem interaction.

    Features:
    - Atomic File Swapping (Temp -> Target)
    - Automated Long-Path support for Windows NTFS (\\\\?\\)
    - Strict boundary enforcement to prevent directory traversal escapes
    - Deep thread-safety for high-concurrency I/O multiplexing
    """

    def __init__(self, root: Union[str, Path]):
        super().__init__()
        self._is_windows = platform.system() == "Windows"
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # Resolve the root path immediately to establish the absolute security boundary (The Jail)
        try:
            self._root_path = Path(root).resolve()
        except OSError:
            Logger.warn(f"Target workspace path '{root}' is inaccessible. Defaulting to current directory.")
            self._root_path = Path.cwd().resolve()

        # Thread safety guard for caching and critical file swaps
        self._mutex = threading.RLock()

    def _sys_log(self, msg: str, color_code: str = "36"):
        """Internal tracing for I/O diagnostics."""
        if _DEBUG_MODE:
            sys.stderr.write(f"\x1b[{color_code};1m[DEBUG: LocalFS]\x1b[0m {msg}\n")
            sys.stderr.flush()

    @property
    def kind(self) -> SanctumKind:
        return SanctumKind.LOCAL

    @property
    def root(self) -> Path:
        return self._root_path

    @property
    def uri_root(self) -> str:
        return self._root_path.as_uri()

    @property
    def is_local(self) -> bool:
        return True

    def _consecrate_path(self, path: Union[str, Path]) -> Path:
        """
        Resolves relative paths, enforces boundary containment to prevent traversal
        vulnerabilities, and applies NTFS long-path prefixes for Windows.
        """
        p_str = str(path)

        try:
            candidate = Path(p_str)
            if not candidate.is_absolute():
                candidate = (self.root / p_str).resolve()
            else:
                candidate = candidate.resolve()
        except OSError:
            # Fallback if path resolution fails due to missing intermediate directories
            candidate = (self.root / p_str).resolve()

        # Boundary Enforcement: Prevent writing outside the designated project root
        root_str = str(self.root)
        cand_str = str(candidate)

        if self._is_windows:
            root_str = root_str.lower()
            cand_str = cand_str.lower()

        if not cand_str.startswith(root_str) and candidate != self.root:
            raise ArtisanHeresy(
                f"Security Violation: Path '{path}' attempts to escape the allowed workspace directory.",
                details=f"Resolved Target: {candidate}\nAllowed Root: {self.root}",
                severity=HeresySeverity.CRITICAL
            )

        # Windows MAX_PATH (260 chars) circumvention
        if self._is_windows:
            abs_path_str = str(candidate)
            if len(abs_path_str) > 240 and not abs_path_str.startswith("\\\\?\\"):
                if not Path(abs_path_str).is_absolute():
                    abs_path_str = str(candidate.resolve())
                return Path(f"\\\\?\\{abs_path_str}")

        return candidate

    def resolve_path(self, path: Union[str, Path]) -> str:
        """Exposes the internal absolute path resolution for external components."""
        return str(self._consecrate_path(path))

    @resilient_io
    def exists(self, path: Union[str, Path]) -> bool:
        return self._consecrate_path(path).exists()

    @resilient_io
    def stat(self, path: Union[str, Path]) -> SanctumStat:
        target = self._consecrate_path(path)
        if not target.exists():
            raise FileNotFoundError(f"File not found: {path}")

        st = target.stat()
        kind = "file"
        if target.is_dir():
            kind = "dir"
        elif target.is_symlink():
            kind = "symlink"

        # Standardizes POSIX and Windows stat responses into a unified contract
        return SanctumStat(
            path=str(path),
            size=st.st_size,
            mtime=st.st_mtime,
            kind=kind,
            permissions=st.st_mode,
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
                raise ArtisanHeresy(f"Path conflict: '{path}' exists but is not a directory.")

    def write_bytes(self, path: Union[str, Path], data: bytes):
        """
        Guarantees Atomic File Writing.

        Data is written to a hidden temporary file first. Once the OS confirms the file
        is fully synced to disk, we perform an atomic `os.replace` to overwrite the
        target. This prevents data corruption resulting from power failures, process
        terminations, or WASM worker panics midway through a file stream.
        """
        if data is None:
            raise ArtisanHeresy("Write Error: Attempted to write null content to disk. Data must be bytes.")

        target = self._consecrate_path(path)
        start_ns = time.perf_counter_ns()

        with self._mutex:
            self._sys_log(f"Initiating atomic write for: {target.name} | Payload: {len(data)} bytes", "36")

            # Hardware Quota Verification
            # We skip this in WASM as IDBFS does not reliably report total free space
            if not self._is_wasm and len(data) > 0:
                try:
                    usage = shutil.disk_usage(target.parent if target.parent.exists() else self.root)
                    if usage.total > 0 and usage.free < len(data) * 2:
                        raise ArtisanHeresy(f"Disk Quota Exceeded: Insufficient space for {len(data)} bytes.")
                except (FileNotFoundError, OSError):
                    pass

            if not target.parent.exists():
                self._sys_log(f"Creating missing parent directory tree: {target.parent}", "30")
                self.mkdir(target.parent)

            # Generate a cryptographically random temporary file name
            nonce = secrets.token_hex(4)
            tmp_name = f".{target.name}.{nonce}.tmp"
            tmp_path = target.parent / tmp_name

            try:
                # 1. Physical Write & Flush
                with open(tmp_path, 'wb') as f:
                    f.write(data)
                    f.flush()
                    # Ensure hardware platter confirmation (Bypass OS caches)
                    if hasattr(os, 'fsync'):
                        try:
                            os.fsync(f.fileno())
                        except OSError:
                            pass

                            # Ensure file handle is released before swap
                del f

                if not tmp_path.exists():
                    raise OSError(f"I/O Error: Temporary file {tmp_path.name} disappeared after write buffer closure.")

                # 2. Target Preparation
                if target.exists():
                    if self._is_wasm:
                        self._sys_log(f"  -> Emscripten IDBFS compliance: unlinking existing '{target.name}'.", "33")
                        try:
                            # In IDBFS, os.replace can occasionally lock if the target node is heavily cached
                            target.unlink()
                        except Exception as e:
                            self._sys_log(f"  -> Pre-swap unlink failed (ignored): {e}", "30")
                    elif not os.access(target, os.W_OK):
                        # Attempt to override Read-Only attributes on Windows
                        self._unlock_file(target)

                # 3. Atomic Substitution
                try:
                    os.replace(tmp_path, target)
                    self._sys_log(f"  -> Atomic swap completed successfully.", "32")
                except OSError as replace_err:
                    # In some environments (like mounted network drives or complex WASM setups),
                    # os.replace can throw an EXDEV error. We degrade gracefully to a copy-delete.
                    self._sys_log(f"  -> Atomic swap failed: {replace_err}. Degrading to physical copy.", "33")
                    shutil.copy2(tmp_path, target)
                    tmp_path.unlink(missing_ok=True)
                    self._sys_log(f"  -> Physical copy substitution successful.", "32")

                # 4. Integrity Verification
                if not target.exists():
                    raise ArtisanHeresy(f"Integrity Verification Failed: '{target.name}' not found after atomic swap.",
                                        severity=HeresySeverity.CRITICAL)

                # Allow IDBFS asynchronous indexing a moment to catch up
                if self._is_wasm: time.sleep(0.005)

                actual_size = target.stat().st_size
                if actual_size != len(data):
                    # Secondary wait for slow virtual mounts
                    time.sleep(0.01)
                    actual_size = target.stat().st_size
                    if actual_size != len(data):
                        raise ArtisanHeresy(
                            f"Write Corruption Detected: Expected {len(data)} bytes, physical node registered {actual_size} bytes.",
                            severity=HeresySeverity.CRITICAL
                        )

                # Merkle Hash Verification (Limited to < 1MB to preserve CPU cycles)
                if len(data) < 1048576:
                    actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
                    willed_hash = hashlib.sha256(data).hexdigest()
                    if actual_hash != willed_hash:
                        raise ArtisanHeresy(f"Checksum mismatch for '{target.name}'. Data corrupted in transit.",
                                            severity=HeresySeverity.CRITICAL)

                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                self._sys_log(f"  -> Validation Success: '{target.name}' written in {duration_ms:.2f}ms\n", "32")

            except Exception as e:
                self._sys_log(f"  -> [ERROR] Write pipeline fractured: {e}\n", "31")
                if isinstance(e, ArtisanHeresy): raise e
                raise ArtisanHeresy(f"File write operation failed for '{path}': {e}", severity=HeresySeverity.CRITICAL)

            finally:
                # Cleanup the ephemeral artifact if the swap failed
                if tmp_path.exists():
                    try:
                        tmp_path.unlink()
                    except:
                        pass

                # Invalidate Python's module cache if we overwrote a Python file
                try:
                    import importlib
                    importlib.invalidate_caches()
                except:
                    pass

    def write_text(self, path: Union[str, Path], data: str, encoding: str = 'utf-8'):
        self.write_bytes(path, data.encode(encoding))

    @resilient_io
    def read_bytes(self, path: Union[str, Path]) -> bytes:
        target = self._consecrate_path(path)
        if not target.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return target.read_bytes()

    @resilient_io
    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        target = self._consecrate_path(path)
        # Deep inspection to prevent UTF-8 decode errors on binary files
        with open(target, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                raise ArtisanHeresy(f"Binary content detected in '{path}'. Cannot process as plain text.")
        return target.read_text(encoding=encoding)

    @resilient_io
    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        """Atomic move implementation with automatic parent directory creation."""
        s = self._consecrate_path(src)
        d = self._consecrate_path(dst)

        if not d.parent.exists():
            self.mkdir(d.parent)

        if d.exists() and not os.access(d, os.W_OK):
            self._unlock_file(d)

        try:
            os.replace(s, d)
        except OSError as e:
            # Fallback for Cross-Device Links (EXDEV)
            if s.is_dir():
                shutil.copytree(s, d, dirs_exist_ok=True)
                shutil.rmtree(s)
            else:
                shutil.copy2(s, d)
                s.unlink()

    @resilient_io
    def unlink(self, path: Union[str, Path]):
        target = self._consecrate_path(path)
        if not target.exists(): return
        try:
            target.unlink()
        except PermissionError:
            # Attempt to strip Read-Only attributes before deleting
            self._unlock_file(target)
            target.unlink()

        if target.exists():
            raise OSError(f"Failed to delete file: {target}")

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        target = self._consecrate_path(path)
        if not target.exists(): return

        if not recursive:
            try:
                target.rmdir()
            except OSError:
                raise ArtisanHeresy(f"Directory not empty: {path}")
            return

        def on_error(func, path, exc_info):
            """Error handler for shutil.rmtree to handle Read-Only file locks."""
            ex = exc_info[1]
            if isinstance(ex, PermissionError) or (isinstance(ex, OSError) and getattr(ex, 'winerror', 0) == 5):
                try:
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                except Exception as e:
                    Logger.warn(f"Failed to remove locked directory '{path}': {e}")
            else:
                raise ex

        shutil.rmtree(target, onerror=on_error)

    @resilient_io
    def copy(self, src: Union[str, Path], dst: Union[str, Path]):
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
        target = self._consecrate_path(path)
        if not target.exists(): return
        try:
            os.chmod(target, mode)
        except OSError:
            # FAT32 and some WASM filesystems ignore chmod
            pass

    def list_dir(self, path: Union[str, Path]) -> List[str]:
        target = self._consecrate_path(path)
        # We automatically filter out OS-level visual noise
        return [p.name for p in target.iterdir() if p.name not in {'.DS_Store', 'Thumbs.db', 'desktop.ini'}]

    def walk(self, top: Union[str, Path], topdown: bool = True) -> Iterator[Any]:
        target = self._consecrate_path(top)
        return os.walk(str(target), topdown=topdown)

    def touch(self, path: Union[str, Path]):
        """Updates file access/modification times, creating the file if necessary."""
        target = self._consecrate_path(path)
        if target.exists():
            os.utime(target, None)
        else:
            with open(target, 'a'):
                os.utime(target, None)

    def symlink(self, target: Union[str, Path], link: Union[str, Path]):
        l_path = self._consecrate_path(link)
        try:
            os.symlink(str(target), l_path)
        except OSError as e:
            # Windows requires Developer Mode or Admin rights to create symlinks
            if self._is_windows and getattr(e, 'winerror', 0) == 1314:
                self._sys_log(f"Symlink privilege denied on Windows. Degrading to physical copy: {l_path.name}")
                t_path = self._consecrate_path(target)
                if t_path.exists():
                    self.copy(t_path, l_path)
                else:
                    raise ArtisanHeresy("Permission Error: Creating symlinks on Windows requires Administrator rights.",
                                        severity=HeresySeverity.WARNING)
            else:
                raise e

    def _unlock_file(self, path: Path):
        """Forcefully sets the IWRITE bit to allow deletion of read-only files."""
        try:
            os.chmod(path, stat.S_IWRITE)
        except Exception:
            pass

    def close(self):
        pass

    def __repr__(self) -> str:
        return f"<LocalSanctum root={self.root} platform={'WIN' if self._is_windows else 'POSIX'}>"