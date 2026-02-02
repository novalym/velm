# Path: core/runtime/engine/execution/transaction.py
# --------------------------------------------------

import shutil
import os
import uuid
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class FileOp:
    type: str  # 'create', 'modify', 'delete'
    path: Path
    backup_path: Optional[Path] = None
    timestamp: float = field(default_factory=time.time)


class TransactionManager:
    """
    =============================================================================
    == THE CHRONOS VAULT (ATOMIC FILE SYSTEM TRANSACTIONAL MEMORY)             ==
    =============================================================================
    LIF: INFINITY | ROLE: ENTROPY_REVERSAL

    Allows the Engine to perform file operations that can be rolled back upon
    failure. It tracks changed files and restores them from a shadow backup
    if the rite is aborted.
    """

    def __init__(self, logger):
        self.logger = logger
        # Map[TransactionID, List[FileOp]]
        self._active_transactions: Dict[str, List[FileOp]] = {}
        # The Shadow Realm for backups
        self._staging_area = Path(".scaffold/chronos")

    @contextmanager
    def atomic_rite(self, operation_name: str):
        """
        Starts a transaction scope.
        If an exception bubbles up, ROLLBACK is triggered.
        If the block exits cleanly, COMMIT is triggered.
        """
        tx_id = f"{operation_name}-{uuid.uuid4().hex[:8]}"
        self._active_transactions[tx_id] = []

        # Ensure staging area exists (Lazy Init)
        if not self._staging_area.exists():
            self._staging_area.mkdir(parents=True, exist_ok=True)
            # Hide it on Windows
            if os.name == 'nt':
                try:
                    import ctypes
                    ctypes.windll.kernel32.SetFileAttributesW(str(self._staging_area), 2)
                except:
                    pass

        try:
            yield tx_id
            # On success, clear backups (commit)
            self._commit(tx_id)
        except Exception as e:
            # On failure, restore (rollback)
            self.logger.warn(f"Rite '{operation_name}' shattered. Reversing entropy via Chronos Vault.")
            self._rollback(tx_id)
            raise e
        finally:
            self._active_transactions.pop(tx_id, None)

    def register_intent(self, tx_id: str, file_path: Path, intent: str = 'modify'):
        """
        Registers an intent to modify a file. Backs it up if necessary.
        Must be called BEFORE the write occurs.
        """
        if tx_id not in self._active_transactions:
            return  # Not in a transaction scope

        file_path = file_path.resolve()

        # Check if we already tracked this file in this transaction to avoid double-backup
        if any(op.path == file_path for op in self._active_transactions[tx_id]):
            return

        if intent == 'create' or not file_path.exists():
            # If creating, rollback means deleting
            self._active_transactions[tx_id].append(FileOp(type='create', path=file_path))

        elif intent == 'modify' or intent == 'delete':
            # If modifying/deleting, rollback means restoring from backup
            backup_path = self._staging_area / f"{tx_id}_{uuid.uuid4().hex[:4]}_{file_path.name}.bak"
            try:
                shutil.copy2(file_path, backup_path)
                self._active_transactions[tx_id].append(FileOp(
                    type=intent,
                    path=file_path,
                    backup_path=backup_path
                ))
            except Exception as e:
                self.logger.warn(f"Failed to backup {file_path.name}: {e}")

    def _commit(self, tx_id: str):
        """
        The Rite of Finality.
        Deletes the shadow backups as the new reality is accepted.
        """
        ops = self._active_transactions.get(tx_id, [])
        for op in ops:
            if op.backup_path and op.backup_path.exists():
                try:
                    op.backup_path.unlink()
                except:
                    pass

    def _rollback(self, tx_id: str):
        """
        The Rite of Reversal.
        Undoes all operations in reverse chronological order.
        """
        ops = reversed(self._active_transactions.get(tx_id, []))

        for op in ops:
            try:
                if op.type == 'create':
                    # Undo Creation: Delete the file/dir
                    if op.path.exists():
                        if op.path.is_dir():
                            shutil.rmtree(op.path)
                        else:
                            op.path.unlink()

                elif op.type == 'modify' or op.type == 'delete':
                    # Undo Modification/Deletion: Restore from backup
                    if op.backup_path and op.backup_path.exists():
                        # Ensure parent dir exists (in case it was deleted too)
                        op.path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(op.backup_path, op.path)

            except Exception as e:
                self.logger.error(f"Chronos Reversal Failed for {op.path.name}: {e}")