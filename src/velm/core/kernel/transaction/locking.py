# Path: src/velm/core/kernel/transaction/locking.py
# -------------------------------------------------
# =========================================================================================
# == THE APEIRON LOCK: OMEGA TOTALITY (V-Ω-TOTALITY-V310-SUBSTRATE-AGNOSTIC)             ==
# =========================================================================================
# LIF: ∞ | ROLE: CONCURRENCY_GUARDIAN | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_WARDEN_LOCK_V310_WASM_HEALED_2026_FINALIS
# =========================================================================================

import json
import platform
import os
import sys
import threading
import time
import hashlib
import uuid
from pathlib import Path
from typing import Optional, Set, Dict, Any, TYPE_CHECKING, Final

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 3]: THE ORACLE OF LIVENESS
try:
    import psutil

    PS_AVAILABLE: Final = True
except ImportError:
    psutil = None
    PS_AVAILABLE: Final = False

if TYPE_CHECKING:
    from .facade import GnosticTransaction

Logger = Scribe("ApeironLock")

# =============================================================================
# == THE POLYGLOT WARD (V-Ω-SUBSTRATE-SUTURE)                                ==
# =============================================================================
# [THE CURE]: We perform a multi-tier import scry to detect WASM/Emscripten.
# This prevents ModuleNotFoundError: No module named 'fcntl' in the browser.

IS_WASM: Final = (
        os.environ.get("SCAFFOLD_ENV") == "WASM" or
        sys.platform == "emscripten" or
        "_pyodide" in sys.modules
)

_LOCK_STRATEGY = "VOID"

if IS_WASM:
    # [ASCENSION 1]: WASM_AMNESTY
    # In the browser worker, file locking is a semantic illusion.
    # We use a pure memory-lock approach to satisfy the API surface.
    _LOCK_STRATEGY = "WASM"


    def file_lock(f):
        """No-Op in the virtualized WASM substrate."""
        pass


    def file_unlock(f):
        """No-Op in the virtualized WASM substrate."""
        pass

elif os.name == 'nt':
    # [ASCENSION 2]: WINDOWS_SUTURE
    _LOCK_STRATEGY = "WINDOWS"
    import msvcrt


    def file_lock(f):
        """Windows-specific atomic file locking."""
        # Lock bytes 0-1. Non-blocking exclusive lock.
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)


    def file_unlock(f):
        """Windows-specific atomic file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
else:
    # [ASCENSION 3]: POSIX_SUTURE
    try:
        import fcntl

        _LOCK_STRATEGY = "POSIX"


        def file_lock(f):
            """Unix Flocking logic: Exclusive + Non-blocking."""
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)


        def file_unlock(f):
            """Unix Flocking logic: Release."""
            fcntl.flock(f, fcntl.LOCK_UN)
    except ImportError:
        # Emergency fallback for restricted containers lacking fcntl
        _LOCK_STRATEGY = "VOID"


        def file_lock(f):
            pass


        def file_unlock(f):
            pass


class GnosticLock:
    """
    =================================================================================
    == THE APEIRON LOCK (V-Ω-TOTALITY-V310-LAZARUS-WASM-RESILIENT)                 ==
    =================================================================================
    LIF: ∞ | ROLE: CONCURRENCY_GUARDIAN | RANK: OMEGA_SOVEREIGN
    """

    # [ASCENSION 5]: RE-ENTRANT THREAD REGISTRY
    _HELD_LOCKS: Set[str] = set()
    _REGISTRY_LOCK = threading.Lock()

    def __init__(self, lock_path: Path, rite_name: str, **kwargs: Any):
        """
        The Rite of Inception for the Guardian.
        """
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

        # [ASCENSION 1]: MACHINE IDENTITY FINGERPRINT
        self.pid = os.getpid()
        self.machine_id = platform.node()
        self.start_time = self._scry_start_time()
        self._is_reentrant_claim = False

    def _scry_start_time(self) -> float:
        """Determines process inception time for lineage verification."""
        if PS_AVAILABLE:
            try:
                return psutil.Process(self.pid).create_time()
            except Exception:
                return 0.0
        return 0.0

    def acquire(self) -> 'GnosticLock':
        """
        =============================================================================
        == THE RITE OF PURE ACQUISITION (V-Ω-GHOST-EVAPORATION)                    ==
        =============================================================================
        Attempts to seize the lock, handling re-entry and stale lock resurrection.
        """
        # 1. THE RE-ENTRY CHECK
        with self._REGISTRY_LOCK:
            if self.lock_key in self._HELD_LOCKS:
                self._is_reentrant_claim = True
                Logger.verbose(f"Re-entrant Gnostic claim perceived for '{self.rite_name}'.")
                return self

        start_time_marker = time.monotonic()
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)

        # [ASCENSION 7]: ADAPTIVE BACKOFF WITH JITTER
        attempts = 0

        while True:
            try:
                # 2. THE PHYSICAL ATTEMPT
                # [THE FIX]: In WASM mode, we bypass physical file handles.
                if _LOCK_STRATEGY != "WASM":
                    self.lock_handle = open(self.lock_path, 'a+', encoding='utf-8')
                    file_lock(self.lock_handle)

                # 3. CONSECRATION: THE LOCK IS OURS
                self._write_dossier()
                self._start_heartbeat()

                with self._REGISTRY_LOCK:
                    self._HELD_LOCKS.add(self.lock_key)

                # [ASCENSION 7]: BROADCAST SUCCESS
                self._project_hud("LOCK_ACQUIRED", "#64ffda")

                Logger.verbose(
                    f"Apeiron Lock acquired via [{_LOCK_STRATEGY}] for '{self.rite_name}'."
                )
                return self

            except (IOError, OSError, PermissionError):
                # 4. CONTENTION: THE GAZE OF LIVENESS
                if self.lock_handle:
                    try:
                        self.lock_handle.close()
                    except Exception:
                        pass
                    self.lock_handle = None

                # [ASCENSION 3]: GHOST DETECTION
                if self._is_lock_stale():
                    Logger.warn(f"Ghost perceived in sanctum '{self.rite_name}'. Exorcising...")
                    self._force_break_lock()
                    continue  # Re-attempt immediately after evaporation

                # 5. THE TEMPORAL LIMIT
                elapsed = time.monotonic() - start_time_marker
                if elapsed > self.timeout:
                    self._handle_contention_failure(elapsed)
                    # If handle_contention allows return, we retry
                    continue

                # 6. YIELD AND RE-SEED
                attempts += 1
                # Randomized sleep to prevent resonance in thundering herds
                sleep_time = min(2.0, 0.1 * (1.5 ** attempts)) + (uuid.uuid4().int % 100 / 500)
                time.sleep(sleep_time)

    def _is_lock_stale(self) -> bool:
        """
        =============================================================================
        == THE GAZE OF LIVENESS (V-Ω-ACHRONAL-BIOPSY)                              ==
        =============================================================================
        Determines if the current lock holder is a phantom or a living process.
        """
        if not self.lock_path.exists():
            return False

        try:
            # [ASCENSION 8]: READ THE DOSSIER
            content = self.lock_path.read_text(encoding='utf-8')
            if not content:
                return True  # Empty file is a void

            dossier = json.loads(content)
            holder_pid = dossier.get("pid")
            holder_machine = dossier.get("host")
            holder_start = dossier.get("start_time", 0.0)
            last_pulse = dossier.get("last_heartbeat", 0.0)

            # Case 1: Different Realm (Machine)
            if holder_machine != self.machine_id:
                # We rely strictly on the Heartbeat Pulse for remote machines
                return (time.time() - last_pulse) > (self.heartbeat_interval * 4)

            # Case 2: Same Realm (Local Machine)
            if PS_AVAILABLE:
                if not psutil.pid_exists(holder_pid):
                    return True  # Process is dead

                # [ASCENSION 3]: LINEAGE VERIFICATION
                proc = psutil.Process(holder_pid)
                if abs(proc.create_time() - holder_start) > 1.0:
                    return True  # PID was recycled by a new soul

                if proc.status() == psutil.STATUS_ZOMBIE:
                    return True  # Soul is trapped, but inactive
            else:
                # Fallback without psutil
                try:
                    os.kill(holder_pid, 0)
                except OSError:
                    return True  # Dead

            # Case 3: Heartbeat flatline (Stalled logic)
            if (time.time() - last_pulse) > (self.heartbeat_interval * 6):
                return True

            return False
        except Exception:
            # If the dossier is profane (corrupt JSON), it is stale.
            return True

    def _handle_contention_failure(self, elapsed: float):
        """The Socratic Adjudication of Contention."""
        from rich.prompt import Confirm
        from rich.panel import Panel

        dossier = self._read_existing_dossier() or {}
        holder_pid = dossier.get("pid", "Unknown")
        holder_rite = dossier.get("rite_name", "Unknown Rite")

        self._project_hud("LOCK_CONTENTION", "#fbbf24")

        if self.non_interactive:
            raise ArtisanHeresy(
                f"Lattice Contention: Rite '{self.rite_name}' is warded by PID {holder_pid} ({holder_rite}).",
                severity=HeresySeverity.CRITICAL,
                details=f"Timeout after {elapsed:.1f}s. Silence willed by --non-interactive."
            )

        console = get_console()
        console.print(Panel(
            f"The Sanctum is currently warded by another Architect.\n\n"
            f"[bold cyan]Holder PID:[/] {holder_pid}\n"
            f"[bold cyan]Active Rite:[/] {holder_rite}\n"
            f"[bold cyan]Duration:[/] {elapsed:.1f}s",
            title="[bold red]Lattice Contention[/]",
            border_style="red"
        ))

        if Confirm.ask("[bold yellow]The Guardian is persistent. Shall we forcefully break the seal?[/]",
                       default=False):
            self._force_break_lock()
            return

        raise ArtisanHeresy(f"Rite '{self.rite_name}' stayed by Architect decision.")

    def _force_break_lock(self):
        """
        =============================================================================
        == THE TERMINATOR PROTOCOL (V-Ω-SURGICAL-EXORCISM)                         ==
        =============================================================================
        Annihilates the lock handle grip using the Inquisitor's Scalpel.
        """
        try:
            # On Windows, deleting a file held open requires harvesting the holder
            if os.name == 'nt' and PS_AVAILABLE:
                my_pid = os.getpid()
                for proc in psutil.process_iter(['pid', 'open_files']):
                    try:
                        if proc.pid == my_pid:
                            continue
                        files = proc.info.get('open_files') or []
                        for f in files:
                            if f.path == str(self.lock_path):
                                Logger.warn(f"Exorcising PID {proc.pid} to release lock handle...")
                                proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

            self.lock_path.unlink(missing_ok=True)
            Logger.success(f"Sanctum Purified. Lock Shard annihilated.")
        except Exception as e:
            Logger.error(f"Terminator Protocol fractured: {e}")
            # Desperate fallback: Rename the shard to clear the path
            try:
                trash_path = self.lock_path.with_suffix(f".void_{uuid.uuid4().hex[:4]}")
                self.lock_path.rename(trash_path)
            except Exception:
                pass

    def _write_dossier(self, update_heartbeat: bool = False):
        """Inscribes the Gnostic Dossier into the physical lock file."""
        if _LOCK_STRATEGY == "WASM":
            return

        with self._io_mutex:
            if not self.lock_handle or self.lock_handle.closed:
                return

            now = time.time()
            dossier = {
                "pid": self.pid,
                "start_time": self.start_time,
                "host": self.machine_id,
                "rite_name": self.rite_name,
                "command_line": f"{sys.executable} {' '.join(sys.argv)}",
                "last_heartbeat": now,
                "session": getattr(self, 'acquired_at', now)
            }
            if not hasattr(self, 'acquired_at'):
                self.acquired_at = now

            dossier.update(self._extra_metadata)

            try:
                self.lock_handle.seek(0)
                self.lock_handle.truncate()
                json.dump(dossier, self.lock_handle, indent=2)
                self.lock_handle.flush()
                # Ensure physical commitment to the substrate
                if hasattr(os, 'fsync'):
                    os.fsync(self.lock_handle.fileno())
            except (IOError, OSError, ValueError):
                pass

    def _start_heartbeat(self):
        """[ASCENSION 2]: THE LAZARUS HEARTBEAT."""
        if _LOCK_STRATEGY == "WASM":
            return

        self._stop_heartbeat.clear()

        def _pulse():
            while not self._stop_heartbeat.wait(self.heartbeat_interval):
                try:
                    self._write_dossier(update_heartbeat=True)
                except Exception:
                    break

        self._heartbeat_thread = threading.Thread(
            target=_pulse,
            daemon=True,
            name=f"Heartbeat-{self.rite_name}"
        )
        self._heartbeat_thread.start()

    def release(self):
        """The Rite of Graceful Dissolution."""
        if self._is_reentrant_claim:
            self._is_reentrant_claim = False
            return

        self._stop_heartbeat.set()
        if self._heartbeat_thread:
            self._heartbeat_thread.join(timeout=1.0)

        with self._REGISTRY_LOCK:
            self._HELD_LOCKS.discard(self.lock_key)

        try:
            if self.lock_handle:
                try:
                    file_unlock(self.lock_handle)
                    self.lock_handle.close()
                except Exception:
                    pass
                finally:
                    self.lock_handle = None

            if self.lock_path.exists():
                try:
                    self.lock_path.unlink(missing_ok=True)
                except OSError:
                    pass

            Logger.verbose(f"Apeiron Lock for '{self.rite_name}' dissolved.")
        except Exception as e:
            Logger.error(f"Paradox during lock dissolution: {e}")

    def _read_existing_dossier(self) -> Optional[Dict[str, Any]]:
        """Safe scrying of an existing lock file."""
        try:
            if self.lock_path.exists():
                with open(self.lock_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            return None
        return None

    def _project_hud(self, label: str, color: str):
        """[ASCENSION 7]: BROADCAST TO OCULAR UI."""
        # This is a prophecy. We assume the active transaction or engine
        # can reach the Akashic Record if it exists in the current thread.
        pass

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# == SCRIPTURE SEALED: THE CONCURRENCY GUARDIAN REACHES OMEGA TOTALITY ==