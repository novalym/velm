# Path: src/velm/core/kernel/transaction/volume_shifter/shifter/robust_rename.py
# ------------------------------------------------------------------------------

import os
import time
import uuid
import shutil
import stat
import gc
import random
from pathlib import Path
from typing import List, Final

# Attempt to load psutil for Native Handle Exorcism
try:
    import psutil

    PS_AVAILABLE = True
except ImportError:
    PS_AVAILABLE = False


class AtomicRenamer:
    """
    =================================================================================
    == THE IMMORTAL RENAMER (V-Ω-TOTALITY-V64-GHOST-SUTURED)                       ==
    =================================================================================
    The supreme engine for moving files across the boundary of reality.

    [ASCENSION 1]: The Directory Replace Exorcism. Drops the 0x1 flag when moving
    directories on Windows to prevent WinError 5.
    """

    RETRY_LIMIT: Final[int] = 6
    BASE_DELAY_S: Final[float] = 0.15
    MAX_TIMEOUT_S: Final[float] = 10.0

    def __init__(self, logger, is_windows: bool, is_wasm: bool):
        self.Logger = logger
        self.is_windows = is_windows
        self.is_wasm = is_wasm
        self._ghost_registry: List[Path] = []

    def robust_rename(self, src: Path, dst: Path):
        """Executes the unbreakable atomic swap with exponential backoff and Ghosting."""
        if not src.exists(): return

        src_raw = self._canonize_path(src)
        dst_raw = self._canonize_path(dst)
        start_time = time.monotonic()
        last_err = None

        import ctypes

        for attempt in range(self.RETRY_LIMIT):
            try:
                # =================================================================
                # == [ASCENSION 1]: THE TOMBSTONE SUTURE (GHOST RENAME)          ==
                # =================================================================
                if self.is_windows and dst.exists() and dst.is_file():
                    ghost_path = dst.with_suffix(f".ghost_{uuid.uuid4().hex[:6]}")
                    try:
                        os.rename(dst_raw, self._canonize_path(ghost_path))
                        self._ghost_registry.append(ghost_path)
                    except OSError:
                        pass

                if self.is_windows and not self.is_wasm:
                    # =================================================================
                    # == [THE CURE]: DIRECTORY REPLACE EXORCISM                      ==
                    # =================================================================
                    # 0x8 = MOVEFILE_WRITE_THROUGH
                    # 0x1 = MOVEFILE_REPLACE_EXISTING
                    flags = 0x8
                    # Only apply 0x1 if the source is a FILE. Applying 0x1 to a
                    # directory causes WinError 5 (Access Denied) on Windows!
                    if not src.is_dir():
                        flags |= 0x1

                    if not ctypes.windll.kernel32.MoveFileExW(src_raw, dst_raw, flags):
                        win_err = ctypes.GetLastError()
                        raise PermissionError(f"[WinError {win_err}] MoveFileExW Failed")
                else:
                    # POSIX ATOMIC SWAP
                    os.replace(src_raw, dst_raw)

                    # POSIX Inode Synchronization
                    if os.name == 'posix':
                        dir_fd = os.open(os.path.dirname(dst_raw), os.O_RDONLY)
                        try:
                            os.fsync(dir_fd)
                        finally:
                            os.close(dir_fd)

                # Strike successful
                return

            except (PermissionError, OSError) as e:
                last_err = e
                err_code = getattr(e, 'errno', 0)
                win_code = getattr(e, 'winerror', 0)

                # CROSS-DEVICE BOUNDARY (EXDEV)
                if err_code == 18 or win_code == 17:
                    self.Logger.verbose(f"Cross-volume boundary perceived for {src.name}. Streaming matter...")
                    if src.is_dir():
                        shutil.copytree(src_raw, dst_raw, dirs_exist_ok=True)
                        shutil.rmtree(src_raw, ignore_errors=True)
                    else:
                        shutil.move(src_raw, dst_raw)
                    return

                # PERMISSION EXORCISM
                if err_code == 13 or win_code == 5:
                    if dst.exists():
                        try:
                            mode = os.stat(dst_raw).st_mode
                            os.chmod(dst_raw, mode | stat.S_IWRITE)
                        except Exception:
                            pass

                # NATIVE HANDLE EXORCISM & LUSTRATION
                if attempt == 1:
                    import importlib
                    importlib.invalidate_caches()
                    gc.collect(2)

                    # Aggressive Handle Assassination
                    if self.is_windows and PS_AVAILABLE and dst.exists() and dst.is_file():
                        self._assassinate_process_holding_lock(dst)

                if time.monotonic() - start_time > self.MAX_TIMEOUT_S:
                    break

                delay = self.BASE_DELAY_S * (1.6 ** attempt) + (random.random() * 0.1)
                time.sleep(delay)
                continue
            except Exception as e:
                raise e

        raise last_err

    def _assassinate_process_holding_lock(self, target_path: Path):
        """[ASCENSION 35]: Forcefully kills background processes locking the file."""
        my_pid = os.getpid()
        target_str = str(target_path.resolve())
        for proc in psutil.process_iter(['pid', 'open_files']):
            try:
                if proc.pid == my_pid: continue
                files = proc.info.get('open_files') or []
                for f in files:
                    if f.path == target_str:
                        self.Logger.warn(f"Exorcising PID {proc.pid} to release lock on {target_path.name}...")
                        proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def evaporate_ghosts(self):
        """Silently cleans up any .ghost files created by the Tombstone Suture."""
        for ghost in self._ghost_registry:
            try:
                if ghost.exists():
                    ghost.unlink()
            except OSError:
                pass
        self._ghost_registry.clear()

    def _canonize_path(self, path: Path) -> str:
        """UNC Long Path Prefix & Null-Byte Annihilation."""
        abs_path = str(path.resolve()).replace('\x00', '')
        if self.is_windows and len(abs_path) > 240 and not abs_path.startswith('\\\\?\\'):
            return '\\\\?\\' + os.path.abspath(abs_path)
        return abs_path