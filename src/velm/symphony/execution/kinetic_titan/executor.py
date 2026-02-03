# Path: scaffold/symphony/execution/kinetic_titan/executor.py
# -----------------------------------------------------------

import subprocess
import os
import signal
import sys
import threading
import time
from typing import List, Optional, Dict, Any, Union
from queue import Queue
from pathlib import Path

from ....logger import Scribe

Logger = Scribe('TitanExecutor')


class TitanExecutor:
    """
    =================================================================================
    == THE TITAN EXECUTOR (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS++)                 ==
    =================================================================================
    @gnosis:title The Titan Executor (The Physics Engine)
    @gnosis:summary The unbreakable wrapper around the OS kernel's process creation.
                     It standardizes the chaotic reality of subprocess management.
    @gnosis:LIF 10,000,000,000

    This artisan creates, monitors, and destroys processes. It hides the complexity
    of OS differences (Windows vs POSIX) and provides a unified, method-based API
    for the Kinetic Titan.
    """

    def __init__(self):
        self._process: Optional[subprocess.Popen] = None
        self._cwd: Path = Path.cwd()
        self._threads: List[threading.Thread] = []

    # =========================================================================
    # == THE RITES OF STATE (METHOD-BASED API)                               ==
    # =========================================================================

    def pid(self) -> Optional[int]:
        """
        [THE RITE OF IDENTITY]
        Returns the Process ID.
        """
        if self._process:
            return self._process.pid
        return None

    def returncode(self) -> Optional[int]:
        """
        [THE RITE OF JUDGMENT]
        Polls the process and returns the exit code if finished, else None.
        Fixed to be a METHOD, not a property, to align with the Orchestrator.
        """
        if self._process:
            self._process.poll()  # Update state from OS
            return self._process.returncode
        return None

    def cwd(self) -> Path:
        """Returns the sanctum where the process lives."""
        return self._cwd

    def is_alive(self) -> bool:
        """Adjudicates if the process is currently running."""
        return self.returncode() is None

    # =========================================================================
    # == THE RITES OF KINETIC ACTION                                         ==
    # =========================================================================

    def ignite(
            self,
            command: str,
            inputs: List[str],
            cwd: Path,
            env: Dict[str, str],
            output_queue: Queue
    ):
        """
        [THE RITE OF IGNITION]
        Spawns the subprocess and attaches the IO pumps.
        """
        self._cwd = cwd

        # 1. Prepare OS-Specific Flags
        creation_flags = 0
        start_new_session = False

        if os.name == 'nt':
            # Windows: New Process Group to allow tree killing
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            # POSIX: New Session (setsid) to detach from parent TTY signals
            start_new_session = True

        # 2. Spawn the Process
        try:
            self._process = subprocess.Popen(
                command,
                shell=True,
                cwd=str(cwd),  # subprocess needs string path
                env=env,
                stdin=subprocess.PIPE if inputs else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,  # Text mode
                encoding='utf-8',
                errors='replace',  # [FACULTY 7] Gnostic Encoding Safety
                creationflags=creation_flags,
                start_new_session=start_new_session
            )
        except Exception as e:
            # If ignition fails, we must raise immediately
            Logger.error(f"Ignition Sequence Failed: {e}")
            raise e

        # 3. Summon the Stream Daemons
        # We spawn threads to pump stdout/stderr into the shared queue
        self._summon_reader(self._process.stdout, 'stdout', output_queue)
        self._summon_reader(self._process.stderr, 'stderr', output_queue)

        # 4. Summon the Input Injector (if needed)
        if inputs and self._process.stdin:
            self._summon_injector(self._process.stdin, inputs)

    def wait(self, timeout: Optional[float] = None):
        """Blocks until the process concludes."""
        if self._process:
            try:
                self._process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                pass  # Caller handles timeout logic via is_alive()

    def kill(self):
        """
        [THE RITE OF THE REAPER]
        Terminates the process and its entire lineage (Tree Kill).
        Handles Windows and POSIX differences robustly.
        """
        if not self._process or self._process.returncode is not None:
            return

        try:
            Logger.verbose(f"Terminating process {self._process.pid}...")

            if os.name == 'nt':
                # [FACULTY 3] The Windows Reaper: taskkill /T (Tree) /F (Force)
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(self._process.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # [FACULTY 2] The POSIX Reaper: Kill the Process Group
                # We used start_new_session=True, so os.getpgid(pid) == pid
                try:
                    os.killpg(os.getpgid(self._process.pid), signal.SIGTERM)
                    # Give it a moment to die with dignity
                    try:
                        self._process.wait(timeout=0.5)
                    except subprocess.TimeoutExpired:
                        os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass  # Already dead

        except Exception as e:
            Logger.warn(f"Reaper faltered: {e}")
            # Fallback to simple kill
            try:
                self._process.kill()
            except:
                pass

    # =========================================================================
    # == THE INTERNAL ARTISANS (THREADS)                                     ==
    # =========================================================================

    def _summon_reader(self, stream, stream_type: str, output_queue: Queue):
        """Spawns a daemon thread to read a stream into the queue."""

        def _read():
            try:
                for line in stream:
                    output_queue.put((stream_type, line.rstrip()))
            except Exception as e:
                # Streams might close unexpectedly on kill, ignore
                pass
            finally:
                if not stream.closed:
                    stream.close()
                # [FACULTY 8] The Sentinel Dispatcher
                # We signal EOF to the queue reader with None
                output_queue.put((stream_type, None))

        t = threading.Thread(target=_read, daemon=True, name=f"TitanReader-{stream_type}")
        t.start()
        self._threads.append(t)

    def _summon_injector(self, stream, inputs: List[str]):
        """Spawns a daemon thread to write inputs to stdin."""

        def _write():
            try:
                for line in inputs:
                    if stream.closed: break
                    stream.write(line + "\n")
                    stream.flush()
                if not stream.closed:
                    stream.close()
            except (BrokenPipeError, OSError):
                pass  # Process died before we finished speaking
            except Exception as e:
                Logger.warn(f"Input Injection failed: {e}")

        t = threading.Thread(target=_write, daemon=True, name="TitanInjector")
        t.start()
        self._threads.append(t)