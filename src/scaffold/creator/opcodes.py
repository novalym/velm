# Path: scaffold/creator/opcodes.py
# ---------------------------------
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Union, Optional, Dict, Any


class OpCode(Enum):
    """
    The Atomic Operations of the Quantum VM (Instruction Set Architecture v2.0).
    """
    # --- File Operations ---
    MKDIR = auto()  # Create Directory Sanctum
    WRITE = auto()  # Inscribe Scripture (File)
    COPY = auto()  # Clone Reality (File/Dir Copy)
    SYMLINK = auto()  # Forge Neural Link (Symlink)
    CHMOD = auto()  # Consecrate Permissions

    # --- Execution & Logic ---
    EXEC = auto()  # Maestro's Edict (Shell Command)
    VERIFY = auto()  # Gnostic Check (Assert existence/content)
    NOOP = auto()  # Void / Comment


@dataclass
class Instruction:
    """
    A single, atomic unit of work for the VM.
    Ideally immutable once compiled.
    """
    op: OpCode
    target: Union[Path, str]  # The primary object of the operation
    payload: Optional[str] = None  # Secondary data (content, permissions, source path)
    metadata: Dict[str, Any] = field(default_factory=dict)  # Provenance, user info, etc.
    line_num: int = 0  # Debug info: Source line in blueprint

    def __repr__(self):
        return f"INSTR<{self.op.name} target='{self.target}' payload_len={len(self.payload) if self.payload else 0}>"