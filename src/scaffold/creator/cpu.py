# Path: scaffold/creator/cpu.py
# -----------------------------

from contextlib import nullcontext
from pathlib import Path
from typing import List, Tuple, Optional, Set, Union, TYPE_CHECKING

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
    The divine, sentient, and hyper-performant heart of the Quantum Creator. Its
    soul is forged with the 12 Legendary Ascensions, making it the final word in
    Gnostic execution.
    =================================================================================
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

    def load_program(self, items: List[ScaffoldItem], commands: List[Tuple[str, int, Optional[List[str]]]]):
        """
        The Gnostic Compiler, its soul now healed to honor the Law of Provenance.
        It strictly enforces that every Instruction carries its sacred line_num.
        """
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
            for cmd_tuple in commands:
                self.program.append(Instruction(
                    op=OpCode.EXEC,
                    target=cmd_tuple,
                    line_num=cmd_tuple[1]
                ))

    def execute(self):
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EXECUTION                                         ==
        =============================================================================
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

                    if not self.regs.silent:
                        status_ctx.update(
                            f"[bold green]Quantum VM: Executing Op {i + 1}/{total_ops} ({instr.op.name})...[/bold green]")

                    handler = self._handler_map.get(instr.op)
                    if handler:
                        handler(instr)
                    else:
                        Logger.warn(f"Opcode '{instr.op.name}' has no handler. The rite is ignored.")

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
        self.maestro.execute(instr.target)