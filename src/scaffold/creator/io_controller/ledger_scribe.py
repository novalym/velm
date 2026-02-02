# Path: scaffold/creator/io_controller/ledger_scribe.py
from __future__ import annotations
from typing import Union, Optional, TYPE_CHECKING

from ...core.state import ActiveLedger
from ...core.state.contracts import LedgerOperation, LedgerEntry
from ...contracts.heresy_contracts import ArtisanHeresy

if TYPE_CHECKING:
    from ...core.sanctum import SanctumInterface
    from pathlib import Path


class LedgerScribe:
    """
    =================================================================================
    == THE SCRIBE OF CAUSALITY (V-Ω-LEDGER-WRITER)                                 ==
    =================================================================================
    The memory of the I/O Conductor. Before any physical action is taken, this
    Scribe is commanded to inscribe a vow of intent into the global Gnostic Ledger.
    It is the artisan responsible for making all I/O operations reversible.
    =================================================================================
    """

    def __init__(self, sanctum: "SanctumInterface"):
        self.sanctum = sanctum

    def record_mkdir(self, path: str):
        ActiveLedger.record(LedgerEntry(
            actor="IOController",
            operation=LedgerOperation.MKDIR,
            reversible=True,
            forward_state={"path": path},
            inverse_state={"path": path}  # Inverse is RMDIR
        ))

    def record_write(self, path: str, new_content: Union[str, bytes]):
        old_content: Optional[str] = None
        if self.sanctum.exists(path) and self.sanctum.is_file(path):
            try:
                # The Gaze of Forgiveness: Attempt to read as text, but fall back gracefully.
                old_content = self.sanctum.read_text(path)
            except (UnicodeDecodeError, ArtisanHeresy):
                old_content = "[binary content]"

        forward_content = new_content
        if isinstance(forward_content, bytes):
            try:
                forward_content = forward_content.decode('utf-8')
            except UnicodeDecodeError:
                forward_content = "[binary content]"

        ActiveLedger.record(LedgerEntry(
            actor="IOController",
            operation=LedgerOperation.WRITE_FILE,
            reversible=True,
            forward_state={"path": path, "content": forward_content},
            inverse_state={"path": path, "content": old_content}
        ))

    def record_delete(self, path: str, recursive: bool):
        # For directories, the inverse is complex (recreating all files).
        # For this ascension, we only make file deletions truly reversible.
        operation = LedgerOperation.RMDIR if recursive else LedgerOperation.DELETE_FILE

        old_content: Optional[str] = None
        is_reversible = False
        if not recursive and self.sanctum.exists(path) and self.sanctum.is_file(path):
            is_reversible = True
            try:
                old_content = self.sanctum.read_text(path)
            except (UnicodeDecodeError, ArtisanHeresy):
                old_content = "[binary content]"

        ActiveLedger.record(LedgerEntry(
            actor="IOController",
            operation=operation,
            reversible=is_reversible,
            forward_state={"path": path, "recursive": recursive},
            inverse_state={"path": path, "content": old_content}  # Inverse is WRITE_FILE
        ))

    def record_chmod(self, path: str, new_mode: str):
        old_mode: Optional[str] = None
        # A true Sanctum interface would have a `stat` method.
        # We perform a humble gaze for now.
        if self.sanctum.exists(path):
            # This logic is a prophecy; it requires the Sanctum to provide mode info.
            # For a LocalSanctum, we could implement this directly.
            pass

        ActiveLedger.record(LedgerEntry(
            actor="IOController",
            operation=LedgerOperation.CHMOD,
            reversible=old_mode is not None,
            forward_state={"path": path, "mode": new_mode},
            inverse_state={"path": path, "mode": old_mode}
        ))

    def record_symlink(self, link_path: str, target_path: str):
        # The inverse of creating a symlink is simply deleting it.
        ActiveLedger.record(LedgerEntry(
            actor="IOController",
            # We use RENAME as a semantic placeholder for "pointing A to B"
            operation=LedgerOperation.RENAME,
            reversible=True,
            forward_state={"src": target_path, "dest": link_path},
            inverse_state={"path": link_path}  # Corresponds to a DELETE operation
        ))