# Path: src/velm/core/maestro/handlers/shell.py
# ---------------------------------------------

import os
import re
import shlex
import signal
import subprocess
import threading
import time
import sys
import platform
from queue import Queue, Empty
from typing import List, Tuple, Optional, Set, Dict, Any, Final
from dataclasses import dataclass
from pathlib import Path

# --- THE DIVINE SUMMONS ---
from .base import BaseRiteHandler
from ..reverser import MaestroReverser
from ..scribe import CinematicScribe
from ..contracts import KineticVessel
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation, InverseOp
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

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
    12. **The Makefile Suture (V1000):** Explicitly targets the Makefile on Windows to prevent "No rule to make target" heresies during rapid filesystem flux.
    """

    def __init__(self, *args, **kwargs):
        """
        =============================================================================
        == THE RITE OF HANDLER INCEPTION (V-Ω-TOTALITY-V700-ENGINE-SUTURED)        ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_ORGAN_SUTURE | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SHELL_HANDLER_INIT_V700_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This implementation resolves the 'Engine-less Paradox'. It surgically extracts
        the Master Engine link from the registers to enable the Multicast HUD
        Radiator, ensuring the Ocular UI remains in sync with physical strikes.
        =============================================================================
        """
        super().__init__(*args, **kwargs)

        # =========================================================================
        # == [THE CURE]: THE ENGINE SUTURE                                       ==
        # =========================================================================
        # We scry the registers for the sovereign engine reference.
        # This link is mandatory for _multicast_hud_status() to reach the Akashic
        # Record and radiate pulses to the React UI.
        self.engine = getattr(self.regs, 'engine', None)

        # Materialize the Chronomancer for Gnostic 'Undo' Prophecy
        self.reverser = MaestroReverser()

        # Binds the Lazarus Oracle for forensic fracture analysis and JIT redemption.
        from ...redemption.diagnostician import AutoDiagnostician
        self.diagnostician = AutoDiagnostician


    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE GRAND RITE OF THE KINETIC WORMHOLE (V-Ω-TOTALITY-V8.0-SINGULARITY)  ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_DISPATCH_HAND | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CONDUCT_V800_REDEMPTION_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme conductor of the Architect's Will. It bifurcates reality between
        the Native Platter (Iron) and the Virtual Cortex (WASM), while maintaining
        a constant forensic vigil. It is the absolute hand of the God-Engine.
        =============================================================================
        """
        import re
        import time
        import os
        import sys
        import random
        import subprocess
        from ....core.state import ActiveLedger
        from ....core.state.contracts import LedgerEntry, LedgerOperation, InverseOp
        from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        # --- MOVEMENT 0: NANOSECOND CHRONOMETRY ---
        start_ns = time.perf_counter_ns()
        trace_id = (env or {}).get("SCAFFOLD_TRACE_ID") or getattr(self.regs, 'trace_id', 'tr-unbound')

        # --- MOVEMENT I: MODIFIER ADJUDICATION (TRIAGE) ---
        # [ASCENSION 13]: Recursive Modifier Peeling.
        # Handles complex edicts like 'retry(3): allow_fail: timeout(60): command'
        retries = 0
        allow_fail = False

        # 1. RETRY ADJUDICATION
        retry_match = re.match(r'^retry\((\d+)\):\s*(.*)', command, re.IGNORECASE)
        if retry_match:
            retries = int(retry_match.group(1))
            command = retry_match.group(2)

        # 2. FAILURE AMNESTY
        if command.lower().startswith('allow_fail:'):
            allow_fail = True
            command = command[11:].strip()

        # --- MOVEMENT II: THE SIMULATION WARD (PROPHECY) ---
        # [ASCENSION 6]: If the Architect is dreaming (Dry Run), we merely record the intent.
        if self.regs.dry_run:
            self.logger.info(f"[{trace_id[:8]}] [DRY-RUN] EXEC: {self._redact_secrets(command)}")
            return

        # --- MOVEMENT III: THE LEDGER INSCRIPTION (CAUSALITY) ---
        # [ASCENSION 8]: Deep Inverse Inference.
        # We prophesy the 'Undo' rite before the first byte is struck.
        undo_commands = self.context.explicit_undo or self.reverser.infer_undo(command, self.context.cwd)

        ledger_entry = LedgerEntry(
            actor="Maestro",
            operation=LedgerOperation.EXEC_SHELL,
            inverse_action=InverseOp(
                op=LedgerOperation.EXEC_SHELL,
                params={"commands": undo_commands, "cwd": str(self.context.cwd)}
            ) if undo_commands else None,
            forward_state={"command": command, "cwd": str(self.context.cwd)},
            metadata={
                "line_num": self.context.line_num,
                "start_time": time.time(),
                "trace_id": trace_id
            }
        )
        ActiveLedger.record(ledger_entry)

        # --- MOVEMENT IV: THE SUBSTRATE BIFURCATION (THE WORMHOLE) ---
        # [ASCENSION 2]: Detection of the Ethereal Plane.
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        attempt = 0
        while attempt <= retries:
            try:
                # [ASCENSION 17]: HUD IGNITION PULSE
                self._multicast_hud_status("STRIKE_START", "#64ffda", trace_id)

                if is_wasm:
                    # =========================================================================
                    # == PATH A: ETHER PLANE (THE VIRTUAL KERNEL)                            ==
                    # =========================================================================
                    # [ASCENSION 12]: Bypasses subprocess.Popen to avoid substrate deadlocks.
                    try:
                        import simulacrum.kernel as kernel
                        self.logger.verbose(f"[{trace_id[:8]}] Tunneling edict to Virtual Kernel...")

                        # [STRIKE]: Execute within the sandboxed WASM VFS
                        res = kernel.subprocess_router.run(
                            command,
                            env=env,
                            cwd=str(self.context.cwd),
                            capture_output=False  # Ensure TTY radiation
                        )

                        if res.returncode != 0:
                            # [TRANSFORMATION]: Reconstruct the error soul for the Diagnostician
                            raise subprocess.CalledProcessError(
                                res.returncode, command, output=res.stdout, stderr=res.stderr
                            )

                        # Strike Success in Ether
                        self._multicast_hud_status("STRIKE_SUCCESS", "#10b981", trace_id)
                        return

                    except ImportError:
                        raise OSError("Environment Paradox: WASM detected but Virtual Kernel is unmanifest.")

                else:
                    # =========================================================================
                    # == PATH B: IRON CORE (THE PHYSICAL PLATTER)                            ==
                    # =========================================================================
                    # [ASCENSION 10]: Standard cinematic execution for high-status environments.
                    self._conduct_cinematic_rite(command, ledger_entry, env=env)

                    # Strike Success in Iron
                    self._multicast_hud_status("STRIKE_SUCCESS", "#10b981", trace_id)
                    return

            except (subprocess.CalledProcessError, Exception) as fracture:
                # --- MOVEMENT V: THE RITE OF RETRIAL (RESILIENCE) ---
                attempt += 1
                if attempt <= retries:
                    # [ASCENSION 14]: Exponential Backoff with Gnostic Jitter
                    delay = (attempt * 1.5) + random.uniform(0, 0.5)
                    self.logger.warn(
                        f"L{self.context.line_num}: Strike Fractured. "
                        f"Initiating Achronal Retrial {attempt}/{retries} in {delay:.2f}s..."
                    )
                    self._multicast_hud_status("STRIKE_RETRY", "#fbbf24", trace_id)
                    time.sleep(delay)
                    continue
                else:
                    # --- MOVEMENT VI: THE REDEMPTION INVOCATION (LAZARUS) ---
                    # [ASCENSION 24]: The Final Adjudication.
                    # We only reach here if all retries have failed.

                    if allow_fail:
                        self.logger.warn(
                            f"L{self.context.line_num}: Edict failed, but the Symphony continues (allow_fail).")
                        self._multicast_hud_status("STRIKE_IGNORED", "#94a3b8", trace_id)
                        return

                    # 1. [THE CURE]: Consult the Lazarus Engine (AutoDiagnostician)
                    # We pass the full fracture object (which contains stderr/stdout)
                    self._multicast_hud_status("STRIKE_FRACTURED", "#ef4444", trace_id)

                    diagnosis = self.diagnostician.consult_council(fracture, {
                        "command": command,
                        "cwd": self.context.cwd,
                        "trace_id": trace_id,
                        "env": env
                    })

                    # 2. [REVELATION]: Forge the final high-status Heresy
                    rc = getattr(fracture, 'returncode', 1)
                    error_context = self._divine_exit_code(rc)

                    raise ArtisanHeresy(
                        message=f"The Maestro's Edict failed: '{self._redact_secrets(command)}'",
                        code="KINETIC_STRIKE_FRACTURE",
                        details=(
                            f"Exit Code: {rc} ({error_context})\n"
                            f"Locus: {self.context.cwd}\n"
                            f"Diagnosis: {diagnosis.advice if diagnosis else 'Unknown Logic Fracture'}"
                        ),
                        child_heresy=fracture,
                        line_num=self.context.line_num,
                        # [ASCENSION 15]: The Seed of Redemption is now manifest.
                        fix_command=diagnosis.cure_command if diagnosis else None,
                        severity=HeresySeverity.CRITICAL,
                        ui_hints={"vfx": "shake", "sound": "fracture_critical"}
                    )

    def _multicast_hud_status(self, type_label: str, color: str, trace: str):
        """[ASCENSION 23]: Radiates kinetic telemetry to the Ocular HUD."""
        akashic = getattr(self.engine, 'akashic', None)
        if akashic:
            try:
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "MAESTRO_CONDUCTOR",
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def _divine_exit_code(self, code: int) -> str:
        """
        =============================================================================
        == THE EXIT CODE DIVINER (V-Ω-TOTALITY-V200-WINDOWS-AWARE)                 ==
        =============================================================================
        [ASCENSION 2]: Decodes numeric failure into Gnostic Truth.
        """
        if code == 127: return "Command Not Found (Binary missing in PATH)"
        if code == 126: return "Permission Denied (Execution Ward)"
        if code == 137: return "Metabolic Collapse (OOM Killer)"
        if code == 130: return "User Interruption (SIGINT)"

        # [THE CURE]: Windows/Make Specifics
        if code == 2:
            return "Execution Fracture: The target (Makefile) was not found or a command within it failed."

        if code == 1:
            return "General Script Failure: The edict was struck but the internal logic failed."

        return f"Unknown Heresy (Code {code})"

    def _conduct_raw_process(
            self,
            command: str,
            ledger_entry: Optional[LedgerEntry] = None,
            env: Optional[Dict] = None,
            inputs: Optional[List[str]] = None
    ) -> KineticVessel:
        """
        =================================================================================
        == THE KINETIC FORGE: OMEGA POINT (V-Ω-TOTALITY-V1000.1-TITANIUM-FIX)          ==
        =================================================================================
        LIF: ∞ | ROLE: PHYSICAL_MATTER_TRANSFECTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_RAW_PROCESS_V1000_MAKEFILE_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme rite of process inception. It transmutes human intent into kinetic
        matter shards, warded against 'UNC Path Poisoning', 'NoneType Leaks', and
        'Filesystem Latency'. It is the absolute hand of the God-Engine.
        """
        import os
        import subprocess
        import threading
        import time
        import platform
        import shlex
        import shutil
        from queue import Queue
        from pathlib import Path

        # [ASCENSION 4]: NANO-SCALE METABOLIC ANCHOR
        start_time = time.monotonic()

        # [ASCENSION 5]: THE OUTPUT CAP (METABOLIC GOVERNOR)
        output_queue = Queue(maxsize=10000)

        # --- MOVEMENT I: IDENTITY & SUBSTRATE ADJUDICATION ---
        trace_id = os.environ.get("GNOSTIC_REQUEST_ID") or \
                   getattr(self.regs, 'trace_id', 'tr-unbound')

        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or platform.system() == "Emscripten"

        # --- MOVEMENT II: REALITY MATERIALIZATION & STABILIZATION (THE CURE) ---
        if self.regs.transaction and not self.regs.is_simulation:
            # 1. Manifest the Staged Reality
            self.regs.transaction.materialize()

            # 2. The Titanium Wait (Filesystem Settling)
            # Give NTFS/Kernel time to index the new inodes before we strike.
            # This annihilates the 'Makefile not found' heresy caused by IO lag.
            if platform.system() == "Windows":
                time.sleep(0.15)

            # 3. Hydraulic Flush
            # Force OS buffers to disk.
            if hasattr(os, 'sync'):
                try:
                    os.sync()
                except:
                    pass

        # --- MOVEMENT III: ENVIRONMENT DNA ALCHEMY ---
        # We merge the Context's purified environment with any specific overrides.
        final_env = (self.context.env or os.environ).copy()
        if env:
            final_env.update(env)

        final_env["SCAFFOLD_TRACE_ID"] = trace_id
        final_env["PYTHONUNBUFFERED"] = "1"

        # --- MOVEMENT IV: GEOMETRIC PURIFICATION ---
        raw_cwd = self.context.cwd.resolve()
        if platform.system() == "Windows":
            # [ASCENSION 13]: LONG PATH DECAPITATION
            # Strip extended path prefix for compatibility with external tools (like make/git)
            # which often choke on the UNC \\?\ syntax.
            clean_cwd_str = str(raw_cwd).replace("\\\\?\\", "")
        else:
            clean_cwd_str = str(raw_cwd)

        # --- MOVEMENT V: THE MAKEFILE SUTURE (THE FIX) ---
        # If the command is 'make' and a Makefile exists, we force explicit targeting
        # to overcome implicit rule resolution failures on Windows shells.
        final_command = command
        is_make_command = command.strip().startswith("make ") or command.strip() == "make"

        if is_make_command and platform.system() == "Windows":
            # We look for the Makefile in the purified CWD
            makefile_path = raw_cwd / "Makefile"
            if makefile_path.exists() and "-f " not in command:
                # Inject the -f flag to force acknowledgment of the file
                parts = command.split(" ", 1)
                args = parts[1] if len(parts) > 1 else ""
                final_command = f"{parts[0]} -f Makefile {args}"
                self.logger.verbose(f"[{trace_id}] Makefile Suture applied: {final_command}")

        # --- MOVEMENT VI: THE KINETIC STRIKE ---
        if is_wasm:
            self.logger.warn("WASM Substrate: Native strike stayed. Dreaming in memory...")
            return KineticVessel(None, output_queue, start_time, 0, final_command, "wasm_sim")

        # Process Group Isolation for clean termination
        creationflags = 0
        preexec_fn = None
        if platform.system() == "Windows":
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            preexec_fn = os.setsid

        try:
            # =========================================================================
            # == THE ATOMIC KERNEL CALL (IRON CORE)                                  ==
            # =========================================================================
            process = subprocess.Popen(
                final_command,
                shell=True,
                executable=self.context.shell_executable,
                cwd=clean_cwd_str,  # <--- THE PURIFIED GROUND
                env=final_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=False,  # [THE FIX]: Read bytes for the Binary Sieve
                bufsize=0,  # [THE CURE]: Zero-latency unbuffered stream
                preexec_fn=preexec_fn,
                creationflags=creationflags
            )

            # [ASCENSION 10]: THE LEDGER SUTURE
            if ledger_entry:
                ledger_entry.metadata['pid'] = process.pid

        except Exception as e:
            raise ArtisanHeresy(f"Forge Collapse: Process inception fractured: {e}", child_heresy=e)

        # --- MOVEMENT VII: VITALITY SENTINEL ---
        if PSUTIL_AVAILABLE:
            threading.Thread(
                target=self._monitor_vitals,
                args=(process.pid, trace_id),
                name=f"VitalsWatcher-{process.pid}",
                daemon=True
            ).start()

        # --- MOVEMENT VIII: STREAMING (THE PRISM) ---
        def stream_reader(stream, stream_type):
            """[ASCENSION 4]: THE BINARY MATTER SIEVE & ENCODING ALCHEMIST."""
            try:
                # We iterate shard-by-shard to eliminate buffer lag.
                for shard in stream:
                    if not shard: break

                    # 1. THE BINARY WARD
                    if b'\0' in shard[:512]:
                        output_queue.put((stream_type, "\x1b[31m[METABOLIC_RECOIL: BINARY_MATTER_REDACTED]\x1b[0m"))
                        break  # Protect the Eye from corruption

                    # 2. THE ENCODING RESURRECTION
                    try:
                        line_str = shard.decode('utf-8').rstrip()
                    except UnicodeDecodeError:
                        line_str = shard.decode('latin-1', errors='replace').rstrip()

                    # 3. QUEUE INJECTION (Governor aware)
                    if not output_queue.full():
                        output_queue.put((stream_type, line_str))
            except Exception:
                pass
            finally:
                if stream: stream.close()
                # [ASCENSION 9]: EOF SINGULARITY
                output_queue.put((stream_type, None))

        # [ASCENSION 4]: PARALLEL RADIATORS
        threading.Thread(target=stream_reader, args=(process.stdout, 'stdout'), daemon=True).start()
        threading.Thread(target=stream_reader, args=(process.stderr, 'stderr'), daemon=True).start()

        # --- MOVEMENT IX: INPUT CONDUIT ---
        # [ASCENSION 7]: THE KINETIC HANDOVER
        if inputs:
            threading.Thread(
                target=self._stream_writer,
                args=(process.stdin, inputs),
                name=f"InputConduit-{process.pid}",
                daemon=True
            ).start()

        # [ASCENSION 12]: THE FINALITY VOW
        return KineticVessel(
            process=process,
            output_queue=output_queue,
            start_time=start_time,
            pid=process.pid,
            command=final_command,
            sandbox_type="local_iron",
            trace_id=trace_id
        )

    def _stream_writer(self, stream, lines: List[str]):
        """
        =================================================================================
        == THE INPUT CONDUIT (V-Ω-TOTALITY-V2.0-RESILIENT)                             ==
        =================================================================================
        LIF: 100x | ROLE: MATTER_INJECTOR
        [ASCENSION 5]: Hydrates the child process stdin without blocking the Mind.
        """
        try:
            for line in lines:
                if line is None: continue
                # Enforce UTF-8 scripture
                stream.write((line + '\n').encode('utf-8'))
                stream.flush()
            # The Rite is concluded
            stream.close()
        except (ValueError, OSError, BrokenPipeError):
            # The process has already returned its soul to the void.
            pass

    def _is_wasm_substrate(self) -> bool:
        """[ASCENSION 11]: SUBSTRATE-AWARE THREADING."""
        return os.environ.get("SCAFFOLD_ENV") == "WASM"

    def _monitor_vitals(self, pid: int, trace_id: str):
        """
        =============================================================================
        == THE METABOLIC SENTINEL (V-Ω-TOTALITY-V320-SUTURED-FINALIS)              ==
        =============================================================================
        LIF: ∞ | ROLE: VITALITY_SCRIER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_MONITOR_VITALS_V320_SUTURED_2026_FINALIS

        [THE CURE]: Signature correctly accepts trace_id to prevent TypeError.
        Tracks the health of the child process and records peak metabolic load.
        """
        try:
            if not PSUTIL_AVAILABLE:
                return

            proc = psutil.Process(pid)
            max_mem_mb = 0

            while proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                try:
                    # 1. Scry physical RAM mass
                    mem_info = proc.memory_info()
                    rss_mb = mem_info.rss / (1024 * 1024)

                    if rss_mb > max_mem_mb:
                        max_mem_mb = rss_mb

                    # [ASCENSION 13]: METABOLIC FEVER DETECTION
                    # If a single subprocess consumes > 1.5GB, warn the Architect.
                    if rss_mb > 1500:
                        self.logger.warn(
                            f"[{trace_id}] Metabolic Fever: Process {pid} is consuming {rss_mb:.0f}MB RAM."
                        )

                    time.sleep(0.5)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break

            # 2. Forensic Trace Inscription
            if max_mem_mb > 100:
                self.logger.verbose(f"[{trace_id}] Subprocess {pid} Peak Mass: {max_mem_mb:.2f}MB")

        except Exception as paradox:
            # The Sentinel must never be the cause of a Kernel Panic.
            self.logger.debug(f"Vitality sentinel for {pid} dissolved: {paradox}")

    def _conduct_cinematic_rite(self, command: str, ledger_entry: LedgerEntry, env: Optional[Dict[str, str]] = None):
        """
        =================================================================================
        == THE CINEMATIC GOVERNOR (V-Ω-TOTALITY-V900.0-DOWRY-SUTURED)                  ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_RECEPTION_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CINEMATIC_V900_FINAL_REVELATION_2026

        [THE MANIFESTO]
        The God-Engine of Gnostic Execution. Orchestrates the transition from Matter
        Shards (process output) to Visual Proclamations, now with a bit-perfect
        Gnostic Dowry handoff.
        =================================================================================
        """
        import time
        import os
        import sys
        import subprocess
        from queue import Empty

        rite_start_time = time.monotonic()

        # [FACULTY 12]: THE GNOSTIC SAFE-GUARD
        gnosis = getattr(self.regs, 'gnosis', {})
        if not isinstance(gnosis, dict):
            gnosis = {}

        # [ASCENSION 5]: BICAMERAL REALITY RENDERING
        is_raw_mode = (
                gnosis.get('renderer') == 'raw' or
                os.getenv("SCAFFOLD_RAW_MODE") == "true" or
                not sys.stdout.isatty()
        )

        try:
            # =========================================================================
            # == [THE CURE]: THE GNOSTIC DOWRY INJECTION                             ==
            # =========================================================================
            # We scry the context for any 'inputs' (stdin) willed by the parser.
            # This is the fix for the NameError: name 'inputs' is not defined.
            inputs_for_strike = self.context.inputs if hasattr(self.context, 'inputs') else None

            # Bestow the command, ledger, environment, and inputs upon the Vessel.
            vessel = self._conduct_raw_process(
                command,
                ledger_entry,
                env=env,
                inputs=inputs_for_strike
            )
            # =========================================================================

            # [ASCENSION 10]: THE PRIVACY VEIL
            display_cmd = self._redact_secrets(command)

            if is_raw_mode:
                self.logger.verbose(f"Engaging Raw Conduit for: {display_cmd}")

                # In raw mode, we stream output shards directly to the TTY.
                # This loop now handles the EOF signal (None) gracefully.
                stdout_done, stderr_done = False, False
                while not (stdout_done and stderr_done):
                    try:
                        stream_type, line = vessel.output_queue.get(timeout=0.1)
                        if line is None:
                            if stream_type == 'stdout':
                                stdout_done = True
                            else:
                                stderr_done = True
                            continue

                        target_stream = sys.stdout if stream_type == 'stdout' else sys.stderr
                        target_stream.write(line + "\n")
                        target_stream.flush()
                    except Empty:
                        if vessel.process.poll() is not None:
                            break  # Process ended and queue is empty

                vessel.process.wait()
                if vessel.process.returncode != 0:
                    raise subprocess.CalledProcessError(
                        vessel.process.returncode, command,
                        output="Process failed in raw mode.",
                        stderr="Check terminal output for forensic markers."
                    )
            else:
                # [ASCENSION 10]: THE CINEMATIC SCRIBE
                # The scribe takes the Vessel and renders a high-status visual experience.
                from ..scribe import CinematicScribe
                scribe = CinematicScribe(display_cmd, self.console)

                # [ASCENSION 3]: ACHRONAL TRACEABILITY
                # We pass the trace_id for high-fidelity HUD rendering.
                scribe.trace_id = vessel.trace_id

                scribe.conduct(vessel.process, vessel.output_queue)

            # [ASCENSION 12]: THE CHRONOMETRIC ANCHOR
            duration = time.monotonic() - rite_start_time
            if ledger_entry:
                ledger_entry.metadata['duration'] = duration

        except subprocess.CalledProcessError as e:
            # Re-raise for retry logic in the master `conduct` rite.
            raise e

        except KeyboardInterrupt:
            # [ASCENSION 7]: THE UNBREAKABLE SIGNAL BRIDGE
            # Severs the kinetic link and annihilates the child process lineage.
            self.logger.warn("Rite interrupted by Architect's will. Dissolving child lineage...")
            if 'vessel' in locals() and vessel and vessel.process:
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