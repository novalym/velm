from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ....contracts.data_contracts import _GnosticNode

@dataclass
class StackFrame:
    """
    A single slice of the Weaver's memory.
    Holds the Node, its visual indentation level, and the physical path context.
    """
    node: _GnosticNode
    indent: int
    physical_path: Path

    @property
    def is_root(self) -> bool:
        return self.indent == -1