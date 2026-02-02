# Path: scaffold/creator/io_controller/operations.py
from __future__ import annotations
import os
import platform
import shutil
from pathlib import Path
from typing import Union, Dict, Any, TYPE_CHECKING

from ...contracts.data_contracts import GnosticWriteResult
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe
from ..writer import GnosticWriter

if TYPE_CHECKING:
    from ..registers import QuantumRegisters
    from .transaction_router import TransactionRouter

Logger = Scribe("PhysicalOperations")


class PhysicalOperations:
    """
    =================================================================================
    == THE HAND OF CREATION (V-Ω-PHYSICAL-ARTISAN)                                 ==
    =================================================================================
    This artisan is the pure, physical hand of the I/O Conductor. It contains no
    logic for state, security, or alchemy. Its one true purpose is to receive a
    final, adjudicated, physical path from the TransactionRouter and perform the
    requested rite upon the target Sanctum. It is the final link in the chain
    of causality.
    =================================================================================
    """

    def __init__(self, registers: "QuantumRegisters", router: "TransactionRouter"):
        self.regs = registers
        self.router = router
        self.sanctum = registers.sanctum
        # The GnosticWriter is now a tool of the Hand, not the Conductor.
        self.writer = GnosticWriter(registers)
        self.is_windows = platform.system() == "Windows"

    def perform_mkdir(self, physical_path: Path) -> bool:
        """Forges a sanctum at the specified physical location."""
        try:
            self.sanctum.mkdir(physical_path, parents=True, exist_ok=True)
            if self.regs.verbose:
                Logger.verbose(f"Sanctum physically forged: {physical_path}")
            return True
        except Exception as e:
            Logger.error(f"Physical sanctum creation failed at '{physical_path}': {e}")
            if not self.regs.force: raise
            return False

    def perform_write(self, logical_path_str: str, content: Union[str, bytes],
                      metadata: Dict[str, Any]) -> GnosticWriteResult:
        """
        Performs the Rite of Inscription.
        The GnosticWriter handles the atomic write and dry-run logic.
        """
        # The Writer is a specialist that needs the logical path for its chronicle.
        # It internally uses the router to find the physical destination.
        return self.writer.write(
            logical_path=Path(logical_path_str),
            content=content,
            metadata=metadata
        )

    def perform_delete(self, physical_path: Path, recursive: bool):
        """Performs the Rite of Annihilation."""
        try:
            if self.sanctum.is_dir(physical_path):
                self.sanctum.rmdir(physical_path, recursive=recursive)
            elif self.sanctum.exists(physical_path):
                self.sanctum.unlink(physical_path)

            Logger.verbose(f"Physically annihilated: {physical_path}")
        except Exception as e:
            Logger.warn(f"Failed to physically annihilate '{physical_path}': {e}")

    def perform_chmod(self, physical_path: Path, mode_str: str):
        """Performs the Rite of Consecration."""
        try:
            mode = int(str(mode_str), 8)
            self.sanctum.chmod(physical_path, mode)
            if self.regs.verbose:
                Logger.verbose(f"Permissions consecrated for '{physical_path}' to {mode_str}.")
        except Exception as e:
            Logger.warn(f"Physical permission consecration failed for '{physical_path}': {e}")

    def perform_symlink(self, physical_link_path: Path, logical_target_path: str) -> bool:
        """Performs the Rite of Linking."""
        # This rite is complex and deeply tied to the local filesystem reality.
        # It requires careful relative path calculation.
        if not self.sanctum.is_local:
            Logger.warn("Symlink Rite is not fully supported on non-local Sanctums yet.")
            return False

        full_link_path = (self.sanctum.root / physical_link_path).resolve()

        try:
            full_target_path = (self.sanctum.root / logical_target_path).resolve()
            relative_target = os.path.relpath(full_target_path, full_link_path.parent)
        except ValueError:
            relative_target = logical_target_path

        try:
            if full_link_path.exists(follow_symlinks=False) or full_link_path.is_symlink():
                if self.regs.force:
                    if full_link_path.is_dir() and not full_link_path.is_symlink():
                        shutil.rmtree(full_link_path)
                    else:
                        full_link_path.unlink()
                else:
                    Logger.warn(f"Symlink obstruction: '{physical_link_path}' already exists.")
                    return False

            full_link_path.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(relative_target, full_link_path)
            Logger.verbose(f"Symlink forged: {physical_link_path} -> {relative_target}")
            return True

        except OSError as e:
            if self.is_windows and getattr(e, 'winerror', 0) == 1314:
                Logger.error("Privilege Heresy: Symlinks on Windows require Developer Mode or Admin rights.")
            else:
                Logger.error(f"Symlink Paradox at '{physical_link_path}': {e}")
            if not self.regs.force: raise
            return False