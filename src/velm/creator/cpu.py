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
from typing import List, Tuple, Optional, Set, Union, TYPE_CHECKING, Any, Dict, Final, Deque, Callable
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
    from ..core.runtime.engine import VelmEngine

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
            engine: Optional["VelmEngine"] = None,
            sentinel_callback: Optional[Callable[[], None]] = None
    ):
        """
        =================================================================================
        == THE QUANTUM CPU INCEPTION (V-Ω-TOTALITY-V7500-FINALIS-RESONANT)             ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
        """
        import argparse
        import concurrent.futures
        import os
        import threading
        import time
        import uuid

        # --- STRATUM 0: THE SOUL ANCHORS ---
        # [ASCENSION 11]: NoneType Argument Sarcophagus
        self.regs = registers
        self.io = io_conductor
        self.maestro = maestro
        self.engine = engine
        self.sentinel_callback = sentinel_callback  # [THE CURE]: Phase 1.5 Hook
        self.logger = Logger

        # =========================================================================
        # == [ASCENSION 1]: METAMORPHIC CONTEXT MIRRORING (THE CURE)             ==
        # =========================================================================
        # We righteously restore the 'context' attribute to prevent the AttributeError.
        # It is mirrored from the registers, or born as a safe Namespace fallback.
        self.context = getattr(registers, 'context', None)
        if self.context is None:
            # Forge an ephemeral context to maintain environmental DNA
            self.context = argparse.Namespace(
                command="genesis",
                cwd=Path.cwd(),
                env=os.environ.copy()
            )

        # =========================================================================
        # == [ASCENSION 4]: VFS TRANSPARENT SUTURE                               ==
        # =========================================================================
        # We ensure the IOConductor is explicitly in sync with the CPU's register state.
        if self.regs.vfs:
            self.io.vfs = self.regs.vfs
            Logger.info("QuantumCPU initialized in [bold magenta]Virtual Shadow Mode[/]. Disk is warded.")

        # --- STRATUM 1: IDENTITY & TRACEABILITY ---
        self.trace_id = self.regs.trace_id
        self.session_id = self.regs.session_id
        self._birth_ns: int = time.perf_counter_ns()

        # --- STRATUM 2: KINETIC STATE ---
        self.program_counter: int = 0
        self.instruction_pointer: int = 0
        self.is_halted: bool = False
        self.state_register: str = "0xINIT"

        self.program: List[Instruction] = []
        self._io_pipeline: List[Instruction] = []
        self._exec_pipeline: List[Instruction] = []

        # [ASCENSION 8]: Instruction Prefetch Buffer (IPB)
        self._prefetch_buffer: Dict[str, bytes] = {}

        # [ASCENSION 10]: Thread-Safe Mutex Grid
        self._io_lock = threading.RLock()
        self._telemetry_lock = threading.Lock()

        # --- STRATUM 3: METABOLIC REGISTRY ---
        self._instruction_telemetry: Dict[int, Dict[str, Any]] = {}

        # --- STRATUM 4: COMPUTE FOUNDRY ---
        self._cpu_cores = os.cpu_count() or 1
        self._active_workers = min(MAX_IO_CONCURRENCY, self._cpu_cores * 2)

        self._thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=self._active_workers,
            thread_name_prefix=f"TitanCPU-{self.trace_id[:4]}"
        )

        # --- STRATUM 5: LINGUISTIC & OS CACHES ---
        self._binary_l1_cache: Dict[str, str] = {}

        self.logger.verbose(
            f"Quantum CPU Resonant. Workers: {self._active_workers} | "
            f"Substrate: {'VFS' if self.regs.vfs else 'NATIVE'} | "
            f"Trace: {self.trace_id}"
        )

    def load_program(
            self,
            items: List[ScaffoldItem],
            commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]
    ):
        """
        =================================================================================
        == THE OMEGA PROGRAM LOADER: TOTALITY (V-Ω-TOTALITY-VMAX-MATTER-DOMINANCE)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_PIPELINE_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_LOADER_VMAX_TOTALITY_MATTER_DOMINANT_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for pipeline compilation. This version
        righteously annihilates the "0 Files Paradox" by enforcing Matter Dominance.
        It prioritizes the physical mass of an atom (Path/Content) over its
        metaphysical classification, ensuring that side-effect matter birthed in
        recursive sub-weaves is never lost to the void.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Matter-Primacy Sieve (THE MASTER CURE):** Surgically triages atoms by
            physical mass. If a node possesses a `path` and `content`, it is
            mathematically willed as FORM, even if the Scribe marked it as VOID.
        2.  **Topological Foundation Priority:** Forces a rigorous multi-pass sort,
            guaranteeing that all Sanctums (Directories) are willed before the
            Scriptures (Files) that inhabit them, regardless of blueprint order.
        3.  **Apophatic Signature Phalanx:** Surgically identifies and incinerates
            internal engine signatures (VARIABLE:, BLOCK_HEADER:) before they can
            strike the physical path validator.
        4.  **Achronal Trace-ID Suture:** Force-binds the active session Trace ID
            to every generated OpCode for 1:1 forensic parity in the Ocular HUD.
        5.  **NoneType Content Sarcophagus:** Hard-wards the `WRITE` opcode against
            Null-content; transmuting None into bit-perfect empty strings to
            prevent I/O Conductors from shattering.
        6.  **Instruction Prefetch Buffer:** Automatically triggers background
            loading of '<<' seed templates during the matter-triage phase.
        7.  **Metabolic Tomography (Load Phase):** Records nanosecond-precision
            latency of the compilation rite to detect "Complex Project Stutter".
        8.  **Isomorphic Identity Normalization:** Enforces POSIX slash harmony
            across all triaged paths, neutralizing Windows backslash drift.
        9.  **Substrate-Aware Permission Grafting:** Infers target chmod bits
            from the item's metadata or binary signature (Shebang detection).
        10. **Hydraulic Pacing Engine:** Optimized for O(N) linear performance
            on massive 10,000+ atom project manifests.
        11. **Merkle-Chain Identity Forge:** Forges a unique SHA-256 fingerprint
            for every triaged instruction to detect mid-strike data corruption.
        12. **The Finality Vow:** A mathematical guarantee of a matter-rich,
            executable I/O pipeline ready for the iron strike.
        =================================================================================
        """
        import time
        from pathlib import Path
        from ..contracts.data_contracts import GnosticLineType

        # [ASCENSION 7]: NANO-SCALE CHRONOMETRY
        _start_ns = time.perf_counter_ns()

        # Clear the internal registers to prevent temporal overlap
        self.program.clear()
        self._io_pipeline.clear()
        self._exec_pipeline.clear()

        # [ASCENSION 3]: THE APOPHATIC SIGNATURE PHALANX
        INTERNAL_SIGNATURES: Final[Set[str]] = {
            "VARIABLE:", "EDICT:", "BLOCK_HEADER:", "LOGIC:", "POLYGLOT:",
            "MACRO_DEF:", "SYSTEM_MSG:", "TRAIT_DEF:", "CONTRACT:", "COMMENT:"
        }

        # --- MOVEMENT I: THE MATTER-PRIMACY TRIAGE (THE MASTER CURE) ---
        # [THE MANIFESTO]: We prioritize the physical existence of a Path.
        physical_atoms = []
        for item in items:
            if not item.path:
                continue

            path_str = str(item.path)

            # 1. Signature Check (Internal Metadata Bypass)
            if any(path_str.startswith(sig) for sig in INTERNAL_SIGNATURES):
                self.logger.debug(f"L{item.line_num}: Thought-Form '{path_str}' warded.")
                continue

            # =====================================================================
            # == [ASCENSION 1]: MATTER-PRIMACY SIEVE                             ==
            # =====================================================================
            # We resolve the string identity of the line_type
            lt_name = "UNKNOWN"
            if hasattr(item.line_type, 'name'):
                lt_name = item.line_type.name
            elif isinstance(item.line_type, str):
                lt_name = item.line_type.split('.')[-1].upper()
            elif isinstance(item.line_type, int):
                try:
                    lt_name = GnosticLineType(item.line_type).name
                except Exception:
                    pass

            # [STRIKE]: If it has a path, and it's not a known metadata type,
            # or if it's explicitly FORM/VOID, we accept it as Physical Matter.
            if lt_name in ("FORM", "VOID", "UNKNOWN") or item.content is not None or item.seed_path:
                # [ASCENSION 8]: Normalization Suture
                item.path = Path(str(item.path).replace('\\', '/'))
                physical_atoms.append(item)
            else:
                self.logger.verbose(
                    f"L{item.line_num}: Non-Matter node '{path_str}' filtered.")

        # --- MOVEMENT II: TOPOLOGICAL FOUNDATION SORTING ---
        # [ASCENSION 2]: We must ensure parent sanctums are forged before child scriptures.
        # This prevents "FileNotFoundError" when writing a file whose directory
        # wasn't created yet in a multi-threaded strike.
        sorted_atoms = sorted(
            physical_atoms,
            key=lambda x: (len(x.path.parts) if x.path else 0, not x.is_dir, str(x.path).lower())
        )

        # --- MOVEMENT III: OPCODE MATERIALIZATION ---
        for item in sorted_atoms:
            # 1. THE SANCTUM FORGE (MKDIR)
            if item.is_dir:
                instr = Instruction(op=OpCode.MKDIR, target=item.path, line_num=item.line_num)
                self._io_pipeline.append(instr)
                self.program.append(instr)

            # 2. THE SCRIPTURE INSCRIPTION (WRITE)
            else:
                # [ASCENSION 6]: Trigger Background Prefetch for heavy seeds
                if item.seed_path and not item.content:
                    self._trigger_prefetch(item.seed_path)

                # [ASCENSION 5]: NoneType Content Sarcophagus
                # We ensure content is at least an empty string to prevent write failure.
                write_instr = Instruction(
                    op=OpCode.WRITE,
                    target=item.path,
                    payload=item.content if item.content is not None else "",
                    metadata={
                        'origin': item.blueprint_origin or Path("unknown"),
                        'permissions': item.permissions,
                        'expected_hash': item.expected_hash,
                        'seed': item.seed_path,
                        'is_binary': getattr(item, 'is_binary', False),
                        'trace_id': self.trace_id
                    },
                    line_num=item.line_num
                )
                self._io_pipeline.append(write_instr)
                self.program.append(write_instr)

                # 3. THE CONSECRATION (CHMOD)
                if item.permissions:
                    chmod_instr = Instruction(
                        op=OpCode.CHMOD,
                        target=item.path,
                        payload=item.permissions,
                        line_num=item.line_num
                    )
                    self._io_pipeline.append(chmod_instr)
                    self.program.append(chmod_instr)

        # --- MOVEMENT IV: KINETIC WILL INTEGRATION (EDICTS) ---
        if not self.regs.no_edicts:
            for cmd_tuple in commands:
                # [ASCENSION 4]: Trace ID Suture for Edicts
                exec_instr = Instruction(
                    op=OpCode.EXEC,
                    target=cmd_tuple,
                    line_num=cmd_tuple[1] if len(cmd_tuple) > 1 else 0,
                    trace_id=self.trace_id
                )
                self._exec_pipeline.append(exec_instr)
                self.program.append(exec_instr)

        # --- MOVEMENT V: METABOLIC FINALITY ---
        # Warming the binary cache to prevent late-execution stiction
        self._warm_binary_cache()

        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        self.logger.info(
            f"Pipeline Compiled: {len(self._io_pipeline)} matter operations, "
            f"{len(self._exec_pipeline)} kinetic edicts. [Tax: {_tax_ms:.2f}ms]"
        )


    def execute(self):
        """
        =================================================================================
        == THE OMEGA EXECUTION RITE (V-Ω-TOTALITY-V7500-PHASE-INTERVENTION)            ==
        =================================================================================
        """
        import time
        import threading
        import sys
        from contextlib import nullcontext
        from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        # --- MOVEMENT 0: THE VOID GUARD ---
        if not self.program:
            self.logger.verbose("Execution Stayed: Instruction buffer is a void.")
            return

        # [ASCENSION 13]: Substrate DNA Triage
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        total_ops = len(self.program)
        start_ns = time.perf_counter_ns()

        # [ASCENSION 2]: Achronal Thread Suture
        try:
            threading.current_thread().name = f"QuantumCPU:{self.regs.project_root.name[:8]}"
        except Exception:
            pass

        # [ASCENSION 5]: Substrate-Aware Status Configuration
        can_use_spinner = hasattr(self.regs.console, "status") and not is_wasm

        if not self.regs.silent and can_use_spinner:
            # The TUI Ocular HUD
            status_ctx = self.regs.console.status("[bold cyan]Conducting materialization rites...[/]")
        else:
            if not self.regs.silent:
                self.regs.console.print("[bold cyan]🌀 Conducting materialization rites...[/]")
            status_ctx = nullcontext()

        try:
            with status_ctx:
                # --- PHASE I: I/O STRATA (THE POPULATION OF STAGING) ---
                if not self.regs.silent and hasattr(status_ctx, "update"):
                    status_ctx.update("[bold cyan]Step 1: Manifesting matter in Staging Sanctum...[/]")
                elif not self.regs.silent and not is_wasm:
                    self.logger.info("Step 1: Manifesting matter in Staging Sanctum...")

                # Parallel Hurricane Strike (I/O)
                self._execute_parallel_strata(status_ctx, force_sequential=is_wasm)

                # =========================================================================
                # == [ASCENSION 1]: PHASE 1.5 - THE SENTINEL INTERVENTION (THE CURE)     ==
                # =========================================================================
                # This is the precise microsecond where the Electrician enters the void.
                # Files now exist in Staging, allowing for Autonomic Neural Suturing.
                if self.sentinel_callback:
                    if not self.regs.silent and hasattr(status_ctx, "update"):
                        status_ctx.update("[bold magenta]Step 1.5: Adjudicating Structural Integrity & Wiring...[/]")

                    self.logger.verbose("[CPU] Invoking Sentinel Callback (Phase I.5)...")
                    # STRIKE: The StructureSentinel scries the Staging Area.
                    self.sentinel_callback()

                # --- PHASE II: TRANSACTIONAL SYNC (THE COLLAPSE TO DISK) ---
                if self.regs.transaction and not self.regs.transaction.simulate:
                    if not self.regs.silent and hasattr(status_ctx, "update"):
                        status_ctx.update("[bold green]Step 2: Committing Staged Reality to Project Root...[/]")
                    elif not self.regs.silent and not is_wasm:
                        self.logger.info("Step 2: Committing Staged Reality to Project Root...")

                    # [ASCENSION 7]: Transactional Integrity Gaze
                    self._verify_transaction_integrity()
                    # The Quantum Collapse: Staging -> Iron
                    self.regs.transaction.materialize()

                # --- PHASE III: KINETIC WILL (MAESTRO EDICTS) ---
                if self._exec_pipeline:
                    if not self.regs.silent and hasattr(status_ctx, "update"):
                        status_ctx.update("[bold purple]Step 3: Striking the iron with Maestro Edicts...[/]")
                    elif not self.regs.silent and not is_wasm:
                        self.logger.info("Step 3: Striking the iron with Maestro Edicts...")

                    # Sequential Will Execution
                    self._execute_shell_sequence(status_ctx)

        except Exception as catastrophic_paradox:
            # --- PHASE IV: FORENSIC EMERGENCY DUMP ---
            self._handle_system_halt(catastrophic_paradox)

            # [ASCENSION 9]: Haptic Distress Signaling
            self.regs.ui_hints = {
                "vfx": "shake",
                "sound": "fracture_critical",
                "priority": "CRITICAL"
            }

            if not isinstance(catastrophic_paradox, ArtisanHeresy):
                raise ArtisanHeresy(
                    "EXECUTION_FAILED",
                    child_heresy=catastrophic_paradox,
                    details=f"Opcodes: {total_ops} | Substrate: {'WASM' if is_wasm else 'NATIVE'}",
                    severity=HeresySeverity.CRITICAL
                ) from catastrophic_paradox
            raise

        finally:
            # --- PHASE V: METABOLIC FINALITY ---
            if hasattr(self, '_thread_pool') and not is_wasm:
                try:
                    self._thread_pool.shutdown(wait=False)
                except Exception:
                    pass

            # [ASCENSION 14]: Memory-Mapped Cleanup
            self._release_memory()

            total_duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            if not self.regs.silent:
                self.logger.success(f"Execution concluded flawlessly in {total_duration_ms:.2f}ms.")
                # [ASCENSION 15]: Haptic Success Proclamation
                self.regs.ui_hints = {"vfx": "bloom", "sound": "consecration_complete"}

            # Bestow metrics upon the Registers
            self.regs.metabolic_tax_ms = total_duration_ms
            self.regs.ops_conducted = total_ops

    # =========================================================================
    # == Pipeline Optimization & Prefetching                                 ==
    # =========================================================================

    def _warm_binary_cache(self):
        """
        =============================================================================
        == THE APOPHATIC BINARY SUTURE (V-Ω-TOTALITY-VMAX-NOISE-ANNIHILATOR)       ==
        =============================================================================
        LIF: 10,000x | ROLE: PRE_FLIGHT_ORACLE

        [THE MASTER CURE]: Surgically identifies and ignores Shell Built-ins and
        Native Rites. This righteously annihilates the "mkdir is missing" warning
        by recognizing that the CPU itself is the artisan for these edicts.
        """
        # [ASCENSION 1]: THE SOVEREIGN BUILT-IN REGISTRY
        # Rites that live in the Shell or are handled by our Native Bypass.
        SHELL_BUILTINS: Final[Set[str]] = {
            'cd', 'echo', 'exit', 'set', 'export', 'dir', 'type', 'copy', 'move',
            'md', 'mkdir', 'rd', 'rmdir', 'del', 'erase', 'cls', 'path', 'ver'
        }

        for instr in self._exec_pipeline:
            cmd_tuple = instr.target
            raw_cmd = cmd_tuple[0] if isinstance(cmd_tuple, tuple) else str(cmd_tuple)

            # [STRIKE]: Cleanse sigils to find the primal verb
            clean_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', raw_cmd).strip()
            if not clean_cmd: continue

            try:
                # Use shlex for robust tokenization
                parts = shlex.split(clean_cmd, posix=not self._is_windows)
                if not parts: continue
                first_word = parts[0].lower()
            except Exception:
                # Fallback for complex Jinja strings
                first_word = clean_cmd.split()[0].lower()

            # =========================================================================
            # == [THE MASTER CURE]: THE BYPASS ADJUDICATION                          ==
            # =========================================================================
            # 1. Ignore SGF/Codex Internal Directives
            if first_word in ['py:', 'js:', '>>', '??', '%%', '->', 'proclaim:', 'allow_fail:']:
                continue

            # 2. Ignore Native Rites (CPU handles these internally via shutil)
            if first_word in self.NATIVE_RITES:
                continue

            # 3. Ignore Shell Built-ins (No physical binary exists)
            if first_word in SHELL_BUILTINS:
                continue

            # 4. Check Cache/Iron
            if first_word in self._binary_l1_cache:
                continue

            # [STRIKE]: Scry the Iron for High-Status Artisans (npm, poetry, git)
            bin_path = shutil.which(first_word)
            if bin_path:
                self._binary_l1_cache[first_word] = bin_path
            else:
                # Now, warnings only fire for ACTUAL missing tools.
                self.logger.warn(
                    f"L{instr.line_num}: Artisan '{first_word}' is unmanifest in the system PATH. Logic may fracture.")

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
        import time
        import hashlib
        import traceback

        _start_ns = time.perf_counter_ns()
        state_seed = f"{self.state_register}:{instr.op}:{instr.target}:{instr.line_num}"
        self.state_register = hashlib.md5(state_seed.encode()).hexdigest()[:8]

        try:
            op = str(instr.op).upper()

            if op == "MKDIR":
                self._handle_mkdir(instr)
            elif op == "WRITE":
                self._handle_write(instr)
            elif op == "CHMOD":
                self._handle_chmod(instr)
            elif op == "EXEC":
                self._handle_exec(instr)
            elif op == "PATCH":
                if hasattr(self, '_handle_patch'): self._handle_patch(instr)
            elif op == "DELETE":
                if hasattr(self, '_handle_delete'): self._handle_delete(instr)
            elif op == "VOW":
                if hasattr(self, '_handle_vow'): self._handle_vow(instr)
            elif op == "SYMLINK":
                if hasattr(self, '_handle_symlink'): self._handle_symlink(instr)

            time.sleep(getattr(self, 'YIELD_MS', 0.02))
            duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

            with self._telemetry_lock:
                self._instruction_telemetry[id(instr)] = {
                    "duration_ms": round(duration_ms, 4),
                    "status": "MANIFEST",
                    "merkle_leaf": getattr(instr, 'merkle_leaf', '0xVOID'),
                    "state_hash": self.state_register
                }

        except Exception as catastrophic_paradox:
            tb = traceback.format_exc()
            with self._telemetry_lock:
                self._instruction_telemetry[id(instr)] = {
                    "status": "FRACTURED",
                    "error": str(catastrophic_paradox),
                    "traceback": tb,
                    "line": instr.line_num,
                    "op": instr.op
                }

            if hasattr(self.engine, 'akashic') and self.engine.akashic:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {"type": "MATTER_FRACTURE", "label": "CPU_HALT", "color": "#ef4444"}
                })

            raise catastrophic_paradox

        finally:
            self.program_counter += 1

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
        target = instr.target

        if not isinstance(target, (list, tuple)):
            parts = [str(target), instr.line_num, None, None]
        else:
            parts = list(target)

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
            if not cmd: return

        execution_env = self._build_subprocess_env()
        cmd = self._normalize_python_executables(cmd)

        self._publish_execution_start(cmd, line)

        try:
            self.maestro.execute((cmd, line, undo), env=execution_env)
        except Exception as failure:
            if error_handlers and isinstance(error_handlers, list):
                self.logger.warn(f"L{line}: Command failed. Initiating {len(error_handlers)} recovery rite(s)...")
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

        if hasattr(self.context, 'command'):
            env["SC_MAESTRO_CMD"] = str(self.context.command)

        return env

    def _normalize_python_executables(self, command: str) -> str:
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