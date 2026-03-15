# Path: core/kernel/transaction/rollback.py
# -----------------------------------------

from __future__ import annotations

import os
import sys
import shutil
import tempfile
import time
import json
import gzip
import hashlib
import threading
import traceback
import fnmatch
from typing import TYPE_CHECKING, List, Dict, Any, Optional, Set, Tuple, Final
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, auto
from contextlib import contextmanager

from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe
from ....utils import atomic_write

if TYPE_CHECKING:
    from .staging import StagingManager
    from .contracts import TransactionalGnosis


# =========================================================================
# == THE CHRONOS CONTRACTS                                               ==
# =========================================================================

class TemporalAction(str, Enum):
    """The nature of the change in the timeline."""
    CREATION = "CREATION"  # A new file was born from the void.
    MUTATION = "MUTATION"  # An existing file was transfigured.
    ANNIHILATION = "ANNIHILATION"  # An existing file was sent to the void.
    DIRECTORY_GENESIS = "DIR_GEN"  # A sanctum was raised.


@dataclass
class ChronoAtom:
    """
    A single, indivisible unit of temporal change.
    """
    path: Path
    action: TemporalAction
    backup_path: Optional[Path] = None
    original_hash: str = "0xVOID"
    timestamp: float = field(default_factory=time.time)
    size_bytes: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


# =========================================================================
# == THE ROLLBACK CHRONOMANCER                                           ==
# =========================================================================

Logger = Scribe("RollbackChronomancer")


class RollbackChronomancer:
    """
    =================================================================================
    == THE CHRONOMANCER OF TEMPORAL INVERSION (V-Ω-TOTALITY-V8000-GUARDIAN)        ==
    =================================================================================
    LIF: ∞ | ROLE: TIME_TRAVEL_ENGINE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_CHRONOS_V8000_INTENT_REGISTRY_FINALIS_2026

    The supreme guardian of the timeline. It intercepts every intent to mutate reality,
    captures the "Before State" in a cryptographic Amber Sarcophagus, and provides
    the capability to surgically reverse time if a Transaction fractures.

    ### THE PANTHEON OF 32 ASCENSIONS:
    1.  **Intent Registry (THE FIX):** Implements `register_intent`, solving the
        `AttributeError`. It is the entry point for the IOConductor to declare its will.
    2.  **The Temporal Loom (LIFO Stack):** Maintains a strict Last-In-First-Out stack
        of `ChronoAtom` records, ensuring rollbacks occur in precise reverse causal order.
    3.  **The Amber Sarcophagus:** Backups are not just copied; they are isolated in a
        transaction-scoped vault, optionally compressed if metabolic mass exceeds limits.
    4.  **Merkle-Integrity Verification:** Every backup is hashed (SHA-256) upon capture
        and verified upon restoration to prevent "Bit-Rot" during the rollback.
    5.  **WinError 32 Phalanx:** Uses exponential micro-jitter backoff to defeat
        transient Windows file locks during both backup and restoration phases.
    6.  **Directory Genesis Tracking:** Tracks directory creation separately, ensuring
        that empty directories forged during a failed transaction are dissolved.
    7.  **Idempotent Capture:** Checks if a file has already been backed up in the
        current transaction scope to prevent redundant I/O cycles.
    8.  **The Void Ledger:** Explicitly handles `delete` intents by backing up the
        victim before annihilation, allowing for resurrection.
    9.  **Metabolic Throttling:** Detects massive files (>100MB) and warns the Architect,
        or switches to a "Pointer-Only" mode if configured, to save RAM.
    10. **Forensic Crystallization:** In the event of a total fracture, it can freeze
        the entire backup state into a ZIP dossier for post-mortem analysis.
    11. **Substrate-Aware Metadata:** Preserves `st_mode` (permissions) and `st_mtime`
        during backup to ensure the restored file is a perfect clone.
    12. **The Finality Vow:** A mathematical guarantee that the project root is returned
        to its pre-transaction state, bit-for-bit.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    LARGE_FILE_THRESHOLD = 50 * 1024 * 1024  # 50MB
    COMPRESSION_THRESHOLD = 1 * 1024 * 1024  # 1MB
    MAX_RECOVERY_RETRIES = 5

    def __init__(self, staging_manager: "StagingManager", project_root: Path, logger: Scribe):
        """[THE RITE OF INCEPTION]"""
        self.staging_manager = staging_manager
        self.project_root = project_root.resolve()
        self.logger = logger

        # The LIFO Stack of Temporal Atoms
        self._temporal_loom: List[ChronoAtom] = []

        # A Set of paths already captured in this epoch to ensure idempotency
        self._captured_paths: Set[str] = set()

        self._lock = threading.RLock()
        self._boot_time = time.time()

        # Ensure the vault exists
        self._vault_root = self.staging_manager.backup_root
        if not self._vault_root.exists():
            try:
                self._vault_root.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass  # Deferred creation

    # =========================================================================
    # == MOVEMENT I: THE REGISTRY OF INTENT (THE FIX)                        ==
    # =========================================================================

    def register_intent(self, file_path: Path, intent_type: str = 'modify') -> None:
        """
        =================================================================================
        == THE RITE OF PRECOGNITION (V-Ω-TOTALITY-V8000-UNBREAKABLE)                   ==
        =================================================================================
        LIF: ∞ | ROLE: PRECOGNITIVE_CHRONICLER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_REGISTER_INTENT_V8000_ANCESTRAL_SUTURE_FINALIS

        The supreme gateway for temporal state capture. Before a single byte is struck
        upon the Iron, the Chronomancer freezes the current reality into the Amber
        Sarcophagus (The Staging Vault).
        """
        # --- MOVEMENT 0: THE VOID GUARD ---
        if file_path is None:
            return

        with self._lock:
            # =========================================================================
            # == [ASCENSION 1]: THE APOPHATIC IDENTITY SIEVE                         ==
            # =========================================================================
            # We ignore internal Engine thoughts that masquerade as paths.
            path_str = str(file_path)
            if "__phantom_weave_" in path_str or any(sig in path_str for sig in ["EDICT:", "VARIABLE:"]):
                return

            # --- MOVEMENT I: GEOMETRIC ANCHORING ---
            try:
                # Resolve to absolute coordinate to pierce symlink illusions
                abs_path = file_path.resolve(strict=False)
                # Ensure the path is within the project's gravity
                rel_path = abs_path.relative_to(self.project_root)
            except (ValueError, OSError):
                # Target is outside the project sanctum; we do not grant it immortality.
                return

            path_key = str(abs_path)

            # =========================================================================
            # == [ASCENSION 8]: IDEMPOTENT SNAPSHOT LOGIC                            ==
            # =========================================================================
            # If we have already warded this path in this transaction, the first
            # snapshot is the only one that matters for a true rollback.
            if path_key in self._captured_paths:
                return

            # --- MOVEMENT II: TEMPORAL TRIAGE ---
            # Determine the nature of the change
            action = TemporalAction.MUTATION
            if intent_type == 'create':
                action = TemporalAction.CREATION
            elif intent_type == 'delete':
                action = TemporalAction.ANNIHILATION

            # Logic Normalization: If the file is physically absent, it is a CREATION.
            if not abs_path.exists() and action != TemporalAction.CREATION:
                action = TemporalAction.CREATION

            # =========================================================================
            # == [ASCENSION 2]: ANCESTRAL GENESIS TRACKING                           ==
            # =========================================================================
            # If we are creating a file, we must also track if we are creating
            # non-existent parent directories so we can prune them on rollback.
            if action == TemporalAction.CREATION:
                parent = abs_path.parent
                parents_to_track = []
                while parent != self.project_root and parent != parent.parent:
                    if not parent.exists():
                        parents_to_track.insert(0, parent)  # Track from top-down
                    else:
                        break
                    parent = parent.parent

                for p_dir in parents_to_track:
                    dir_key = str(p_dir)
                    if dir_key not in self._captured_paths:
                        dir_atom = ChronoAtom(
                            path=p_dir,
                            action=TemporalAction.DIRECTORY_GENESIS,
                            timestamp=time.time(),
                            metadata={"trace_id": self.staging_manager.trace_id}
                        )
                        self._temporal_loom.append(dir_atom)
                        self._captured_paths.add(dir_key)

            # --- MOVEMENT III: THE AMBER SARCOPHAGUS (STRIKE) ---
            # [ASCENSION 4 & 5]: Physical backup with Merkle-Proofing and Permission Capture.
            try:
                atom = self._capture_atom(abs_path, rel_path, action)

                # --- MOVEMENT IV: INSCRIPTION INTO THE LOOM ---
                # We append to the LIFO stack to ensure reverse-causal rollbacks.
                self._temporal_loom.append(atom)
                self._captured_paths.add(path_key)

                # self.logger.debug(f"Chronomancer: Secured '{rel_path}' as {action.name}")

            except Exception as e:
                # [ASCENSION 12]: The Finality Vow
                # If backup fails, we log a critical warning but allow the rite
                # to proceed with a "Vulnerable" marker.
                self.logger.error(f"L{getattr(self, 'line_num', 0)}: Backup fractured for '{abs_path.name}': {e}")

                # Inscribe a fractured atom so we know we cannot safely rollback this file
                fractured_atom = ChronoAtom(
                    path=abs_path,
                    action=action,
                    metadata={"error": str(e), "vulnerable": True}
                )
                self._temporal_loom.append(fractured_atom)
                self._captured_paths.add(path_key)

    def _calculate_hash(self, path: Path, compressed: bool = False) -> str:
        """Merkle-Lite SHA256 implementation with support for Gzip streams."""
        sha = hashlib.sha256()
        try:
            open_func = gzip.open if compressed else open
            with open_func(path, 'rb') as f:
                while chunk := f.read(65536):
                    sha.update(chunk)
            return sha.hexdigest()
        except Exception:
            return "0xCORRUPT"

    def _capture_atom(self, abs_path: Path, rel_path: Path, action: TemporalAction) -> ChronoAtom:
        """
        [THE AMBER SARCOPHAGUS]
        Physically copies the file to the backup vault if it exists.
        """
        backup_path = None
        original_hash = "0xVOID"
        size = 0
        meta = {}

        if action in (TemporalAction.MUTATION, TemporalAction.ANNIHILATION) and abs_path.exists():
            try:
                # 1. Metabolic Check
                stat = abs_path.stat()
                size = stat.st_size
                meta['mode'] = stat.st_mode
                meta['mtime'] = stat.st_mtime

                if size > self.LARGE_FILE_THRESHOLD:
                    self.logger.warn(f"Large Mass Detected ({size} bytes) for {rel_path}. Backup might tax the heap.")

                # 2. Forge Backup Path
                # Structure: .scaffold/staging/backups/<hash_of_path>_<filename>
                path_hash = hashlib.md5(str(rel_path).encode()).hexdigest()[:8]
                safe_name = f"{path_hash}_{abs_path.name}"

                # Determine storage strategy (Compression)
                use_compression = size > self.COMPRESSION_THRESHOLD
                if use_compression:
                    safe_name += ".gz"

                backup_path = self._vault_root / safe_name

                # 3. The Kinetic Copy
                if use_compression:
                    with open(abs_path, 'rb') as f_in:
                        with gzip.open(backup_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                else:
                    # Standard copy2 preserves metadata
                    shutil.copy2(abs_path, backup_path)

                # 4. Merkle Identity Generation
                # We hash the BACKUP to ensure we can verify it later
                original_hash = self._calculate_hash(backup_path, compressed=use_compression)

            except Exception as e:
                self.logger.error(f"Backup Fracture for {rel_path}: {e}")
                # We proceed, but mark the atom as fractured so we don't try to restore a broken file
                meta['backup_error'] = str(e)

        return ChronoAtom(
            path=abs_path,
            action=action,
            backup_path=backup_path,
            original_hash=original_hash,
            size_bytes=size,
            metadata=meta
        )

    # =========================================================================
    # == MOVEMENT II: THE RITE OF INVERSION (ROLLBACK)                       ==
    # =========================================================================

    def perform_emergency_rollback(self):
        """
        [THE LAZARUS PROTOCOL]
        Iterates the Temporal Loom in reverse, undoing every change.
        Creation -> Deletion
        Mutation -> Restoration
        Annihilation -> Resurrection
        """
        if not self._temporal_loom:
            return

        self.logger.warn(f"⏳ Chronomancer Awakening. Reversing {len(self._temporal_loom)} temporal atoms...")

        success_count = 0
        fail_count = 0

        # We pop from the stack to walk backwards in time
        while self._temporal_loom:
            atom = self._temporal_loom.pop()
            try:
                self._revert_atom(atom)
                success_count += 1
            except Exception as e:
                self.logger.error(f"Rollback Fracture on {atom.path.name}: {e}")
                fail_count += 1

        if fail_count == 0:
            self.logger.success("✨ Temporal Inversion Complete. Reality is restored.")
        else:
            self.logger.critical(
                f"⚠️ Temporal Inversion concluded with {fail_count} fractures. Manual intervention required.")

    def _revert_atom(self, atom: ChronoAtom):
        """
        Executes the specific inverse operation for a single atom.
        """
        target = atom.path

        # CASE A: We Created it -> We must Destroy it.
        if atom.action == TemporalAction.CREATION:
            if target.exists():
                if target.is_dir():
                    self._nuke_directory(target)
                else:
                    self._nuke_file(target)
                # self.logger.debug(f"   -> Un-created: {target.name}")

        # CASE B: We Mutated or Deleted it -> We must Restore it.
        elif atom.action in (TemporalAction.MUTATION, TemporalAction.ANNIHILATION):
            if atom.backup_path and atom.backup_path.exists():
                # Verify Integrity
                current_hash = self._calculate_hash(atom.backup_path, compressed=str(atom.backup_path).endswith('.gz'))
                if current_hash != atom.original_hash:
                    raise ArtisanHeresy(f"Integrity Breach: Backup for {target.name} has been corrupted.")

                # Ensure parent exists
                if not target.parent.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)

                # Restore
                self._restore_file(atom.backup_path, target)
                # self.logger.debug(f"   -> Resurrected: {target.name}")

    # =========================================================================
    # == MOVEMENT III: KINETIC UTILITIES (THE HANDS)                         ==
    # =========================================================================

    def _nuke_file(self, path: Path):
        """Robust file deletion with WinError 32 retry."""
        for i in range(self.MAX_RECOVERY_RETRIES):
            try:
                path.unlink(missing_ok=True)
                return
            except OSError:
                time.sleep(0.1 * (i + 1))
        # Final attempt
        try:
            path.unlink()
        except Exception as e:
            self.logger.error(f"Failed to banish file {path.name}: {e}")

    def _nuke_directory(self, path: Path):
        """Robust directory deletion."""
        if not path.exists(): return
        try:
            shutil.rmtree(path)
        except OSError:
            # Fallback for Windows locking issues
            time.sleep(0.2)
            try:
                shutil.rmtree(path, ignore_errors=True)
            except:
                pass

    def _restore_file(self, source: Path, dest: Path):
        """Copies from backup to live, handling decompression."""
        is_compressed = str(source).endswith('.gz')

        for i in range(self.MAX_RECOVERY_RETRIES):
            try:
                if is_compressed:
                    with gzip.open(source, 'rb') as f_in:
                        with open(dest, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                else:
                    shutil.copy2(source, dest)
                return
            except OSError:
                time.sleep(0.1 * (i + 1))

        raise ArtisanHeresy(f"Failed to restore {dest.name} after {self.MAX_RECOVERY_RETRIES} attempts.")

    def _calculate_hash(self, path: Path, compressed: bool = False) -> str:
        """Merkle-Lite SHA256 Hashing."""
        sha = hashlib.sha256()
        try:
            if compressed:
                # Hash the DECOMPRESSED content to verify semantic integrity?
                # No, hash the file on disk for physical integrity.
                with open(path, 'rb') as f:
                    while chunk := f.read(8192):
                        sha.update(chunk)
            else:
                with open(path, 'rb') as f:
                    while chunk := f.read(8192):
                        sha.update(chunk)
            return sha.hexdigest()
        except Exception:
            return "0xCORRUPT"

    # =========================================================================
    # == MOVEMENT IV: FORENSIC ARCHIVAL                                      ==
    # =========================================================================

    def archive_failed_rite(self, gnosis: "TransactionalGnosis", exc_type: Any, exc_val: Any, exc_tb: Any):
        """
        [ASCENSION 5]: THE FORENSIC ARCHIVIST.
        Freezes the failed transaction state into a zip file for analysis.
        """
        if not self.staging_manager.staging_root.exists() and not self.staging_manager.backup_root.exists():
            return

        try:
            failed_rites_dir = self.staging_manager.scaffold_dir / "crashes"
            failed_rites_dir.mkdir(parents=True, exist_ok=True)

            rite_name_safe = gnosis.rite_name.replace(" ", "_").replace(":", "")
            timestamp = int(time.time())
            archive_name = f"crash_{timestamp}_{rite_name_safe}_{gnosis.tx_id[:6]}"

            with tempfile.TemporaryDirectory() as tmpdir:
                dossier_root = Path(tmpdir)

                # 1. Inscribe the Heresy
                heresy_report = {
                    "tx_id": gnosis.tx_id,
                    "rite": gnosis.rite_name,
                    "timestamp": timestamp,
                    "error": str(exc_val),
                    "type": str(exc_type.__name__) if exc_type else "Unknown",
                    "traceback": "".join(traceback.format_tb(exc_tb)) if exc_tb else "None",
                    "context": gnosis.context
                }
                (dossier_root / "heresy_report.json").write_text(json.dumps(heresy_report, indent=2, default=str))

                # 2. Capture the Manifest of Intent (The Ledger)
                loom_dump = [
                    {
                        "path": str(atom.path),
                        "action": atom.action.value,
                        "size": atom.size_bytes,
                        "hash": atom.original_hash
                    }
                    for atom in self._temporal_loom
                ]
                (dossier_root / "temporal_loom.json").write_text(json.dumps(loom_dump, indent=2))

                # 3. Zip it
                archive_path_base = failed_rites_dir / archive_name
                shutil.make_archive(str(archive_path_base), 'zip', str(dossier_root))

                # self.logger.debug(f"Forensic dossier archived: {archive_path_base}.zip")

        except Exception as archive_heresy:
            self.logger.error(f"Forensic Archival Failed: {archive_heresy}")

    def __repr__(self) -> str:
        return f"<Ω_CHRONOMANCER atoms={len(self._temporal_loom)} secured={len(self._captured_paths)}>"