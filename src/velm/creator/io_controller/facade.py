# Path: src/velm/creator/io_controller/facade.py
# ----------------------------------------------
# LIF: INFINITY // ROLE: KINETIC_IO_CONDUCTOR // RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONDUCTOR_V40000_DRIVER_NATIVE_FINALIS
# ----------------------------------------------

from __future__ import annotations

import os
import time
import hashlib
from pathlib import Path
from typing import Union, Dict, Any, TYPE_CHECKING, Tuple, Optional, List

# --- THE DIVINE UPLINKS ---
from .path_alchemist import PathAlchemist
from .security import SecurityWards
from .transaction_router import TransactionRouter
from ..writer.normalizer import ContentNormalizer
from ..writer.security import SecretSentinel
from ..writer.differential import DifferentialEngine
from ...contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe
from ...core.runtime.vessels import GnosticSovereignDict

# === THE ACHRONAL LEDGER IMPORTS ===
from ...creator.io_controller.trash import TrashManager
from ...core.state import ActiveLedger
from ...core.state.contracts import LedgerEntry, LedgerOperation, InverseOp

if TYPE_CHECKING:
    from ..registers import QuantumRegisters
    from ...core.sanctum.base import SanctumInterface

Logger = Scribe("IOConductor")


class IOConductor:
    """
    =================================================================================
    == THE GOD-ENGINE OF CAUSALITY (V-Ω-TOTALITY-V40000-DRIVER-NATIVE)             ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_IO_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN

    The supreme authority for physical and virtual manifestation. It transmutes
    Gnostic Intent into Substance by commanding the Multiversal Driver Lattice.
    """

    def __init__(self, registers: "QuantumRegisters"):
        """[THE RITE OF INCEPTION]"""
        self.regs = registers
        self.project_root = registers.project_root or Path.cwd()

        # --- THE FORGING OF THE PANTHEON ---
        self.alchemist = PathAlchemist(registers.gnosis)
        self.security = SecurityWards()
        self.router = TransactionRouter(registers)

        # Substrate-Agnostic Helpers
        self.normalizer = ContentNormalizer(is_windows=(os.name == 'nt'))
        self.differ = DifferentialEngine()
        self.trash = TrashManager(self.project_root)

        # Telemetry
        self._start_time = time.monotonic()

        Logger.verbose(
            f"IOConductor resonant. Substrate: {'ETHER' if os.environ.get('SCAFFOLD_ENV') == 'WASM' else 'IRON'}")

    # =========================================================================
    # == THE ELEMENTAL RITES (CREATION & DESTRUCTION)                        ==
    # =========================================================================

    def write(self, logical_path: Union[str, Path], content: Union[str, bytes],
              metadata: Dict[str, Any]) -> GnosticWriteResult:
        """
        =============================================================================
        == THE RITE OF UNIVERSAL INSCRIPTION (WRITE)                               ==
        =============================================================================
        Transmutes intent into matter across any Driver (Local, S3, SSH, Memory).
        """
        start_ns = time.perf_counter_ns()
        path_str = str(logical_path)

        try:
            # --- MOVEMENT I: ALCHEMICAL PURIFICATION ---
            # 1. Resolve Variables
            transmuted_path = self.alchemist.transmute(path_str)

            # 2. Security Adjudication
            # URIs bypass local jail checks but are warded by the Driver.
            if "://" not in transmuted_path:
                self.security.adjudicate_path(transmuted_path)

            # 3. Mass & Entropy Check
            self.security.verify_metabolic_mass(content)

            # --- MOVEMENT II: SPATIOTEMPORAL RESOLUTION ---
            # [ASCENSION 1]: Triangulate the Driver and the physical coordinate.
            driver, physical_locus = self.router.resolve(transmuted_path)

            # --- MOVEMENT III: THE FORENSIC SNAPSHOT ---
            # [ASCENSION 3]: Capture the Ancestral Soul for Undo-capability.
            snapshot: Optional[bytes] = None
            if driver.exists(physical_locus) and driver.is_file(physical_locus):
                try:
                    snapshot = driver.read_bytes(physical_locus)
                except Exception:
                    pass  # Non-readable matter cannot be snapshotted

            # --- MOVEMENT IV: THE LEDGER VOW ---
            # Formulate the Antidote before the Strike.
            inverse_op = (
                InverseOp(op=LedgerOperation.WRITE_FILE, params={"path": transmuted_path, "content_is_snapshot": True})
                if snapshot is not None else
                InverseOp(op=LedgerOperation.DELETE_FILE, params={"path": transmuted_path})
            )

            entry = LedgerEntry(
                actor="IOConductor",
                operation=LedgerOperation.WRITE_FILE,
                forward_state={"path": transmuted_path, "driver": driver.kind.name, "metadata": metadata},
                inverse_action=inverse_op,
                snapshot_content=snapshot
            )

            # Etch the intent into the chronicle
            ActiveLedger.record(entry)

            # --- MOVEMENT V: THE KINETIC STRIKE ---
            if self.regs.dry_run:
                return GnosticWriteResult.forge_success(
                    message=f"Prophecy resonant for {transmuted_path}",
                    path=Path(transmuted_path),
                    action_taken=InscriptionAction.DRY_RUN_CREATED,
                    bytes_written=len(content) if isinstance(content, bytes) else len(str(content))
                )

            # 1. Content Normalization
            if isinstance(content, str):
                # Apply Secret Redaction
                purified_text = SecretSentinel.scan_and_warn(content, Path(transmuted_path).name)
                # Apply EOL/Tab Normalization
                final_matter = self.normalizer.sanctify(Path(transmuted_path), purified_text).encode('utf-8')
            else:
                final_matter = content

            # 2. Idempotency Check
            current_hash = hashlib.sha256(final_matter).hexdigest()
            if snapshot and hashlib.sha256(snapshot).hexdigest() == current_hash:
                if not self.regs.force:
                    return GnosticWriteResult.forge_success(
                        message="Reality is already congruent.",
                        path=Path(transmuted_path),
                        action_taken=InscriptionAction.ALREADY_MANIFEST
                    )

            # 3. [STRIKE]: Command the Driver
            driver.write_bytes(physical_locus, final_matter)

            # 4. Consecrate Permissions
            if metadata.get("permissions"):
                mode = int(str(metadata["permissions"]), 8) if str(metadata["permissions"]).isdigit() else 0o644
                driver.chmod(physical_locus, mode)

            # --- MOVEMENT VI: REVELATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            action = InscriptionAction.TRANSFIGURED if snapshot else InscriptionAction.CREATED

            return GnosticWriteResult(
                success=True,
                path=Path(transmuted_path),
                action_taken=action,
                bytes_written=len(final_matter),
                gnostic_fingerprint=current_hash,
                duration_ms=duration_ms,
                metadata={"driver": driver.kind.name, "uri": driver.uri_root}
            )

        except Exception as fracture:
            Logger.error(f"Inscription fractured for '{path_str}': {fracture}")
            return GnosticWriteResult(
                success=False,
                path=Path(path_str),
                action_taken=InscriptionAction.FAILED_IO,
                error=str(fracture)
            )

    def mkdir(self, logical_path: Union[str, Path]) -> bool:
        """The Grand Rite of Sanctum Forging."""
        transmuted_path = self.alchemist.transmute(str(logical_path))
        driver, physical_locus = self.router.resolve(transmuted_path)

        if self.regs.dry_run:
            return True

        try:
            entry = LedgerEntry(
                actor="IOConductor",
                operation=LedgerOperation.MKDIR,
                forward_state={"path": transmuted_path, "driver": driver.kind.name},
                inverse_action=InverseOp(op=LedgerOperation.RMDIR, params={"path": transmuted_path, "recursive": True})
            )
            ActiveLedger.record(entry)

            driver.mkdir(physical_locus, parents=True, exist_ok=True)
            return True
        except Exception as e:
            Logger.error(f"Sanctum forge failed at '{transmuted_path}': {e}")
            if not self.regs.force: raise e
            return False

    def delete(self, logical_path: Union[str, Path], recursive: bool = False):
        """The Grand Rite of Annihilation."""
        transmuted_path = self.alchemist.transmute(str(logical_path))
        driver, physical_locus = self.router.resolve(transmuted_path)

        if not driver.exists(physical_locus):
            return

        if self.regs.dry_run:
            return

        try:
            # Capture snapshot for rollback if it's a file
            snapshot = None
            if not recursive and driver.is_file(physical_locus):
                snapshot = driver.read_bytes(physical_locus)

            entry = LedgerEntry(
                actor="IOConductor",
                operation=LedgerOperation.DELETE_FILE if not recursive else LedgerOperation.RMDIR,
                forward_state={"path": transmuted_path, "recursive": recursive},
                inverse_action=InverseOp(op=LedgerOperation.WRITE_FILE, params={"path": transmuted_path,
                                                                                "content_is_snapshot": True}) if snapshot else None,
                snapshot_content=snapshot
            )
            ActiveLedger.record(entry)

            if recursive:
                driver.rmdir(physical_locus, recursive=True)
            else:
                driver.unlink(physical_locus)

        except Exception as e:
            Logger.error(f"Annihilation failed for '{transmuted_path}': {e}")
            if not self.regs.force: raise e

    # =========================================================================
    # == THE KINETIC RITES (TRANSLOCATION & REPLICATION)                     ==
    # =========================================================================

    def move(self, src: Union[str, Path], dest: Union[str, Path]) -> bool:
        """
        =============================================================================
        == THE RITE OF TRANSLOCATION (MOVE)                                        ==
        =============================================================================
        [ASCENSION 2]: Now supports cross-reality moves (e.g. Local -> S3).
        """
        t_src = self.alchemist.transmute(str(src))
        t_dest = self.alchemist.transmute(str(dest))

        d_src, p_src = self.router.resolve(t_src)
        d_dest, p_dest = self.router.resolve(t_dest)

        if self.regs.dry_run:
            return True

        # --- THE CROSS-DIMENSIONAL BRIDGE ---
        if d_src.kind != d_dest.kind:
            Logger.info(f"Cross-Reality Translocation: {d_src.kind.name} -> {d_dest.kind.name}")
            try:
                # We use the Base Interface's projection faculty
                d_src.project_to(d_dest, p_src, p_dest)
                d_src.rmdir(p_src, recursive=True) if d_src.is_dir(p_src) else d_src.unlink(p_src)
                return True
            except Exception as e:
                Logger.error(f"Cross-Reality Translocation fractured: {e}")
                return False

        # --- THE ATOMIC INTRA-DRIVER MOVE ---
        try:
            ActiveLedger.record(LedgerEntry(
                actor="IOConductor",
                operation=LedgerOperation.RENAME,
                forward_state={"src": t_src, "dest": t_dest},
                inverse_action=InverseOp(op=LedgerOperation.RENAME, params={"src": t_dest, "dest": t_src})
            ))
            d_src.rename(p_src, p_dest)
            return True
        except Exception as e:
            Logger.error(f"Translocation failed: {e}")
            return False

    def copy(self, src: Union[str, Path], dest: Union[str, Path]) -> bool:
        """The Rite of Replication."""
        t_src = self.alchemist.transmute(str(src))
        t_dest = self.alchemist.transmute(str(dest))

        d_src, p_src = self.router.resolve(t_src)
        d_dest, p_dest = self.router.resolve(t_dest)

        if self.regs.dry_run: return True

        try:
            if d_src.kind != d_dest.kind:
                d_src.project_to(d_dest, p_src, p_dest)
            else:
                d_src.copy(p_src, p_dest)
            return True
        except Exception as e:
            Logger.error(f"Replication failed: {e}")
            return False

    # =========================================================================
    # == THE RITES OF RECALL (READING)                                       ==
    # =========================================================================

    def read_text(self, logical_path: Union[str, Path]) -> str:
        """Perceives text across any substrate."""
        transmuted_path = self.alchemist.transmute(str(logical_path))
        driver, physical_locus = self.router.resolve(transmuted_path)
        return driver.read_text(physical_locus)

    def read_json(self, logical_path: Union[str, Path]) -> Any:
        """Thaws a JSON soul from any substrate."""
        transmuted_path = self.alchemist.transmute(str(logical_path))
        driver, physical_locus = self.router.resolve(transmuted_path)
        # Leverage the Driver's higher-order faculty
        return driver.read_json(physical_locus)

    def __repr__(self) -> str:
        return f"<Ω_IO_CONDUCTOR status=RESONANT trace={getattr(self.regs, 'trace_id', 'void')[:8]}>"
