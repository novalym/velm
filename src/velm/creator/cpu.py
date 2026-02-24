# Path: creator/cpu.py
# --------------------


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

# --- THE DIVINE UPLINKS ---
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

# [PHYSICS CONSTANTS OF THE VIRTUAL MACHINE]
MAX_IO_CONCURRENCY: Final[int] = 32
RETRY_THRESHOLD: Final[int] = 5
METABOLIC_YIELD_MS: Final[float] = 0.02
INSTRUCTION_CACHE_SIZE: Final[int] = 1024


class QuantumCPU:
    """
    =================================================================================
    == THE OMEGA QUANTUM CPU (V-Ω-TOTALITY-V1000.7-ALIEN-FORGE-HEALED)             ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_VIRTUAL_MACHINE | RANK: OMEGA_SINGULARITY
    AUTH: Ω_EXEC_V1000_PROCLAIM_SUTURE_FINALIS
    """

    def __init__(
            self,
            registers: QuantumRegisters,
            io_conductor: IOConductor,
            maestro: "MaestroUnit",
            engine: Optional["ScaffoldEngine"] = None
    ):
        import argparse

        # --- STRATUM-0: SOVEREIGN ORGAN BINDING ---
        self.regs = registers
        self.io = io_conductor
        self.maestro = maestro
        self.engine = engine
        self.logger = Logger

        # --- STRATUM-1: THE CONTEXTUAL SUTURE (ASCENSION 19) ---
        self.context = getattr(registers, 'context', None)
        if self.context is None:
            self.context = argparse.Namespace(
                command="genesis",
                cwd=Path.cwd(),
                env=os.environ.copy()
            )

        # --- STRATUM-2: ACHRONAL POINTERS & REGISTERS ---
        self.program_counter: int = 0
        self.instruction_pointer: int = 0
        self.is_halted: bool = False
        self._state_flags: int = 0x00

        # [ASCENSION 4]: Cryptographic State Registers
        self.csr: str = "0xINIT"

        # --- STRATUM-3: THE INSTRUCTION PIPELINE ---
        self.program: List[Instruction] = []
        self._form_pipeline: List[Instruction] = []
        self._will_pipeline: List[Instruction] = []

        # [ASCENSION 3]: Instruction Prefetch Buffer (IPB)
        self._prefetch_buffer: Dict[str, bytes] = {}

        # --- STRATUM-4: METABOLIC TOMOGRAPHY ---
        self._birth_ns: int = time.perf_counter_ns()
        self._instruction_telemetry: Dict[int, Dict[str, Any]] = {}
        self._state_merkle: str = "0xVOID"

        self._io_lock = threading.RLock()
        self._telemetry_lock = threading.Lock()

        # [ASCENSION 10]: Hyper-Threading Nexus
        self._cpu_cores = os.cpu_count() or 1
        self._active_workers = min(MAX_IO_CONCURRENCY, self._cpu_cores * 2)

        # [ASCENSION 12]: Isomorphic Binary Loader (L1 Cache)
        self._binary_l1_cache: Dict[str, str] = {}

        self._suture_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._active_workers,
            thread_name_prefix=f"TitanCPU-{self.regs.trace_id[:4]}"
        )

        self.trace_id = self.regs.trace_id
        self.session_id = self.regs.session_id

        self.logger.verbose(
            f"Quantum CPU [Ω] materialised. "
            f"Lattice: {self._active_workers} nodes | "
            f"Trace: {self.trace_id} | "
            f"Status: ALIEN_FORGE_READY"
        )

    def load_program(
            self,
            items: List[ScaffoldItem],
            commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]
    ):
        """
        =============================================================================
        == THE GNOSTIC COMPILER (V-Ω-TRI-PHASIC-SORT)                              ==
        =============================================================================
        Compiles the AST into two distinct pipelines (Form and Will) to facilitate
        the Tri-Phasic Execution Model (Form -> Sync -> Will).
        """
        self.program.clear()
        self._form_pipeline.clear()
        self._will_pipeline.clear()

        # 1. TOPOLOGICAL PRE-SORT (FORM)
        sorted_items = sorted(
            items,
            key=lambda x: (len(x.path.parts) if x.path else 0, not x.is_dir)
        )

        for item in sorted_items:
            if not item.path: continue

            if item.is_dir:
                instr = Instruction(op=OpCode.MKDIR, target=item.path, line_num=item.line_num)
                self._form_pipeline.append(instr)
                self.program.append(instr)
            else:
                origin = item.blueprint_origin or Path("unknown")

                # [ASCENSION 3]: Trigger Prefetching for large seeds
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
                self._form_pipeline.append(write_instr)
                self.program.append(write_instr)

                if item.permissions:
                    chmod_instr = Instruction(
                        op=OpCode.CHMOD,
                        target=item.path,
                        payload=item.permissions,
                        line_num=item.line_num
                    )
                    self._form_pipeline.append(chmod_instr)
                    self.program.append(chmod_instr)

        # 2. COMPILE WILL (KINETIC EDICTS)
        if not self.regs.no_edicts:
            for cmd_tuple in commands:
                exec_instr = Instruction(
                    op=OpCode.EXEC,
                    target=cmd_tuple,
                    line_num=cmd_tuple[1]
                )
                self._will_pipeline.append(exec_instr)
                self.program.append(exec_instr)

        # [ASCENSION 2]: Heuristic Branch Prediction
        self._predict_and_warm()

        self.logger.verbose(
            f"Compilation complete: {len(self._form_pipeline)} Form ops, {len(self._will_pipeline)} Will ops.")

    def execute(self):
        """
        =================================================================================
        == THE GRAND SYMPHONY OF EXECUTION (V-Ω-TOTALITY-V1000.5-TRI-PHASIC)           ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SINGULARITY
        """
        if not self.program:
            self.logger.verbose("Void Intent: Program is empty. Skipping Strike.")
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
            status_ctx = self.regs.console.status("[bold cyan]Quantum CPU: Materializing Reality...[/]")
        else:
            if not self.regs.silent:
                self.regs.console.print("[bold cyan]🌀 Quantum CPU: Materializing Reality...[/]")
            status_ctx = nullcontext()

        try:
            with status_ctx:

                # =========================================================================
                # == PHASE I: FETCH_FORM (PHYSICAL MATTER STRIKE)                        ==
                # =========================================================================
                if not self.regs.silent and hasattr(status_ctx, "update"):
                    status_ctx.update("[bold cyan]Movement I: Forging Form (Physical Matter into Staging)...[/]")
                elif not self.regs.silent and not is_wasm:
                    self.logger.info("Movement I: Forging Form (Physical Matter into Staging)...")

                self._execute_parallel_strata(status_ctx, force_sequential=is_wasm)

                # =========================================================================
                # == PHASE II: ACHRONAL_SYNC (THE VOLUME SUTURE)                         ==
                # =========================================================================
                if self.regs.transaction and not self.regs.transaction.simulate:
                    if not self.regs.silent and hasattr(status_ctx, "update"):
                        status_ctx.update("[bold green]Movement II: Achronal Volume Synchronization...[/]")
                    elif not self.regs.silent and not is_wasm:
                        self.logger.info("Movement II: Achronal Volume Synchronization...")

                    # [ASCENSION 22]: Pre-verify volume state
                    self._verify_volumetric_lock()

                    self.logger.verbose("CPU Halting pipeline to flush Staging to Shadow Volume...")
                    self.regs.transaction.materialize()
                    self.logger.verbose("CPU Pipeline resumed. Shadow Volume is now physically resonant.")

                # =========================================================================
                # == PHASE III: EXECUTE_WILL (KINETIC EDICTS)                            ==
                # =========================================================================
                if self._will_pipeline:
                    if not self.regs.silent and hasattr(status_ctx, "update"):
                        status_ctx.update("[bold purple]Movement III: Conducting Will (Kinetic Edicts)...[/]")
                    elif not self.regs.silent and not is_wasm:
                        self.logger.info("Movement III: Conducting Will (Kinetic Edicts)...")

                    self._execute_kinetic_sequence(status_ctx)

        except Exception as fracture:
            self._conduct_emergency_autopsy(fracture)
            self.regs.ui_hints = {"vfx": "shake", "sound": "fracture_critical", "priority": "CRITICAL"}

            if not isinstance(fracture, ArtisanHeresy):
                raise ArtisanHeresy(
                    "KINETIC_CPU_FRACTURE",
                    child_heresy=fracture,
                    details=f"Opcodes: {total_ops} | Substrate: {'WASM' if is_wasm else 'NATIVE'}",
                    severity=HeresySeverity.CRITICAL
                ) from fracture
            raise

        finally:
            if hasattr(self, '_suture_pool') and not is_wasm:
                try:
                    self._suture_pool.shutdown(wait=False)
                except Exception:
                    pass

            # [ASCENSION 15]: The Entropy Siphon
            self._siphon_entropy()

            total_duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.regs.silent:
                self.logger.success(f"Quantum CPU Halted. Totality achieved in {total_duration_ms:.2f}ms.")

            self.regs.metabolic_tax_ms = total_duration_ms
            self.regs.ops_conducted = total_ops

    # =========================================================================
    # == THE ALIEN ASCENSIONS (INTERNAL ORGANS)                              ==
    # =========================================================================

    def _predict_and_warm(self):
        """
        [ASCENSION 2 & 12]: Heuristic Branch Predictor & Isomorphic Binary Loader.
        Scans the Will pipeline for common binaries (make, npm, poetry) and caches
        their paths. If a binary is missing, it logs a prophetic warning before execution.
        """
        for instr in self._will_pipeline:
            cmd_tuple = instr.target
            raw_cmd = cmd_tuple[0] if isinstance(cmd_tuple, tuple) else str(cmd_tuple)

            clean_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', raw_cmd).strip()
            if not clean_cmd: continue

            first_word = clean_cmd.split()[0].lower()

            if first_word in self._binary_l1_cache:
                continue

            if first_word in ['cd', 'echo', 'py:', 'js:', '>>', '??', '%%', '->', 'proclaim:', 'allow_fail:']:
                continue

            bin_path = shutil.which(first_word)
            if bin_path:
                self._binary_l1_cache[first_word] = bin_path
            else:
                self.logger.debug(f"Branch Predictor Warning: Binary '{first_word}' unmanifest in PATH.")

    def _trigger_prefetch(self, seed_path: Union[str, Path]):
        try:
            path_obj = Path(seed_path)
            if path_obj.exists() and path_obj.is_file():
                if path_obj.stat().st_size < 50 * 1024 * 1024:
                    self._suture_pool.submit(self._async_load_seed, path_obj)
        except Exception:
            pass

    def _async_load_seed(self, path: Path):
        try:
            self._prefetch_buffer[str(path)] = path.read_bytes()
        except Exception:
            pass

    def _verify_volumetric_lock(self):
        tx = getattr(self.regs, 'transaction', None)
        if tx and hasattr(tx, 'volume_shifter'):
            shifter = tx.volume_shifter
            if getattr(shifter, 'state', None) and shifter.state.name == "FRACTURED":
                raise ArtisanHeresy(
                    "Volumetric State Heresy: The Shadow Volume is fractured. Cannot synchronize.",
                    severity=HeresySeverity.CRITICAL
                )

    def _siphon_entropy(self):
        self._prefetch_buffer.clear()
        self.program.clear()
        self._form_pipeline.clear()
        self._will_pipeline.clear()
        gc.collect(2)

    # =========================================================================
    # == INTERNAL PIPELINES (KINETIC EXECUTION)                              ==
    # =========================================================================

    def _execute_parallel_strata(self, status_ctx: Any, force_sequential: bool = False):
        if not self._form_pipeline:
            return

        strata: Dict[int, List[Any]] = defaultdict(list)
        for instr in self._form_pipeline:
            if isinstance(instr.target, (str, Path)):
                depth = len(Path(instr.target).parts)
            else:
                depth = 0
            strata[depth].append(instr)

        for depth in sorted(strata.keys()):
            batch = strata[depth]
            batch.sort(key=lambda x: str(x.target).lower())

            if not self.regs.silent and status_ctx and hasattr(status_ctx, 'update'):
                status_ctx.update(f"[bold cyan]🏗️  Materializing Stratum {depth} ({len(batch)} atoms)...[/]")
            elif not self.regs.silent:
                self.regs.console.print(f"[dim]   -> Stratum {depth}: {len(batch)} atoms[/]")

            self._check_metabolic_fever()

            if force_sequential:
                for instr in batch:
                    try:
                        self._dispatch_instruction(instr)
                    except Exception as e:
                        self._handle_matter_failure(instr, e)
            else:
                deduped_batch = {str(i.target): i for i in batch}.values()

                futures = {
                    self._suture_pool.submit(self._dispatch_instruction, instr): instr
                    for instr in deduped_batch
                }
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as paradox:
                        instr = futures[future]
                        self._handle_matter_failure(instr, paradox)

        self._multicast_strata_completion(len(self._form_pipeline))

    def _handle_matter_failure(self, instr: Any, e: Exception):
        err_msg = f"Matter Fission Failure at L{instr.line_num}: {str(e)}"
        self.logger.error(err_msg)
        raise ArtisanHeresy(
            err_msg,
            severity=HeresySeverity.CRITICAL,
            details=f"Opcode: {instr.op} | Target: {instr.target}",
            line_num=instr.line_num,
            suggestion="Verify filesystem permissions or available Gnostic space."
        )

    def _multicast_strata_completion(self, count: int):
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_MANIFESTED",
                        "label": "GNOSTIC_FORGE",
                        "value": count,
                        "color": "#64ffda"
                    }
                })
            except:
                pass

    def _execute_kinetic_sequence(self, status_ctx: Any):
        for instr in self._will_pipeline:
            # We strip purely for the UI display
            cmd_str = str(instr.target[0]) if isinstance(instr.target, tuple) else str(instr.target)
            display_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', cmd_str).strip()

            if not self.regs.silent and hasattr(status_ctx, "update"):
                status_ctx.update(f"[bold yellow]Executing Edict: {display_cmd[:30]}...[/]")
            self._dispatch_instruction(instr)

    def _dispatch_instruction(self, instr: Instruction):
        start_ns = time.perf_counter_ns()
        self.csr = hashlib.md5(f"{self.csr}:{instr.op.name}:{instr.target}".encode()).hexdigest()[:8]

        try:
            if instr.op == OpCode.MKDIR:
                self._handle_mkdir(instr)
            elif instr.op == OpCode.WRITE:
                self._handle_write(instr)
            elif instr.op == OpCode.CHMOD:
                self._handle_chmod(instr)
            elif instr.op == OpCode.EXEC:
                self._handle_exec(instr)

            time.sleep(METABOLIC_YIELD_MS)

            duration = (time.perf_counter_ns() - start_ns) / 1_000_000
            with self._telemetry_lock:
                self._instruction_telemetry[id(instr)] = {"duration_ms": duration, "status": "PURE"}
        except Exception as e:
            with self._telemetry_lock:
                self._instruction_telemetry[id(instr)] = {"status": "FRACTURED", "error": str(e)}
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
                time.sleep(METABOLIC_YIELD_MS * (attempt + 2))

    def _handle_write(self, instr: Instruction):
        path = Path(instr.target)
        payload = instr.payload
        seed_path = instr.metadata.get('seed')
        if seed_path and str(seed_path) in self._prefetch_buffer:
            payload = self._prefetch_buffer[str(seed_path)]

        result = self.io.write(path, payload, instr.metadata)

        if result.success:
            with self._io_lock:
                self.regs.bytes_written += result.bytes_written
                if result.action_taken == InscriptionAction.CREATED:
                    self.regs.files_forged += 1

        if self.regs.transaction:
            self.regs.transaction.record(result)

    def _handle_chmod(self, instr: Instruction):
        self.io.chmod(Path(instr.target), instr.payload)

    def _handle_exec(self, instr: Instruction):
        """
        =============================================================================
        == THE OMEGA KINETIC CONDUCTOR (V-Ω-TOTALITY-V514-PROCLAIM-SUTURE)         ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_DISPATCHER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_EXEC_V514_PROCLAIM_INTERCEPT_FINALIS

        [THE CURE]: The CPU now natively intercepts `proclaim:` edicts and passes them
        directly to the Maestro's `proclaim` handler, bypassing the OS shell entirely.
        This annihilates the `Exit Code 1` heresy caused by arrows (`->`) leaking into bash.
        """
        # --- MOVEMENT I: THE GNOSTIC N-TUPLE SIEVE ---
        cmd_tuple = instr.target
        parts = list(cmd_tuple) if isinstance(cmd_tuple, (tuple, list)) else [cmd_tuple]
        while len(parts) < 4:
            parts.append(None)

        cmd, line, undo, heresy_cmds = parts[:4]

        # --- MOVEMENT II: THE SIGIL EXORCISM (THE WARD) ---
        if isinstance(cmd, str):
            # 1. Universal Arrow Exorcism. Strips '->' and '>>' and '!!' perfectly.
            # Using zero-or-more quantifiers to catch '-> >> ' or just '-> '
            clean_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', cmd).strip()

            # 2. PROCLAMATION INTERCEPT (THE CURE)
            # If the command is a proclamation, we transmute it into a direct handler call.
            # We preserve the 'proclaim:' prefix so the Maestro can route it to ProclaimHandler.
            if clean_cmd.lower().startswith("proclaim:"):
                # We strip potential outer quotes around the whole command if present
                # but let the handler deal with the message content
                pass
            elif clean_cmd.lower().startswith("echo "):
                # Transmute echo to proclaim for internal consistency
                clean_cmd = "proclaim: " + clean_cmd[5:]

            # 3. Update the command variable for execution
            cmd = clean_cmd

            # 4. Handle the Void
            if not cmd:
                self.logger.warn(f"L{line}: Kinetic Void perceived. Skipping empty edict.")
                return

        # --- MOVEMENT III: ENVIRONMENT DNA & TRANSMUTATION ---
        execution_env = self._terraform_environment()
        transmuted_cmd = self._transmute_artisan_plea(cmd)
        self._multicast_kinetic_start(transmuted_cmd, line)

        # --- MOVEMENT IV: THE STRIKE & REDEMPTION ---
        try:
            # [STRIKE]: Execute via the Maestro
            self.maestro.execute((transmuted_cmd, line, undo), env=execution_env)

        except Exception as fracture:
            # [ASCENSION 9]: THE RITE OF CASCADING REDEMPTION
            if heresy_cmds:
                self.logger.warn(f"L{line}: Rite fractured. Initiating Redemption Sequence...")
                for h_cmd in heresy_cmds:
                    try:
                        self.maestro.execute((h_cmd, line, None), env=execution_env)
                    except Exception as nested_fail:
                        self.logger.error(f"Redemption Fragment Failed: {nested_fail}")

            if "127" in str(fracture) or "not found" in str(fracture).lower():
                self._diagnose_missing_artisan(cmd, line)

            raise fracture

    # =========================================================================
    # == ALCHEMICAL UTILITIES                                                ==
    # =========================================================================

    def _terraform_environment(self, env_from_caller: Optional[Dict[str, str]] = None) -> Dict[str, str]:
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

        for venv_name in [".venv", "venv", "env"]:
            bin_dir = "Scripts" if platform.system() == "Windows" else "bin"
            venv_path = project_root / venv_name / bin_dir
            if venv_path.exists():
                path_lattice.append(str(venv_path))
                env.pop("VIRTUAL_ENV", None)
                env["VIRTUAL_ENV"] = str(project_root / venv_name)
                break

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

        if os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            env["SCAFFOLD_PRIORITY"] = "HIGH"
            env["NODE_OPTIONS"] = "--max-old-space-size=4096"

        if hasattr(self.context, 'command'):
            env["SC_MAESTRO_CMD"] = str(self.context.command)

        return env

    def _transmute_artisan_plea(self, command: str) -> str:
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
            self.logger.debug(f"Transmuting Artisan: {first_word} -> {sys.executable} -m {PYTHON_MAP[first_word]}")
            exe_path = f'"{sys.executable}"'
            parts[0] = f"{exe_path} -m {PYTHON_MAP[first_word]}"
            return " ".join(parts)

        return command

    def _check_metabolic_fever(self):
        if self.engine and hasattr(self.engine, 'watchdog'):
            vitals = self.engine.watchdog.get_vitals()
            if vitals.get("load_percent", 0) > 90.0:
                self.logger.verbose("Metabolic Fever detected. Injecting Yield Protocol.")
                time.sleep(0.5)
                gc.collect(1)

    def _diagnose_missing_artisan(self, cmd: str, line: int):
        artisan = cmd.split()[0]
        self.logger.error(f"L{line}: Artisan '{artisan}' is unmanifest in this reality.")
        if artisan == "pytest":
            self.logger.info("💡 Hint: `pip install pytest` is required for this Vow.")
        elif artisan == "git":
            self.logger.info("💡 Hint: Git is not installed on the host machine.")

    def _multicast_kinetic_start(self, cmd: str, line: int):
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "KINETIC_STRIKE",
                    "label": f"STRIKE: {cmd[:20]}...",
                    "color": "#fbbf24",
                    "line": line
                }
            })

    def _conduct_emergency_autopsy(self, error: Exception):
        self.logger.critical(f"QUANTUM_CPU_HALT: Reality collapsed at Op {self.program_counter + 1} / CSR: {self.csr}.")

    def __repr__(self) -> str:
        return f"<Ω_QUANTUM_CPU program_len={len(self.program)} csr={self.csr} state=ALIEN_FORGE_RESONANT>"