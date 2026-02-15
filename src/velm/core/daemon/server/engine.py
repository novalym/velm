# Path: core/daemon/server/engine.py
# ----------------------------------
# LIF: INFINITY | ROLE: LIFECYCLE_ORCHESTRATOR | AUTH_CODE: Ω_ENGINE_SINGULARITY_V100
# =================================================================================
# == THE DAEMON ENGINE (V-Ω-LIFECYCLE-SINGULARITY)                               ==
# =================================================================================
# [PURPOSE]: The Container of the Soul.
#            It manages the loop of existence, the heartbeat of vitality,
#            and the inevitable return to the void.
#
# [ARCHITECTURE]:
# 1. BOOT: Parse Args -> Init Components -> Bind Socket.
# 2. VIGIL: Monitor Parent/Pulse -> Write Heartbeat -> Adjust Sleep.
# 3. DRAIN: Reject New Conns -> Finish Tasks -> Close Socket.
# 4. VOID: Release Resources -> Exit Process.

import sys
import time
import threading
import argparse
import os
import json
import traceback
from enum import Enum, auto
from pathlib import Path
from typing import Optional, Dict, Any

# --- GNOSTIC IMPORTS ---
from ..nexus import GnosticNexus
from ..constants import (
    PROTOCOL_VERSION,
    HEARTBEAT_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_HOST,
    CRASH_DUMP_FILE
)
from .vitality import VitalityMonitor
from .signals import SignalInterceptor
from .banner import proclaim_banner
from ....logger import Scribe

Logger = Scribe("DaemonEngine")


class EngineState(Enum):
    """The Phases of Existence."""
    BOOT = auto()  # Initialization
    VIGIL = auto()  # Running & Monitoring
    DRAINING = auto()  # Shutting down, finishing tasks
    VOID = auto()  # Terminated


class DaemonServer:
    """
    The High-Fidelity Lifecycle Manager.
    Orchestrates the interplay between the Network (Nexus) and the OS (Server).
    """

    def __init__(self, nexus: GnosticNexus, pulse_file: str = None, parent_pid: int = None):
        self.logger = Logger
        self.nexus = nexus
        self._state = EngineState.BOOT
        self._shutdown_event = threading.Event()
        self.vitality = VitalityMonitor(parent_pid, pulse_file)
        self.signals = SignalInterceptor(on_shutdown=self.initiate_shutdown)
        self._start_time = time.time()
        self._tick_count = 0

    def run_forever(self):
        """
        [THE ETERNAL LOOP]
        """
        try:
            # 1. Arm Signals
            self.signals.arm()

            # 2. Ignite Nexus (This prints the Handshake)
            self.nexus.ignite()

            # 3. Transition
            self._state = EngineState.VIGIL

            # [THE FIX]: Don't print banner to STDOUT. Use STDERR.
            # STDOUT is reserved for the Handshake JSON.
            # proclaim_banner is safe (it uses stderr).
            proclaim_banner(self.nexus.port, PROTOCOL_VERSION)

            # Use logger (stderr) for state change
            Logger.system(f"Engine State: [green]{self._state.name}[/green]")

            # 5. Vigil Loop
            self._vigil_loop()

        except KeyboardInterrupt:
            Logger.warn("Manual Interruption Detected.")
            self.initiate_shutdown()

        except Exception as e:
            self._handle_crash(e)

        finally:
            self._finalize_shutdown()

    def initiate_shutdown(self):
        """
        [THE RITE OF CLOSURE]
        Triggers the shutdown sequence. Safe to call from any thread (Signal Handler).
        """
        if self._shutdown_event.is_set():
            return  # Idempotent: Already shutting down

        Logger.system("Shutdown Signal Received. Initiating DRAIN sequence...")
        self._state = EngineState.DRAINING
        self._shutdown_event.set()

    def _vigil_loop(self):
        """
        =============================================================================
        == THE VIGIL OF THE ETERNAL DAEMON (V-Ω-TOTALITY-V20000.12-ISOMORPHIC)     ==
        =============================================================================
        LIF: ∞ | ROLE: VITALITY_GOVERNOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_VIGIL_V20000_ISOMORPHIC_HEARTBEAT_2026_FINALIS
        """
        import time
        import os
        import threading
        import random

        # --- MOVEMENT I: THE SOVEREIGN HANDOVER ---
        # [ASCENSION 1]: Silence the forensic guardians to prevent heartbeat feedback loops.
        try:
            # We reach through the Nexus to the Engine to the active Pipeline.
            engine = getattr(self.nexus, 'engine', None)
            pipeline = getattr(engine, 'pipeline', None)
            if pipeline and hasattr(pipeline, 'muzzle_watchdog'):
                pipeline.muzzle_watchdog()
        except Exception as e:
            self.logger.debug(f"Muzzle Rite deferred: {e}")

        # --- MOVEMENT II: SUBSTRATE-AWARE PRIORITY ---
        # [ASCENSION 2 & 4]: Optimized Priority Inversion.
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        if os.name == 'nt' and not is_wasm:
            try:
                import psutil
                # On Windows, we move the Daemon to IDLE priority.
                # This ensures the Ocular UI and Architect's IDE always have precedence.
                psutil.Process().nice(psutil.IDLE_PRIORITY_CLASS)
                self.logger.verbose("Priority Inversion: Daemon set to IDLE strata.")
            except (ImportError, Exception):
                pass

        self.logger.success(f"The Eternal Vigil is manifest on substrate [{'ETHER' if is_wasm else 'IRON'}].")

        # --- MOVEMENT III: THE METABOLIC RHYTHM ---
        while not self._shutdown_event.is_set():
            loop_start = time.perf_counter()
            self._tick_count += 1

            # 1. VITALITY ADJUDICATION
            # [ASCENSION 8]: The Lazarus check. If the leash is broken, we dissolve.
            try:
                if not self.vitality.check_vitals():
                    self.logger.critical("Vitality Fracture: The Silver Cord has been severed.")
                    self.initiate_shutdown()
                    break
            except Exception as e:
                self.logger.debug(f"Vitality Inquest Paradox: {e}")

            # 2. PRESSURE SENSING (HYDRAULIC GAZE)
            # [ASCENSION 3]: Scry the depth of the Cortex work queue.
            q_size = 0
            try:
                engine = getattr(self.nexus, 'engine', None)
                dispatcher = getattr(engine, 'dispatcher', None)
                # Look for the Cortex worker pool queue size
                pool = getattr(dispatcher, 'cortex_pool', None)
                q_size = pool._work_queue.qsize() if hasattr(pool, '_work_queue') else 0
            except:
                pass

            # 3. ATOMIC PULSE INSCRIPTION
            # [ASCENSION 7]: Enshrine the current state into the Pulse File.
            try:
                self.vitality.write_pulse(metadata={
                    "connections": len(getattr(self.nexus, 'active_connections', [])),
                    "threads": threading.active_count(),
                    "pressure": q_size,
                    "state": self._state.name,
                    "substrate": "ETHER" if is_wasm else "IRON",
                    "uptime": int(time.time() - getattr(self, '_start_time', time.time())),
                    "ticks": self._tick_count
                })
            except Exception as e:
                self.logger.debug(f"Pulse Inscription deferred: {e}")

            # 4. METABOLIC REGULATION (ADAPTIVE SLEEP)
            # Adjust the heartbeat based on system pressure (Queue depth).
            # If the queue is busy (q_size > 0), we pulse faster (Adrenaline).
            base_sleep = 0.5 if q_size > 0 else getattr(self, 'HEARTBEAT_INTERVAL', 3.0)

            # [ASCENSION 6]: Entropy Jitter
            # Prevents synchronous polling collisions with the Frontend.
            jitter = (random.random() - 0.5) * 0.2

            elapsed = time.perf_counter() - loop_start
            # Calculate the drift (How much longer the loop took than expected)
            drift = max(0, elapsed - base_sleep)

            final_sleep = max(0.1, (base_sleep - elapsed) + jitter)

            # [ASCENSION 12]: THE HOLLOW-WAIT
            # Efficient kernel-level wait on the shutdown event.
            if self._shutdown_event.wait(timeout=final_sleep):
                break

            # [ASCENSION 9]: Hydraulic Yield
            if is_wasm:
                # In WASM, we must yield to the JS event loop to process messages.
                time.sleep(0)

        self.logger.system("Vigil Loop Terminated. Reality Dissolving into the Void.")

    def _handle_crash(self, error: Exception):
        """
        [ASCENSION 2]: THE PANIC ROOM
        Dumps forensic data to disk before dying.
        """
        Logger.critical(f"Catastrophic Engine Failure: {error}")

        try:
            dump = {
                "error": str(error),
                "traceback": traceback.format_exc(),
                "timestamp": time.time(),
                "uptime": time.time() - self._start_time,
                "state": self._state.name
            }

            # Attempt to write to project root if known, else CWD
            dump_path = self.nexus.project_root / CRASH_DUMP_FILE if self.nexus.project_root else Path(CRASH_DUMP_FILE)

            with open(dump_path, 'w', encoding='utf-8') as f:
                json.dump(dump, f, indent=2)

            Logger.system(f"Forensic crash dump inscribed to: {dump_path}")

        except Exception as e:
            print(f"Failed to write crash dump: {e}", file=sys.stderr)

        self.initiate_shutdown()

    def _finalize_shutdown(self):
        """
        [THE VOID RITE]
        Clean up resources and exit.
        """
        if self._state == EngineState.VOID:
            return

        self._state = EngineState.VOID
        Logger.system("Finalizing cleanup...")

        # 1. Stop Nexus (Closes Sockets & Thread Pools)
        if self.nexus:
            self.nexus.shutdown()

        # 2. Force Flush Stdout
        sys.stdout.flush()
        sys.stderr.flush()

        Logger.system("Daemon Terminated. Returning to the Void.")

        # [ASCENSION 9]: FORCE EXIT
        # Prevents hanging on non-daemon threads imported by plugins
        os._exit(0)


# =================================================================================
# == THE CLI ENTRY POINT (V-Ω-ARGUMENT-CITADEL)                                  ==
# =================================================================================
def main():
    """
    =================================================================================
    == THE DAEMON ENTRYPOINT (V-Ω-GHOST-BOOT-ASCENSION)                            ==
    =================================================================================
    LIF: INFINITY | ROLE: SOVEREIGN_LIFECYCLE_MANAGER

    [THE STRATEGY]:
    1. PROCLAMATION: Emit AWAKENING signal before any heavy imports.
    2. NANO-PARSING: Use surgical arg-parsing to avoid framework overhead.
    3. LATE-BINDING: Lazy-load GnosticNexus and DaemonServer only when ready to run.
    4. CATASTROPHIC WARD: Bulletproof try/except to handle boot-time fractures.
    =================================================================================
    """
    # --- MOVEMENT I: THE GHOST PROCLAMATION ---
    # This signal instantly informs the CLI that the process is manifest.
    # We use raw sys.stdout.write for absolute speed, bypassing any logger.
    sys.stdout.write("DAEMON_VITALITY:AWAKENING\n")
    sys.stdout.flush()

    # --- MOVEMENT II: SURGICAL ARGUMENT TRIAGE ---
    # We define local constants to avoid importing 'constants.py' too early.
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 5555

    parser = argparse.ArgumentParser(description="Ideabox Quantum Daemon - Sovereign Mode")
    parser.add_argument("--port", type=int, default=int(os.environ.get("SCAFFOLD_PORT", DEFAULT_PORT)))
    parser.add_argument("--host", type=str, default=os.environ.get("SCAFFOLD_HOST", DEFAULT_HOST))
    parser.add_argument("--auth-token", type=str, default=os.environ.get("SCAFFOLD_TOKEN", None))
    parser.add_argument("--parent-pid", type=int, default=None)
    parser.add_argument("--pulse-file", type=str, default=None)
    parser.add_argument("--allow-remote", action="store_true")

    # Use parse_known_args to ensure we don't crash on future flags passed by the CLI shims
    args, unknown = parser.parse_known_args()

    # --- MOVEMENT III: LATE-BOUND INCEPTION (THE HEAVY LIFT) ---
    try:
        # ONLY NOW do we enter the heavy Gnostic namespaces.
        # This is where the ~8-10 second delay usually lives.
        # Because we already said "AWAKENING", the CLI is now in "Wait for Port" mode.
        from ..nexus import GnosticNexus
        from .engine import DaemonServer
        from ....logger import Scribe

        Logger = Scribe("DaemonBoot")

        if unknown and os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
            Logger.warn(f"Ghost-Boot absorbed unknown coordinates: {unknown}")

        # --- MOVEMENT IV: MATERIALIZING THE NEXUS ---
        # The Nexus __init__ is now optimized to be a hollow shell.
        nexus = GnosticNexus(
            host="0.0.0.0" if args.allow_remote else args.host,
            port=args.port,
            auth_token=args.auth_token,
            parent_pid=args.parent_pid,
            pulse_file=args.pulse_file
        )

        # --- MOVEMENT V: FORGING THE SERVER ---
        server = DaemonServer(
            nexus=nexus,
            pulse_file=args.pulse_file,
            parent_pid=args.parent_pid
        )

        # --- MOVEMENT VI: THE ETERNAL VIGIL ---
        # run_forever() will eventually call nexus.ignite()
        server.run_forever()

    except Exception as e:
        # The Final Ward: If the heavy imports fail, we must proclaim the fracture.
        sys.stderr.write(f"\n[CATASTROPHIC BOOT FRACTURE] Reality collapsed: {e}\n")
        traceback.print_exc(file=sys.stderr)

        # If we failed before the logger existed, we use raw exit.
        # If we can, we log to the crash dump.
        try:
            from ..constants import CRASH_DUMP_FILE
            dump_path = os.path.join(".scaffold", "daemon_boot_crash.json")
            with open(dump_path, 'w') as f:
                import json
                json.dump({"error": str(e), "traceback": traceback.format_exc(), "time": time.time()}, f)
        except:
            pass

        sys.exit(1)


if __name__ == "__main__":
    main()