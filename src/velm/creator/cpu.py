# Path: src/velm/creator/cpu.py
# -----------------------------
# LIF: INFINITY | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SUPREME
# AUTH_CODE: #@#()#!)(@#()) | VERSION: Ω-V500.0-TOTALITY
# =========================================================================================
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
from typing import List, Tuple, Optional, Set, Union, TYPE_CHECKING, Any, Dict, Final
from collections import defaultdict
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

    def __init__(
            self,
            registers: QuantumRegisters,
            io_conductor: IOConductor,
            maestro: "MaestroUnit",
            engine: Optional["ScaffoldEngine"] = None
    ):
        """
        =================================================================================
        == THE RITE OF CPU INCEPTION (V-Ω-TOTALITY-V505.0-CONTEXT-HEALED)              ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_EXECUTOR | RANK: OMEGA_SUPREME
        AUTH: Ω_CPU_INIT_V505_CONTEXT_SUTURE_2026_FINALIS

        The materialization of the Quantum CPU. This rite establishes the
        fundamental organs of execution, including the Instruction Pointer,
        the Metabolic Telemetry lattice, and the Hydraulic Thread Pool.

        [ASCENSION LOG]:
        1.  **Contextual Suture (THE FIX):** Explicitly initializes `self.context`
            using a safe proxy from `registers.context` or a void Namespace.
            This annihilates the `AttributeError` in `_terraform_environment`.
        2.  **Organ Binding:** Sutures the IO, Maestro, and Engine references.
        3.  **Achronal Pointers:** Zeros the Program Counter and Instruction Pointer.
        4.  **Metabolic Tomography:** Establishes nanosecond-precision birth timestamps.
        5.  **Merkle Accumulator:** Prepares the `_state_merkle` for integrity hashing.
        6.  **Hydraulic Concurrency:** Dynamically sizes the `_suture_pool` based on
            host CPU cores (Iron) vs. clamped limits (Wasm).
        7.  **Sovereign Identity:** Inherits `trace_id` and `session_id` from Registers.
        """
        import argparse  # Ensure local availability for the void proxy

        # --- STRATUM-0: SOVEREIGN ORGAN BINDING ---
        self.regs = registers
        self.io = io_conductor
        self.maestro = maestro
        self.engine = engine
        self.logger = Logger

        # --- STRATUM-1: THE CONTEXTUAL SUTURE (THE CURE) ---
        # We ensure 'self.context' exists. We prioritize the register's context,
        # falling back to a safe Void Namespace to satisfy 'hasattr' checks.
        self.context = getattr(registers, 'context', None)
        if self.context is None:
            # Create a safe proxy that won't crash on attribute access
            self.context = argparse.Namespace(
                command="genesis",
                cwd=Path.cwd(),
                env=os.environ.copy()
            )

        # --- STRATUM-2: ACHRONAL POINTERS ---
        self.program_counter: int = 0
        self.instruction_pointer: int = 0
        self.is_halted: bool = False

        # [ASCENSION 2]: Logic Flags (Bitmask for high-speed state scrying)
        # 0x01: ADRENALINE, 0x02: PANIC, 0x04: TRACE_ACTIVE
        self._state_flags: int = 0x00

        # --- STRATUM-3: THE PROGRAM BUFFER ---
        # [ASCENSION 8]: Pre-allocated vessel for the Compiled Gnostic Program.
        self.program: List[Instruction] = []

        # --- STRATUM-4: METABOLIC TOMOGRAPHY & TELEMETRY ---
        # [ASCENSION 3 & 9]: Nanosecond Chronometry and forensic history.
        self._birth_ns: int = time.perf_counter_ns()
        self._instruction_telemetry: Dict[int, Dict[str, Any]] = {}

        # [ASCENSION 5]: Merkle Accumulator (Running hash of physical transmutations)
        self._state_merkle: str = "0xVOID"

        # --- STRATUM-5: HYDRAULIC CONCURRENCY GRID ---
        # [ASCENSION 6]: Atomic guards for thread-safe materialization.
        self._io_lock = threading.Lock()
        self._telemetry_lock = threading.Lock()

        # [ASCENSION 4]: THE SUTURE POOL
        # Dynamically calculates worker density based on hardware substrate.
        # In WASM, os.cpu_count might be None or 1.
        cpu_count = os.cpu_count() or 1
        final_workers = min(MAX_IO_CONCURRENCY, cpu_count * 2)

        self._suture_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=final_workers,
            thread_name_prefix=f"TitanCPU-{self.regs.trace_id[:4]}"
        )

        # --- STRATUM-6: OCULAR & TRACE SUTURE ---
        # [ASCENSION 11]: Projecting context DNA from the Registers.
        self.trace_id = self.regs.trace_id
        self.session_id = self.regs.session_id

        # [ASCENSION 12]: THE FINALITY VOW
        # The CPU is now manifest. We proclaim its resonance to the log.
        self.logger.verbose(
            f"Quantum CPU [Ω] materialised. "
            f"Lattice: {final_workers} nodes | "
            f"Trace: {self.trace_id} | "
            f"Status: RESONANT"
        )


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
        == THE GRAND SYMPHONY OF EXECUTION (V-Ω-TOTALITY-V505.5-WASM-STABILIZED)   ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SUPREME
        AUTH_CODE: Ω_EXECUTE_V505_THREAD_SILENCE_2026_FINALIS
        """
        import time
        import os
        import sys
        from contextlib import nullcontext

        if not self.program:
            self.logger.verbose("Void Intent: Program is empty. Skipping Strike.")
            return

        # [ASCENSION 1]: SUBSTRATE IDENTITY DIVINATION (THE FIX)
        # We divine the substrate at nanosecond zero to ensure the identity
        # is available to the error handlers in the event of an early fracture.
        # This annihilates the 'UnboundLocalError: local variable is_wasm' heresy.
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        total_ops = len(self.program)
        start_ns = time.perf_counter_ns()

        # [ASCENSION 11]: SOVEREIGN IDENTITY
        try:
            import threading
            threading.current_thread().name = f"QuantumCPU:{self.regs.project_root.name[:8]}"
        except Exception:
            pass

        # =========================================================================
        # == [THE CURE]: THE THREAD-SILENCE VOW                                  ==
        # =========================================================================
        # We scry the substrate and the console. If we are in WASM, we FORBID the
        # Rich Status Spinner, as it attempts to spawn an illegal background thread.
        # This annihilates the 'RuntimeError: can't start new thread' heresy.
        can_use_spinner = hasattr(self.regs.console, "status") and not is_wasm

        if not self.regs.silent and can_use_spinner:
            status_ctx = self.regs.console.status(
                "[bold cyan]Quantum CPU: Materializing Reality...[/]"
            )
        else:
            # Passive Proclamation for Thread-silent or Silent environments
            if not self.regs.silent:
                self.regs.console.print("[bold cyan]🌀 Quantum CPU: Materializing Reality...[/]")
            status_ctx = nullcontext()
        # =========================================================================

        try:
            with status_ctx:
                # --- MOVEMENT I: THE RITE OF FORM ---

                # [THE FIX]: DEFENSIVE UPDATE GUARD
                # Prevents 'nullcontext' object has no attribute 'update' errors.
                if not self.regs.silent and hasattr(status_ctx, "update"):
                    status_ctx.update("[bold cyan]Movement I: Forging Form (Physical Matter)...[/]")
                elif not self.regs.silent and not is_wasm:
                    self.logger.info("Movement I: Forging Form (Physical Matter)...")

                # Conduct the Form Materialization
                # force_sequential is mandatory in WASM to avoid ThreadPool collisions
                self._execute_parallel_strata(status_ctx, force_sequential=is_wasm)

                # --- MOVEMENT II: THE RITE OF WILL ---
                if not self.regs.silent and hasattr(status_ctx, "update"):
                    status_ctx.update("[bold purple]Movement II: Conducting Will (Kinetic Edicts)...[/]")
                elif not self.regs.silent and not is_wasm:
                    self.logger.info("Movement II: Conducting Will (Kinetic Edicts)...")

                self._execute_kinetic_sequence(status_ctx)

        except Exception as fracture:
            # [ASCENSION 4 & 9]: FORENSIC EMERGENCY DUMP
            self._conduct_emergency_autopsy(fracture)

            # [ASCENSION 8]: HAPTIC DISTRESS SIGNAL
            self.regs.ui_hints = {"vfx": "shake", "sound": "fracture_critical", "priority": "CRITICAL"}

            if not isinstance(fracture, ArtisanHeresy):
                # [THE FIX]: 'is_wasm' is now guaranteed manifest here via Movement I.
                raise ArtisanHeresy(
                    "KINETIC_CPU_FRACTURE",
                    child_heresy=fracture,
                    details=f"Opcodes: {total_ops} | Substrate: {'WASM' if is_wasm else 'NATIVE'}",
                    severity=HeresySeverity.CRITICAL
                ) from fracture
            raise

        finally:
            # [ASCENSION 5 & 10]: HYDRAULIC POOL DRAIN
            if hasattr(self, '_suture_pool') and not is_wasm:
                try:
                    self._suture_pool.shutdown(wait=False)
                except Exception:
                    pass

            # [ASCENSION 3]: FINAL TELEMETRY CAPTURE
            total_duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.regs.silent:
                self.logger.success(f"Quantum CPU Halted. Totality achieved in {total_duration_ms:.2f}ms.")

            # Record metrics in registers for the final revelation
            self.regs.metabolic_tax_ms = total_duration_ms
            self.regs.ops_conducted = total_ops

    # =========================================================================
    # == INTERNAL ORGANS (KINETIC EXECUTION)                                 ==
    # =========================================================================

    def _execute_parallel_strata(self, status_ctx: Any, force_sequential: bool = False):
        """
        =============================================================================
        == THE STRATUM MATERIALIZER (V-Ω-TOTALITY-V505.2-WASM-RESONANT)            ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_FISSION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_STRATA_V505_WASM_SUTURE_2026_FINALIS
        """
        from collections import defaultdict
        from pathlib import Path
        import concurrent.futures


        # --- MOVEMENT I: THE CENSUS OF MATTER ---
        # We only parallelize pure I/O operations. SYMLINKS and EXECS are sequential.
        io_ops = (OpCode.MKDIR, OpCode.WRITE, OpCode.CHMOD)
        io_instructions = [i for i in self.program if i.op in io_ops]

        if not io_instructions:
            return

        # [ASCENSION 2]: TOPOLOGICAL STRATIFICATION
        # Group by tree depth to ensure parent directories exist before children.
        strata: Dict[int, List[Any]] = defaultdict(list)
        for instr in io_instructions:
            # Resolve depth by part-count
            if isinstance(instr.target, (str, Path)):
                depth = len(Path(instr.target).parts)
            else:
                depth = 0
            strata[depth].append(instr)

        # --- MOVEMENT II: THE RITE OF DEPTH ---
        # We walk the tree from root to leaf (lowest depth to highest)
        for depth in sorted(strata.keys()):
            batch = strata[depth]

            # [ASCENSION 5]: DETERMINISTIC SIBLING SORT
            # Ensures bit-perfect repeatability across all timelines.
            batch.sort(key=lambda x: str(x.target).lower())

            if not self.regs.silent and status_ctx and hasattr(status_ctx, 'update'):
                status_ctx.update(f"[bold cyan]🏗️  Materializing Stratum {depth} ({len(batch)} atoms)...[/]")
            elif not self.regs.silent:
                self.regs.console.print(f"[dim]   -> Stratum {depth}: {len(batch)} atoms[/]")

            # [ASCENSION 4]: METABOLIC FEVER VIGIL
            # Scry hardware load before each burst.
            self._check_metabolic_fever()

            # =========================================================================
            # == [THE CURE]: SUBSTRATE-AWARE DISPATCH                                ==
            # =========================================================================
            if force_sequential:
                # PATH A: ETHER PLANE (SEQUENTIAL)
                # In WASM, we conduct the instructions one-by-one to avoid Thread Panic.
                for instr in batch:
                    try:
                        self._dispatch_instruction(instr)
                    except Exception as e:
                        self._handle_matter_failure(instr, e)
            else:
                # PATH B: IRON CORE (PARALLEL)
                # Unleash the ThreadPoolExecutor for high-speed native execution.
                futures = {
                    self._suture_pool.submit(self._dispatch_instruction, instr): instr
                    for instr in batch
                }

                # [ASCENSION 3]: ATOMIC BARRIER SYNC
                # Wait for the entire depth-level to stabilize before proceeding.
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as paradox:
                        instr = futures[future]
                        self._handle_matter_failure(instr, paradox)
            # =========================================================================

        # Final Proclamation for the Ocular HUD
        self._multicast_strata_completion(len(io_instructions))

    def _handle_matter_failure(self, instr: Any, e: Exception):
        """[ASCENSION 9]: FAULT-ISOLATED HERESY MAPPING."""

        err_msg = f"Matter Fission Failure at L{instr.line_num}: {str(e)}"

        # Log the heresy for the forensic dossier
        self.logger.error(err_msg)

        # Transmute into a Critical Heresy to trigger rollback
        raise ArtisanHeresy(
            err_msg,
            severity=HeresySeverity.CRITICAL,
            details=f"Opcode: {instr.op} | Target: {instr.target}",
            line_num=instr.line_num,
            suggestion="Verify filesystem permissions or available Gnostic space."
        )

    def _multicast_strata_completion(self, count: int):
        """[ASCENSION 6]: HUD TELEMETRY DISPATCH."""
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
        """
        [ASCENSION 2 & 12]: Executes shell commands with Venv Suture.
        """
        kinetic_instructions = [i for i in self.program if i.op == OpCode.EXEC]
        for instr in kinetic_instructions:
            # [THE FIX]: DEFENSIVE UPDATE GUARD
            # Prevents 'nullcontext' object has no attribute 'update'
            if not self.regs.silent and hasattr(status_ctx, "update"):
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

    def _terraform_environment(self, env_from_caller: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        =================================================================================
        == THE ENVIRONMENT ALCHEMIST: OMEGA (V-Ω-TOTALITY-V2000-DIMENSIONAL-FORGE)     ==
        =================================================================================
        LIF: ∞ | ROLE: ATMOSPHERIC_CONSTRUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_TERRAFORM_V2000_SUBSTRATE_AWARE_FINALIS

        [THE MANIFESTO]
        This rite constructs the physics of the execution environment. It resolves the
        'Substrate Schism' by intelligently branching between IRON (Native) and ETHER
        (WASM) realities, ensuring that paths, encodings, and identities are bit-perfect.

        ### THE PANTHEON OF 7 ASCENSIONS:
        1.  **Substrate-Aware Anchoring:** Automatically detects WASM/Pyodide and forces
            the Project Root to `/vault/project` if the logical anchor is void.
        2.  **The Venv Supremacy:** Scans for `.venv`, `venv`, and `env`. If found,
            it injects their `bin` (or `Scripts`) directory to the *front* of PATH,
            guaranteeing local dependency precedence over system libraries.
        3.  **The Node/NPM Bridge:** Automatically detects `node_modules/.bin` and
            sutures it into the PATH, enabling `npm run` style execution for raw shells.
        4.  **Windows Titanium Hardening:** Explicitly sets `COMSPEC`, `SHELL`, and
            `MAKESHELL` to `cmd.exe` on NT systems, annihilating the "Make Error 2" heresy.
        5.  **Linguistic Purification:** Enforces `PYTHONIOENCODING=utf-8` and
            `LANG=C.UTF-8` to prevent Unicode fractures in the log stream.
        6.  **The Causal Silver Cord:** Injects `SCAFFOLD_TRACE_ID` and `SCAFFOLD_SESSION_ID`
            deep into the child process's DNA for distributed observability.
        7.  **The Adrenaline Injection:** If the Engine is in `ADRENALINE_MODE`, it
            sets process priority flags within the environment for the Scheduler.
        =================================================================================
        """
        import os
        import sys
        import platform
        import uuid
        import time
        from pathlib import Path

        # [ASCENSION 0]: NANO-SCALE CHRONOMETRY
        # We stamp the birth of this environment for latency tracking.
        creation_ns = time.perf_counter_ns()

        # --- MOVEMENT I: PRIMORDIAL DNA REPLICATION ---
        # We start with the host's OS DNA, then overlay the caller's intent.
        env = os.environ.copy()
        if env_from_caller:
            env.update(env_from_caller)

        # [ASCENSION 1]: SUBSTRATE SENSING & ANCHORING
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # Scry the Logical Root. If void in WASM, anchor to the Virtual Vault.
        raw_root = getattr(self.regs, 'project_root', None)
        if not raw_root and is_wasm:
            raw_root = "/vault/project"

        # Resolve to absolute physical path
        project_root = Path(raw_root or ".").resolve()

        # --- MOVEMENT II: THE PATH LATTICE (BINARIES) ---
        # We construct a prioritized list of binary search paths.
        path_lattice: List[str] = []
        path_sep = ";" if platform.system() == "Windows" else ":"

        # 1. LOCAL VIRTUAL ENVIRONMENTS (The Venv Supremacy)
        # We search for the holy trinity of python environments.
        for venv_name in [".venv", "venv", "env"]:
            bin_dir = "Scripts" if platform.system() == "Windows" else "bin"
            venv_path = project_root / venv_name / bin_dir
            if venv_path.exists():
                path_lattice.append(str(venv_path))
                # [THE FIX]: Unset global VIRTUAL_ENV to prevent contamination
                env.pop("VIRTUAL_ENV", None)
                # Set local VIRTUAL_ENV to the discovered one
                env["VIRTUAL_ENV"] = str(project_root / venv_name)
                break

                # 2. LOCAL NODE MODULES (The NPM Bridge)
        node_bin = project_root / "node_modules" / ".bin"
        if node_bin.exists():
            path_lattice.append(str(node_bin))

        # 3. HOST PYTHON BINARIES (The Interpreter)
        python_bin_dir = Path(sys.executable).parent.resolve()
        path_lattice.append(str(python_bin_dir))

        # 4. INHERITED SYSTEM PATHS (The Foundation)
        current_path = env.get("PATH", "")
        if current_path:
            path_lattice.append(current_path)

        # Consecrate the new PATH
        env["PATH"] = path_sep.join(path_lattice)

        # --- MOVEMENT III: THE IMPORT LATTICE (PYTHONPATH) ---
        # Ensure the project root and current python path are visible to the child.
        current_python_path = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{str(project_root)}{path_sep}{current_python_path}"

        # --- MOVEMENT IV: THE WINDOWS COMPATIBILITY WARD ---
        # [ASCENSION 4]: ADJUDICATING THE 'MAKE' PARADOX
        if platform.system() == "Windows":
            # Force the shell soul to CMD.exe to stabilize Makefiles
            comspec = os.getenv("COMSPEC", "C:\\Windows\\system32\\cmd.exe")
            env["SHELL"] = comspec
            env["COMSPEC"] = comspec
            # Special flags for GNU Make on Windows
            env["MAKE_MODE"] = "win32"
            env["MAKESHELL"] = comspec

            # Disable MSYS path conversion if Git Bash is involved
            env["MSYS_NO_PATHCONV"] = "1"

        # --- MOVEMENT V: THE SILVER CORD (CAUSAL IDENTITY) ---
        # Inject traceability so the Daemon can map logs back to this specific request.
        trace_id = os.environ.get("GNOSTIC_REQUEST_ID",
                                  getattr(self.regs, 'trace_id', f"tr-maes-{uuid.uuid4().hex[:4]}"))

        env["SCAFFOLD_TRACE_ID"] = trace_id
        env["GNOSTIC_REQUEST_ID"] = trace_id
        env["SCAFFOLD_SESSION_ID"] = getattr(self.regs, 'session_id', 'SCAF-CORE')
        env["SCAFFOLD_MACHINE_ID"] = str(platform.node())

        # [ASCENSION 6]: TEMPORAL MARKER
        env["SCAFFOLD_RITE_START_TIME"] = str(creation_ns)

        # --- MOVEMENT VI: THERMODYNAMIC LOGGING DNA ---
        # Force unbuffered IO and UTF-8 to prevent log fractures.
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["LANG"] = "C.UTF-8"
        env["FORCE_COLOR"] = "1"
        env["TERM"] = "xterm-256color"

        # [ASCENSION 7]: ADRENALINE INJECTION
        if os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            env["SCAFFOLD_PRIORITY"] = "HIGH"
            # Node.js specific memory expansion for heavy builds
            env["NODE_OPTIONS"] = "--max-old-space-size=4096"

        # [METADATA GRAFT]: Contextual Awareness for the Child
        if hasattr(self.context, 'command'):
            env["SC_MAESTRO_CMD"] = str(self.context.command)

        # [THE FINALITY VOW]
        # The atmosphere is resonant. The chemistry is pure.
        # The child process will be born into a deterministic universe.
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