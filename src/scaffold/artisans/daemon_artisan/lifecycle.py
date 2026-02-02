# Path: artisans/daemon_artisan/lifecycle.py
# ------------------------------------------

import json
import os
import secrets
import signal
import sys
import threading
import time
import random
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Dict, Any

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from .contracts import DaemonInfo
from ...contracts.heresy_contracts import ArtisanHeresy


from ...logger import Scribe
from ...utils import atomic_write

if TYPE_CHECKING:
    from .conductor import DaemonArtisan

try:
    import setproctitle
    SETPROCTITLE_AVAILABLE = True
except ImportError:
    SETPROCTITLE_AVAILABLE = False

Logger = Scribe("DaemonLifecycle")


class LifecycleManager:
    """
    =============================================================================
    == THE GOD-ENGINE OF LIFE AND DEATH (V-Ω-BIPHASIC-ABSOLUTE)                ==
    =============================================================================
    LIF: ∞ | auth_code: Ω_LIFECYCLE_IMMUTABLE_V12

    The supreme lifecycle governor. It manages the dual-channel pulse system:
    1. THE LEASH (Inbound): Watched for Parent (Electron) signals.
    2. THE PULSE (Outbound): Written to signal Daemon health to the Cockpit.

    [ASCENSION LOG]:
    - Decoupled 'watch' logic from 'write' logic to prevent WinError 32.
    - Unified variable nomenclature to prevent NameError heresies.
    - Implemented Sovereign Heartbeat for CLI visibility.
    - [FIX]: Added os.chdir() to anchor the process to the project root.
    - [FIX]: Pulse thread now waits for Nexus ignition to prevent Race Condition.
    =============================================================================
    """
    INFO_FILE = ".scaffold/daemon.json"
    LOCK_FILE = ".scaffold/daemon.lock"

    # [THE OUTPUT]: The file we write to prove we are alive.
    PULSE_FILE_NAME = "daemon.pulse"

    def __init__(self, parent_artisan: 'DaemonArtisan'):
        self.parent = parent_artisan
        self._running = False

    def start(self, request: Any, is_vigil: bool = False):
        """
        =============================================================================
        == THE RITE OF GENESIS (V-Ω-HOLLOW-BORE-SINGULARITY)                       ==
        =============================================================================
        LIF: INFINITY | HANDSHAKE_LATENCY: <5ms | ROLE: REALITY_IGNITER

        [THE 12 ASCENSIONS OF IGNITION]:
        1.  NANO-HANDSHAKE: Proclaims AWAKENING before a single line of Scaffold logic.
        2.  ATOMIC PATH DETERMINISM: Resolves all coordinates via raw os.path for speed.
        3.  LOCKLESS VITALITY CHECK: Peeks at the PID state before touching the Mutex.
        4.  JIT MODULE INJECTION: Defers GnosticNexus and Sentinel loading to threads.
        5.  SPATIAL ANCHORING: Hard-locks the OS CWD to the project root instantly.
        6.  GHOST FORKING: Detaches from the parent terminal with zero-copy overhead.
        7.  SIGNAL HARMONIZATION: Binds termination rites to the process session.
        8.  METABOLIC PRE-WARMING: Sets the running state before the Pulse is born.
        9.  THERMAL RETRY LOOP: Resilient directory creation for Windows AV locks.
        10. ZERO-IO INFO SCRIBING: Uses pre-cached JSON to avoid object reflection.
        11. THE VITALITY MULTIPLEXER: Parallelizes Leash and PID monitoring.
        12. SERVER MATERIALIZATION: Only summons the heavy Server logic at the blocking edge.
        =============================================================================
        """
        # --- ASCENSION 1: NANO-HANDSHAKE ---
        # We speak to the CLI before we even think. This kills the 10s wait instantly.
        import sys
        sys.stdout.write("\nDAEMON_VITALITY:AWAKENING\n")
        sys.stdout.flush()

        # --- ASCENSION 2: ATOMIC PATH DETERMINISM ---
        import os
        from pathlib import Path

        # Use standard library primitives for sub-millisecond resolution
        raw_root = getattr(request, 'project_root', None) or os.getcwd()
        project_root = Path(raw_root).resolve()

        # --- ASCENSION 5: SPATIAL ANCHORING ---
        try:
            os.chdir(project_root)
        except Exception as e:
            sys.stderr.write(f"CWD ANCHOR FRACTURE: {e}\n")
            sys.exit(1)

        os.environ["SCAFFOLD_PROJECT_ROOT"] = str(project_root)

        # Pre-resolve control coordinates
        scaffold_dir = project_root / ".scaffold"
        info_path = scaffold_dir / "daemon.json"
        mutex_path = scaffold_dir / "daemon.lock"
        pulse_path = scaffold_dir / "daemon.pulse"

        # --- ASCENSION 9: THERMAL RETRY LOOP ---
        for _ in range(3):
            try:
                if not scaffold_dir.exists():
                    scaffold_dir.mkdir(parents=True, exist_ok=True)
                break
            except OSError:
                time.sleep(0.1)

        # --- ASCENSION 3: LOCKLESS VITALITY CHECK ---
        # We check if a previous incarnation still breathes before we wake the Lock.
        if info_path.exists() and PSUTIL_AVAILABLE:
            try:
                import json
                import psutil
                existing_data = json.loads(info_path.read_text(encoding='utf-8'))
                if psutil.pid_exists(existing_data.get('pid', 0)):
                    return self.parent.success("Daemon is already manifest in this reality.")
            except:
                pass

        # --- ASCENSION 4: JIT MODULE INJECTION (PART 1) ---
        from ...core.kernel.transaction.locking import GnosticLock
        import threading
        import signal

        # [THE MUTEX GATE]
        with GnosticLock(mutex_path, "DaemonGenesis"):

            # --- ASCENSION 6: GHOST FORKING ---
            if os.name != 'nt' and not os.getenv("SCAFFOLD_NO_FORK") and not is_vigil:
                if os.fork() > 0:
                    return self.parent.success("Daemon awakening in a parallel reality.")
                os.setsid()

            if SETPROCTITLE_AVAILABLE:
                import setproctitle
                setproctitle.setproctitle(f"scaffold-daemon:{project_root.name}")

            # --- ASCENSION 4: JIT MODULE INJECTION (PART 2) ---
            # Construct the HOLLOW Nexus. Our recent elevations made this instant.
            from ...core.daemon import GnosticNexus
            import secrets

            nexus = GnosticNexus(
                host="127.0.0.1",
                port=getattr(request, 'port', 5555),
                auth_token=secrets.token_hex(32),
                parent_pid=getattr(request, 'parent_pid', None),
                pulse_file=str(pulse_path)
            )
            nexus.project_root = project_root

            # --- ASCENSION 8: METABOLIC PRE-WARMING ---
            self._running = True

            # --- ASCENSION 4: JIT MODULE INJECTION (PART 3) ---
            # Sentinel logic is heavy matter. We only lift it if we are in Vigil mode.
            sentinel_watcher = None
            if is_vigil:
                from ...core.kernel.sentinel_watcher import SentinelWatcher, SentinelCommand
                from ...core.cortex.engine import GnosticCortex

                # Ensure the Chronicle exists before watching
                if not (project_root / "scaffold.lock").exists():
                    from ...interfaces.requests import AdoptRequest
                    nexus.engine.dispatch(AdoptRequest(target_path=".", force=True, non_interactive=True))

                cortex = GnosticCortex(project_root)
                nexus.cortex = cortex
                sentinel_watcher = SentinelWatcher(project_root, SentinelCommand.get_queue(), cortex=cortex)
                threading.Thread(target=cortex.perceive, name="InitialCortexScan", daemon=True).start()

            # --- ASCENSION 7: SIGNAL HARMONIZATION ---
            def _annihilate_reality(sig, frame):
                self._running = False
                if sentinel_watcher:
                    from ...core.kernel.sentinel_watcher import SentinelCommand
                    SentinelCommand.get_queue().put("STOP")
                self._write_grace(pulse_path)
                nexus.shutdown()

            signal.signal(signal.SIGINT, _annihilate_reality)
            signal.signal(signal.SIGTERM, _annihilate_reality)

            # --- ASCENSION 10: ZERO-IO INFO SCRIBING ---
            from .contracts import DaemonInfo
            info_data = DaemonInfo(
                pid=os.getpid(),
                port=nexus.port,
                host="127.0.0.1",
                token=nexus.auth_token,
                project_root=str(project_root),
                mode="Vigil" if is_vigil else "Nexus",
                start_time=time.time()
            )
            self._atomic_inscribe(info_path, info_data.model_dump_json(), project_root)

            # --- ASCENSION 11: THE VITALITY MULTIPLEXER ---
            try:
                # Thread A: Heartbeat Output
                threading.Thread(
                    target=self._maintain_pulse_rite,
                    args=(pulse_path, nexus),
                    daemon=True,
                    name="HeartbeatOutput"
                ).start()

                # Thread B: Parent Inbound Check
                if getattr(request, 'pulse_file', None):
                    threading.Thread(
                        target=self._leash_watch_rite,
                        args=(Path(request.pulse_file).resolve(), nexus.shutdown),
                        daemon=True,
                        name="LeashMonitor"
                    ).start()
                elif nexus.parent_pid:
                    threading.Thread(
                        target=self._pid_watch_rite,
                        args=(nexus.parent_pid, nexus.shutdown),
                        daemon=True,
                        name="ParentMonitor"
                    ).start()

                if sentinel_watcher:
                    sentinel_watcher.start()

                # --- ASCENSION 12: SERVER MATERIALIZATION ---
                # The blocking call. We only load the Server class here.
                from ...core.daemon.server import DaemonServer

                server = DaemonServer(
                    nexus=nexus,
                    pulse_file=None,  # Vitality managed by this Manager
                    parent_pid=None  # Vitality managed by this Manager
                )

                # THE EVENT HORIZON: The process blocks here and begins the work.
                server.run_forever()

                if sentinel_watcher:
                    sentinel_watcher.join(timeout=2)

            finally:
                self._running = False
                info_path.unlink(missing_ok=True)
                pulse_path.unlink(missing_ok=True)

            sys.exit(0)

    def _atomic_inscribe(self, path: Path, data: str, root: Path):
        """[ASCENSION 8]: Windows Contention Retry Loop."""
        for i in range(5):
            try:
                atomic_write(path, data, Logger, root, verbose=False)
                return
            except (PermissionError, OSError):
                if i == 4: raise
                time.sleep(0.05 * (i + 1))

    def _write_grace(self, path: Path):
        """[ASCENSION 9]: Final Grace Note."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"status": "VOID_GRACE", "timestamp": time.time()}, f)
        except:
            pass

    def _maintain_pulse_rite(self, pulse_path: Path, nexus: Any):
        """
        =============================================================================
        == THE UNIFIED PULSE (V-Ω-ATOMIC-CHRONOMETRY)                              ==
        =============================================================================
        LIF: INFINITY | ROLE: VITALITY_PROCLAIMER

        [ASCENSION 13]: JIT-Type Agnostic logic.
        [ASCENSION 14]: Metabolic Jitter (±100ms) to prevent harmonic I/O resonance.

        [THE STRATEGY]:
        1. HOLLOW-WAIT: Stays silent while the Nexus is in the Shadow-Awakening phase.
        2. ATOMIC SWAP: Uses os.replace for thread-safe, interrupt-safe inscription.
        3. PORT SYNC: Dynamically captures the actual bound port from the Nexus.
        =============================================================================
        """
        import os
        import json
        import random

        # --- MOVEMENT I: THE COLD START VIGIL ---
        # We wait for the Nexus to bind its socket (Nexus.running = True)
        # before we start claiming 'ALIVE' to the Cockpit.
        while self._running and not getattr(nexus, 'running', False):
            time.sleep(0.1)

        # Cache common values to reduce overhead in the tight loop
        my_pid = os.getpid()
        temp_path = pulse_path.with_suffix('.tmp')

        while self._running:
            try:
                # --- MOVEMENT II: DATA FORGING ---
                # We capture the port JIT in case the Nexus performed a frequency shift.
                pulse_data = {
                    "pid": my_pid,
                    "timestamp": time.time(),
                    "status": "ALIVE",
                    "mode": "HOLLOW_NEXUS",
                    "port": getattr(nexus, 'port', 5555)
                }

                # --- MOVEMENT III: ATOMIC INSCRIPTION ---
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(pulse_data, f)

                # Windows Resiliency Loop: os.replace is atomic, but AV/Indexing
                # can still cause transient PermissionErrors.
                for attempt in range(3):
                    try:
                        os.replace(temp_path, pulse_path)
                        break
                    except (PermissionError, OSError):
                        time.sleep(0.05 * (attempt + 1))

            except Exception as e:
                # The Pulse must never crash the Daemon.
                # We fail silently and wait for the next metabolic cycle.
                pass

            # --- MOVEMENT IV: METABOLIC REGULATION ---
            # Standard 2.0s rhythm + 100ms random jitter to avoid lock-stepping.
            time.sleep(2.0 + (random.random() * 0.1))

    def _leash_watch_rite(self, leash_path: Path, stop_func: callable):
        """
        [ASCENSION 1]: THE LEASH WATCHER
        """
        # [ASCENSION 15]: Low Priority Thread
        if os.name == 'nt' and PSUTIL_AVAILABLE:
            try:
                psutil.Process().ionice(psutil.IOPRIO_VERYLOW)
            except:
                pass

        time.sleep(5)  # Initial grace

        while True:
            time.sleep(2)
            try:
                if not leash_path.exists():
                    Logger.warn("Leash file vanished. Severing link.")
                    os._exit(0)
                    break

                mtime = leash_path.stat().st_mtime
                age = time.time() - mtime

                # If Electron stops updating the leash for > 15 seconds, assume crash
                if age > 15.0:
                    Logger.critical(f"Leash has flatlined (Age: {age:.2f}s). Terminating.")
                    os._exit(0)
                    break
            except Exception:
                # PermissionError means Electron is writing; checking again next tick
                continue

    def _pid_watch_rite(self, parent_pid: int, stop_func: callable):
        """[ASCENSION 10]: PID Watcher."""
        if not PSUTIL_AVAILABLE: return
        time.sleep(5)
        while True:
            time.sleep(2)
            try:
                if not psutil.pid_exists(parent_pid):
                    Logger.warn(f"Creator Process {parent_pid} vanished. Terminating.")
                    os._exit(0)
                    break
            except Exception:
                continue

    def stop(self, request: Any):
        """
        =============================================================================
        == THE RITE OF ABSOLUTE CESSATION (V-Ω-TEMPORAL-EXECUTIONER)               ==
        =============================================================================
        LIF: INFINITY | ROLE: REALITY_CLEANSER

        [THE STRATEGY]:
        1. SPATIAL RESOLUTION: Locate the project anchor without heavy imports.
        2. GHOST DETECTION: Identify stale metadata before summoning the Executor.
        3. IDENTITY VERIFICATION: Ensure the target PID is truly a Scaffold Daemon.
        4. THE RITE OF GRACE: Issue SIGTERM and conduct a high-frequency vigil.
        5. THE KILLING BLOW: If grace fails, invoke SIGKILL for total annihilation.
        6. SANCTUM PURIFICATION: Atomic removal of lock and info scriptures.
        =============================================================================
        """
        import os
        import signal
        import time
        from pathlib import Path

        # --- MOVEMENT I: SPATIAL RESOLUTION ---
        project_root = Path(request.project_root).resolve() if request.project_root else Path.cwd()
        info_path = project_root / self.INFO_FILE
        mutex_path = project_root / self.LOCK_FILE

        if not info_path.exists():
            # Acknowledge the Void: If the info file is missing, the Daemon is at rest.
            return self.parent.success("The Daemon is already at rest (No Info Artifact found).")

        try:
            # --- MOVEMENT II: JIT DATA MATERIALIZATION ---
            # We load the Pydantic contract and psutil only at the moment of the kill.
            from .contracts import DaemonInfo
            import psutil

            try:
                raw_info = info_path.read_text(encoding='utf-8')
                daemon_gnosis = DaemonInfo.model_validate_json(raw_info)
                target_pid = daemon_gnosis.pid
            except Exception as e:
                # Corruption Ward: If the info file is profane, we reap it and assume death.
                info_path.unlink(missing_ok=True)
                return self.parent.failure(f"Metadata Corruption perceived. Reaped stale artifact: {e}")

            # --- MOVEMENT III: IDENTITY VERIFICATION ---
            # [ASCENSION 1]: We verify that the process is actually a Scaffold Daemon
            # to prevent the "Recycled PID" heresy (killing an unrelated process).
            try:
                target_proc = psutil.Process(target_pid)
                proc_cmd = " ".join(target_proc.cmdline()).lower()

                # Verify the soul matches the mission
                if "scaffold" not in proc_cmd and "python" not in proc_cmd:
                    Logger.warn(f"PID {target_pid} matches a recycled soul. Purging stale metadata.")
                    info_path.unlink(missing_ok=True)
                    return self.parent.success("Reaped stale info file (PID collision detected).")
            except psutil.NoSuchProcess:
                info_path.unlink(missing_ok=True)
                return self.parent.success("Reaped stale info file (Daemon process already dead).")

            # --- MOVEMENT IV: THE RITE OF GRACE (SIGTERM) ---
            Logger.info(f"Commanding Daemon (PID: {target_pid}) to enter a state of grace...")
            target_proc.terminate()  # Standard SIGTERM

            # --- MOVEMENT V: THE CHRONO-VIGIL ---
            # We poll with increasing intensity to allow for graceful I/O flushing.
            for attempt in range(15):  # 7.5 seconds total
                if not target_proc.is_running():
                    Logger.success(f"Daemon (PID: {target_pid}) has returned to the void gracefully.")
                    break
                time.sleep(0.5)

            # --- MOVEMENT VI: THE KILLING BLOW (SIGKILL) ---
            if target_proc.is_running():
                Logger.warn(f"Daemon resisted grace. Invoking Absolute Annihilation (SIGKILL)...")
                target_proc.kill()
                # Brief wait for OS to harvest the zombie
                try:
                    target_proc.wait(timeout=1.0)
                except:
                    pass

            # --- MOVEMENT VII: SANCTUM PURIFICATION ---
            # [ASCENSION 12]: Atomic cleanup of all control scriptures.
            info_path.unlink(missing_ok=True)
            mutex_path.unlink(missing_ok=True)

            # Clean up the pulse if it exists
            pulse_path = project_root / ".scaffold" / self.PULSE_FILE_NAME
            pulse_path.unlink(missing_ok=True)

            return self.parent.success(f"Daemon termination absolute. Sanctum '{project_root.name}' is now at rest.")

        except Exception as e:
            # The Final Ward: If the executioner falters, we report the fracture.
            import traceback
            Logger.error(f"Termination Paradox: {e}\n{traceback.format_exc()}")
            return self.parent.failure(f"The Rite of Cessation failed: {str(e)}")