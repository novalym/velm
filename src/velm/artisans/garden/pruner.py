# Path: artisans/garden/pruner.py
# -------------------------------

from typing import List
from pathlib import Path
from .contracts import WitheredVine
from ...utils import atomic_write
from ...logger import Scribe

Logger = Scribe("GardenPruner")


class GardenPruner:
    """
    =============================================================================
    == THE SURGICAL SCALPEL (V-Ω-AST-REMOVAL)                                  ==
    =============================================================================
    Removes files and excises byte-ranges for dead symbols.
    """

    def __init__(self, project_root: Path):
        self.root = project_root

    def prune(self, vines: List[WitheredVine]) -> int:
        count = 0

        # Group by file for atomic surgery
        surgery_plan = {}
        files_to_delete = []

        for vine in vines:
            if vine.type == "file":
                files_to_delete.append(vine.path)
            elif vine.start_byte is not None and vine.end_byte is not None:
                if vine.path not in surgery_plan: surgery_plan[vine.path] = []
                surgery_plan[vine.path].append(vine)

        # 1. Delete Files
        for path in files_to_delete:
            if path.exists():
                path.unlink()
                Logger.info(f"Annihilated dead scripture: {path.name}")
                count += 1

        # 2. Perform Surgery (Symbols)
        for path, symbols in surgery_plan.items():
            if not path.exists(): continue

            content_bytes = path.read_bytes()
            # Sort symbols descending by position to keep offsets valid
            symbols.sort(key=lambda x: x.start_byte, reverse=True)

            # Mutable byte array for surgery
            data = bytearray(content_bytes)

            for sym in symbols:
                # Excise the range
                # We also want to remove the preceding newline(s) if possible for clean deletion
                start, end = sym.start_byte, sym.end_byte

                # Simple excision
                del data[start:end]
                Logger.info(f"Surgically removed {sym.type} '{sym.name}' from {path.name}")
                count += 1

            # Atomic Write Back
            atomic_write(path, data.decode('utf-8'), Logger, self.root)

        return count