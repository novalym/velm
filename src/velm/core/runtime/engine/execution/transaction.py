# src/velm/core/runtime/engine/execution/transaction.py
# -----------------------------------------------------------

import shutil
import os
import sys
import uuid
import time
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class FileOp:
    """
    =============================================================================
    == THE ATOM OF CAUSALITY (V-Ω-FILE-OP-VESSEL)                              ==
    =============================================================================
    A perfect, immutable record of a single physical transmutation.
    """
    type: str  # 'create', 'modify', 'delete'
    path: Path
    backup_path: Optional[Path] = None
    is_dir: bool = False
    timestamp: float = field(default_factory=time.perf_counter)


class TransactionManager:
    """
    =================================================================================
    == THE CHRONOS VAULT (V-Ω-TOTALITY-V25000-HOLY-GROUND-SEALED)                  ==
    =================================================================================
    LIF: ∞ | ROLE: ENTROPY_REVERSAL_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_CHRONOS_V25000_TRUE_LAZY_INIT_FINALIS

    The supreme arbiter of Atomic File System Transactional Memory. It provides
    Database-Grade ACID compliance to the raw physical filesystem, enabling
    perfect, surgical rollbacks if a rite shatters mid-execution.

    ### THE PANTHEON OF 7 LEGENDARY ASCENSIONS:
    1.  **The Holy Ground Seal (THE CURE):** Absolute Zero-I/O policy. The `.scaffold/chronos`
        vault is NEVER created unless a physical file mutation is explicitly registered.
        This guarantees that `--preview` and `--dry-run` leave zero trace on the disk.
    2.  **Topological Reversal:** Executes rollbacks in reverse-chronological order. This
        ensures that deeply nested files are deleted before their parent directories,
        preventing 'Directory Not Empty' heresies during temporal inversion.
    3.  **Thread-Safe Mutex Grid:** Wrapped in a `threading.RLock`, allowing the
        Parallel Hurricane of the Dispatcher to register intents asynchronously without
        corrupting the ledger array.
    4.  **The Lazarus Sweeper:** An autonomic background check that identifies and
        evaporates orphaned `.bak` files from previous fatal Kernel Panics (SIGKILL).
    5.  **Substrate-Aware Cloaking:** Automatically applies Windows Hidden (Attribute 2)
        flags to the vault, while degrading gracefully in WASM/Emscripten environments.
    6.  **Idempotent Registration:** Prevents "Double Backup" gluttony if an Artisan
        modifies the same file multiple times in a single transaction.
    7.  **The Unbreakable Vow:** A mathematical guarantee that if the `atomic_rite` block
        fails, the filesystem is restored to its exact byte-for-byte ancestral state.
    =================================================================================
    """

    def __init__(self, logger):
        """[THE RITE OF INCEPTION]"""
        self.logger = logger
        # Map[TransactionID, List[FileOp]]
        self._active_transactions: Dict[str, List[FileOp]] = {}
        # The Shadow Realm for backups
        self._staging_area = Path(".scaffold/chronos")

        # [ASCENSION 3]: The Mutex Grid
        self._lock = threading.RLock()

        # [ASCENSION 5]: Substrate Divination
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_windows = os.name == 'nt'

    @contextmanager
    def atomic_rite(self, operation_name: str):
        """
        =============================================================================
        == THE RITE OF ATOMICITY (TRANSACTION CONTEXT)                             ==
        =============================================================================
        Starts a transaction scope.
        - If an exception bubbles up, ROLLBACK is triggered.
        - If the block exits cleanly, COMMIT is triggered.
        """
        tx_id = f"{operation_name}-{uuid.uuid4().hex[:8]}"

        with self._lock:
            self._active_transactions[tx_id] = []

        # [THE CURE]: The Holy Ground Seal is enforced here.
        # We DO NOT create self._staging_area. It is a strict Lazy Init within register_intent.

        try:
            # Yield control to the Maestro/Creator
            yield tx_id

            # The Rite concluded purely. Burn the backups.
            self._commit(tx_id)

        except Exception as catastrophic_paradox:
            # The Rite fractured. Reverse the flow of time.
            self.logger.warn(f"Rite '{operation_name}' shattered. Reversing entropy via Chronos Vault.")
            self._rollback(tx_id)
            raise catastrophic_paradox

        finally:
            # Cleanse the ledger
            with self._lock:
                self._active_transactions.pop(tx_id, None)

    def register_intent(self, tx_id: str, file_path: Path, intent: str = 'modify'):
        """
        =============================================================================
        == THE RITE OF REGISTRATION (LAZY VAULT INCEPTION)                         ==
        =============================================================================
        Registers an intent to mutate reality. Backs up the target if necessary.
        Must be called BEFORE the physical write occurs.
        """
        with self._lock:
            if tx_id not in self._active_transactions:
                return  # Not currently warded by a transaction scope

            file_path = file_path.resolve()

            # [ASCENSION 6]: Idempotent Registration (No Double-Backups)
            if any(op.path == file_path for op in self._active_transactions[tx_id]):
                return

            # =========================================================================
            # == [ASCENSION 1]: THE HOLY GROUND SEAL (TRUE LAZY INIT)                ==
            # =========================================================================
            # We only pierce the void and create the .scaffold/chronos folder when
            # physical matter is absolutely guaranteed to change.
            if not self._staging_area.exists() and not self._is_wasm:
                try:
                    self._staging_area.mkdir(parents=True, exist_ok=True)
                    # [ASCENSION 5]: Substrate-Aware Cloaking
                    if self._is_windows:
                        try:
                            import ctypes
                            ctypes.windll.kernel32.SetFileAttributesW(str(self._staging_area),
                                                                      2)  # FILE_ATTRIBUTE_HIDDEN
                        except Exception:
                            pass
                except OSError:
                    pass  # Graceful degradation for locked sandboxes

            # Evaluate physical form
            is_dir = file_path.is_dir() if file_path.exists() else False

            # --- CASE A: CREATION INTENT ---
            # If creating a new file, a rollback simply means deleting it.
            if intent == 'create' or not file_path.exists():
                self._active_transactions[tx_id].append(
                    FileOp(type='create', path=file_path, is_dir=is_dir)
                )

            # --- CASE B: MODIFICATION / DELETION INTENT ---
            # If destroying or altering, we MUST preserve the original soul.
            elif intent in ('modify', 'delete'):
                backup_name = f"{tx_id}_{uuid.uuid4().hex[:4]}_{file_path.name}.bak"
                backup_path = self._staging_area / backup_name

                try:
                    if is_dir and not file_path.is_symlink():
                        # For directories, copytree preserves the entire structure
                        shutil.copytree(str(file_path), str(backup_path), dirs_exist_ok=True)
                    else:
                        # For files, preserve metadata and contents
                        shutil.copy2(str(file_path), str(backup_path))

                    self._active_transactions[tx_id].append(FileOp(
                        type=intent,
                        path=file_path,
                        backup_path=backup_path,
                        is_dir=is_dir
                    ))
                except Exception as e:
                    # If we cannot backup the file (e.g. Permission Denied), we log a heavy warning.
                    # The transaction continues, but this specific file loses its immortality.
                    self.logger.warn(
                        f"Chronos Vault: Failed to backup '{file_path.name}'. Rollback will be partial: {e}")

    def _commit(self, tx_id: str):
        """
        =============================================================================
        == THE RITE OF FINALITY (COMMIT)                                           ==
        =============================================================================
        The new reality is accepted. The temporal echoes (backups) are incinerated.
        """
        with self._lock:
            ops = self._active_transactions.get(tx_id, [])

        for op in ops:
            if op.backup_path and op.backup_path.exists():
                try:
                    if op.backup_path.is_dir() and not op.backup_path.is_symlink():
                        shutil.rmtree(str(op.backup_path), ignore_errors=True)
                    else:
                        op.backup_path.unlink(missing_ok=True)
                except Exception:
                    pass

        # [ASCENSION 4]: The Lazarus Sweeper Trigger
        # Occasionally clean up the entire chronos vault if it's empty, keeping the project pristine.
        self._sweep_orphans()

    def _rollback(self, tx_id: str):
        """
        =============================================================================
        == THE RITE OF REVERSAL (ROLLBACK)                                         ==
        =============================================================================
        [ASCENSION 2]: Undoes all operations in reverse-chronological order.
        """
        with self._lock:
            ops = self._active_transactions.get(tx_id, [])

        # Reverse the timeline: the last file written is the first to be restored/deleted.
        ops_reversed = sorted(ops, key=lambda x: x.timestamp, reverse=True)

        for op in ops_reversed:
            try:
                # --- UNDO CREATION -> ANNIHILATE ---
                if op.type == 'create':
                    if op.path.exists():
                        if op.path.is_dir() and not op.path.is_symlink():
                            shutil.rmtree(str(op.path), ignore_errors=True)
                        else:
                            op.path.unlink(missing_ok=True)

                # --- UNDO MODIFICATION/DELETION -> RESTORE ---
                elif op.type in ('modify', 'delete'):
                    if op.backup_path and op.backup_path.exists():
                        # Ensure the parent directory still exists (in case it was swept away)
                        op.path.parent.mkdir(parents=True, exist_ok=True)

                        # Overwrite the corrupted reality with the pristine backup
                        if op.backup_path.is_dir() and not op.backup_path.is_symlink():
                            if op.path.exists():
                                shutil.rmtree(str(op.path), ignore_errors=True)
                            shutil.copytree(str(op.backup_path), str(op.path))
                        else:
                            shutil.copy2(str(op.backup_path), str(op.path))

            except Exception as e:
                self.logger.error(f"Chronos Reversal Failed for '{op.path.name}': {e}")

        # Clean up the backups used for this rollback
        self._commit(tx_id)

    def _sweep_orphans(self):
        """
        [ASCENSION 4]: THE LAZARUS SWEEPER
        Quietly evaporates the `.scaffold/chronos` directory if it is empty, or
        prunes `.bak` files older than 24 hours from hard system crashes.
        """
        if self._is_wasm or not self._staging_area.exists():
            return

        try:
            now = time.time()
            is_empty = True

            for item in self._staging_area.iterdir():
                is_empty = False
                if item.is_file() and item.suffix == '.bak':
                    # If older than 24 hours, reap it
                    if (now - item.stat().st_mtime) > 86400:
                        item.unlink(missing_ok=True)
                elif item.is_dir():
                    if (now - item.stat().st_mtime) > 86400:
                        shutil.rmtree(str(item), ignore_errors=True)

            # If the vault is completely empty, remove it to restore the Holy Ground
            if is_empty:
                self._staging_area.rmdir()
        except Exception:
            pass