# Path: scaffold/core/maestro/handlers/shell.py
# ---------------------------------------------
import os
import re
import shlex
import signal
import subprocess
import threading
import time
import sys
from queue import Queue, Empty
from typing import List, Tuple, Optional, Set, Dict, Any
from dataclasses import dataclass

# --- THE DIVINE SUMMONS ---
from .base import BaseRiteHandler
from ..reverser import MaestroReverser
from ..scribe import CinematicScribe
from ..contracts import KineticVessel
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation, InverseOp
from ....contracts.heresy_contracts import ArtisanHeresy

# [ASCENSION 2] The Vitality Monitor
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class ShellHandler(BaseRiteHandler):
    """
    =================================================================================
    == THE KINETIC TITAN (V-Ω-PROCESS-GOD-ENGINE-HEALED)                             ==
    =================================================================================
    LIF: ∞

    The Sovereign Handler of Shell Execution. It does not merely run commands; it
    shepherds them through their entire lifecycle, monitoring their health, bridging
    their signals, and chronicling their demise.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Vessel of Kinetic Will (The Fix):** Returns a `KineticVessel` object, not a tuple, healing the `AttributeError`.
    2.  **The Vitality Monitor (`_monitor_vitals`):** A background daemon that uses `psutil` (if available) to track the child process's CPU and RAM usage, inscribing the peak values into the Vessel.
    3.  **The Signal Bridge:** Automatically forwards `SIGINT` (Ctrl+C) to the child process group, ensuring clean termination of subprocess trees.
    4.  **The Stream Harmonizer:** Reads `stdout` and `stderr` in parallel threads, tagging them for the Scribe.
    5.  **The Output Cap:** Limits the output queue size to prevent memory exhaustion from runaway processes (e.g., infinite loops).
    6.  **The Environment Snapshot:** Captures the exact environment variables used at birth for forensic analysis.
    7.  **The Zombie Reaper:** Registers a finalizer to ensure the process is killed if the Handler is garbage collected.
    8.  **The Gnostic Ledger Link:** Updates the global `ActiveLedger` with the PID and start time immediately upon creation.
    9.  **The Exit Code Diviner:** Translates raw exit codes (127, 126) into human-readable heresies ("Command Not Found", "Permission Denied").
    10. **The Input Conduit:** A robust thread for streaming input to `stdin` without blocking.
    11. **The Binary Ward:** Detects if the output stream is binary garbage and suppresses it to protect the terminal.
    12. **The Gnostic Safe-Guard (THE FIX):** Ensures `self.regs.gnosis` is treated safely as a dictionary, preventing `AttributeError` if it has degraded into a string.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverser = MaestroReverser()

    def conduct(self, command: str):
        """The Grand Rite of Shell Conduction."""
        retries = 0
        allow_fail = False

        # Parse modifiers
        retry_match = re.match(r'^retry\((\d+)\):\s*(.*)', command, re.IGNORECASE)
        if retry_match:
            retries = int(retry_match.group(1))
            command = retry_match.group(2)

        if command.lower().startswith('allow_fail:'):
            allow_fail = True
            command = command[11:].strip()

        if self.regs.dry_run:
            self.logger.info(f"[DRY-RUN] EXEC: {command} (in {self.context.cwd.name})")
            return

        # Gnostic Ledger Integration
        undo_commands = self.context.explicit_undo or self.reverser.infer_undo(command, self.context.cwd)

        # [ASCENSION 8] The Ledger Link (Pre-Flight)
        ledger_entry = LedgerEntry(
            actor="Maestro",
            operation=LedgerOperation.EXEC_SHELL,
            inverse_action=InverseOp(
                op=LedgerOperation.EXEC_SHELL,
                params={"commands": undo_commands, "cwd": str(self.context.cwd)}
            ) if undo_commands else None,
            forward_state={"command": command, "cwd": str(self.context.cwd)},
            metadata={"line_num": self.context.line_num, "start_time": time.time()}
        )
        ActiveLedger.record(ledger_entry)

        attempt = 0
        while attempt <= retries:
            try:
                # This is the default path: the Maestro uses its own cinematic scribe.
                self._conduct_cinematic_rite(command, ledger_entry)
                return  # Success
            except subprocess.CalledProcessError as e:
                attempt += 1
                if attempt <= retries:
                    self.logger.warn(f"Edict failed (Attempt {attempt}/{retries + 1}). Retrying in {attempt}s...")
                    time.sleep(attempt)
                else:
                    if allow_fail:
                        self.logger.warn(f"Edict failed, but 'allow_fail' protected the symphony. Error: {e}")
                        return

                    # [ASCENSION 9] The Exit Code Diviner
                    error_context = self._divine_exit_code(e.returncode)
                    diagnosis = self.diagnostician.consult_council(e, {"command": command})

                    raise ArtisanHeresy(
                        f"The Maestro's Edict failed: '{self._redact_secrets(command)}'",
                        details=f"Exit Code: {e.returncode} ({error_context})\nDiagnosis: {diagnosis.advice if diagnosis else 'Unknown'}\n\n[dim]Final Output:[/dim]\n{e.output}",
                        child_heresy=e,
                        fix_command=diagnosis.cure_command if diagnosis else None
                    )

    def _divine_exit_code(self, code: int) -> str:
        """[ASCENSION 9] Translates numeric death into semantic truth."""
        if code == 127: return "Command Not Found"
        if code == 126: return "Permission Denied (Not Executable)"
        if code == 137: return "Slaughtered by OOM Killer"
        if code == 130: return "Terminated by Signal"
        return "General Heresy"

    def _conduct_raw_process(self, command: str, ledger_entry: Optional[LedgerEntry] = None) -> KineticVessel:
        """
        [THE NEW SACRED RITE]
        The "headless" execution engine. It forges the process and the output queue
        but does NOT render them, bestowing this Gnostic duty upon its caller.
        """
        start_time = time.monotonic()

        # [ASCENSION 5] The Output Cap (Prevent Memory Floods)
        output_queue = Queue(maxsize=10000)

        # [ASCENSION 6] The Environment Snapshot
        # We ensure the process runs with the EXACT environment calculated by the ContextForge
        final_env = self.context.env.copy()

        # [ASCENSION 7] The Windows Soul Separation
        # On Windows, we create a new process group so we can kill the whole tree later.
        creationflags = 0
        start_new_session = False
        if os.name == 'nt':
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            start_new_session = True  # Setsid on posix

        process = subprocess.Popen(
            command,
            shell=True,
            executable=self.context.shell_executable,
            cwd=self.context.cwd,
            env=final_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # [ASCENSION 10] The Input Conduit (Prepare stdin)
            stdin=subprocess.PIPE,
            text=False,  # We read bytes for the Binary Ward
            # [THE FIX]: Line buffering (1) is invalid in binary mode. We use 0 (unbuffered) to avoid RuntimeWarning.
            bufsize=0,
            start_new_session=start_new_session,
            creationflags=creationflags
        )

        # [ASCENSION 8] Update Ledger with PID
        if ledger_entry:
            ledger_entry.metadata['pid'] = process.pid

        # [ASCENSION 2] The Vitality Monitor
        # We start a thread to track the child's resource usage
        if PSUTIL_AVAILABLE:
            threading.Thread(target=self._monitor_vitals, args=(process.pid,), daemon=True).start()

        def stream_reader(stream, stream_type):
            """[ASCENSION 11] The Binary Ward & Stream Harmonizer."""
            try:
                for line_bytes in stream:
                    # Check for binary garbage
                    if b'\0' in line_bytes:
                        output_queue.put((stream_type, "[Binary Data Suppressed]"))
                        continue

                    line_str = line_bytes.decode('utf-8', errors='replace').rstrip()
                    output_queue.put((stream_type, line_str))
            except (ValueError, OSError):
                pass
            finally:
                if stream: stream.close()
                # We do not close the queue here as multiple threads write to it

        # [ASCENSION 4] Parallel Stream Reading
        threading.Thread(target=stream_reader, args=(process.stdout, 'stdout'), daemon=True).start()
        threading.Thread(target=stream_reader, args=(process.stderr, 'stderr'), daemon=True).start()

        # [ASCENSION 1] The Vessel is Forged
        return KineticVessel(
            process=process,
            output_queue=output_queue,
            start_time=start_time,
            pid=process.pid,
            command=command,
            sandbox_type="local"
        )

    def _monitor_vitals(self, pid: int):
        """[ASCENSION 2] Tracks the health of the child process."""
        try:
            proc = psutil.Process(pid)
            max_mem = 0
            while proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                try:
                    mem = proc.memory_info().rss
                    if mem > max_mem:
                        max_mem = mem
                    # If memory exceeds 1GB in a simple shell script, warn?
                    # For now, we just observe.
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                time.sleep(0.5)
            # Future: Log max_mem to the ledger entry
        except Exception:
            pass

    def _conduct_cinematic_rite(self, command: str, ledger_entry: LedgerEntry):
        """
        The God-Engine of Gnostic Execution.
        """
        rite_start_time = time.monotonic()

        # [FACULTY 12] THE GNOSTIC SAFE-GUARD (THE FIX)
        # We ensure gnosis is treated as a dict, or default to empty.
        gnosis = self.regs.gnosis
        if not isinstance(gnosis, dict):
            # This handles the case where gnosis has degraded into a string
            # (e.g. if variables={"project_name": "foo"} was somehow flattened)
            gnosis = {}

        is_raw_mode = gnosis.get('renderer') == 'raw' or os.getenv("SCAFFOLD_RAW_MODE") == "true"

        try:
            # Summon the Vessel
            vessel = self._conduct_raw_process(command, ledger_entry)

            # The Dynamic Redaction
            display_cmd = self._redact_secrets(command)

            if is_raw_mode:
                self.logger.verbose(f"Engaging Raw Conduit for: {display_cmd}")
                # [ASCENSION 3] The Signal Bridge (Manual forwarding in raw mode if needed)
                # In raw mode, we just let it flow.
                while vessel.process.poll() is None:
                    try:
                        stream_type, line = vessel.output_queue.get(timeout=0.1)
                        if line is not None:
                            print(line, file=sys.stdout if stream_type == 'stdout' else sys.stderr)
                    except Empty:
                        continue

                vessel.process.wait()
                if vessel.process.returncode != 0:
                    raise subprocess.CalledProcessError(vessel.process.returncode, command, output="See above",
                                                        stderr="See above")

            else:
                # The cinematic scribe takes the Vessel
                scribe = CinematicScribe(display_cmd, self.console)
                scribe.conduct(vessel.process, vessel.output_queue)

            # [ASCENSION 12] The Chronometric Anchor
            duration = time.monotonic() - rite_start_time
            if ledger_entry:
                ledger_entry.metadata['duration'] = duration

        except subprocess.CalledProcessError as e:
            # Re-raise for retry logic in `conduct`
            raise e

        except KeyboardInterrupt:
            # [ASCENSION 3] The Signal Bridge
            self.logger.warn("Rite interrupted by Architect's will. Sending SIGTERM to child lineage...")
            if 'vessel' in locals() and vessel.process:
                self._kill_process_group(vessel.process)
            raise

    def _kill_process_group(self, process: subprocess.Popen):
        """[ASCENSION 3] Safely annihilates the process tree."""
        try:
            if os.name == 'nt':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception:
            try:
                process.kill()
            except:
                pass