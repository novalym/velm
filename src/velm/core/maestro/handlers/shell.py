# Path: src/velm/core/maestro/handlers/shell.py
# ---------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_SHELL_HANDLER_V40000_NATIVE_BYPASS_FINALIS
# PEP 8 Adherence: STRICT // Gnostic Alignment: ABSOLUTE
# ---------------------------------------------

import os
import re
import shlex
import signal
import subprocess
import tempfile
import threading
import time
import sys
import platform
import gc
import random
import glob
import shutil
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
    == THE KINETIC TITAN (V-Ω-PROCESS-GOD-ENGINE-HEALED-V11-NATIVE-BYPASS)         ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_DISPATCH_HAND | RANK: OMEGA_SOVEREIGN

    The Sovereign Handler of Shell Execution.

    [THE CURE]: Implements **The Native Pythonic Bypass**.
    Instead of transmuting `rm` to `del` and hoping `cmd.exe` behaves, this handler
    intercepts standard filesystem commands (`rm`, `mkdir`, `touch`, `cp`, `mv`)
    and executes them **In-Process** using `shutil` and `os`.

    This guarantees cross-platform determinism, zero-latency execution, and
    immunity to PATH configuration heresies.
    """

    MAX_CMD_LENGTH: Final[int] = 8000

    # [ASCENSION 1]: The Grimoire of Native Rites
    NATIVE_RITES: Final[Set[str]] = {"rm", "mkdir", "touch", "cp", "mv"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = getattr(self.regs, 'engine', None)
        self.reverser = MaestroReverser()
        from ...redemption.diagnostician import AutoDiagnostician
        self.diagnostician = AutoDiagnostician
        self._is_windows = os.name == 'nt'

    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        """
        The Rite of Kinetic Execution.
        """
        start_ns = time.perf_counter_ns()
        trace_id = (env or {}).get("SCAFFOLD_TRACE_ID") or getattr(self.regs, 'trace_id', 'tr-unbound')

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

        if hydrated_cmd.lower().startswith(('proclaim:', 'echo ')):
            msg = re.sub(r'^(proclaim:|echo )\s*', '', hydrated_cmd, flags=re.IGNORECASE).strip('"\'')
            self.logger.info(f"» {msg}")
            return

        # =========================================================================
        # == [ASCENSION 1]: THE NATIVE PYTHONIC BYPASS (THE TRUE CURE)           ==
        # =========================================================================
        # We attempt to execute simple FS commands internally.
        # This bypasses the OS shell entirely, solving the "command not found" heresy.
        if self._attempt_native_bypass(hydrated_cmd, trace_id):
            return

        if self.regs.dry_run:
            self.logger.info(f"[{trace_id[:8]}] [DRY-RUN] EXEC: {self._redact_secrets(hydrated_cmd)}")
            return

        # --- MOVEMENT II: TEMPORAL INFERENCE (UNDO) ---
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
                "line_num": human_line_num,
                "start_time": time.time(),
                "trace_id": trace_id
            }
        )
        ActiveLedger.record(ledger_entry)

        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # --- MOVEMENT III: THE KINETIC LOOP (SUBPROCESS FALLBACK) ---
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
                            f"Diagnosis: {diagnosis.advice if diagnosis else 'Unknown Logic Fracture'}\n"
                            f"Causal Origin:\n    {str(fracture)}"
                        ),
                        child_heresy=fracture,
                        line_num=human_line_num,
                        fix_command=diagnosis.cure_command if diagnosis else None,
                        severity=HeresySeverity.CRITICAL,
                        ui_hints={"vfx": "shake", "sound": "fracture_critical"}
                    )

    def _attempt_native_bypass(self, command: str, trace_id: str) -> bool:
        """
        [ASCENSION 1]: THE NATIVE PYTHONIC BYPASS.
        Intercepts basic filesystem commands and executes them in-process.
        This provides 100% OS compatibility and massive speedups.
        Returns True if handled, False if it must be passed to the Shell.
        """
        # 1. Check for complexity (Pipes, Redirects, Chaining)
        # If the command uses shell magic, we cannot bypass it safely.
        if any(char in command for char in ['|', '>', '<', '&', ';']):
            return False

        parts = shlex.split(command, posix=not self._is_windows)
        if not parts: return False

        verb = parts[0]
        args = parts[1:]

        # Handle 'rm' with flags
        if verb == "rm":
            return self._exec_native_rm(args, trace_id)

        # Handle 'mkdir' with flags
        elif verb == "mkdir":
            return self._exec_native_mkdir(args, trace_id)

        # Handle 'touch'
        elif verb == "touch":
            return self._exec_native_touch(args, trace_id)

        # Handle 'cp'
        elif verb == "cp":
            return self._exec_native_cp(args, trace_id)

        # Handle 'mv'
        elif verb == "mv":
            return self._exec_native_mv(args, trace_id)

        return False

    def _resolve_glob_args(self, args: List[str]) -> List[Path]:
        """Expands globs relative to CWD and returns Path objects."""
        cwd = self.context.cwd
        targets = []

        for arg in args:
            if arg.startswith('-'): continue  # Skip flags

            # Expand Glob
            if '*' in arg or '?' in arg:
                matches = glob.glob(str(cwd / arg), recursive=True)
                targets.extend([Path(m) for m in matches])
            else:
                targets.append(cwd / arg)

        return targets

    def _exec_native_rm(self, args: List[str], trace_id: str) -> bool:
        """Native implementation of 'rm -rf'."""
        targets = self._resolve_glob_args(args)

        if self.regs.dry_run:
            self.logger.info(f"[{trace_id[:8]}] [DRY-RUN] NATIVE: rm {args}")
            return True

        self.logger.verbose(f"[{trace_id[:8]}] Native Strike: rm ({len(targets)} targets)")

        for target in targets:
            if not target.exists(): continue
            try:
                if target.is_dir() and not target.is_symlink():
                    shutil.rmtree(target, ignore_errors=True)
                else:
                    target.unlink()
            except Exception as e:
                self.logger.warn(f"Native rm failed for {target.name}: {e}")
                # We do not raise here to mimic 'rm -f' behavior (force/silent)

        return True

    def _exec_native_mkdir(self, args: List[str], trace_id: str) -> bool:
        """Native implementation of 'mkdir -p'."""
        targets = self._resolve_glob_args(args)

        if self.regs.dry_run:
            self.logger.info(f"[{trace_id[:8]}] [DRY-RUN] NATIVE: mkdir {args}")
            return True

        for target in targets:
            try:
                target.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise ArtisanHeresy(f"Native mkdir failed for {target.name}: {e}")

        return True

    def _exec_native_touch(self, args: List[str], trace_id: str) -> bool:
        """Native implementation of 'touch'."""
        targets = self._resolve_glob_args(args)

        if self.regs.dry_run:
            self.logger.info(f"[{trace_id[:8]}] [DRY-RUN] NATIVE: touch {args}")
            return True

        for target in targets:
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch(exist_ok=True)
            except Exception as e:
                raise ArtisanHeresy(f"Native touch failed for {target.name}: {e}")

        return True

    def _exec_native_cp(self, args: List[str], trace_id: str) -> bool:
        """Native implementation of 'cp -r'."""
        # cp source dest
        # Only simple case supported: 1 source, 1 dest
        non_flag_args = [a for a in args if not a.startswith('-')]
        if len(non_flag_args) != 2: return False  # Fallback to shell for complex copy

        src = self.context.cwd / non_flag_args[0]
        dst = self.context.cwd / non_flag_args[1]

        if self.regs.dry_run:
            self.logger.info(f"[{trace_id[:8]}] [DRY-RUN] NATIVE: cp {src.name} -> {dst.name}")
            return True

        try:
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        except Exception as e:
            raise ArtisanHeresy(f"Native cp failed: {e}")

        return True

    def _exec_native_mv(self, args: List[str], trace_id: str) -> bool:
        """Native implementation of 'mv'."""
        non_flag_args = [a for a in args if not a.startswith('-')]
        if len(non_flag_args) != 2: return False

        src = self.context.cwd / non_flag_args[0]
        dst = self.context.cwd / non_flag_args[1]

        if self.regs.dry_run:
            self.logger.info(f"[{trace_id[:8]}] [DRY-RUN] NATIVE: mv {src.name} -> {dst.name}")
            return True

        try:
            shutil.move(str(src), str(dst))
        except Exception as e:
            raise ArtisanHeresy(f"Native mv failed: {e}")

        return True

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

        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        if self.regs.transaction and not self.regs.is_simulation:
            # [ASCENSION 23]: Volumetric Isolation Suture
            self.regs.transaction.materialize()
            if self._is_windows:
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

        if self._is_windows:
            clean_cwd_str = str(raw_cwd).replace("\\\\?\\", "")
        else:
            clean_cwd_str = str(raw_cwd)

        # [ASCENSION 4]: RECURSIVE MANIFEST HUNTER
        final_command = command
        cmd_stripped = command.strip()
        is_make_command = cmd_stripped.startswith("make ") or cmd_stripped == "make"
        is_npm_command = re.match(r'^(npm|yarn|pnpm|bun)\s+', cmd_stripped)
        is_poetry_command = cmd_stripped.startswith("poetry ")
        is_cargo_command = cmd_stripped.startswith("cargo ")
        is_go_command = cmd_stripped.startswith("go ")

        target_dir = None

        if is_make_command:
            target_dir = self._hunt_for_manifest(raw_cwd, "Makefile")
            if target_dir and target_dir != raw_cwd:
                self.logger.verbose(f"Redirecting Make execution to: {target_dir}")
                if "-C" not in command:
                    final_command = f"{command} -C {target_dir}"
                if self._is_windows and "-f " not in final_command and "-C " not in final_command:
                    parts = command.split(" ", 1)
                    args = parts[1] if len(parts) > 1 else ""
                    final_command = f"{parts[0]} -f Makefile {args}"

        elif is_npm_command:
            target_dir = self._hunt_for_manifest(raw_cwd, "package.json")
            if target_dir and target_dir != raw_cwd:
                self.logger.verbose(f"Redirecting NPM execution to: {target_dir}")
                clean_cwd_str = str(target_dir).replace("\\\\?\\", "") if self._is_windows else str(target_dir)

        elif is_poetry_command:
            target_dir = self._hunt_for_manifest(raw_cwd, "pyproject.toml")
            if target_dir and target_dir != raw_cwd:
                self.logger.verbose(f"Redirecting Poetry execution to: {target_dir}")
                clean_cwd_str = str(target_dir).replace("\\\\?\\", "") if self._is_windows else str(target_dir)

        if (is_make_command or is_npm_command or is_poetry_command) and not target_dir:
            if "--version" not in cmd_stripped and "-v" not in cmd_stripped and "help" not in cmd_stripped:
                self._scream_directory_contents(raw_cwd)
                raise ArtisanHeresy(
                    f"Spacetime Displacement Heresy: The manifest for '{cmd_stripped.split()[0]}' is unmanifest.",
                    details=f"Scanned: {raw_cwd}. See logs for Forensic Biopsy.",
                    severity=HeresySeverity.CRITICAL
                )

        if is_wasm:
            self.logger.warn("WASM Substrate: Native strike stayed. Dreaming in memory...")
            return KineticVessel(None, output_queue, start_time, 0, final_command, "wasm_sim", trace_id)

        # [ASCENSION 5]: ARGUMENT SHARDING FOR WINDOWS
        if self._is_windows and len(final_command) > self.MAX_CMD_LENGTH:
            self.logger.warn("Command exceeds Windows buffer. Sharding into batch script.")
            fd, bat_path = tempfile.mkstemp(suffix=".bat", text=True)
            with os.fdopen(fd, 'w') as f:
                f.write(f"@echo off\n{final_command}")
            final_command = bat_path

        creationflags = 0
        preexec_fn = None
        if self._is_windows:
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            preexec_fn = os.setsid

        try:
            if os.environ.get("SCAFFOLD_ADRENALINE") == "1" and self._is_windows:
                creationflags |= 0x00000080

            process = subprocess.Popen(
                final_command,
                shell=True,
                executable=self.context.shell_executable,
                cwd=clean_cwd_str,
                env=final_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=False,
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
                    if b'\x00' in shard[:512]:
                        output_queue.put((stream_type, "\x1b[31m[METABOLIC_RECOIL: BINARY_MATTER_REDACTED]\x1b[0m"))
                        break

                    try:
                        line_str = shard.decode('utf-8').replace('\r\n', '\n').rstrip('\n')
                    except UnicodeDecodeError:
                        try:
                            line_str = shard.decode('cp1252', errors='replace').replace('\r\n', '\n').rstrip('\n')
                        except:
                            line_str = shard.decode('latin-1', errors='replace').replace('\r\n', '\n').rstrip('\n')

                    if "sk_live_" in line_str or "ghp_" in line_str:
                        line_str = self._redact_secrets(line_str)

                    if not output_queue.full():
                        output_queue.put((stream_type, line_str))

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

        if inputs:
            threading.Thread(target=self._stream_writer, args=(process.stdin, inputs),
                             name=f"InputConduit-{process.pid}", daemon=True).start()

        return KineticVessel(process, output_queue, start_time, process.pid, final_command, "local_iron", trace_id)

    def _hunt_for_manifest(self, raw_cwd: Path, manifest_name: str) -> Optional[Path]:
        if (raw_cwd / manifest_name).exists():
            return raw_cwd

        self.logger.warn(f"'{manifest_name}' unmanifest at root. Scanning deep strata...")
        base_str = str(raw_cwd.resolve()).replace('\\', '/').lower()

        try:
            for root, dirs, files in os.walk(raw_cwd):
                root_str = str(Path(root).resolve()).replace('\\', '/').lower()
                if root_str.startswith(base_str):
                    rel_str = root_str[len(base_str):].strip('/')
                    depth = len(rel_str.split('/')) if rel_str else 0
                else:
                    depth = 0

                if depth > 3:
                    del dirs[:]
                    continue

                if manifest_name in files:
                    target_dir = Path(root)
                    self.logger.success(f"'{manifest_name}' discovered in nested sanctum: {target_dir.name}")
                    return target_dir
        except Exception as e:
            self.logger.debug(f"Manifest Hunt encountered friction: {e}")

        return None

    def _scream_directory_contents(self, path: Path):
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
            if vessel and vessel.process and vessel.process.poll() is None:
                self._kill_process_group(vessel.process)
            raise e
        finally:
            if vessel and vessel.process and vessel.process.poll() is None:
                self._kill_process_group(vessel.process)

    def _kill_process_group(self, process: subprocess.Popen):
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