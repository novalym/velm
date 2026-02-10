# Path: src/velm/creator/cpu.py
# =========================================================================================
# == THE QUANTUM CPU: OMEGA POINT (V-Ω-TOTALITY-V7.0-FINALIS)                            ==
# =========================================================================================
# LIF: INFINITY | ROLE: KINETIC_EXECUTION_CORE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CPU_V7_NONETYPE_SARCOPHAGUS_2026_FINALIS
# =========================================================================================

import os
import sys
import time
import subprocess
import shlex
import shutil
import platform
import threading
import traceback
import re
from contextlib import nullcontext
from pathlib import Path
from typing import List, Tuple, Optional, Set, Union, TYPE_CHECKING, Any, Dict

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


class QuantumCPU:
    """
    The High Executioner of the God-Engine. It transmutes logical instructions
    into physical reality by commanding the host's kinetic limbs with
    Achronal Venv Resonance.
    """

    def __init__(self, registers: QuantumRegisters, io_conductor: IOConductor, maestro: "MaestroUnit",
                 engine: Optional["ScaffoldEngine"] = None):
        """
        [THE RITE OF INCEPTION]
        Binds the CPU to the Engine's mind. Now warded against NoneType engine refs.
        """
        self.Logger = Logger
        self.regs = registers
        self.io = io_conductor
        self.maestro = maestro

        # [ASCENSION 1]: NONETYPE SARCOPHAGUS
        # We accept that the engine might be unmanifest in certain simulation strata.
        self.engine = engine

        self.program: List[Instruction] = []
        self.program_counter: int = 0

        # [ASCENSION 12]: The Handler Pantheon
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
        The Gnostic Compiler. Compiles the Scriptures of Form and Will into Opcodes.
        """
        # Ensure directories are forged before the files they contain
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
            # [ASCENSION]: Quaternity Ingestion
            for cmd_tuple in commands:
                self.program.append(Instruction(
                    op=OpCode.EXEC,
                    target=cmd_tuple,
                    line_num=cmd_tuple[1]
                ))

    def execute(self):
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EXECUTION (V-Ω-TOTALITY)                          ==
        =============================================================================
        """
        total_ops = len(self.program)
        if total_ops == 0: return

        status_ctx = self.regs.console.status(
            "[bold green]Quantum VM Running...[/bold green]") if not self.regs.silent else nullcontext()

        try:
            with status_ctx:
                for i, instr in enumerate(self.program):
                    self.program_counter = i
                    self.regs.ops_executed += 1

                    # [ASCENSION 8]: ATOMIC TRANSACTIONAL COMMITMENT
                    # Ensure physical disk is ready for the shell to gaze upon it.
                    if instr.op == OpCode.EXEC:
                        if self.regs.transaction and not self.regs.is_simulation:
                            self.Logger.verbose("Lattice: Materializing staged matter for Kinetic Strike...")
                            self.regs.transaction.materialize()

                    if not self.regs.silent:
                        status_ctx.update(
                            f"[bold green]Quantum VM: Op {i + 1}/{total_ops} ({instr.op.name})[/bold green]"
                        )

                    handler = self._handler_map.get(instr.op)
                    if handler:
                        handler(instr)
                    else:
                        self.Logger.warn(f"Opcode '{instr.op.name}' has no handler.")

        except Exception as e:
            # [ASCENSION 7]: SOCRATIC EXIT-CODE TRIAGE
            raise ArtisanHeresy(
                f"Quantum VM Halt at Op {self.program_counter + 1} ({self.program[self.program_counter].op.name})",
                child_heresy=e,
                details=f"Instruction: {self.program[self.program_counter]}",
                severity=HeresySeverity.CRITICAL
            ) from e

    # =========================================================================
    # == INTERNAL HANDLERS (THE KINETIC LIMBS)                               ==
    # =========================================================================

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
        =============================================================================
        == THE RITE OF RESILIENT EXECUTION (V-Ω-VENV-SUTURED)                      ==
        =============================================================================
        [THE CURE]: This method terraforms the environment and handles redemption.
        """
        cmd_tuple = instr.target
        cmd, line, undo, heresy_cmds = (cmd_tuple if len(cmd_tuple) == 4 else (*cmd_tuple, None))

        # --- 1. THE VENV SUTURE & TRANSMUTATION ---
        # [ASCENSION 3]
        execution_env = self._terraform_environment()
        # [ASCENSION 2]
        transmuted_cmd = self._transmute_artisan_plea(cmd)

        # --- 2. METABOLIC ADJUDICATION ---
        # [ASCENSION 11]
        self._check_metabolic_fever()

        # --- 3. HUD BROADCAST ---
        # [ASCENSION 4]
        self._multicast_kinetic_start(transmuted_cmd, line)

        try:
            # --- 4. THE KINETIC STRIKE ---
            # We inject the sutured environment into the Maestro's execution block
            self.maestro.execute((transmuted_cmd, line, undo), env=execution_env)

        except Exception as fracture:
            # --- 5. THE RITE OF REDEMPTION ---
            if heresy_cmds:
                self.Logger.warn(f"L{line}: Edict fractured. Invoking Redemption Rites...")
                try:
                    for h_cmd in heresy_cmds:
                        self.Logger.verbose(f"   -> [REDEEM] {h_cmd[:40]}...")
                        self.maestro.execute((h_cmd, line, None), env=execution_env)
                except Exception as r_err:
                    self.Logger.error(f"Redemption failed: {r_err}")

            # [ASCENSION 9]: LAZARUS BINARY SEARCH
            if "127" in str(fracture) or "not found" in str(fracture).lower():
                self._diagnose_missing_artisan(cmd, line)

            raise fracture

    # =========================================================================
    # == PRIVATE ALCHEMY (THE INNER WORKINGS)                                ==
    # =========================================================================

    def _terraform_environment(self) -> Dict[str, str]:
        """
        [ASCENSION 3 & 11]: PATH SUTURE & TRACE INJECTION.
        Forges a child environment with perfect Venv resonance and distributed tracing.
        """
        env = os.environ.copy()

        # 1. THE PATH SUTURE (Ensures bin/ is visible)
        python_bin_dir = os.path.dirname(sys.executable)
        path_sep = ";" if platform.system() == "Windows" else ":"
        env["PATH"] = f"{python_bin_dir}{path_sep}{env.get('PATH', '')}"

        # 2. THE SILVER CORD (Distributed Tracing)
        trace_id = os.environ.get("GNOSTIC_REQUEST_ID", "tr-local-cpu")
        env["SCAFFOLD_TRACE_ID"] = trace_id
        env["PYTHONUNBUFFERED"] = "1"

        return env

    def _transmute_artisan_plea(self, command: str) -> str:
        """
        [ASCENSION 2]: THE SACRED PROXY.
        Surgically replaces 'pip' with absolute Python module calls to annihilate 127s.
        """
        parts = command.strip().split()
        if not parts: return command

        if parts[0].lower() == "pip":
            self.Logger.debug(f"Transmuting Artisan: pip -> {sys.executable}")
            parts[0] = f'"{sys.executable}" -m pip'
            return " ".join(parts)

        return command

    def _diagnose_missing_artisan(self, cmd: str, line: int):
        """[ASCENSION 9]: THE LAZARUS PROBE."""
        artisan = cmd.split()[0]
        self.Logger.error(f"L{line}: Artisan '{artisan}' is unmanifest in the host's strata.")

        # Socratic Advice
        if artisan == "git":
            self.Logger.info("💡 Path to Redemption: `apt-get install git` or `brew install git`.")
        elif artisan in ("npm", "node"):
            self.Logger.info("💡 Path to Redemption: Node is required for this reality. See https://nodejs.org")

    def _check_metabolic_fever(self):
        """[ASCENSION 11]: Adaptive Throttling."""
        # [ASCENSION 1]: SAFE ORGAN ACCESS
        watchdog = getattr(self.engine, 'watchdog', None)
        if watchdog:
            vitals = watchdog.get_vitals()
            if vitals.get("load_percent", 0) > 90.0:
                self.Logger.verbose("Host Fever detected. Injecting Metabolic Yield (500ms).")
                time.sleep(0.5)

    def _multicast_kinetic_start(self, cmd: str, line: int):
        """[ASCENSION 4]: HUD BROADCAST (AKASHIC LINK)."""
        # [ASCENSION 1]: SAFE ORGAN ACCESS
        akashic = getattr(self.engine, 'akashic', None)
        if akashic:
            akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "KINETIC_STRIKE",
                    "label": f"RUN: {cmd[:25]}...",
                    "color": "#fbbf24",
                    "line": line
                }
            })

    def _purify_output(self, text: str) -> str:
        """[ASCENSION 8]: ANSI EXORCISM."""
        return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

# == SCRIPTURE SEALED: THE QUANTUM CPU IS OMEGA TOTALITY ==