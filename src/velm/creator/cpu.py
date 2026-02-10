# Path: src/velm/creator/cpu.py
# -----------------------------
# LIF: INFINITY | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SUPREME
# AUTH_CODE: #@#()#!)(@#()) | VERSION: Ω-V500.0-TOTALITY
# =========================================================================================

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
from typing import List, Tuple, Optional, Set, Union, TYPE_CHECKING, Any, Dict, Final

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
    from ..runtime.engine import ScaffoldEngine

Logger = Scribe("QuantumCPU")

# [PHYSICS CONSTANTS]
MAX_IO_CONCURRENCY: Final[int] = 16
RETRY_THRESHOLD: Final[int] = 3
METABOLIC_YIELD_MS: Final[float] = 0.05


class QuantumCPU:
    """
    =================================================================================
    == THE OMEGA QUANTUM CPU (V-Ω-TOTALITY-V500.0-INDESTRUCTIBLE)                  ==
    =================================================================================
    The Supreme Executioner of the God-Engine. It transmutes the Architect's
    Gnosis into Physical Matter with absolute precision and parallel speed.
    """

    def __init__(self,
                 registers: QuantumRegisters,
                 io_conductor: IOConductor,
                 maestro: "MaestroUnit",
                 engine: Optional["ScaffoldEngine"] = None):
        """
        [THE RITE OF INCEPTION]
        Binds the CPU to the Engine organs.
        """
        self.regs = registers
        self.io = io_conductor
        self.maestro = maestro
        self.engine = engine
        self.logger = Logger

        # --- THE INTERNAL STRATA ---
        self.program: List[Instruction] = []
        self._io_lock = threading.Lock()
        self._telemetry_lock = threading.Lock()

        # [ASCENSION 1]: The Suture Pool for Parallel Materialization
        self._suture_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=MAX_IO_CONCURRENCY,
            thread_name_prefix="SutureNode"
        )

        # [ASCENSION 9]: Metabolic Tomography Registry
        self._instruction_telemetry: Dict[int, Dict[str, Any]] = {}

        self.logger.verbose("Quantum CPU materialised. Concurrency Lattice: ACTIVE.")

    def load_program(
            self,
            items: List[ScaffoldItem],
            commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]
    ):
        """
        =============================================================================
        == THE GNOSTIC COMPILER (V-Ω-TOPOLOGICAL-SORT)                             ==
        =============================================================================
        [ASCENSION 3 & 5]: Compiles Form and Will into a safe, ordered instruction set.
        """
        self.program.clear()

        # 1. TOPOLOGICAL PRE-SORT
        # [THE CURE]: Directories MUST precede files to prevent "Sanctum Void" errors.
        # We sort by depth, then by type (dirs first).
        sorted_items = sorted(
            items,
            key=lambda x: (len(x.path.parts) if x.path else 0, not x.is_dir)
        )

        # 2. COMPILE FORM (PHYSICAL MATTER)
        for item in sorted_items:
            if not item.path: continue

            if item.is_dir:
                self.program.append(Instruction(
                    op=OpCode.MKDIR,
                    target=item.path,
                    line_num=item.line_num
                ))
            else:
                # [ASCENSION 4]: IN integrity scrying
                origin = item.blueprint_origin or Path("unknown")
                self.program.append(Instruction(
                    op=OpCode.WRITE,
                    target=item.path,
                    payload=item.content or "",
                    metadata={
                        'origin': origin,
                        'permissions': item.permissions,
                        'expected_hash': item.expected_hash
                    },
                    line_num=item.line_num
                ))

                if item.permissions:
                    self.program.append(Instruction(
                        op=OpCode.CHMOD,
                        target=item.path,
                        payload=item.permissions,
                        line_num=item.line_num
                    ))

        # 3. COMPILE WILL (KINETIC EDICTS)
        if not self.regs.no_edicts:
            for cmd_tuple in commands:
                self.program.append(Instruction(
                    op=OpCode.EXEC,
                    target=cmd_tuple,
                    line_num=cmd_tuple[1]
                ))

        self.logger.verbose(f"Compilation complete: {len(self.program)} Opcodes in memory.")

    def execute(self):
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EXECUTION (V-Ω-TOTALITY)                          ==
        =============================================================================
        LIF: INFINITY | Conducts the materialization of reality.
        """
        if not self.program:
            return

        total_ops = len(self.program)
        start_ns = time.perf_counter_ns()

        status_ctx = self.regs.console.status(
            "[bold cyan]Quantum CPU: Materializing Reality...[/]"
        ) if not self.regs.silent else nullcontext()

        try:
            with status_ctx:
                # --- MOVEMENT I: THE RITE OF FORM (PARALLEL I/O) ---
                # We identify groups of I/O instructions that can be safely run in parallel.
                # (Instructions at the same depth level in the file tree).
                self._execute_parallel_strata(status_ctx)

                # --- MOVEMENT II: THE RITE OF WILL (SEQUENTIAL KINETIC) ---
                # Shell commands remain sequential to preserve causal state (cd, export, etc).
                self._execute_kinetic_sequence(status_ctx)

        except Exception as fracture:
            self._conduct_emergency_autopsy(fracture)
            raise

        finally:
            self._suture_pool.shutdown(wait=False)
            total_duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.regs.silent:
                self.logger.success(f"Quantum CPU Halted. Totality achieved in {total_duration_ms:.2f}ms.")

    # =========================================================================
    # == INTERNAL ORGANS (KINETIC EXECUTION)                                 ==
    # =========================================================================

    def _execute_parallel_strata(self, status_ctx: Any):
        """
        [ASCENSION 1]: Materializes physical matter shards in parallel blocks.
        """
        io_instructions = [i for i in self.program if i.op in (OpCode.MKDIR, OpCode.WRITE, OpCode.CHMOD)]
        if not io_instructions: return

        # Group by tree depth to ensure parent directories exist before children.
        strata: Dict[int, List[Instruction]] = collections.defaultdict(list)
        for instr in io_instructions:
            depth = len(Path(instr.target).parts) if isinstance(instr.target, Path) else 0
            strata[depth].append(instr)

        for depth in sorted(strata.keys()):
            batch = strata[depth]
            if not self.regs.silent and status_ctx:
                status_ctx.update(f"[bold cyan]Materializing Stratum {depth} ({len(batch)} atoms)...[/]")

            # [ASCENSION 11]: Hydraulic Governor
            self._check_metabolic_fever()

            futures = {self._suture_pool.submit(self._dispatch_instruction, instr): instr for instr in batch}

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    instr = futures[future]
                    raise ArtisanHeresy(
                        f"Matter Fission Failure at L{instr.line_num}: {e}",
                        severity=HeresySeverity.CRITICAL,
                        details=f"Opcode: {instr.op.name} | Target: {instr.target}"
                    )

    def _execute_kinetic_sequence(self, status_ctx: Any):
        """
        [ASCENSION 2 & 12]: Executes shell commands with Venv Suture.
        """
        kinetic_instructions = [i for i in self.program if i.op == OpCode.EXEC]
        for instr in kinetic_instructions:
            if not self.regs.silent and status_ctx:
                status_ctx.update(f"[bold yellow]Executing Edict: {str(instr.target[0])[:30]}...[/]")
            self._dispatch_instruction(instr)

    def _dispatch_instruction(self, instr: Instruction):
        """
        [THE ATOMIC HAND]
        Directs a single opcode to its handler with Metabolic Tomography.
        """
        start_ns = time.perf_counter_ns()

        try:
            # 1. RITE TRIAGE
            if instr.op == OpCode.MKDIR:
                self._handle_mkdir(instr)
            elif instr.op == OpCode.WRITE:
                self._handle_write(instr)
            elif instr.op == OpCode.CHMOD:
                self._handle_chmod(instr)
            elif instr.op == OpCode.EXEC:
                self._handle_exec(instr)

            # 2. [ASCENSION 9]: RECORD TOMOGRAPHY
            duration = (time.perf_counter_ns() - start_ns) / 1_000_000
            with self._telemetry_lock:
                self._instruction_telemetry[id(instr)] = {
                    "duration_ms": duration,
                    "status": "PURE"
                }

        except Exception as e:
            with self._telemetry_lock:
                self._instruction_telemetry[id(instr)] = {"status": "FRACTURED", "error": str(e)}
            raise

    # =========================================================================
    # == HANDLER PANTHEON                                                    ==
    # =========================================================================

    def _handle_mkdir(self, instr: Instruction):
        # [ASCENSION 6]: Lazarus Retry for MKDIR
        for attempt in range(RETRY_THRESHOLD):
            try:
                if self.io.mkdir(Path(instr.target)):
                    with self._io_lock: self.regs.sanctums_forged += 1
                return
            except OSError:
                if attempt == RETRY_THRESHOLD - 1: raise
                time.sleep(METABOLIC_YIELD_MS * (attempt + 1))

    def _handle_write(self, instr: Instruction):
        # [ASCENSION 8]: REAL-TIME INTEGRITY SEALING
        path = Path(instr.target)
        result = self.io.write(path, instr.payload, instr.metadata)

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
        [THE RITE OF RESILIENT EXECUTION]
        Terraforms the environment and conducts the strike.
        """
        cmd_tuple = instr.target
        cmd, line, undo, heresy_cmds = (cmd_tuple if len(cmd_tuple) == 4 else (*cmd_tuple, None))

        # [ASCENSION 8 & 10]: THE VAULT SEAL
        # Suture the environment with Venv resonance and trace identity.
        execution_env = self._terraform_environment()

        # [ASCENSION 2]: THE SACRED PROXY
        transmuted_cmd = self._transmute_artisan_plea(cmd)

        # [ASCENSION 4]: HUD NOTIFICATION
        self._multicast_kinetic_start(transmuted_cmd, line)

        try:
            # THE KINETIC STRIKE
            self.maestro.execute((transmuted_cmd, line, undo), env=execution_env)

        except Exception as fracture:
            # THE RITE OF REDEMPTION
            if heresy_cmds:
                self.logger.warn(f"L{line}: Rite fractured. Initiating Redemption Sequence.")
                for h_cmd in heresy_cmds:
                    self.maestro.execute((h_cmd, line, None), env=execution_env)

            # [ASCENSION 9]: LAZARUS PROBE
            if "127" in str(fracture) or "not found" in str(fracture).lower():
                self._diagnose_missing_artisan(cmd, line)

            raise fracture

    # =========================================================================
    # == ALCHEMICAL UTILITIES                                                ==
    # =========================================================================

    def _terraform_environment(self) -> Dict[str, str]:
        """
        [ASCENSION 2 & 10]: THE VENV SUTURE.
        Forges a perfect execution environment.
        """
        env = os.environ.copy()

        # 1. THE PATH SUTURE (Venv Awareness)
        python_bin_dir = os.path.dirname(sys.executable)
        path_sep = ";" if platform.system() == "Windows" else ":"

        # We prepend to ensure our venv binaries have absolute priority.
        env["PATH"] = f"{python_bin_dir}{path_sep}{env.get('PATH', '')}"

        # 2. THE SILVER CORD (Tracing)
        trace_id = os.environ.get("GNOSTIC_REQUEST_ID", f"tr-cpu-{uuid4().hex[:4]}")
        env["SCAFFOLD_TRACE_ID"] = trace_id
        env["PYTHONUNBUFFERED"] = "1"

        # 3. [ASCENSION 10]: THE VAULT MASK
        # Mask sensitive variables from child process stdout/stderr
        env["SCAFFOLD_SECRET_MASK"] = "True"

        return env

    def _transmute_artisan_plea(self, command: str) -> str:
        """
        [ASCENSION 2]: THE MODULE TRANSMUTER.
        Replaces 'pip' with 'python -m pip' to survive broken symlinks.
        """
        parts = command.strip().split()
        if not parts: return command

        # The Grimoire of Pythonic Artisans
        PYTHON_MAP = {
            "pip": "pip", "pytest": "pytest", "uvicorn": "uvicorn",
            "black": "black", "ruff": "ruff", "alembic": "alembic"
        }

        artisan = parts[0].lower()
        if artisan in PYTHON_MAP:
            self.logger.debug(f"Transmuting Artisan: {artisan} -> {sys.executable} -m {PYTHON_MAP[artisan]}")
            # [ASCENSION 7]: Indestructible Handle for Windows
            exe_path = f'"{sys.executable}"'
            parts[0] = f"{exe_path} -m {PYTHON_MAP[artisan]}"
            return " ".join(parts)

        return command

    def _check_metabolic_fever(self):
        """[ASCENSION 11]: ADAPTIVE THROTTLING."""
        if self.engine and hasattr(self.engine, 'watchdog'):
            vitals = self.engine.watchdog.get_vitals()
            if vitals.get("load_percent", 0) > 90.0:
                self.logger.verbose("Metabolic Fever detected. Injecting Yield Protocol.")
                time.sleep(0.5)
                gc.collect()

    def _diagnose_missing_artisan(self, cmd: str, line: int):
        """[ASCENSION 9]: SOCRATIC EXIT-CODE TRIAGE."""
        artisan = cmd.split()[0]
        self.logger.error(f"L{line}: Artisan '{artisan}' is unmanifest in this reality.")

        # The Path to Redemption
        if artisan == "pytest":
            self.logger.info("💡 Hint: `pip install pytest` is required for this Vow.")
        elif artisan == "git":
            self.logger.info("💡 Hint: Git is not installed on the host machine.")

    def _multicast_kinetic_start(self, cmd: str, line: int):
        """Broadcasts to Ocular HUD."""
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
        """[ASCENSION 12]: THE FINALITY VOW."""
        self.logger.critical(f"QUANTUM_CPU_HALT: Reality collapsed at Op {self.program_counter + 1}.")
        if self.engine and hasattr(self.engine, 'healer'):
            # Pass to the high priest for forensic enshrinement
            pass

    def __repr__(self) -> str:
        return f"<Ω_QUANTUM_CPU program_len={len(self.program)} state=RESONANT>"