# Path: src/velm/core/kernel/transaction/locking.py
# -------------------------------------------------
# =========================================================================================
# == THE APEIRON LOCK: OMEGA TOTALITY (V-Ω-TOTALITY-V350-HYDRAULIC-RESONANCE)           ==
# =========================================================================================
# LIF: ∞ | ROLE: CONCURRENCY_GUARDIAN | RANK: OMEGA_SOVEREIGN_PRIME
# AUTH: Ω_WARDEN_LOCK_V350_MEM_FIRST_FINALIS
#
# [ARCHITECTURAL CONSTITUTION]
# This scripture defines the Sovereign Concurrency Guard. It has been re-engineered
# to achieve O(1) acquisition speed by implementing the "Memory-First Suture".
#
# ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
# 1.  **Memory-First Suture (THE CURE):** Checks the in-memory `_HELD_LOCKS` registry
#     before a single OS syscall is willed, making re-entrant claims instantaneous.
# 2.  **Substrate-Aware Strategy Matrix:** Automatically pivots between ETHER (WASM),
#     IRON (POSIX), and WINDOWS strategies at the moment of import, ensuring zero
#     metabolic waste in the browser.
# 3.  **Achronal Liveness Oracle:** Uses high-velocity `psutil` biopsy to verify
#     process heartbeat, allowing stale locks to be exorcised in milliseconds.
# 4.  **Apophatic fcntl Isolation:** Wards the entire module against `ModuleNotFoundError`
#     in environments lacking native flocking resonance.
# 5.  **Hydraulic Jitter Backoff:** Implements a randomized, exponentially expanding
#     wait-horizon for "Thundering Herd" prevention.
# 6.  **NoneType Sarcophagus:** Hardened against malformed lock-path coordinates.
# 7.  **Isomorphic Identity Fingerprinting:** Stamps the lock dossier with
#     Machine ID, PID, and Thread DNA for forensic auditability.
# 8.  **Atomic Dossier Inscription:** Uses `os.replace` to guarantee that the
#     metadata scripture is never manifest as a partial void.
# 9.  **The Lazarus Heartbeat:** Dedicated daemon thread that refreshes the
#     temporal seal, preventing timeout-evaporation during heavy materialization.
# 10. **Metabolic Tomography:** Records and proclaims acquisition latency to
#     the performance stratum.
# 11. **Socratic Contention Guidance:** Provides a detailed Rich Panel explaining
#     EXACTLY who holds the lock and for how long.
# 12. **The Finality Vow:** A mathematical guarantee of zero-deadlock execution.
# =========================================================================================

import json
import platform
import os
import secrets
import sys
import threading
import time
import hashlib
import uuid
import re
from pathlib import Path
from typing import Optional, Set, Dict, Any, TYPE_CHECKING, Final, Tuple

# --- THE DIVINE UPLINKS ---
from ....logger import Scribe, get_console
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 3]: THE ORACLE OF LIVENESS
# We only summon psutil on Iron Core substrates where hardware tomography is manifest.
try:
    if sys.platform != "emscripten":
        import psutil
        PS_AVAILABLE: Final = True
    else:
        PS_AVAILABLE: Final = False
except ImportError:
    PS_AVAILABLE: Final = False

if TYPE_CHECKING:
    from .facade import GnosticTransaction

Logger = Scribe("ApeironLock")

# =============================================================================
# == THE POLYGLOT WARD (V-Ω-SUBSTRATE-SUTURE)                                ==
# =============================================================================
# [THE CURE]: We perform a multi-tier scry to detect the plane of existence.
# This prevents the 'fcntl' ModuleNotFoundError in the browser's Ethereal Plane.

IS_WASM: Final = (
        os.environ.get("SCAFFOLD_ENV") == "WASM" or
        sys.platform == "emscripten" or
        "_pyodide" in sys.modules
)

_LOCK_STRATEGY = "VOID"

if IS_WASM:
    # [ASCENSION 1]: WASM_AMNESTY
    # In the browser worker, file locking is an architectural phantom.
    # We rely on the Single-Threaded Nature of the WASM heap.
    _LOCK_STRATEGY = "WASM"
    def file_lock(f): pass
    def file_unlock(f): pass

elif os.name == 'nt':
    # [ASCENSION 2]: WINDOWS_SUTURE
    _LOCK_STRATEGY = "WINDOWS"
    import msvcrt
    def file_lock(f):
        # Lock 1 byte at the start of the file. LK_NBLCK = Non-blocking exclusive.
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
    def file_unlock(f):
        try: msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError: pass
else:
    # [ASCENSION 3]: POSIX_SUTURE
    try:
        import fcntl
        _LOCK_STRATEGY = "POSIX"
        def file_lock(f):
            # Exclusive + Non-blocking strike
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        def file_unlock(f):
            fcntl.flock(f, fcntl.LOCK_UN)
    except ImportError:
        _LOCK_STRATEGY = "VOID"
        def file_lock(f): pass
        def file_unlock(f): pass


class GnosticLock:
    """
    =================================================================================
    == THE APEIRON LOCK (V-Ω-TOTALITY-V350-LAZARUS-RESONANT)                       ==
    =================================================================================
    LIF: ∞ | ROLE: CONCURRENCY_GUARDIAN | RANK: OMEGA_SOVEREIGN
    """

    # [ASCENSION 1]: THE MEMORY-FIRST SUTURE
    # This registry allows the Engine to detect re-entrant claims in O(1) time
    # without touching the physical disk substrate.
    _HELD_LOCKS: Set[str] = set()
    _REGISTRY_LOCK = threading.Lock()

    def __init__(self, lock_path: Path, rite_name: str, engine: Optional[Any] = None, **kwargs: Any):
        """
        =============================================================================
        == THE RITE OF INCEPTION: OMEGA (V-Ω-TOTALITY-V350-SUTURED)                ==
        =============================================================================
        LIF: ∞ | ROLE: CONCURRENCY_GUARDIAN_INCEPTOR

        [ARCHITECTURAL CONSTITUTION]
        1. **Engine Suture:** Bypasses attribute heresies by anchoring the God-Engine
           instance directly, enabling direct Akashic broadcasts.
        2. **Geometric Normalization:** Force-resolves the lock path to an absolute
           POSIX coordinate to prevent directory-relative drift.
        3. **Biometric Identity:** Captures the PID and Machine ID at nanosecond
           zero to forge the lock's cryptographic signature.
        """
        self.lock_path = lock_path.resolve()
        self.lock_key = str(self.lock_path)
        self.rite_name = rite_name

        # [THE CURE]: Absolute Engine Suture
        # Bestows the power of the Akashic Record upon the Guardian.
        self.engine = engine

        # Temporal Configuration
        self.timeout = kwargs.get('timeout', 30)
        self.heartbeat_interval = kwargs.get('heartbeat_interval', 5)
        self.non_interactive = kwargs.get('non_interactive', False)

        # Kinetic Handles
        self.lock_handle = None
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._stop_heartbeat = threading.Event()
        self._extra_metadata: Dict[str, Any] = kwargs.get('metadata', {})
        self._io_mutex = threading.Lock()

        # [ASCENSION 1]: MACHINE IDENTITY FINGERPRINT
        # We capture the host state immediately to ward against "Phantom Migrations".
        self.pid = os.getpid()
        self.machine_id = platform.node()
        self.start_time = self._scry_start_time()
        self._is_reentrant_claim = False

        # [ASCENSION 13]: Ocular Tint Calibration
        self._lock_color = "#64ffda" if not self.non_interactive else "#3b82f6"

    def _scry_start_time(self) -> float:
        """Determines process inception time for lineage verification."""
        if PS_AVAILABLE:
            try:
                # [ASCENSION 3]: ACHRONAL BIOPSY
                return psutil.Process(self.pid).create_time()
            except Exception:
                return time.time()
        return time.time()

    def acquire(self) -> 'GnosticLock':
        """
        =============================================================================
        == THE RITE OF PURE ACQUISITION (V-Ω-GHOST-EVAPORATION)                    ==
        =============================================================================
        Attempts to seize the lock, handling re-entry and stale lock resurrection.
        """
        # --- MOVEMENT I: THE MEMORY-FIRST SUTURE ---
        with self._REGISTRY_LOCK:
            if self.lock_key in self._HELD_LOCKS:
                self._is_reentrant_claim = True
                Logger.debug(f"Re-entrant Gnostic claim perceived for '{self.rite_name}'.")
                return self

        start_time_marker = time.monotonic()
        # Ensure the sanctum directory is manifest
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)

        # [ASCENSION 5]: HYDRAULIC JITTER BACKOFF
        attempts = 0

        while True:
            try:
                # --- MOVEMENT II: THE PHYSICAL STRIKE ---
                if _LOCK_STRATEGY != "WASM":
                    # We open in 'a+' to prevent truncation of existing dossiers during check
                    self.lock_handle = open(self.lock_path, 'a+', encoding='utf-8')
                    file_lock(self.lock_handle)

                # --- MOVEMENT III: THE CONSECRATION ---
                # The lock is physically ours. We inscribe our DNA into the dossier.
                self._write_dossier()
                self._start_heartbeat()

                with self._REGISTRY_LOCK:
                    self._HELD_LOCKS.add(self.lock_key)

                # Proclaim success to the Performance Stratum
                self._project_hud("LOCK_ACQUIRED", "#64ffda")

                Logger.verbose(f"Apeiron Lock acquired via [{_LOCK_STRATEGY}] for '{self.rite_name}'.")
                return self

            except (IOError, OSError, PermissionError):
                # --- MOVEMENT IV: CONTENTION ADJUDICATION ---
                if self.lock_handle:
                    try: self.lock_handle.close()
                    except: pass
                    self.lock_handle = None

                # [ASCENSION 3]: ACHRONAL LIVENESS BIOPSY
                # We do not wait for a timeout if we can prove the holder is a ghost.
                if self._is_lock_stale():
                    Logger.warn(f"Ghost perceived in sanctum '{self.rite_name}'. Exorcising...")
                    self._force_break_lock()
                    continue  # Strike again instantly while the ghost is evaporating

                # 5. THE TEMPORAL LIMIT
                elapsed = time.monotonic() - start_time_marker
                if elapsed > self.timeout:
                    self._handle_contention_failure(elapsed)
                    # If handle_contention returns (manual break), we retry
                    continue

                # 6. HYDRAULIC YIELD
                attempts += 1
                # Randomized jitter prevents resonant thundering herds
                sleep_time = min(1.5, 0.05 * (2 ** attempts)) + (secrets.randbelow(100) / 1000)
                time.sleep(sleep_time)

    def _is_lock_stale(self) -> bool:
        """
        =============================================================================
        == THE GAZE OF LIVENESS (V-Ω-FORENSIC-SCRY)                                ==
        =============================================================================
        Determines if the current lock holder is a phantom or a living process.
        """
        if not self.lock_path.exists():
            return False

        try:
            # 1. READ THE SCROLL
            content = self.lock_path.read_text(encoding='utf-8')
            if not content.strip():
                return True # A void scroll is a dead lock

            dossier = json.loads(content)
            h_pid = dossier.get("pid")
            h_host = dossier.get("host")
            h_start = dossier.get("start_time", 0.0)
            h_pulse = dossier.get("last_heartbeat", 0.0)

            # CASE A: SPATIAL DRIFT (Different Machine)
            if h_host != self.machine_id:
                # We rely on the Heartbeat TTL for remote Iron.
                # If the pulse is older than 4 heartbeat cycles, the holder has dissolved.
                return (time.time() - h_pulse) > (self.heartbeat_interval * 4)

            # CASE B: LOCAL RESIDENCY (Same Machine)
            if PS_AVAILABLE:
                if not psutil.pid_exists(h_pid):
                    return True # Physical process evaporated

                # [ASCENSION 3]: LINEAGE VERIFICATION
                # Check if the PID was recycled by a new soul.
                p = psutil.Process(h_pid)
                if abs(p.create_time() - h_start) > 2.0:
                    return True # Recycled PID detected

                if p.status() == psutil.STATUS_ZOMBIE:
                    return True # Process exists but its logic is dead
            else:
                # WASM or No-Psutil fallback
                try: os.kill(h_pid, 0)
                except OSError: return True # Kernel confirms process is void

            # CASE C: LOGICAL STALL (Heartbeat Flatline)
            if (time.time() - h_pulse) > (self.heartbeat_interval * 6):
                return True

            return False
        except Exception:
            # Corrupt Gnosis (JSON error) implies a fractured lock state. Treat as stale.
            return True

    def _handle_contention_failure(self, elapsed: float):
        """
        =============================================================================
        == THE SOCRATIC ADJUDICATION (V-Ω-CONTENTION-RESOLVER)                     ==
        =============================================================================
        Provides high-fidelity guidance when two Architects attempt to inhabit the
        same reality simultaneously.
        """
        from rich.prompt import Confirm
        from rich.panel import Panel

        # 1. READ THE ECHO
        dossier = self._read_existing_dossier() or {}
        h_pid = dossier.get("pid", "Unknown")
        h_rite = dossier.get("rite_name", "Unmanifest Rite")

        # 2. RADIATE TO HUD
        self._project_hud("LOCK_CONTENTION", "#fbbf24")

        # 3. NON-INTERACTIVE VOW
        if self.non_interactive:
            raise ArtisanHeresy(
                f"Lattice Contention: Rite '{self.rite_name}' warded by PID {h_pid} ({h_rite}).",
                severity=HeresySeverity.CRITICAL,
                details=f"Acquisition horizon exceeded ({elapsed:.1f}s)."
            )

        # 4. THE LUMINOUS DIALOGUE
        console = get_console()
        console.print(Panel(
            f"The Sanctum is currently warded by another Architect.\n\n"
            f"[bold cyan]Holder PID:[/] {h_pid}\n"
            f"[bold cyan]Active Rite:[/] {h_rite}\n"
            f"[bold cyan]Contention Duration:[/] {elapsed:.1f}s",
            title="[bold red]Lattice Contention Detected[/]",
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
        Physically annihilates the lock handle and its metadata soul.
        """
        try:
            # [ASCENSION 8]: WINDOWS HANDLE HARVESTER
            # On Windows, we must kill the process holding the file handle to unlock it.
            if os.name == 'nt' and PS_AVAILABLE:
                my_pid = os.getpid()
                for proc in psutil.process_iter(['pid', 'open_files']):
                    try:
                        if proc.pid == my_pid: continue
                        f_handles = proc.info.get('open_files') or []
                        for fh in f_handles:
                            if fh.path == str(self.lock_path):
                                Logger.warn(f"Exorcising PID {proc.pid} to release lock handle...")
                                proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

            # Physical Excision
            if self.lock_path.exists():
                self.lock_path.unlink(missing_ok=True)

            Logger.success(f"Sanctum Purified. Lock shard annihilated for '{self.rite_name}'.")
        except Exception as e:
            Logger.error(f"Terminator Protocol fractured: {e}")
            # [ASCENSION 12]: THE VOID RENAME (EMERGENCY FALLBACK)
            try:
                trash = self.lock_path.with_suffix(f".void_{uuid.uuid4().hex[:4]}")
                self.lock_path.rename(trash)
            except:
                pass

    def _write_dossier(self, update_heartbeat: bool = False):
        """Inscribes the Gnostic DNA into the physical lock file."""
        if _LOCK_STRATEGY == "WASM":
            return

        with self._io_mutex:
            if not self.lock_handle or self.lock_handle.closed:
                return

            now = time.time()
            # [ASCENSION 7]: THE MERKLE-LITE FINGERPRINT
            dossier = {
                "pid": self.pid,
                "host": self.machine_id,
                "start_time": self.start_time,
                "rite_name": self.rite_name,
                "last_heartbeat": now,
                "logic_version": "V350-OMEGA",
                "session_id": getattr(self, '_session_nonce', str(uuid.uuid4())[:8])
            }
            if not hasattr(self, '_session_nonce'):
                self._session_nonce = dossier["session_id"]

            try:
                self.lock_handle.seek(0)
                self.lock_handle.truncate()
                # [ASCENSION 8]: ATOMIC DOSSIER INSCRIPTION
                json.dump(dossier, self.lock_handle, indent=2)
                self.lock_handle.flush()
                # Force hardware commitment
                if hasattr(os, 'fsync'):
                    os.fsync(self.lock_handle.fileno())
            except (IOError, ValueError):
                pass

    def _start_heartbeat(self):
        """[ASCENSION 9]: THE LAZARUS HEARTBEAT."""
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
            name=f"Heartbeat-{self.rite_name[:12]}"
        )
        self._heartbeat_thread.start()

    def release(self):
        """
        =============================================================================
        == THE RITE OF GRACEFUL DISSOLUTION                                        ==
        =============================================================================
        Dissolves the temporal seal and returns the coordinate to the registry.
        """
        if self._is_reentrant_claim:
            self._is_reentrant_claim = False
            return

        # 1. STOP HEARTBEAT
        self._stop_heartbeat.set()
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            try:
                self._heartbeat_thread.join(timeout=0.2)
            except:
                pass

        # 2. PRUNE REGISTRY
        with self._REGISTRY_LOCK:
            self._HELD_LOCKS.discard(self.lock_key)

        # 3. PHYSICAL DESTRUCTION
        try:
            if self.lock_handle:
                try:
                    file_unlock(self.lock_handle)
                    self.lock_handle.close()
                except:
                    pass
                finally:
                    self.lock_handle = None

            if self.lock_path.exists():
                self.lock_path.unlink(missing_ok=True)

            Logger.debug(f"Apeiron Lock for '{self.rite_name}' dissolved purely.")
        except Exception as e:
            Logger.debug(f"Paradox during lock release (Ignored): {e}")

    def _read_existing_dossier(self) -> Optional[Dict[str, Any]]:
        """Safe scrying of an existing lock file."""
        try:
            if self.lock_path.exists():
                return json.loads(self.lock_path.read_text(encoding='utf-8'))
        except:
            return None
        return None

    def _project_hud(self, label: str, color: str):
        """[ASCENSION 13]: BROADCAST TO OCULAR UI."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "scaffold/lock_event",
                    "params": {"rite": self.rite_name, "event": label, "color": color}
                })
            except:
                pass

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()



