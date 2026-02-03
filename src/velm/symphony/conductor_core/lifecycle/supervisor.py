# Path: scaffold/symphony/conductor_core/lifecycle/supervisor.py
# --------------------------------------------------------------

import io
import os
import signal
import subprocess
import threading
import time
from typing import Optional, TYPE_CHECKING

from .contracts import ServiceConfig, ServiceState
from ....logger import Scribe

if TYPE_CHECKING:
    from .manager import SymphonyLifecycleManager


class ServiceSupervisor(threading.Thread):
    """
    =================================================================================
    == THE GNOSTIC SUPERVISOR (V-Ω-SELF-HEALING-DAEMON)                            ==
    =================================================================================
    LIF: 10,000,000,000

    A sentient thread that watches over a single subprocess.
    It possesses the faculties of:
    1.  **The Phoenix Protocol:** Automatically resurrects the process if it crashes,
        respecting the `restart_policy`.
    2.  **The Vitality Gaze:** Periodically executes a `healthcheck_cmd` to verify
        internal consistency, not just process existence.
    3.  **The Log Scribe:** Redirects stdout/stderr to a dedicated file in `.scaffold/logs`.
    4.  **The Graceful Reaper:** Uses Process Groups (`setsid`) to ensure no child
        process is left orphaned when the supervisor terminates.
    """

    def __init__(self, config: ServiceConfig, manager: 'SymphonyLifecycleManager'):
        super().__init__(daemon=True, name=f"Supervisor-{config.name}")
        self.config = config
        self.manager = manager
        self.process: Optional[subprocess.Popen] = None
        self.state = ServiceState.PENDING
        self._stop_event = threading.Event()
        self.log_file_handle: Optional[io.TextIOWrapper] = None
        self.scribe = Scribe(f"Service:{config.name}")
        self._pid: Optional[int] = None

    def run(self):
        """The Eternal Vigil."""
        self.scribe.info(f"Awakening supervisor. Command: {self.config.command}")
        self._ignite()

        while not self._stop_event.is_set():
            if self._stop_event.wait(timeout=2.0):  # Heartbeat interval
                break
            self._tick()

        self._terminate()

    def stop(self):
        """Commands the supervisor to end its vigil."""
        self._stop_event.set()

    def _ignite(self):
        """The Rite of First Breath."""
        self._update_state(ServiceState.STARTING)
        self._spawn_process()
        # Grace period for startup
        if not self._stop_event.is_set():
            time.sleep(self.config.initial_delay_s)

    def _spawn_process(self):
        """Materializes the subprocess."""
        try:
            # 1. Forge Log Sanctum
            log_dir = self.manager.conductor.execution_root / ".scaffold" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"{self.config.name}.log"

            # Open in append mode to preserve history across restarts
            self.log_file_handle = open(log_path, 'a', encoding='utf-8')
            self.log_file_handle.write(f"\n--- [GNOSTIC RESTART] {time.ctime()} ---\n")
            self.log_file_handle.flush()

            # 2. Prepare Environment
            env = os.environ.copy()
            env.update(self.config.env)

            # 3. Spawn (Process Group Leader)
            # On Unix, setsid ensures we can kill the whole tree.
            preexec = os.setsid if os.name != 'nt' else None

            self.process = subprocess.Popen(
                self.config.command,
                shell=True,
                cwd=self.config.cwd,
                stdout=self.log_file_handle,
                stderr=subprocess.STDOUT,
                env=env,
                preexec_fn=preexec,
                # On Windows, we might use creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            self._pid = self.process.pid

            # Register PID with the Admiral for global cleanup safety
            self.manager.register_pid(self._pid)

            self._update_state(ServiceState.RUNNING)
            self.scribe.success(f"Spawned with PID [green]{self._pid}[/green].")

        except Exception as e:
            self.scribe.error(f"Failed to spawn: {e}", exc_info=True)
            self._update_state(ServiceState.CRASHED)

    def _tick(self):
        """The Heartbeat Check."""
        # 1. Check Process Vitality
        if not self.process:
            return

        return_code = self.process.poll()
        if return_code is not None:
            self.scribe.warn(f"Process exited with code {return_code}.")
            self._handle_exit(return_code)
            return

        # 2. Check Semantic Health
        self._perform_healthcheck()

    def _handle_exit(self, code: int):
        """Decides whether to resurrect or mourn."""
        self._update_state(ServiceState.CRASHED if code != 0 else ServiceState.STOPPED)

        should_restart = False
        if self.config.restart_policy == "always":
            should_restart = True
        elif self.config.restart_policy == "on-failure" and code != 0:
            should_restart = True

        if should_restart and not self._stop_event.is_set():
            self.scribe.info("Phoenix Protocol Initiated: Resurrecting...")
            self._update_state(ServiceState.RESTARTING)
            time.sleep(1)  # Backoff
            self._spawn_process()
        else:
            self.scribe.info("Service has finished. Supervisor entering dormancy.")
            self.stop()

    def _perform_healthcheck(self):
        """Queries the service to see if it is truly alive."""
        if not self.config.healthcheck_cmd:
            # If running and no check, assume healthy
            if self.state == ServiceState.RUNNING:
                self._update_state(ServiceState.HEALTHY)
            return

        try:
            # We run the check with a strict timeout
            res = subprocess.run(
                self.config.healthcheck_cmd,
                shell=True,
                timeout=5,
                cwd=self.config.cwd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if res.returncode == 0:
                self._update_state(ServiceState.HEALTHY)
            else:
                self._update_state(ServiceState.UNHEALTHY)
        except subprocess.TimeoutExpired:
            self.scribe.warn("Healthcheck timed out.")
            self._update_state(ServiceState.UNHEALTHY)
        except Exception as e:
            self.scribe.warn(f"Healthcheck failed: {e}")
            self._update_state(ServiceState.UNHEALTHY)

    def _terminate(self):
        """The Rite of Clean Death."""
        if self.process and self.process.poll() is None:
            self.scribe.info("Sending termination signal...")
            try:
                # UNIX: Kill the process group
                if os.name != 'nt':
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                else:
                    self.process.terminate()

                # Wait for grace
                try:
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.scribe.warn("Process resisted. Sending SIGKILL.")
                    if os.name != 'nt':
                        os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                    else:
                        self.process.kill()
            except Exception as e:
                self.scribe.error(f"Termination error: {e}")

        self._update_state(ServiceState.STOPPED)

        if self.log_file_handle:
            try:
                self.log_file_handle.close()
            except:
                pass

    def _update_state(self, new_state: ServiceState):
        if self.state != new_state:
            self.state = new_state
            self.manager.broadcast_state(self.config.name, new_state)