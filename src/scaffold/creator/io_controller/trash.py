# Path: scaffold/core/io_controller/trash.py
# ------------------------------------------

import shutil
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

from ...logger import Scribe
from ...core.state.contracts import LedgerEntry, RiteLedger
# === THE APOTHEOSIS IS COMPLETE ===


Logger = Scribe("TheVoidManager")


class TrashManager:
    """
    =================================================================================
    == THE VOID MANAGER (V-Ω-REVERSIBLE-DESTRUCTION)                               ==
    =================================================================================
    LIF: 10,000,000,000

    This artisan manages the `.scaffold/trash` sanctum. It ensures that no file is
    ever truly annihilated without a path of return. It moves deleted or overwritten
    files into a transaction-scoped void and chronicles the event for the Undo Artisan.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.trash_root = self.project_root / ".scaffold" / "trash"
        self._ensure_sanctum()

    def _ensure_sanctum(self):
        if not self.trash_root.exists():
            self.trash_root.mkdir(parents=True, exist_ok=True)

    def _get_tx_trash_path(self, tx_id: str) -> Path:
        """Resolves the trash sanctum for a specific transaction."""
        return self.trash_root / tx_id

    def move_to_trash(self, path: Path, tx_id: str, is_overwrite: bool = False) -> Path:
        """
        Translocates a file to the Void.
        Returns the absolute path in the trash.
        """
        if not path.exists():
            raise FileNotFoundError(f"Cannot trash a void: {path}")

        tx_trash_root = self._get_tx_trash_path(tx_id)
        if not tx_trash_root.exists():
            tx_trash_root.mkdir(parents=True, exist_ok=True)

        # Calculate relative path to preserve structure
        try:
            rel_path = path.relative_to(self.project_root)
        except ValueError:
            # Handle external files by flattening name
            rel_path = Path("__EXTERNAL__") / path.name

        dest_path = tx_trash_root / rel_path

        # Handle Overwrites within the same transaction (e.g., file modified twice)
        if dest_path.exists():
            timestamp = int(time.time() * 1000)
            dest_path = dest_path.with_name(f"{dest_path.name}.{timestamp}.bak")

        # Ensure parent dirs exist in trash
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(path), str(dest_path))

        reason = "Overwrite" if is_overwrite else "Deletion"
        Logger.verbose(f"Sent to Void ({reason}): {rel_path} -> {dest_path.relative_to(self.trash_root)}")

        return dest_path

    def restore_from_trash(self, trash_path: Path, original_path: Path):
        """
        The Rite of Resurrection.
        Moves a file from the Void back to Reality.
        """
        if not trash_path.exists():
            raise FileNotFoundError(f"Trash artifact missing: {trash_path}")

        if original_path.exists():
            # If reality is occupied, we must clear it before restoring (Overwrite Reversal)
            # Or should we fail? Undo implies force.
            if original_path.is_dir():
                shutil.rmtree(original_path)
            else:
                original_path.unlink()

        original_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(trash_path), str(original_path))
        Logger.success(f"Resurrected: {original_path.name}")

    def chronicle_ledger(self, tx_id: str, ledger_entries: List[LedgerEntry]):
        """
        [THE PERSISTENT MEMORY - ASCENDED]
        Saves the transaction ledger, now correctly using the RiteLedger vessel.
        """
        tx_root = self._get_tx_trash_path(tx_id)
        tx_root.mkdir(parents=True, exist_ok=True)

        ledger_path = tx_root / "ledger.json"  # Change to .json for a single object

        # We now create an instance of the RiteLedger data contract
        ledger_vessel = RiteLedger(
            rite_id=tx_id,
            rite_name="Unknown",  # A future ascension could pass the rite name here
            entries=ledger_entries
        )

        ledger_path.write_text(ledger_vessel.model_dump_json(indent=2), encoding='utf-8')

    def read_ledger(self, tx_id: str) -> List[LedgerEntry]:
        """Reads the chronicle from the Void, now understanding the new vessel."""
        ledger_path = self._get_tx_trash_path(tx_id) / "ledger.json"
        if not ledger_path.exists():
            return []

        data = json.loads(ledger_path.read_text(encoding='utf-8'))
        ledger_vessel = RiteLedger.model_validate(data)
        return ledger_vessel.entries