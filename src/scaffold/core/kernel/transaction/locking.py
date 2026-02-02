# Path: core/kernel/transaction/locking.py
# ----------------------------------------

import json
import platform
import os
import sys
import threading
import time
from pathlib import Path
from typing import Optional, Set, Dict, Any, TYPE_CHECKING

# Ascension I: The Gnostic Scribe
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# Ascension III: The Oracle of Liveness
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

if TYPE_CHECKING:
    from .facade import GnosticTransaction

Logger = Scribe("ApeironLock")

# Ascension VII: The Polyglot Ward
if os.name == 'nt':
    import msvcrt


    def file_lock(f):
        # Lock bytes 0-1. Non-blocking.
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)


    def file_unlock(f):
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
else:
    import fcntl


    def file_lock(f):
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)


    def file_unlock(f):
        fcntl.flock(f, fcntl.LOCK_UN)


class GnosticLock:
    """
    =================================================================================
    == THE APEIRON LOCK (V-Ω-LEGENDARY-APOTHEOSIS. THE SENTIENT GUARDIAN)          ==
    =================================================================================
    LIF: ∞ (ETERNAL & DIVINE)

    The divine guardian of the Transactional Sanctum. It wields a cross-platform,
    re-entrant, thread-safe, and self-healing lock mechanism to prevent the heresy
    of concurrent modification.

    [ASCENSION 13]: THE TERMINATOR PROTOCOL.
    On Windows, if a lock file cannot be deleted (`WinError 32`), this entity now
    possesses the faculty to hunt down the process holding the handle and annihilate it.
    """

    _HELD_LOCKS: Set[str] = set()
    _REGISTRY_LOCK = threading.Lock()

    def __init__(self, lock_path: Path, rite_name: str, **kwargs):
        self.lock_path = lock_path.resolve()
        self.lock_key = str(self.lock_path)
        self.rite_name = rite_name
        self.timeout = kwargs.get('timeout', 30)
        self.heartbeat_interval = kwargs.get('heartbeat_interval', 5)
        self.non_interactive = kwargs.get('non_interactive', False)

        self.lock_handle = None
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._stop_heartbeat = threading.Event()
        self._extra_metadata: Dict[str, Any] = {}
        self._io_mutex = threading.Lock()

        self.pid = os.getpid()
        self.tid = threading.get_ident()
        self.command_line = f"{sys.executable} {' '.join(sys.argv)}"
        self._is_reentrant_claim = False

    def acquire(self):
        """The Rite of Pure Acquisition."""
        # Re-entry Check
        with self._REGISTRY_LOCK:
            if self.lock_key in self._HELD_LOCKS:
                self._is_reentrant_claim = True
                Logger.verbose(f"Re-entrant lock claim for '{self.rite_name}'.")
                return self

        start_time = time.monotonic()
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)

        while True:
            try:
                # Open in append mode first to avoid truncating if locked?
                # No, we need 'w' to overwrite if we get the lock.
                # On Windows, 'w' might fail with PermissionError if locked exclusive.
                self.lock_handle = open(self.lock_path, 'w', encoding='utf-8')
                file_lock(self.lock_handle)

                # The lock is ours.
                self._write_dossier()
                self._start_heartbeat()

                with self._REGISTRY_LOCK:
                    self._HELD_LOCKS.add(self.lock_key)

                Logger.verbose(f"Apeiron Lock acquired for '{self.rite_name}'.")
                return self

            except (IOError, OSError, BlockingIOError, PermissionError):
                if self.lock_handle:
                    try:
                        self.lock_handle.close()
                    except:
                        pass
                    self.lock_handle = None

                # Check Timeout
                if time.monotonic() - start_time > self.timeout:
                    self._handle_timeout()
                    # After handling timeout (breaking lock), retry immediately
                    continue

                time.sleep(0.5)

    def release(self):
        """Ascension VI: The Unbreakable Ward of Graceful Release."""
        if self._is_reentrant_claim:
            self._is_reentrant_claim = False
            return

        self._stop_heartbeat.set()
        if self._heartbeat_thread:
            self._heartbeat_thread.join(timeout=0.5)

        try:
            if self.lock_handle:
                try:
                    with self._REGISTRY_LOCK:
                        self._HELD_LOCKS.discard(self.lock_key)
                    file_unlock(self.lock_handle)
                    self.lock_handle.close()
                except Exception as e:
                    Logger.warn(f"Minor paradox during lock handle release: {e}")
                finally:
                    self.lock_handle = None

            # Annihilate the physical scripture
            if self.lock_path.exists():
                try:
                    self.lock_path.unlink(missing_ok=True)
                except OSError:
                    # If we can't delete it, someone else might have grabbed it instantly.
                    # Or Windows is being slow to release the handle. We ignore.
                    pass

            Logger.verbose(f"Apeiron Lock for '{self.rite_name}' released.")
        except Exception as e:
            Logger.error(f"Catastrophic paradox during lock release: {e}")

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def _start_heartbeat(self):
        self._stop_heartbeat.clear()
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_rite, daemon=True)
        self._heartbeat_thread.start()

    def _heartbeat_rite(self):
        while not self._stop_heartbeat.wait(self.heartbeat_interval):
            try:
                self._write_dossier(update_heartbeat=True)
            except Exception:
                break

    def _write_dossier(self, update_heartbeat: bool = False):
        with self._io_mutex:
            if not self.lock_handle or self.lock_handle.closed: return

            current_time = time.time()
            dossier = {
                "pid": self.pid,
                "tid": self.tid,
                "host": platform.node(),
                "rite_name": self.rite_name,
                "command_line": self.command_line,
                "acquired_at": getattr(self, 'acquired_at', current_time),
                "last_heartbeat": current_time
            }
            if not hasattr(self, 'acquired_at'):
                self.acquired_at = current_time

            dossier.update(self._extra_metadata)

            try:
                self.lock_handle.seek(0)
                self.lock_handle.truncate()
                json.dump(dossier, self.lock_handle, indent=2)
                self.lock_handle.flush()
                if hasattr(os, 'fsync'): os.fsync(self.lock_handle.fileno())
            except (ValueError, IOError, OSError):
                pass

    def _handle_timeout(self):
        """Ascension V & IX & XI: Adjudication of the Dead."""
        from rich.prompt import Confirm
        from rich.panel import Panel
        from rich.text import Text

        dossier = self._read_existing_dossier() or {}
        holder_pid = dossier.get("pid")

        # If we can't read the dossier, it's likely a Zombie Process holding the file handle tight.
        if not holder_pid and self.lock_path.exists():
            Logger.warn("Lock file exists but is unreadable (Zombie Grip). Initiating Terminator Protocol.")
            self._force_break_lock()
            return

        holder_name = dossier.get("rite_name", "Unknown Rite")

        # Check Liveness
        if holder_pid and self._is_pid_alive(holder_pid):
            # Zombie Check (Heartbeat Age)
            last_beat = dossier.get("last_heartbeat", 0)
            if time.time() - last_beat > (self.heartbeat_interval * 4):
                Logger.warn(f"Lock held by ZOMBIE process {holder_pid}. Breaking seal.")
                self._force_break_lock()
                return

            # Active Contention
            if self.non_interactive:
                raise ArtisanHeresy(f"Lock held by {holder_pid}. Timeout.", severity=HeresySeverity.CRITICAL)

            # Interactive Prompt
            console = get_console()
            console.print(Panel(f"Lock held by PID {holder_pid} ({holder_name})", title="Contention", style="red"))
            if Confirm.ask("Break lock?", console=console, default=False):
                self._force_break_lock()
                return

        else:
            # Dead process
            Logger.warn("Lock held by ghost. Breaking seal.")
            self._force_break_lock()

    def _force_break_lock(self):
        """
        [ASCENSION 13]: THE TERMINATOR PROTOCOL.
        Hunts down the process holding the file handle and forces a release.
        """
        try:
            self.lock_path.unlink(missing_ok=True)
            Logger.info("The Seal has been broken.")
        except PermissionError:
            Logger.warn("Permission Denied on Unlink. A process still grips the shard.")

            if not PSUTIL_AVAILABLE:
                Logger.error("Cannot hunt zombie process: 'psutil' is missing.")
                # We try one last desperate rename
                try:
                    trash = self.lock_path.with_suffix(f".trash_{int(time.time())}")
                    self.lock_path.rename(trash)
                    return
                except:
                    raise ArtisanHeresy("Cannot break lock. File is physically held by OS.")

            # Hunt the handle
            killed = False
            my_pid = os.getpid()

            Logger.info("Scanning process table for handle owners...")
            for proc in psutil.process_iter(['pid', 'name', 'open_files']):
                try:
                    if proc.pid == my_pid: continue

                    files = proc.info.get('open_files') or []
                    for f in files:
                        if f.path == str(self.lock_path.resolve()):
                            Logger.warn(f"Found Lock Owner: {proc.info['name']} (PID: {proc.pid}). Terminating...")
                            proc.kill()
                            killed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if killed:
                time.sleep(0.2)  # Allow OS cleanup
                try:
                    self.lock_path.unlink(missing_ok=True)
                    Logger.success("Zombie process terminated. Lock file annihilated.")
                except Exception as e:
                    Logger.error(f"Failed to delete lock file even after kill: {e}")
            else:
                Logger.error("Could not identify process holding the lock.")

    def _read_existing_dossier(self) -> Optional[Dict[str, Any]]:
        """A Safe Gaze upon the file."""
        try:
            if self.lock_path.exists():
                # Try opening with shared read if possible (standard open is usually fine for read)
                with open(self.lock_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            return None
        return None

    def _is_pid_alive(self, pid: int) -> bool:
        if not PSUTIL_AVAILABLE:
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False
        return psutil.pid_exists(pid)