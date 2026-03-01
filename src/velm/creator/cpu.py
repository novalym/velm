# Path: src/velm/creator/cpu.py
# -----------------------------

from uuid import uuid4
import os
import sys
import time
import subprocess
import shlex
import shutil
import platform
import threading
import concurrent.futures
import hashlib
import re
import gc
from contextlib import nullcontext
from pathlib import Path
from typing import List, Tuple, Optional, Set, Union, TYPE_CHECKING, Any, Dict, Final, Deque
from collections import defaultdict, deque

from .alu import AlchemicalLogicUnit
from .io_controller import IOConductor
from .opcodes import OpCode, Instruction
from .registers import QuantumRegisters
from ..contracts.data_contracts import ScaffoldItem, InscriptionAction
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..logger import Scribe

if TYPE_CHECKING:
    from ..core.maestro import MaestroConductor as MaestroUnit
    from ..core.runtime.engine import ScaffoldEngine

Logger = Scribe("QuantumCPU")

# --- System Constraints ---
MAX_IO_CONCURRENCY: Final[int] = 32
RETRY_THRESHOLD: Final[int] = 5
YIELD_MS: Final[float] = 0.02
INSTRUCTION_CACHE_SIZE: Final[int] = 1024


class QuantumCPU:
    """
    Executes the compiled blueprint instructions reliably across multiple OS platforms.

    The QuantumCPU operates using a two-stage pipeline:
    1. I/O Pipeline: Handles file system generation (MKDIR, WRITE, CHMOD) concurrently.
    2. Execution Pipeline: Handles shell commands (EXEC) sequentially to respect state dependencies.
    """

    def __init__(
            self,
            registers: QuantumRegisters,
            io_conductor: IOConductor,
            maestro: "MaestroUnit",
            engine: Optional["ScaffoldEngine"] = None
    ):
        import argparse

        self.regs = registers
        self.io = io_conductor
        self.maestro = maestro
        self.engine = engine
        self.logger = Logger

        self.context = getattr(registers, 'context', None)
        if self.context is None:
            self.context = argparse.Namespace(
                command="genesis",
                cwd=Path.cwd(),
                env=os.environ.copy()
            )

        self.program_counter: int = 0
        self.instruction_pointer: int = 0
        self.is_halted: bool = False
        self.state_register: str = "0xINIT"

        self.program: List[Instruction] = []
        self._io_pipeline: List[Instruction] = []
        self._exec_pipeline: List[Instruction] = []

        # Instruction Prefetch Buffer (IPB) for large template files
        self._prefetch_buffer: Dict[str, bytes] = {}

        self._birth_ns: int = time.perf_counter_ns()
        self._instruction_telemetry: Dict[int, Dict[str, Any]] = {}
        self._io_lock = threading.RLock()
        self._telemetry_lock = threading.Lock()

        # Hyper-Threading configuration for the native OS layer
        self._cpu_cores = os.cpu_count() or 1
        self._active_workers = min(MAX_IO_CONCURRENCY, self._cpu_cores * 2)

        # L1 Cache for binary resolution (shutil.which)
        self._binary_l1_cache: Dict[str, str] = {}

        self._thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._active_workers,
            thread_name_prefix=f"TitanCPU-{self.regs.trace_id[:4]}"
        )

        self.trace_id = self.regs.trace_id
        self.session_id = self.regs.session_id

        self.logger.verbose(
            f"Execution engine initialized. Workers: {self._active_workers} | Trace: {self.trace_id}"
        )

    def load_program(
            self,
            items: List[ScaffoldItem],
            commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]
    ):
        """
        Compiles the AST into distinct I/O and Execution pipelines.
        Ensures that directories are created before their nested files.
        """
        self.program.clear()
        self._io_pipeline.clear()
        self._exec_pipeline.clear()

        # Topological sorting: Sort by depth, ensuring directories evaluate before files
        sorted_items = sorted(
            items,
            key=lambda x: (len(x.path.parts) if x.path else 0, not x.is_dir)
        )

        for item in sorted_items:
            if not item.path: continue

            if item.is_dir:
                instr = Instruction(op=OpCode.MKDIR, target=item.path, line_num=item.line_num)
                self._io_pipeline.append(instr)
                self.program.append(instr)
            else:
                origin = item.blueprint_origin or Path("unknown")

                # Trigger background prefetching for heavy seed templates to hide network latency
                if item.seed_path and not item.content:
                    self._trigger_prefetch(item.seed_path)

                write_instr = Instruction(
                    op=OpCode.WRITE,
                    target=item.path,
                    payload=item.content or "",
                    metadata={'origin': origin, 'permissions': item.permissions, 'expected_hash': item.expected_hash,
                              'seed': item.seed_path},
                    line_num=item.line_num
                )
                self._io_pipeline.append(write_instr)
                self.program.append(write_instr)

                if item.permissions:
                    chmod_instr = Instruction(
                        op=OpCode.CHMOD,
                        target=item.path,
                        payload=item.permissions,
                        line_num=item.line_num
                    )
                    self._io_pipeline.append(chmod_instr)
                    self.program.append(chmod_instr)

        # Assemble the sequential shell execution pipeline
        if not self.regs.no_edicts:
            for cmd_tuple in commands:
                exec_instr = Instruction(
                    op=OpCode.EXEC,
                    target=cmd_tuple,
                    line_num=cmd_tuple[1]
                )
                self._exec_pipeline.append(exec_instr)
                self.program.append(exec_instr)

        self._warm_binary_cache()

        self.logger.verbose(
            f"Pipeline compiled: {len(self._io_pipeline)} file ops, {len(self._exec_pipeline)} commands.")

    def execute(self):
        """
        Orchestrates the entire execution run.
        """
        if not self.program:
            self.logger.verbose("No instructions found. Skipping execution.")
            return

        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        total_ops = len(self.program)
        start_ns = time.perf_counter_ns()

        try:
            threading.current_thread().name = f"QuantumCPU:{self.regs.project_root.name[:8]}"
        except Exception:
            pass

        can_use_spinner = hasattr(self.regs.console, "status") and not is_wasm

        if not self.regs.silent and can_use_spinner:
            status_ctx = self.regs.console.status("[bold cyan]Building project structure...[/]")
        else:
            if not self.regs.silent:
                self.regs.console.print("[bold cyan]🌀 Building project structure...[/]")
            status_ctx = nullcontext()

        try:
            with status_ctx:
                # --- PHASE I: I/O OPERATIONS ---
                if not self.regs.silent and hasattr(status_ctx, "update"):
                    status_ctx.update("[bold cyan]Step 1: Generating files in staging area...[/]")
                elif not self.regs.silent and not is_wasm:
                    self.logger.info("Step 1: Generating files in staging area...")

                self._execute_parallel_strata(status_ctx, force_sequential=is_wasm)

                # --- PHASE II: TRANSACTIONAL SYNC ---
                if self.regs.transaction and not self.regs.transaction.simulate:
                    if not self.regs.silent and hasattr(status_ctx, "update"):
                        status_ctx.update("[bold green]Step 2: Syncing files to project root...[/]")
                    elif not self.regs.silent and not is_wasm:
                        self.logger.info("Step 2: Syncing files to project root...")

                    self._verify_transaction_integrity()
                    self.regs.transaction.materialize()

                # --- PHASE III: SHELL COMMANDS ---
                if self._exec_pipeline:
                    if not self.regs.silent and hasattr(status_ctx, "update"):
                        status_ctx.update("[bold purple]Step 3: Running post-build commands...[/]")
                    elif not self.regs.silent and not is_wasm:
                        self.logger.info("Step 3: Running post-build commands...")

                    self._execute_shell_sequence(status_ctx)

        except Exception as failure:
            self._handle_system_halt(failure)
            self.regs.ui_hints = {"vfx": "shake", "sound": "fracture_critical", "priority": "CRITICAL"}

            if not isinstance(failure, ArtisanHeresy):
                raise ArtisanHeresy(
                    "EXECUTION_FAILED",
                    child_heresy=failure,
                    details=f"Opcodes: {total_ops} | Substrate: {'WASM' if is_wasm else 'NATIVE'}",
                    severity=HeresySeverity.CRITICAL
                ) from failure
            raise

        finally:
            if hasattr(self, '_thread_pool') and not is_wasm:
                try:
                    self._thread_pool.shutdown(wait=False)
                except Exception:
                    pass

            self._release_memory()

            total_duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.regs.silent:
                self.logger.success(f"Build process completed in {total_duration_ms:.2f}ms.")

            self.regs.metabolic_tax_ms = total_duration_ms
            self.regs.ops_conducted = total_ops

    # =========================================================================
    # == Pipeline Optimization & Prefetching                                 ==
    # =========================================================================

    def _warm_binary_cache(self):
        """
        Scans the execution pipeline for common binaries (make, npm, poetry) and caches
        their system paths. If a binary is missing, logs a warning before execution begins.
        """
        for instr in self._exec_pipeline:
            cmd_tuple = instr.target
            raw_cmd = cmd_tuple[0] if isinstance(cmd_tuple, tuple) else str(cmd_tuple)

            clean_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', raw_cmd).strip()
            if not clean_cmd: continue

            first_word = clean_cmd.split()[0].lower()

            if first_word in self._binary_l1_cache: continue
            if first_word in ['cd', 'echo', 'py:', 'js:', '>>', '??', '%%', '->', 'proclaim:', 'allow_fail:']: continue

            bin_path = shutil.which(first_word)
            if bin_path:
                self._binary_l1_cache[first_word] = bin_path
            else:
                self.logger.debug(f"Pre-flight Warning: Binary '{first_word}' is missing from system PATH.")

    def _trigger_prefetch(self, seed_path: Union[str, Path]):
        try:
            path_obj = Path(seed_path)
            if path_obj.exists() and path_obj.is_file():
                if path_obj.stat().st_size < 50 * 1024 * 1024:
                    self._thread_pool.submit(self._async_load_seed, path_obj)
        except Exception:
            pass

    def _async_load_seed(self, path: Path):
        try:
            self._prefetch_buffer[str(path)] = path.read_bytes()
        except Exception:
            pass

    def _verify_transaction_integrity(self):
        tx = getattr(self.regs, 'transaction', None)
        if tx and hasattr(tx, 'volume_shifter'):
            shifter = tx.volume_shifter
            if getattr(shifter, 'state', None) and shifter.state.name == "FRACTURED":
                raise ArtisanHeresy("File sync failed. Transaction staging area is locked.",
                                    severity=HeresySeverity.CRITICAL)

    def _release_memory(self):
        self._prefetch_buffer.clear()
        self.program.clear()
        self._io_pipeline.clear()
        self._exec_pipeline.clear()
        gc.collect(2)

    # =========================================================================
    # == INTERNAL PIPELINES (KINETIC EXECUTION)                              ==
    # =========================================================================

    def _execute_parallel_strata(self, status_ctx: Any, force_sequential: bool = False):
        if not self._io_pipeline:
            return

        strata: Dict[int, List[Any]] = defaultdict(list)
        for instr in self._io_pipeline:
            if isinstance(instr.target, (str, Path)):
                depth = len(Path(instr.target).parts)
            else:
                depth = 0
            strata[depth].append(instr)

        for depth in sorted(strata.keys()):
            batch = strata[depth]
            batch.sort(key=lambda x: str(x.target).lower())

            if not self.regs.silent and status_ctx and hasattr(status_ctx, 'update'):
                status_ctx.update(f"[bold cyan]Creating directory depth {depth} ({len(batch)} files)...[/]")
            elif not self.regs.silent:
                self.regs.console.print(f"[dim]   -> Depth {depth}: {len(batch)} files[/]")

            self._throttle_system_load()

            # In WASM (Emscripten IDBFS), concurrent heavy writes can lock the event loop.
            # We degrade to forced sequential execution to maintain browser stability.
            if force_sequential:
                for instr in batch:
                    try:
                        self._dispatch_instruction(instr)
                    except Exception as e:
                        self._handle_io_failure(instr, e)
            else:
                deduped_batch = {str(i.target): i for i in batch}.values()

                futures = {
                    self._thread_pool.submit(self._dispatch_instruction, instr): instr
                    for instr in deduped_batch
                }
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as execution_error:
                        instr = futures[future]
                        self._handle_io_failure(instr, execution_error)

        self._publish_progress_event(len(self._io_pipeline))

    def _handle_io_failure(self, instr: Any, e: Exception):
        err_msg = f"File creation failed at L{instr.line_num}: {str(e)}"
        self.logger.error(err_msg)
        raise ArtisanHeresy(
            err_msg,
            severity=HeresySeverity.CRITICAL,
            details=f"Opcode: {instr.op} | Target: {instr.target}",
            line_num=instr.line_num,
            suggestion="Verify filesystem permissions or available disk space."
        )

    def _publish_progress_event(self, count: int):
        """Radiates completion events to the front-end dashboard."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_MANIFESTED",
                        "label": "PROJECT_BUILDER",
                        "value": count,
                        "color": "#64ffda"
                    }
                })
            except:
                pass

    def _execute_shell_sequence(self, status_ctx: Any):
        for instr in self._exec_pipeline:
            cmd_str = str(instr.target[0]) if isinstance(instr.target, tuple) else str(instr.target)
            display_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', cmd_str).strip()

            if not self.regs.silent and hasattr(status_ctx, "update"):
                status_ctx.update(f"[bold yellow]Running command: {display_cmd[:30]}...[/]")
            self._dispatch_instruction(instr)

    def _dispatch_instruction(self, instr: Instruction):
        start_ns = time.perf_counter_ns()
        self.state_register = hashlib.md5(f"{self.state_register}:{instr.op.name}:{instr.target}".encode()).hexdigest()[
                              :8]

        try:
            if instr.op == OpCode.MKDIR:
                self._handle_mkdir(instr)
            elif instr.op == OpCode.WRITE:
                self._handle_write(instr)
            elif instr.op == OpCode.CHMOD:
                self._handle_chmod(instr)
            elif instr.op == OpCode.EXEC:
                self._handle_exec(instr)

            time.sleep(YIELD_MS)

            duration = (time.perf_counter_ns() - start_ns) / 1_000_000
            with self._telemetry_lock:
                self._instruction_telemetry[id(instr)] = {"duration_ms": duration, "status": "OK"}
        except Exception as e:
            with self._telemetry_lock:
                self._instruction_telemetry[id(instr)] = {"status": "ERROR", "error": str(e)}
            raise

    # =========================================================================
    # == HANDLER PANTHEON                                                    ==
    # =========================================================================

    def _handle_mkdir(self, instr: Instruction):
        for attempt in range(RETRY_THRESHOLD):
            try:
                if self.io.mkdir(Path(instr.target)):
                    with self._io_lock: self.regs.sanctums_forged += 1
                return
            except OSError:
                if attempt == RETRY_THRESHOLD - 1: raise
                time.sleep(YIELD_MS * (attempt + 2))

    def _handle_write(self, instr: Instruction):
        from pathlib import Path
        from ..contracts.data_contracts import InscriptionAction
        from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        logical_path = Path(str(instr.target).replace('\\', '/'))
        payload = instr.payload or ""
        seed_path = instr.metadata.get('seed')

        # Retrieve content from prefetch buffer if available
        if seed_path and str(seed_path) in self._prefetch_buffer:
            payload = self._prefetch_buffer[str(seed_path)]

        try:
            result = self.io.write(logical_path, payload, instr.metadata)
        except Exception as strike_fracture:
            raise ArtisanHeresy(
                f"Failed to write '{logical_path.name}'.",
                details=str(strike_fracture),
                line_num=instr.line_num,
                severity=HeresySeverity.CRITICAL
            )

        if result.success:
            with self._io_lock:
                self.regs.bytes_written += result.bytes_written
                if result.action_taken in (InscriptionAction.CREATED, InscriptionAction.DRY_RUN_CREATED):
                    self.regs.files_forged += 1
                self.regs.record_mutation(logical_path, result.bytes_written)

        if self.regs.transaction:
            self.regs.transaction.record(result)

        if self.regs.is_simulation:
            self.regs.virtual_fs.append(logical_path)

        if self.regs.ops_executed % 5 == 0:
            self.regs.pulse_hud("pulse", "#64ffda")

    def _handle_chmod(self, instr: Instruction):
        self.io.chmod(Path(instr.target), instr.payload)

    def _handle_exec(self, instr: Instruction):
        """
        Native interception of internal edicts (like `proclaim:`).
        Passes execution to the Maestro Conductor for safe shell evaluation.
        """
        cmd_tuple = instr.target
        parts = list(cmd_tuple) if isinstance(cmd_tuple, (tuple, list)) else [cmd_tuple]
        while len(parts) < 4:
            parts.append(None)

        cmd, line, undo, error_handlers = parts[:4]

        if isinstance(cmd, str):
            clean_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', cmd).strip()

            if clean_cmd.lower().startswith("proclaim:"):
                pass
            elif clean_cmd.lower().startswith("echo "):
                clean_cmd = "proclaim: " + clean_cmd[5:]

            cmd = clean_cmd

            if not cmd:
                return

        execution_env = self._build_subprocess_env()
        cmd = self._normalize_python_executables(cmd)

        self._publish_execution_start(cmd, line)

        try:
            self.maestro.execute((cmd, line, undo), env=execution_env)
        except Exception as failure:
            if error_handlers:
                self.logger.warn(f"L{line}: Command failed. Attempting recovery steps...")
                for recovery_cmd in error_handlers:
                    try:
                        self.maestro.execute((recovery_cmd, line, None), env=execution_env)
                    except Exception as nested_fail:
                        self.logger.error(f"Recovery Command Failed: {nested_fail}")

            if "127" in str(failure) or "not found" in str(failure).lower():
                self._diagnose_missing_executable(cmd, line)

            raise failure

    # =========================================================================
    # == ENVIRONMENT ISOLATION                                               ==
    # =========================================================================

    def _build_subprocess_env(self, env_from_caller: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Constructs an isolated, deterministic environment for subprocess execution.
        Automatically injects node_modules and virtualenv bin directories into the PATH.
        """
        import os
        import sys
        import platform
        import uuid
        import time
        from pathlib import Path

        creation_ns = time.perf_counter_ns()
        env = os.environ.copy()
        if env_from_caller:
            env.update(env_from_caller)

        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        raw_root = getattr(self.regs, 'project_root', None)
        if not raw_root and is_wasm:
            raw_root = "/vault/project"

        project_root = Path(raw_root or ".").resolve()

        tx = getattr(self.regs, 'transaction', None)
        if tx and hasattr(tx, 'volume_shifter') and getattr(tx.volume_shifter, 'state', None).name == "RESONANT":
            env["SCAFFOLD_VOLUME_ACTIVE"] = "1"

        path_lattice: List[str] = []
        path_sep = ";" if platform.system() == "Windows" else ":"

        # Prioritize local virtual environments
        for venv_name in [".venv", "venv", "env"]:
            bin_dir = "Scripts" if platform.system() == "Windows" else "bin"
            venv_path = project_root / venv_name / bin_dir
            if venv_path.exists():
                path_lattice.append(str(venv_path))
                env.pop("VIRTUAL_ENV", None)
                env["VIRTUAL_ENV"] = str(project_root / venv_name)
                break

        # Prioritize local node modules
        node_bin = project_root / "node_modules" / ".bin"
        if node_bin.exists():
            path_lattice.append(str(node_bin))

        python_bin_dir = Path(sys.executable).parent.resolve()
        path_lattice.append(str(python_bin_dir))

        current_path = env.get("PATH", "")
        if current_path:
            path_lattice.append(current_path)

        env["PATH"] = path_sep.join(path_lattice)

        current_python_path = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{str(project_root)}{path_sep}{current_python_path}"

        if platform.system() == "Windows":
            comspec = os.getenv("COMSPEC", "C:\\Windows\\system32\\cmd.exe")
            env["SHELL"] = comspec
            env["COMSPEC"] = comspec
            env["MAKE_MODE"] = "win32"
            env["MAKESHELL"] = comspec
            env["MSYS_NO_PATHCONV"] = "1"

        trace_id = os.environ.get("GNOSTIC_REQUEST_ID", getattr(self.regs, 'trace_id', f"tr-maes-{uuid4().hex[:4]}"))

        env["SCAFFOLD_TRACE_ID"] = trace_id
        env["GNOSTIC_REQUEST_ID"] = trace_id
        env["SCAFFOLD_SESSION_ID"] = getattr(self.regs, 'session_id', 'SCAF-CORE')
        env["SCAFFOLD_MACHINE_ID"] = str(platform.node())
        env["SCAFFOLD_RITE_START_TIME"] = str(creation_ns)

        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["LANG"] = "C.UTF-8"
        env["FORCE_COLOR"] = "1"
        env["TERM"] = "xterm-256color"

        if hasattr(self.context, 'command'):
            env["SC_MAESTRO_CMD"] = str(self.context.command)

        return env

    def _normalize_python_executables(self, command: str) -> str:
        """Ensures cross-platform reliability for core Python utilities."""
        parts = command.strip().split()
        if not parts: return command

        first_word = parts[0].lower()
        if first_word in self._binary_l1_cache:
            pass

        PYTHON_MAP = {
            "pip": "pip", "pytest": "pytest", "uvicorn": "uvicorn",
            "black": "black", "ruff": "ruff", "alembic": "alembic"
        }

        if first_word in PYTHON_MAP:
            self.logger.debug(f"Translating command '{first_word}' to '{sys.executable} -m {PYTHON_MAP[first_word]}'")
            exe_path = f'"{sys.executable}"'
            parts[0] = f"{exe_path} -m {PYTHON_MAP[first_word]}"
            return " ".join(parts)

        return command

    def _throttle_system_load(self):
        """Injects artificial latency if the host system CPU exceeds 90%."""
        if self.engine and hasattr(self.engine, 'watchdog'):
            vitals = self.engine.watchdog.get_vitals()
            if vitals.get("load_percent", 0) > 90.0:
                time.sleep(0.5)
                gc.collect(1)

    def _diagnose_missing_executable(self, cmd: str, line: int):
        executable = cmd.split()[0]
        self.logger.error(f"L{line}: Command '{executable}' is not installed or not in PATH.")
        if executable == "pytest":
            self.logger.info("Hint: `pip install pytest` is required to run tests.")
        elif executable == "git":
            self.logger.info("Hint: Git must be installed to use version control features.")

    def _publish_execution_start(self, cmd: str, line: int):
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "KINETIC_STRIKE",
                    "label": f"CMD: {cmd[:20]}...",
                    "color": "#fbbf24",
                    "line": line
                }
            })

    def _handle_system_halt(self, error: Exception):
        self.logger.critical(f"Execution halted at instruction {self.program_counter + 1} due to unhandled error.")

    def __repr__(self) -> str:
        return f"<QuantumCPU ops={len(self.program)} state=READY>"