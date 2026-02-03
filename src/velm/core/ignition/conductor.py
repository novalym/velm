# Path: scaffold/core/ignition/conductor.py
# ------------------------------------------
# LIF: 10,000,000,000,000 // AUTH_CODE: Ω_IGNITION_CONDUCTOR_V1
# SYSTEM: IDEABOX QUANTUM // ROLE: KINETIC EXECUTION

import os
import sys
import subprocess
import threading
import time
import signal
import psutil
from pathlib import Path
from typing import Dict, Optional, List, Callable, Any

from .contracts import ExecutionPlan, VitalityState
from .sentinel.priest import ToolchainSentinel
from ...logger import Scribe

Logger = Scribe("IgnitionConductor")


class IgnitionConductor:
    """
    =================================================================================
    == THE IGNITION CONDUCTOR (V-Ω-TOTALITY)                                       ==
    =================================================================================
    The Sovereign Hand of Action.

    Orchestrates the transition from static code to a living, breathing process.
    Responsible for Process Lifecycle, Telemetry, and Graceful Banishment.
    """

    def __init__(self):
        self._active_processes: Dict[str, subprocess.Popen] = {}
        self._lock = threading.Lock()

    def ignite(self,
               plan: ExecutionPlan,
               on_log: Optional[Callable[[str, str], None]] = None,
               on_fracture: Optional[Callable[[int, str], None]] = None) -> int:
        """
        [ASCENSION 1]: The Rite of Ignition.
        Manifests the ExecutionPlan in the Operating System.
        """
        plan_id = plan.merkle_seal

        with self._lock:
            if plan_id in self._active_processes:
                Logger.warn(f"Singularity Conflict: Process {plan_id} already manifest. Banish old soul first.")
                self.banish(plan_id)

        # 1. BIOLOGICAL READINESS CHECK (The Shield)
        if plan.support and not plan.support.is_installed:
            raise RuntimeError(f"Biological Fracture: {plan.support.manifest_type} dependencies missing.")

        # 2. PREPARE KINETIC ENVIRONMENT
        # [ASCENSION 8]: DNA Grafting
        env = os.environ.copy()
        env.update(plan.env)

        # Inject Sentinel-verified paths
        if plan.support:
            # Add venv/bin or node_modules/.bin to PATH
            pass

            # 3. KINETIC SPAWN
        # [ASCENSION 2]: Group Isolation
        creation_flags = 0
        if os.name == 'nt':
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP

        Logger.info(f"Igniting Reality: [bold cyan]{plan.aura.value}[/bold cyan] via {' '.join(plan.command)}")

        try:
            proc = subprocess.Popen(
                plan.command,
                cwd=plan.cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                creationflags=creation_flags,
                start_new_session=True if os.name != 'nt' else False
            )

            self._active_processes[plan_id] = proc

            # 4. AWAKEN TELEMETRIC SCRIBES
            # [ASCENSION 4]: Splicer Threads
            threading.Thread(target=self._scribe_stream, args=(proc.stdout, "STDOUT", on_log), daemon=True).start()
            threading.Thread(target=self._scribe_stream, args=(proc.stderr, "STDERR", on_log), daemon=True).start()

            # 5. ENGAGE VITALITY VIGIL
            threading.Thread(target=self._vigil_loop, args=(plan_id, proc, on_fracture), daemon=True).start()

            return proc.pid

        except Exception as e:
            Logger.critical(f"Ignition Fracture: {str(e)}")
            raise

    def banish(self, plan_id: str):
        """
        [ASCENSION 6]: Graceful Banishment.
        Returns the process and all its children to the void.
        """
        with self._lock:
            proc = self._active_processes.get(plan_id)
            if not proc: return

            Logger.info(f"Banishing Process Soul: {plan_id} (PID: {proc.pid})")

            try:
                parent = psutil.Process(proc.pid)
                children = parent.children(recursive=True)

                # 1. Soft Banish (Terminate)
                for child in children: child.terminate()
                parent.terminate()

                # 2. Wait for dissolution
                _, alive = psutil.wait_procs(children + [parent], timeout=3)

                # 3. Hard Banish (Kill)
                for survivor in alive:
                    survivor.kill()

            except psutil.NoSuchProcess:
                pass
            finally:
                self._active_processes.pop(plan_id, None)

    def _scribe_stream(self, stream, name: str, callback: Optional[Callable]):
        """[ASCENSION 4]: Telemetric Stream Splicer."""
        for line in iter(stream.readline, ''):
            clean_line = line.strip()
            if clean_line:
                if callback: callback(name, clean_line)
                # Also log to global scribe
                Logger.verbose(f"[{name}] {clean_line}")
        stream.close()

    def _vigil_loop(self, plan_id: str, proc: subprocess.Popen, on_fracture: Optional[Callable]):
        """[ASCENSION 3]: Vitality Heartbeat Monitoring."""
        exit_code = proc.wait()

        with self._lock:
            if plan_id in self._active_processes:
                self._active_processes.pop(plan_id)
                Logger.error(f"Reality Fractured: Process {plan_id} exited with code {exit_code}")
                if on_fracture:
                    on_fracture(exit_code, "Unexpected Departure")

    def get_status(self, plan_id: str) -> VitalityState:
        """[ASCENSION 8]: Lifecycle Oracle Query."""
        with self._lock:
            proc = self._active_processes.get(plan_id)
            if not proc: return VitalityState.DORMANT

            if proc.poll() is not None:
                return VitalityState.FRACTURED

            return VitalityState.ONLINE


# [ASCENSION 12]: SOVEREIGN INSTANCE
Conductor = IgnitionConductor()