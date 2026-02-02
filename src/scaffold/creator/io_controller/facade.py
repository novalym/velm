# Path: scaffold/creator/io_controller/facade.py
# ----------------------------------------------

from __future__ import annotations
from pathlib import Path
import stat
from typing import Union, Dict, Any, TYPE_CHECKING, Tuple, Optional

from .operations import PhysicalOperations
from .path_alchemist import PathAlchemist
from .security import SecurityWards
from .transaction_router import TransactionRouter
from ...contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe

# === THE ASCENDED IMPORTS ===
from ...creator.io_controller.trash import TrashManager
from ...core.state import ActiveLedger
from ...core.state.contracts import LedgerEntry, LedgerOperation, InverseOp

if TYPE_CHECKING:
    from ..registers import QuantumRegisters

Logger = Scribe("IOConductor")


class IOConductor:
    """
    =================================================================================
    == THE GOD-ENGINE OF CAUSALITY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                 ==
    =================================================================================
    The Sovereign Gateway for all I/O, ascended to be the Master Scribe of the
    Gnostic Ledger. It ensures every interaction with reality is atomic, reversible,
    and forensically chronicled.
    """

    def __init__(self, registers: "QuantumRegisters"):
        self.regs = registers
        project_root = registers.project_root or Path.cwd()

        # --- The Forging of the Pantheon ---
        self.alchemist = PathAlchemist(registers.gnosis)
        self.security = SecurityWards()
        self.router = TransactionRouter(registers.transaction)
        self.hand = PhysicalOperations(registers, self.router)
        self.trash = TrashManager(project_root)

    def _gaze_upon_soul(self, physical_path: Path) -> Tuple[Optional[bytes], Dict[str, Any]]:
        """[FACULTY 1] Performs a Gaze to capture a scripture's content and metadata."""
        if not physical_path.exists() or not physical_path.is_file():
            return None, {}

        try:
            content = physical_path.read_bytes()
            metadata = {
                "mode": stat.S_IMODE(physical_path.stat().st_mode),
                "mtime": physical_path.stat().st_mtime,
            }
            return content, metadata
        except Exception as e:
            Logger.warn(f"Soul-Reader's Gaze averted for '{physical_path.name}': {e}")
            return None, {}

    def _perform_physical_rite(self, entry: LedgerEntry) -> Any:
        """[FACULTY 4] The Universal Hand. The one true gateway for physical action."""
        op = entry.operation
        params = entry.forward_state

        # Inscribe the vow before acting
        ActiveLedger.record(entry)

        if self.regs.dry_run:
            Logger.info(f"[DRY-RUN] {op.name}: {params.get('path', 'N/A')}")
            if op == LedgerOperation.WRITE_FILE:
                return GnosticWriteResult(success=True, path=Path(params['path']),
                                          action_taken=InscriptionAction.DRY_RUN_CREATED, bytes_written=0)
            return True

        # Delegate to the Hand
        if op == LedgerOperation.MKDIR:
            return self.hand.perform_mkdir(self.router.resolve(params['path']))
        elif op == LedgerOperation.WRITE_FILE:
            return self.hand.perform_write(params['path'], params['content'], params.get('metadata', {}))
        elif op in (LedgerOperation.DELETE_FILE, LedgerOperation.RMDIR):
            # The Hand expects the physical path
            physical_target = self.router.resolve(params['path'])
            # The TrashManager is now a secondary safety net
            self.trash.move_to_trash(physical_target, self.regs.transaction.tx_id)
            return
        elif op == LedgerOperation.CHMOD:
            return self.hand.perform_chmod(self.router.resolve(params['path']), params['mode'])

        raise NotImplementedError(f"Physical rite for {op.name} not implemented.")

    def mkdir(self, logical_path: Union[str, Path]) -> bool:
        """The Grand Rite of Sanctum Forging."""
        try:
            transmuted_path = self.alchemist.transmute(logical_path)
            self.security.adjudicate_path(transmuted_path)

            entry = LedgerEntry(
                actor="IOConductor",
                operation=LedgerOperation.MKDIR,
                forward_state={"path": transmuted_path},
                inverse_action=InverseOp(
                    op=LedgerOperation.RMDIR,
                    params={"path": transmuted_path, "recursive": True}
                )
            )
            return self._perform_physical_rite(entry)

        except ArtisanHeresy as e:
            Logger.error(f"Sanctum forging for '{logical_path}' blocked: {e.message}")
            if not self.regs.force: raise
            return False

    def write(self, logical_path: Union[str, Path], content: Union[str, bytes],
              metadata: Dict[str, Any]) -> GnosticWriteResult:
        """The Grand Rite of Scripture Inscription, now with a perfect memory."""
        try:
            transmuted_path = self.alchemist.transmute(logical_path)
            self.security.adjudicate_path(transmuted_path)
            self.security.verify_resource_quota(content)

            physical_target = self.router.resolve(transmuted_path)

            # [FACULTY 3] Gnostic Triage of Intent
            snapshot, snapshot_meta = self._gaze_upon_soul(physical_target)

            if snapshot is not None:  # Overwrite
                inverse_op = InverseOp(
                    op=LedgerOperation.WRITE_FILE,
                    params={"path": transmuted_path, "content_is_snapshot": True}
                )
            else:  # Create
                inverse_op = InverseOp(
                    op=LedgerOperation.DELETE_FILE,
                    params={"path": transmuted_path}
                )

            entry = LedgerEntry(
                actor="IOConductor",
                operation=LedgerOperation.WRITE_FILE,
                forward_state={"path": transmuted_path, "content": content, "metadata": metadata},
                inverse_action=inverse_op,
                snapshot_content=snapshot,
                snapshot_metadata=snapshot_meta
            )
            return self._perform_physical_rite(entry)

        except ArtisanHeresy as e:
            Logger.error(f"Write blocked for '{logical_path}': {e.message}")
            return GnosticWriteResult(success=False, path=Path(str(logical_path)),
                                      action_taken=InscriptionAction.BLOCKED_SECURITY, bytes_written=0)

    def delete(self, logical_path: Union[str, Path], recursive: bool = False):
        """The Grand Rite of Annihilation, now perfectly reversible."""
        try:
            transmuted_path = self.alchemist.transmute(logical_path)
            self.security.adjudicate_path(transmuted_path)

            physical_target = self.router.resolve(transmuted_path)

            # [FACULTY 5 & 6] Reversible Annihilation
            snapshot, snapshot_meta = self._gaze_upon_soul(physical_target)

            if snapshot is None and not physical_target.is_dir():
                Logger.warn(f"Cannot annihilate void: '{transmuted_path}' does not exist.")
                return

            # Note: For recursive dir deletion, perfect undo is complex. We snapshot what we can.
            inverse_op = InverseOp(
                op=LedgerOperation.WRITE_FILE,
                params={"path": transmuted_path, "content_is_snapshot": True}
            )

            entry = LedgerEntry(
                actor="IOConductor",
                operation=LedgerOperation.RMDIR if recursive else LedgerOperation.DELETE_FILE,
                forward_state={"path": transmuted_path},
                inverse_action=inverse_op if snapshot is not None else None,
                snapshot_content=snapshot,
                snapshot_metadata=snapshot_meta
            )
            self._perform_physical_rite(entry)

        except ArtisanHeresy as e:
            Logger.error(f"Annihilation rite for '{logical_path}' blocked: {e.message}")
            if not self.regs.force: raise

    def chmod(self, logical_path: Union[str, Path], mode_str: str):
        """The Grand Rite of Consecration, now reversible."""
        try:
            transmuted_path = self.alchemist.transmute(logical_path)
            self.security.adjudicate_path(transmuted_path)

            physical_target = self.router.resolve(transmuted_path)
            _, snapshot_meta = self._gaze_upon_soul(physical_target)
            old_mode = snapshot_meta.get("mode")

            inverse_op = None
            if old_mode is not None:
                inverse_op = InverseOp(
                    op=LedgerOperation.CHMOD,
                    params={"path": transmuted_path, "mode": oct(old_mode)}
                )

            entry = LedgerEntry(
                actor="IOConductor",
                operation=LedgerOperation.CHMOD,
                forward_state={"path": transmuted_path, "mode": mode_str},
                inverse_action=inverse_op,
                snapshot_metadata=snapshot_meta
            )
            self._perform_physical_rite(entry)

        except ArtisanHeresy as e:
            Logger.error(f"Consecration rite for '{logical_path}' blocked: {e.message}")
            if not self.regs.force: raise

