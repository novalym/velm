# Path: scaffold/artisans/undo/reverser.py
# ----------------------------------------

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Any, Dict

from ...core.state.contracts import LedgerOperation, InverseOp, LedgerEntry
from ...creator.io_controller.trash import TrashManager
from ...interfaces.base import Artifact
from ...logger import Scribe
from ...creator.io_controller.path_alchemist import PathAlchemist

Logger = Scribe("TemporalReverser")


class TemporalReverser:
    """
    =================================================================================
    == THE GOD-ENGINE OF ENTROPY REVERSAL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)          ==
    =================================================================================
    The physical hand of the Chronomancer. It receives inverse edicts from the Ledger
    and makes them manifest, unwinding the thread of causality with atomic precision
    and Gnostic awareness.
    """

    def __init__(self, trash_manager: TrashManager, project_root: Path, gnosis: Dict[str, Any] = None):
        self.trash = trash_manager
        self.root = project_root
        # [ASCENSION 6] The Polyglot Path Alchemist
        self.alchemist = PathAlchemist(gnosis or {})

    def reverse(self, inverse: InverseOp, entry: LedgerEntry) -> Optional[Artifact]:
        """
        [ASCENSION 1] The Gnostic Unpacking.
        Executes a single inverse operation, now with full Gnostic context from the Ledger Entry.
        """
        op = inverse.op
        params = inverse.params

        # Transmute any paths in the parameters
        transmuted_params = {
            k: self.alchemist.transmute(v) if isinstance(v, str) and ('/' in v or '\\' in v) else v
            for k, v in params.items()
        }

        if op == LedgerOperation.WRITE_FILE:
            return self._restore_file_from_snapshot(transmuted_params, entry)
        elif op == LedgerOperation.DELETE_FILE:
            return self._delete_file(transmuted_params)
        elif op == LedgerOperation.RMDIR:
            return self._rmdir(transmuted_params)
        elif op == LedgerOperation.CHMOD:
            return self._revert_chmod(transmuted_params, entry)
        elif op == LedgerOperation.EXEC_SHELL:
            return self._exec_shell(transmuted_params)
        elif op == LedgerOperation.RESTORE_FILE:  # Legacy fallback
            return self._restore_from_trash(transmuted_params)
        else:
            Logger.warn(f"Unknown Inverse Op: {op}. The timeline at this point is immutable.")
            return None

    def _restore_file_from_snapshot(self, params: dict, entry: LedgerEntry) -> Artifact:
        """
        [ASCENSION 2 & 3] The Quantum State Restorer & Metadata Chronomancer.
        Restores a file's soul and metadata directly from the Ledger's snapshot.
        """
        original_path = self.root / params["path"]

        if params.get("content_is_snapshot"):
            content_bytes = entry.snapshot_content
            if content_bytes is None:
                raise ValueError(f"Ledger promised a snapshot for '{original_path.name}', but its soul is a void.")

            # The Unbreakable Ward
            try:
                original_path.parent.mkdir(parents=True, exist_ok=True)
                original_path.write_bytes(content_bytes)

                # Restore Metadata
                meta = entry.snapshot_metadata
                if meta.get("mode"):
                    original_path.chmod(meta["mode"])
                if meta.get("mtime"):
                    os.utime(original_path, (meta["mtime"], meta["mtime"]))

                Logger.verbose(f"Restored '{original_path.name}' from Gnostic Snapshot.")
                return Artifact(path=original_path, type="file", action="restored")
            except Exception as e:
                raise IOError(f"Failed to restore '{original_path.name}' from snapshot: {e}") from e
        else:
            raise ValueError("InverseOp for WRITE_FILE was missing 'content_is_snapshot' vow.")

    def _delete_file(self, params: dict) -> Artifact:
        """[ASCENSION 5] The Void Sentinel. Annihilates a created file."""
        target = self.root / params["path"]

        if target.exists():
            try:
                target.unlink()
                Logger.verbose(f"Reverted Creation: Annihilated {target.name}")
                return Artifact(path=target, type="file", action="deleted")
            except Exception as e:
                raise IOError(f"Failed to annihilate '{target.name}': {e}") from e
        else:
            Logger.verbose(f"Revert skipped: '{target.name}' already vanished from reality.")
            return Artifact(path=target, type="file", action="skipped")

    def _rmdir(self, params: dict) -> Artifact:
        """[ASCENSION 11] The Recursive Annihilator."""
        target = self.root / params["path"]
        recursive = params.get("recursive", False)

        if target.exists() and target.is_dir():
            try:
                if recursive:
                    shutil.rmtree(target)
                else:
                    target.rmdir()  # Will fail if not empty, which is correct
                Logger.verbose(f"Reverted Mkdir: Returned '{target.name}' to the void.")
                return Artifact(path=target, type="directory", action="deleted")
            except OSError as e:
                Logger.warn(f"Could not revert mkdir for '{target.name}': {e}")
                return Artifact(path=target, type="directory", action="skipped")

        return Artifact(path=target, type="directory", action="skipped")

    def _revert_chmod(self, params: dict, entry: LedgerEntry) -> Artifact:
        """Restores old permissions from the snapshot metadata."""
        target = self.root / params["path"]
        old_mode = entry.snapshot_metadata.get("mode")

        if target.exists() and old_mode is not None:
            try:
                target.chmod(old_mode)
                Logger.verbose(f"Reverted Permissions: {target.name} -> {oct(old_mode)}")
                return Artifact(path=target, type="file", action="chmod_reverted")
            except Exception as e:
                Logger.warn(f"Failed to revert chmod for {target.name}: {e}")

        return Artifact(path=target, type="file", action="skipped")

    def _exec_shell(self, params: dict) -> Optional[Artifact]:
        """[ASCENSION 4] Conducts a Maestro's Counter-Edict."""
        commands = params.get("commands")
        cwd = Path(params.get("cwd", self.root))

        if not commands:
            return None

        for cmd in commands:
            if cmd.startswith("#"):
                Logger.warn(f"[UNDO] {cmd.lstrip('#').strip()}")
                continue

            Logger.info(f"Executing Counter-Edict: [yellow]$ {cmd}[/yellow]")
            try:
                subprocess.run(cmd, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                Logger.error(f"Counter-Edict '{cmd}' failed with exit code {e.returncode}:\n{e.stderr}")
                # We do not halt the undo symphony for a failed counter-edict
        return None

    def _restore_from_trash(self, params: dict) -> Artifact:
        """Legacy fallback to restore from the .scaffold/trash void."""
        trash_path = Path(params["trash_path"])
        original_path = Path(params["original_path"])

        self.trash.restore_from_trash(trash_path, original_path)

        return Artifact(path=original_path, type="file", action="restored")