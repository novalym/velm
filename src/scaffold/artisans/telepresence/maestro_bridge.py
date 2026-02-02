# Path: scaffold/artisans/telepresence/maestro_bridge.py
# ----------------------------------------------------
import os
import sys
import subprocess
import threading
import shlex
import time
import signal
from queue import Queue, Empty
from typing import Dict, Any, List, Optional
from pathlib import Path

from ...logger import Scribe
from ...core.maestro.contracts import KineticVessel
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("MaestroBridge")


class MaestroBridge:
    """
    =================================================================================
    == THE KINETIC BRIDGE (V-Ω-REMOTE-EXECUTION-CONDUCTOR-ULTIMA)                  ==
    =================================================================================
    LIF: INFINITY | AUTH_CODE: ()#@()#@)

    The "Sword" of the Telepresence subsystem. It conducts the Architect's Will
    across the Gnostic Wormhole, providing real-time process entanglement.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self._active_processes: Dict[int, subprocess.Popen] = {}
        self._lock = threading.RLock()

    def conduct_remote_edict(self, command: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        [THE RITE OF KINETIC PROJECTION]
        Forges a live process on the server and streams its soul back to the IDE.
        """
        start_time = time.monotonic()

        # 1. Forge the Gnostic Environment
        # We project the Architect's variables into the remote shell's blood.
        final_env = os.environ.copy()
        for k, v in variables.items():
            if isinstance(v, (str, int, bool)):
                safe_key = f"SC_{str(k).upper()}"
                final_env[safe_key] = str(v)

        final_env["SCAFFOLD_REMOTE_CONDUCT"] = "true"
        final_env["PYTHONUNBUFFERED"] = "1"

        Logger.info(f"Conducting Remote Edict: [yellow]{command}[/yellow]")

        try:
            # 2. Summon the Process (The Birth of Kinetic Will)
            # We start a new session (setsid) to ensure we can kill the whole tree later.
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=self.root,
                env=final_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                start_new_session=True if os.name != 'nt' else False
            )

            with self._lock:
                self._active_processes[process.pid] = process

            # 3. Attach the Nervous System (Streaming Threads)
            output_queue = Queue()

            # [FACULTY 1]: Asynchronous Stream Harmonization
            def stream_reader(pipe, label):
                try:
                    for line in iter(pipe.readline, ''):
                        if line:
                            # [FACULTY 2]: Telemetry Injection
                            # If the output contains common progress markers, tag it.
                            is_progress = any(m in line for m in ['%', '...', 'MB/s', 'Step'])
                            output_queue.put({
                                "type": "log",
                                "stream": label,
                                "content": line.rstrip(),
                                "is_progress": is_progress
                            })
                finally:
                    pipe.close()

            threading.Thread(target=stream_reader, args=(process.stdout, 'stdout'), daemon=True).start()
            threading.Thread(target=stream_reader, args=(process.stderr, 'stderr'), daemon=True).start()

            # 4. The Eternal Vigil (Consumption Loop)
            # This loop runs within the Daemon, pushing notifications to VS Code.
            full_stdout = []
            full_stderr = []

            while process.poll() is None or not output_queue.empty():
                try:
                    msg = output_queue.get(timeout=0.1)
                    if msg['stream'] == 'stdout':
                        full_stdout.append(msg['content'])
                    else:
                        full_stderr.append(msg['content'])

                    # [NERVOUS SYSTEM BROADCAST]
                    # This sends the line directly to the VS Code Output Channel/Terminal
                    Logger.info(msg['content'], tags=["NEURAL_LINK", "PROGRESS" if msg['is_progress'] else "KINETIC"],
                                extra_payload={
                                    "method": "scaffold/remoteOutput",
                                    "params": msg
                                })
                except Empty:
                    continue

            # 5. Final Adjudication
            exit_code = process.wait()
            duration = time.monotonic() - start_time

            with self._lock:
                self._active_processes.pop(process.pid, None)

            # [FACULTY 12]: Forensic Exit Adjudication
            if exit_code != 0:
                Logger.warn(f"Remote Edict failed (Exit: {exit_code}) in {duration:.2f}s")
            else:
                Logger.success(f"Remote Edict succeeded in {duration:.2f}s")

            return {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "duration_ms": int(duration * 1000),
                "pid": process.pid
            }

        except Exception as e:
            Logger.error(f"Kinetic Paradox: {e}")
            return {"success": False, "error": str(e)}

    def kill_all_rites(self):
        """
        =============================================================================
        == THE RITE OF PURIFICATION (THE ORPHAN REAPER)                           ==
        =============================================================================
        Surgically annihilates all active remote process trees.
        """
        with self._lock:
            if not self._active_processes:
                return

            Logger.warn(f"Annihilating {len(self._active_processes)} active remote rites...")

            for pid, proc in self._active_processes.items():
                try:
                    if os.name == 'nt':
                        subprocess.call(['taskkill', '/F', '/T', '/PID', str(pid)])
                    else:
                        # Kill the entire process group (negative PID)
                        os.killpg(os.getpgid(pid), signal.SIGTERM)
                except:
                    proc.kill()

            self._active_processes.clear()

    def send_input(self, pid: int, data: str):
        """
        [FACULTY 5]: Interactive Inquest.
        Injects data into a running process's stdin.
        """
        with self._lock:
            proc = self._active_processes.get(pid)
            if proc and proc.stdin:
                try:
                    proc.stdin.write(data + '\n')
                    proc.stdin.flush()
                    Logger.verbose(f"Stdin Injected into PID {pid}: {data}")
                except Exception as e:
                    Logger.warn(f"Failed to inject stdin: {e}")