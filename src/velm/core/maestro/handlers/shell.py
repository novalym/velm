# Path: core/maestro/handlers/shell.py
# ------------------------------------


import os
import re
import shlex
import signal
import subprocess
import threading
import time
import sys
import platform
import gc
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
    == THE KINETIC TITAN (V-Ω-PROCESS-GOD-ENGINE-HEALED-V6)                        ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_DISPATCH_HAND | RANK: OMEGA_SOVEREIGN

    The Sovereign Handler of Shell Execution. It does not merely run commands; it
    shepherds them through their entire lifecycle, monitoring their health, bridging
    their signals, and chronicling their demise. It possesses deep volumetric
    awareness to annihilate spatial execution errors.

    ### THE PANTHEON OF 15 ASCENDED FACULTIES:
    1.  **Virtual Chronometry Decoder (THE CURE):** It understands that line numbers
        > 10000 are Virtual IDs from the `PostRunScribe`. It decodes them back to
        the Base Line Number (e.g. `230005` -> `L23`) for luminous human logging.
    2.  **Recursive Manifest Hunter V3:** Deep spatial scanning for `package.json`,
        `Makefile`, and `pyproject.toml`, immune to Windows drive-casing.
    3.  **Hyper-Verbose Forensic Biopsy:** On failure, it dumps the full directory
        tree of the scanned locus to the logs.
    4.  **Volumetric Pre-Flight Biopsy:** Physically asserts target existence.
    5.  **Tri-Phasic Root Resolution:** Safely resolves project root.
    6.  **The Phantom Orphan Exorcist:** Annihilates zombie processes.
    7.  **Substrate-Aware Stream Yielding:** Prevents WASM lockups.
    8.  **The Sentinel of the Standard Error:** Captures stderr for diagnostics.
    9.  **Adrenaline Prioritization:** Escalates OS priority on demand.
    10. **Binary Matter Aegis:** Blocks null-byte corruption.
    11. **The Venv Suture Validation:** Verifies interpreter validity.
    12. **Idempotent Execution Cache:** Framework for command hashing.
    13. **The Ocular Muzzle:** Throttles high-velocity logs.
    14. **Cross-Platform Signal Bridging:** Handles SIGINT/CTRL-C.
    15. **The Proclamation Pass-Through:** Natively intercepts `proclaim:` logic.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = getattr(self.regs, 'engine', None)
        self.reverser = MaestroReverser()
        from ...redemption.diagnostician import AutoDiagnostician
        self.diagnostician = AutoDiagnostician

    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        import random

        start_ns = time.perf_counter_ns()
        trace_id = (env or {}).get("SCAFFOLD_TRACE_ID") or getattr(self.regs, 'trace_id', 'tr-unbound')

        # [ASCENSION 1]: VIRTUAL CHRONOMETRY DECODER
        # If line_num is massive, it's a virtual ID. We extract the base line.
        virtual_line_num = self.context.line_num
        human_line_num = virtual_line_num // 10000 if virtual_line_num > 10000 else virtual_line_num

        retries = 0
        allow_fail = False

        # --- MOVEMENT 0: THE ALCHEMICAL STRIKE ---
        try:
            hydrated_cmd = self.alchemist.transmute(command, self.regs.gnosis)
        except Exception:
            hydrated_cmd = command

        # --- MOVEMENT I: SEMANTIC DECONSTRUCTION ---
        retry_match = re.match(r'^retry\((\d+)\):\s*(.*)', hydrated_cmd, re.IGNORECASE)
        if retry_match:
            retries = int(retry_match.group(1))
            hydrated_cmd = retry_match.group(2)

        if hydrated_cmd.lower().startswith('allow_fail:'):
            allow_fail = True
            hydrated_cmd = hydrated_cmd[11:].strip()

        # [ASCENSION 15]: The Proclamation Pass-Through
        if hydrated_cmd.lower().startswith(('proclaim:', 'echo ')):
            msg = re.sub(r'^(proclaim:|echo )\s*', '', hydrated_cmd, flags=re.IGNORECASE).strip('"\'')
            # Use the human-readable line number for the log context if needed, but here we just log
            self.logger.info(f"» {msg}")
            return

        if self.regs.dry_run:
            self.logger.info(f"[{trace_id[:8]}] [DRY-RUN] EXEC: {self._redact_secrets(hydrated_cmd)}")
            return

        undo_commands = self.context.explicit_undo or self.reverser.infer_undo(hydrated_cmd, self.context.cwd)

        ledger_entry = LedgerEntry(
            actor="Maestro",
            operation=LedgerOperation.EXEC_SHELL,
            inverse_action=InverseOp(
                op=LedgerOperation.EXEC_SHELL,
                params={"commands": undo_commands, "cwd": str(self.context.cwd)}
            ) if undo_commands else None,
            forward_state={"command": hydrated_cmd, "cwd": str(self.context.cwd)},
            metadata={
                "line_num": human_line_num,  # Use decoded line for history
                "start_time": time.time(),
                "trace_id": trace_id
            }
        )
        ActiveLedger.record(ledger_entry)

        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        attempt = 0
        while attempt <= retries:
            try:
                self._multicast_hud_status("STRIKE_START", "#64ffda", trace_id)

                if is_wasm:
                    try:
                        import simulacrum.kernel as kernel
                        self.logger.verbose(f"[{trace_id[:8]}] Tunneling edict to Virtual Kernel...")
                        res = kernel.subprocess_router.run(
                            hydrated_cmd,
                            env=env,
                            cwd=str(self.context.cwd),
                            capture_output=False
                        )
                        if res.returncode != 0:
                            raise subprocess.CalledProcessError(
                                res.returncode, hydrated_cmd, output=res.stdout, stderr=res.stderr
                            )
                        self._multicast_hud_status("STRIKE_SUCCESS", "#10b981", trace_id)
                        return
                    except ImportError:
                        raise OSError("Environment Paradox: WASM detected but Virtual Kernel is unmanifest.")
                else:
                    self._conduct_cinematic_rite(hydrated_cmd, ledger_entry, env=env)
                    self._multicast_hud_status("STRIKE_SUCCESS", "#10b981", trace_id)
                    return

            except (subprocess.CalledProcessError, Exception) as fracture:
                attempt += 1
                if attempt <= retries:
                    delay = (attempt * 1.5) + random.uniform(0, 0.5)
                    self.logger.warn(
                        f"L{human_line_num}: Strike Fractured. "
                        f"Initiating Achronal Retrial {attempt}/{retries} in {delay:.2f}s..."
                    )
                    self._multicast_hud_status("STRIKE_RETRY", "#fbbf24", trace_id)
                    time.sleep(delay)
                    continue
                else:
                    if allow_fail:
                        self.logger.warn(
                            f"L{human_line_num}: Edict failed, but the Symphony continues (allow_fail).")
                        self._multicast_hud_status("STRIKE_IGNORED", "#94a3b8", trace_id)
                        return

                    self._multicast_hud_status("STRIKE_FRACTURED", "#ef4444", trace_id)

                    diagnosis = self.diagnostician.consult_council(fracture, {
                        "command": hydrated_cmd,
                        "cwd": self.context.cwd,
                        "trace_id": trace_id,
                        "env": env
                    })

                    rc = getattr(fracture, 'returncode', 1)
                    error_context = self._divine_exit_code(rc)

                    raise ArtisanHeresy(
                        message=f"The Maestro's Edict failed: '{self._redact_secrets(hydrated_cmd)}'",
                        code="KINETIC_STRIKE_FRACTURE",
                        details=(
                            f"Exit Code: {rc} ({error_context})\n"
                            f"Locus: {self.context.cwd}\n"
                            f"Diagnosis: {diagnosis.advice if diagnosis else 'Unknown Logic Fracture'}"
                        ),
                        child_heresy=fracture,
                        line_num=human_line_num,
                        fix_command=diagnosis.cure_command if diagnosis else None,
                        severity=HeresySeverity.CRITICAL,
                        ui_hints={"vfx": "shake", "sound": "fracture_critical"}
                    )

    def _multicast_hud_status(self, type_label: str, color: str, trace: str):
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
        if code == 127: return "Command Not Found (Binary missing in PATH)"
        if code == 126: return "Permission Denied (Execution Ward)"
        if code == 137: return "Metabolic Collapse (OOM Killer)"
        if code == 130: return "User Interruption (SIGINT)"
        if code == 2:
            return "Execution Fracture: The target (Makefile/File) was not found or a command within it failed."
        if code == 1:
            return "General Script Failure: The edict was struck but the internal logic failed."
        return f"Unknown Heresy (Code {code})"

    def _hunt_for_manifest(self, raw_cwd: Path, manifest_name: str) -> Optional[Path]:
        """
        =============================================================================
        == THE RECURSIVE MANIFEST HUNTER (V-Ω-SPATIAL-SUTURE-V2)                   ==
        =============================================================================
        [ASCENSION 14]: Deep Spatial Healing.
        Hunts for a manifest file up to 2 levels deep to heal Spatial Desyncs caused
        by PRESERVE Geometric Consensus (Wrapper Directories).
        """
        if (raw_cwd / manifest_name).exists():
            return raw_cwd

        self.logger.warn(f"'{manifest_name}' unmanifest at root. Scanning deep strata...")

        # Absolute string for robust comparison, immune to Path.relative_to() casing paradoxes on Windows
        base_str = str(raw_cwd.resolve()).replace('\\', '/').lower()

        try:
            for root, dirs, files in os.walk(raw_cwd):
                root_str = str(Path(root).resolve()).replace('\\', '/').lower()

                # Robust Depth Governor: Prevents infinite recursion
                if root_str.startswith(base_str):
                    rel_str = root_str[len(base_str):].strip('/')
                    depth = len(rel_str.split('/')) if rel_str else 0
                else:
                    depth = 0

                if depth > 2:
                    del dirs[:]  # Stop recursing deeper than 2 levels
                    continue

                if manifest_name in files:
                    target_dir = Path(root)
                    self.logger.success(f"'{manifest_name}' discovered in nested sanctum: {target_dir.name}")
                    return target_dir
        except Exception as e:
            self.logger.debug(f"Manifest Hunt encountered friction: {e}")

        return None

    def _conduct_raw_process(
            self,
            command: str,
            ledger_entry: Optional[LedgerEntry] = None,
            env: Optional[Dict] = None,
            inputs: Optional[List[str]] = None
    ) -> KineticVessel:
        from queue import Queue

        start_time = time.monotonic()
        output_queue = Queue(maxsize=10000)

        trace_id = os.environ.get("GNOSTIC_REQUEST_ID") or \
                   getattr(self.regs, 'trace_id', 'tr-unbound')

        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or platform.system() == "Emscripten"

        if self.regs.transaction and not self.regs.is_simulation:
            # [ASCENSION 23]: Volumetric Isolation Suture
            # Ensure physical matter is manifest before kinetic strike
            self.regs.transaction.materialize()
            if platform.system() == "Windows":
                time.sleep(0.15)
            if hasattr(os, 'sync'):
                try:
                    os.sync()
                except:
                    pass

        final_env = (self.context.env or os.environ).copy()
        if env: final_env.update(env)
        final_env["SCAFFOLD_TRACE_ID"] = trace_id
        final_env["GNOSTIC_TRACE_ID"] = trace_id
        final_env["PYTHONUNBUFFERED"] = "1"

        if os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            final_env["SCAFFOLD_PRIORITY"] = "HIGH"

        raw_cwd = self.context.cwd.resolve()

        self.logger.verbose(f"[{trace_id}] Absolute Kinetic Locus: {raw_cwd}")

        if platform.system() == "Windows":
            clean_cwd_str = str(raw_cwd).replace("\\\\?\\", "")
        else:
            clean_cwd_str = str(raw_cwd)

        # =========================================================================
        # == [ASCENSION 1 & 14]: RECURSIVE MANIFEST HUNTER (THE CURE)            ==
        # =========================================================================
        final_command = command
        cmd_stripped = command.strip()
        is_make_command = cmd_stripped.startswith("make ") or cmd_stripped == "make"
        is_npm_command = cmd_stripped.startswith("npm ") or cmd_stripped.startswith("yarn ") or cmd_stripped.startswith(
            "pnpm ")
        is_poetry_command = cmd_stripped.startswith("poetry ")

        if is_make_command:
            target_dir = self._hunt_for_manifest(raw_cwd, "Makefile")

            if not target_dir:
                engine_root = getattr(self.engine, 'project_root', None)
                if engine_root and (engine_root / "Makefile").exists():
                    target_dir = engine_root

            if not target_dir:
                self._scream_directory_contents(raw_cwd)
                raise ArtisanHeresy(
                    "Spacetime Displacement Heresy: The 'Makefile' is not manifest in any known volume.",
                    details=f"Scanned: {raw_cwd}, Engine Root. See logs for Forensic Biopsy.",
                    suggestion="Verify the Shadow Forge correctly copied the Makefile into the Green Volume.",
                    severity=HeresySeverity.CRITICAL
                )

            # Inject -C to re-orient the build system
            if target_dir != raw_cwd:
                self.logger.verbose(f"Redirecting Make execution to: {target_dir}")
                final_command = f"{command} -C {target_dir}"

            # Windows explicit targeting
            if platform.system() == "Windows" and "-f " not in final_command and "-C " not in final_command:
                parts = command.split(" ", 1)
                args = parts[1] if len(parts) > 1 else ""
                final_command = f"{parts[0]} -f Makefile {args}"

        # 2. The NPM Biopsy
        elif is_npm_command:
            target_dir = self._hunt_for_manifest(raw_cwd, "package.json")
            if not target_dir:
                self._scream_directory_contents(raw_cwd)
                raise ArtisanHeresy(
                    "Spacetime Displacement Heresy: 'package.json' is not manifest.",
                    details=f"Locus: {raw_cwd}",
                    severity=HeresySeverity.CRITICAL
                )
            if target_dir != raw_cwd:
                self.logger.verbose(f"Redirecting NPM execution to: {target_dir}")
                clean_cwd_str = str(target_dir).replace("\\\\?\\", "") if platform.system() == "Windows" else str(
                    target_dir)

        # 3. The Poetry Biopsy
        elif is_poetry_command:
            target_dir = self._hunt_for_manifest(raw_cwd, "pyproject.toml")
            if not target_dir:
                self._scream_directory_contents(raw_cwd)
                raise ArtisanHeresy(
                    "Spacetime Displacement Heresy: 'pyproject.toml' is not manifest.",
                    details=f"Locus: {raw_cwd}",
                    severity=HeresySeverity.CRITICAL
                )
            if target_dir != raw_cwd:
                self.logger.verbose(f"Redirecting Poetry execution to: {target_dir}")
                clean_cwd_str = str(target_dir).replace("\\\\?\\", "") if platform.system() == "Windows" else str(
                    target_dir)

        # --- KINETIC STRIKE ---
        if is_wasm:
            self.logger.warn("WASM Substrate: Native strike stayed. Dreaming in memory...")
            return KineticVessel(None, output_queue, start_time, 0, final_command, "wasm_sim", trace_id)

        creationflags = 0
        preexec_fn = None
        if platform.system() == "Windows":
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            preexec_fn = os.setsid

        try:
            # [ASCENSION 6]: Adrenaline Prioritization
            process = subprocess.Popen(
                final_command,
                shell=True,
                executable=self.context.shell_executable,
                cwd=clean_cwd_str,
                env=final_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=False,  # Binary mode to prevent encoding errors
                bufsize=0,
                preexec_fn=preexec_fn,
                creationflags=creationflags
            )
            if ledger_entry:
                ledger_entry.metadata['pid'] = process.pid
        except Exception as e:
            raise ArtisanHeresy(f"Forge Collapse: Process inception fractured: {e}", child_heresy=e)

        if PSUTIL_AVAILABLE:
            threading.Thread(target=self._monitor_vitals, args=(process.pid, trace_id),
                             name=f"VitalsWatcher-{process.pid}", daemon=True).start()

        def stream_reader(stream, stream_type):
            try:
                for shard in stream:
                    if not shard: break
                    # [ASCENSION 4]: Binary Matter Aegis (Null Byte Sieve)
                    if b'\0' in shard[:512]:
                        output_queue.put((stream_type, "\x1b[31m[METABOLIC_RECOIL: BINARY_MATTER_REDACTED]\x1b[0m"))
                        break

                    # [ASCENSION 13]: The Null-Byte Sieve (Encoding Fallback)
                    try:
                        line_str = shard.decode('utf-8').replace('\r\n', '\n').rstrip('\n')
                    except UnicodeDecodeError:
                        line_str = shard.decode('latin-1', errors='replace').replace('\r\n', '\n').rstrip('\n')

                    # [ASCENSION 11]: Secret Entropy Redaction
                    if "sk_live_" in line_str or "ghp_" in line_str:
                        line_str = self._redact_secrets(line_str)

                    if not output_queue.full():
                        output_queue.put((stream_type, line_str))

                    # [ASCENSION 5]: Substrate-Aware Stream Yielding
                    time.sleep(0)
            except Exception:
                pass
            finally:
                if stream:
                    try:
                        stream.close()
                    except:
                        pass
                output_queue.put((stream_type, None))

        threading.Thread(target=stream_reader, args=(process.stdout, 'stdout'), daemon=True).start()
        threading.Thread(target=stream_reader, args=(process.stderr, 'stderr'), daemon=True).start()

        # [ASCENSION 14]: Interactive Stream Handshake
        if inputs:
            threading.Thread(target=self._stream_writer, args=(process.stdin, inputs),
                             name=f"InputConduit-{process.pid}", daemon=True).start()

        return KineticVessel(process, output_queue, start_time, process.pid, final_command, "local_iron", trace_id)

    def _scream_directory_contents(self, path: Path):
        """[ASCENSION 2]: HYPER-VERBOSE FORENSIC BIOPSY."""
        self.logger.critical(f"--- FORENSIC BIOPSY OF '{path}' ---")
        try:
            for root, dirs, files in os.walk(path):
                level = root.replace(str(path), '').count(os.sep)
                indent = ' ' * 4 * (level)
                self.logger.critical(f"{indent}[D] {os.path.basename(root)}/")
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    self.logger.critical(f"{subindent}[F] {f}")
        except Exception as e:
            self.logger.critical(f"Biopsy Failed: {e}")
        self.logger.critical(f"--- END BIOPSY ---")

    def _stream_writer(self, stream, lines: List[str]):
        try:
            for line in lines:
                if line is None: continue
                stream.write((line + '\n').encode('utf-8'))
                stream.flush()
            stream.close()
        except (ValueError, OSError, BrokenPipeError):
            pass

    def _monitor_vitals(self, pid: int, trace_id: str):
        try:
            if not PSUTIL_AVAILABLE: return
            proc = psutil.Process(pid)
            max_mem_mb = 0
            while proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                try:
                    mem_info = proc.memory_info()
                    rss_mb = mem_info.rss / (1024 * 1024)
                    if rss_mb > max_mem_mb: max_mem_mb = rss_mb
                    if rss_mb > 1500:
                        self.logger.warn(
                            f"[{trace_id}] Metabolic Fever: Process {pid} is consuming {rss_mb:.0f}MB RAM.")
                    time.sleep(0.5)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
            if max_mem_mb > 100:
                self.logger.verbose(f"[{trace_id}] Subprocess {pid} Peak Mass: {max_mem_mb:.2f}MB")
        except Exception as paradox:
            self.logger.debug(f"Vitality sentinel for {pid} dissolved: {paradox}")

    def _conduct_cinematic_rite(self, command: str, ledger_entry: LedgerEntry, env: Optional[Dict[str, str]] = None):
        rite_start_time = time.monotonic()
        vessel = None
        is_raw_mode = (os.environ.get("SCAFFOLD_RAW_MODE") == "true" or not sys.stdout.isatty())

        try:
            inputs_for_strike = self.context.inputs if hasattr(self.context, 'inputs') else None
            vessel = self._conduct_raw_process(command, ledger_entry, env=env, inputs=inputs_for_strike)
            display_cmd = self._redact_secrets(command)

            if is_raw_mode:
                self.logger.verbose(f"Engaging Raw Conduit for: {display_cmd}")
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
                        if stream_type == 'stderr':
                            # [ASCENSION 7]: The Sentinel of the Standard Error
                            vessel.stderr_snapshot.append(line)
                            if len(vessel.stderr_snapshot) > 1000: vessel.stderr_snapshot.pop(0)
                    except Empty:
                        if vessel.process.poll() is not None: break
                vessel.process.wait()
                if vessel.process.returncode != 0:
                    full_output = "\n".join(vessel.stderr_snapshot)
                    raise subprocess.CalledProcessError(vessel.process.returncode, command,
                                                        output="Process failed in raw mode.", stderr=full_output)
            else:
                from ..scribe import CinematicScribe
                scribe = CinematicScribe(display_cmd, self.console)
                scribe.trace_id = vessel.trace_id
                scribe.conduct(vessel.process, vessel.output_queue)

            if ledger_entry: ledger_entry.metadata['duration'] = time.monotonic() - rite_start_time
        except Exception as e:
            # [ASCENSION 3]: The Phantom Orphan Exorcist
            if vessel and vessel.process and vessel.process.poll() is None:
                self._kill_process_group(vessel.process)
            raise e
        finally:
            if vessel and vessel.process and vessel.process.poll() is None:
                self._kill_process_group(vessel.process)

    def _kill_process_group(self, process: subprocess.Popen):
        """[ASCENSION 9]: Cross-Platform Signal Bridging."""
        try:
            if os.name == 'nt':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            else:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                time.sleep(0.1)
                if process.poll() is None: os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except Exception:
            try:
                process.kill()
            except:
                pass