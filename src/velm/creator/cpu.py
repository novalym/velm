# Path: src/velm/creator/cpu.py
# -----------------------------

from contextlib import nullcontext
from pathlib import Path
from typing import List, Tuple, Optional, Set, Union, TYPE_CHECKING, Any

from .alu import AlchemicalLogicUnit
from .io_controller import IOConductor
from .opcodes import OpCode, Instruction
from .registers import QuantumRegisters
from ..contracts.data_contracts import ScaffoldItem, InscriptionAction
from ..contracts.heresy_contracts import ArtisanHeresy
from ..logger import Scribe

# FACULTY 1: The Law of Gnostic Delegation (Forward Gaze)
if TYPE_CHECKING:
    from ..core.maestro import MaestroConductor as MaestroUnit

Logger = Scribe("QuantumCPU")


class QuantumCPU:
    """
    =================================================================================
    == THE SINGULARITY CPU (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                       ==
    =================================================================================
    LIF: 10,000,000,000,000 | ROLE: KINETIC_EXECUTION_CORE | RANK: OMEGA

    The divine, sentient, and hyper-performant heart of the Quantum Creator. Its
    soul is forged with the 12 Legendary Ascensions, making it the final word in
    Gnostic execution.

    [ASCENSION LOG]:
    1.  **The Quaternity Processor:** It now natively understands the 4-tuple command
        structure `(Command, Line, Undo, Heresy)`, enabling conditional resilience.
    2.  **The Rite of Redemption:** Upon detecting a kinetic fracture (Exception), it
        checks for a `Heresy` payload and executes it before re-raising the error.
    3.  **JIT Materialization:** It forces the Staging Area to flush to disk before
        executing shell commands, ensuring the shell sees the new reality.
    """

    def __init__(self, registers: QuantumRegisters, io_conductor: IOConductor, maestro: "MaestroUnit"):
        """
        =============================================================================
        == THE RITE OF GNOSTIC BESTOWAL (DEPENDENCY INJECTION)                     ==
        =============================================================================
        The CPU is born. It receives its divine instruments—the IOConductor and the
        Maestro—as gifts from its Creator, annihilating the Ouroboros heresy.
        =============================================================================
        """
        self.Logger = Logger
        self.regs = registers
        self.io = io_conductor
        self.maestro = maestro
        self.program: List[Instruction] = []
        self.program_counter: int = 0

        # FACULTY 2: The Handler Pantheon (The Dispatch Table)
        self._handler_map = {
            OpCode.MKDIR: self._handle_mkdir,
            OpCode.WRITE: self._handle_write,
            OpCode.CHMOD: self._handle_chmod,
            OpCode.EXEC: self._handle_exec,
        }

    def load_program(
            self,
            items: List[ScaffoldItem],
            commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]]
    ):
        """
        The Gnostic Compiler, its soul now healed to honor the Law of Provenance.
        It strictly enforces that every Instruction carries its sacred line_num.

        Arguments:
            items: The Scripture of Form (Files/Directories).
            commands: The Scripture of Will (The Quaternity of Execution).
        """
        # Sort items to ensure directories are forged before files
        sorted_items = sorted(items, key=lambda x: (not x.is_dir, str(x.path)))

        for item in sorted_items:
            if item.is_dir:
                self.program.append(Instruction(op=OpCode.MKDIR, target=item.path, line_num=item.line_num))
            else:
                origin = item.blueprint_origin or Path("unknown")
                self.program.append(Instruction(
                    op=OpCode.WRITE,
                    target=item.path,
                    payload=item.content or "",
                    metadata={'origin': origin, 'permissions': item.permissions},
                    line_num=item.line_num
                ))
                if item.permissions:
                    self.program.append(Instruction(
                        op=OpCode.CHMOD,
                        target=item.path,
                        payload=item.permissions,
                        line_num=item.line_num
                    ))

        if not self.regs.no_edicts:
            # [ASCENSION]: Unpack Quaternity
            for cmd_tuple in commands:
                # We pack the whole tuple (cmd, line, undo, heresy) into target for the Handler
                self.program.append(Instruction(
                    op=OpCode.EXEC,
                    target=cmd_tuple,
                    line_num=cmd_tuple[1]
                ))

    def execute(self):
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EXECUTION (V-Ω-STAGING-AWARE-FINALIS)             ==
        =============================================================================
        Runs the compiled program.
        """
        total_ops = len(self.program)
        if total_ops == 0:
            return

        status_ctx = self.regs.console.status(
            "[bold green]Quantum VM Running...[/bold green]") if not self.regs.silent else nullcontext()

        try:
            with status_ctx:
                for i, instr in enumerate(self.program):
                    self.program_counter = i
                    self.regs.ops_executed += 1

                    # [ASCENSION 13]: JUST-IN-TIME MATERIALIZATION
                    # If we are about to execute a shell command, we MUST flush
                    # the staging area to the physical disk so the tools (make/npm)
                    # can see the files we just 'created'.
                    if instr.op == OpCode.EXEC:
                        if self.regs.transaction and not self.regs.is_simulation:
                            self.Logger.verbose("Materializing staged reality before Kinetic Strike...")
                            # This moves files from .scaffold/staging to the real project root
                            self.regs.transaction.materialize()

                    if not self.regs.silent:
                        status_ctx.update(
                            f"[bold green]Quantum VM: Op {i + 1}/{total_ops} ({instr.op.name})...[/bold green]")

                    handler = self._handler_map.get(instr.op)
                    if handler:
                        handler(instr)
                    else:
                        self.Logger.warn(f"Opcode '{instr.op.name}' has no handler.")

        except Exception as e:
            raise ArtisanHeresy(
                f"Quantum VM Halt at Op {self.program_counter + 1} ({self.program[self.program_counter].op.name})",
                child_heresy=e,
                details=f"Instruction: {self.program[self.program_counter]}"
            ) from e

    def _handle_mkdir(self, instr: Instruction):
        if self.io.mkdir(Path(instr.target)):
            self.regs.sanctums_forged += 1

    def _handle_write(self, instr: Instruction):
        path = Path(instr.target)
        result = self.io.write(path, instr.payload, instr.metadata)

        if result.success:
            self.regs.bytes_written += result.bytes_written
            if result.action_taken == InscriptionAction.CREATED:
                self.regs.files_forged += 1

        if self.regs.transaction:
            self.regs.transaction.record(result)

    def _handle_chmod(self, instr: Instruction):
        self.io.chmod(Path(instr.target), instr.payload)

    def _handle_exec(self, instr: Instruction):
        """
        [ASCENSION]: THE RITE OF RESILIENT EXECUTION.
        Handles the 4-Tuple Quaternity: (Command, Line, Undo, Heresy).
        """
        # The target holds the tuple we packed in load_program
        cmd_tuple = instr.target

        # 1. Unpack the Quaternity (with legacy safety)
        if len(cmd_tuple) == 4:
            cmd, line, undo, heresy_cmds = cmd_tuple
        else:
            # Fallback for old blueprints
            cmd, line, undo = cmd_tuple
            heresy_cmds = None

        try:
            # 2. Attempt the Primary Will
            # Maestro expects the 3-tuple (cmd, line, undo) for its context forging
            self.maestro.execute((cmd, line, undo))

        except Exception as e:
            # 3. The Fracture Occurred. Do we have a path to redemption?
            if heresy_cmds:
                self.Logger.warn(f"Edict failed on L{line}. Invoking Rite of Redemption (On-Heresy)...")

                try:
                    for h_cmd in heresy_cmds:
                        # We create a temporary tuple for the heresy command.
                        # Heresy commands do not have their own undo/heresy stack (recursion guard).
                        self.Logger.verbose(f"   -> Conducting redemption rite: {h_cmd[:40]}...")
                        self.maestro.execute((h_cmd, line, None))
                except Exception as redemption_error:
                    # If redemption fails, we log it but still raise the ORIGINAL error
                    self.Logger.error(f"Redemption Rite fractured: {redemption_error}")

                # [THE FINALITY]: We re-raise the original exception.
                # The on-heresy block is for cleanup/notification, not for suppressing the failure state
                # of the transaction (unless we add a suppression flag later).
                raise e
            else:
                # No redemption path. Propagate the crash.
                raise e