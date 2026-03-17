# Path: core/runtime/engine/execution/transaction.py
# -----------------------------------------------------------

import shutil
import os
import sys
import uuid
import time
import threading
import hashlib
import contextvars
import gc
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Final, Union, Set
from contextlib import contextmanager
from dataclasses import dataclass, field

from .....logger import Scribe
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....interfaces.base import Artifact

# =========================================================================================
# == [ASCENSION 1]: THE CONTEXTUAL SILVER-CORD                                           ==
# =========================================================================================
# This provides O(1) thread-safe access to the active Vessel across the entire Mind.
_ACTIVE_TX_VESSEL: contextvars.ContextVar[Optional['TransactionVessel']] = contextvars.ContextVar("_ACTIVE_TX_VESSEL",
                                                                                                  default=None)

Logger = Scribe("TransactionManager")


@dataclass
class FileOp:
    """
    =============================================================================
    == THE ATOM OF CAUSALITY (V-Ω-FILE-OP-VESSEL)                              ==
    =============================================================================
    """
    type: str  # 'create', 'modify', 'delete', 'edict', 'virtual'
    path: Path
    backup_path: Optional[Path] = None
    is_dir: bool = False
    timestamp: float = field(default_factory=time.perf_counter)
    merkle_hash: str = "0xVOID"
    edict_command: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class TransactionVessel:
    """
    =============================================================================
    == THE TRANSACTION VESSEL: THE BODY OF THE STRIKE (V-Ω-TOTALITY-VMAX)      ==
    =============================================================================
    LIF: ∞ | ROLE: TEMPORAL_STATE_CONTAINER | RANK: OMEGA
    """
    __slots__ = ('tx_id', 'operation_name', 'trace_id', 'ops', 'write_dossier', 'start_ts', '_lock', 'metadata')

    def __init__(self, tx_id: str, op_name: str, trace_id: str):
        self.tx_id = tx_id
        self.operation_name = op_name
        self.trace_id = trace_id
        self.ops: List[FileOp] = []
        self.write_dossier: Dict[Path, Artifact] = {}
        self.start_ts = time.perf_counter()
        self.metadata: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def record(self, artifact: Union[Artifact, Any]):
        """Records a completed artifact into the dossier."""
        with self._lock:
            p = getattr(artifact, 'path', Path("VOID"))
            # Ensure path is a Path object for the key
            key_path = Path(p) if not isinstance(p, Path) else p
            self.write_dossier[key_path] = artifact

    def __repr__(self) -> str:
        return f"<Ω_TX_VESSEL id={self.tx_id[:8]} ops={len(self.ops)} status=ACTIVE>"


class TransactionManager:
    """
    =================================================================================
    == THE CHRONOS VAULT: OMEGA POINT (V-Ω-TOTALITY-VMAX-ACID-SUTURED-HEALED)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ENTROPY_REVERSAL_GOVERNOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_CHRONOS_VMAX_SUTURE_2026_FINALIS_!#()@#()

    [THE MANIFESTO]
    The supreme final authority for Atomic File System Transactional Memory. This
    version has been radically re-aligned to annihilate the residual attribute
    void during Engine shutdown.
    =================================================================================
    """

    STAGING_DIR: Final[Path] = Path(".scaffold/chronos")

    # [ASCENSION 1]: ATTRIBUTE SOVEREIGNTY
    __slots__ = ('logger', '_active_transactions', '_lock', '_is_wasm', '_is_windows', '_staged_paths_bloom')

    def __init__(self, logger: Optional[Any] = None):
        """
        =============================================================================
        == THE RITE OF INCEPTION (V-Ω-TOTALITY-VMAX-HEALED)                        ==
        =============================================================================
        [THE MASTER CURE]: Explicitly initializes _active_transactions to prevent
        AttributeError in the engine.shutdown() pathway.
        """
        self.logger = logger or Logger

        # --- THE MASTER CURE ---
        # Annihilates the 'AttributeError' by ensuring the ledger exists at birth.
        self._active_transactions: Dict[str, TransactionVessel] = {}

        self._lock = threading.RLock()
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._is_windows = os.name == 'nt'

        # [ASCENSION 12]: Merkle-Bloom Sieve for fast lookups
        self._staged_paths_bloom: Set[str] = set()

    # =========================================================================
    # == [THE MASTER CURE]: THE HOLOGRAPHIC DISCOVERY RITES                  ==
    # =========================================================================

    def get_active_transaction(self) -> Optional[TransactionVessel]:
        """
        =============================================================================
        == THE RITE OF THE GNOSTIC EYE (V-Ω-TOTALITY-VMAX-HEALED)                  ==
        =============================================================================
        LIF: O(1) | Returns the living TransactionVessel from the thread context.
        """
        return _ACTIVE_TX_VESSEL.get()

    @contextmanager
    def atomic_rite(self, operation_name: str, trace_id: Optional[str] = None):
        """
        =============================================================================
        == THE RITE OF ATOMICITY (ACID COMPLIANCE)                                 ==
        =============================================================================
        LIF: ∞ | Wraps a block of intent in a transactional womb.
        """
        tx_uuid = uuid.uuid4().hex[:8].upper()
        tx_id = f"TX-{operation_name.upper()}-{tx_uuid}"
        active_trace = trace_id or f"tr-tx-{tx_uuid.lower()}"

        # 1. MATERIALIZE THE VESSEL
        vessel = TransactionVessel(tx_id, operation_name, active_trace)

        # 2. SUTURE TO CONTEXT
        token = _ACTIVE_TX_VESSEL.set(vessel)

        # 3. REGISTER IN GLOBAL LEDGER
        with self._lock:
            self._active_transactions[tx_id] = vessel

        self._radiate_hud_pulse(tx_id, "TX_BEGIN", "#3b82f6", active_trace)

        try:
            # Yield control to the Architect's Rite
            yield vessel

            # [STRIKE]: Transaction Pure. Consecrate the iron.
            self._commit(vessel)

        except Exception as catastrophic_paradox:
            # [REVERSAL]: Transaction Fractured. Reverse the flow of time.
            self.logger.critical(f"Lattice Fracture in '{tx_id}'. Reversing entropy.")
            self._rollback(vessel)
            raise catastrophic_paradox

        finally:
            # 4. EVAPORATE FROM MIND
            _ACTIVE_TX_VESSEL.reset(token)
            with self._lock:
                self._active_transactions.pop(tx_id, None)

            # [ASCENSION 34]: Metabolic Yielding
            gc.collect(0)

    def register_intent(self, vessel_id: Union[TransactionVessel, str], file_path: Path, intent: str = 'modify'):
        """
        =============================================================================
        == THE RITE OF REGISTRATION (V-Ω-CAUSAL-ANCHORING)                         ==
        =============================================================================
        """
        # Resolve Vessel Instance
        vessel = vessel_id if isinstance(vessel_id, TransactionVessel) else self._active_transactions.get(vessel_id)
        if not vessel:
            vessel = self.get_active_transaction()
        if not vessel: return

        with vessel._lock:
            # [ASCENSION 21]: Geometric Normalization
            abs_path = file_path.resolve()
            path_key = str(abs_path).replace('\\', '/')

            # [ASCENSION 20]: Idempotency Shield (Avoid double-backups)
            if any(op.path == abs_path for op in vessel.ops):
                return

            # [ASCENSION 1]: SANCTUM MATERIALIZATION
            if not self._is_wasm and not self.STAGING_DIR.exists():
                self._pierce_the_void()

            is_dir = abs_path.is_dir() if abs_path.exists() else False

            # --- CASE A: CREATION ---
            if intent == 'create' or not abs_path.exists():
                vessel.ops.append(FileOp(type='create', path=abs_path, is_dir=is_dir))

            # --- CASE B: MUTATION (MODIFY/DELETE) ---
            elif intent in ('modify', 'delete'):
                backup_name = f"{vessel.tx_id}_{uuid.uuid4().hex[:4]}_{abs_path.name}.bak"
                backup_path = self.STAGING_DIR / backup_name

                try:
                    # [ASCENSION 13]: Hydraulic Copy Pacing
                    if is_dir and not abs_path.is_symlink():
                        shutil.copytree(str(abs_path), str(backup_path), dirs_exist_ok=True)
                    else:
                        shutil.copy2(str(abs_path), str(backup_path))

                    # Calculate local Merkle fragment for the op
                    m_hash = self._calculate_merkle_sample(abs_path)

                    vessel.ops.append(FileOp(
                        type=intent, path=abs_path, backup_path=backup_path,
                        is_dir=is_dir, merkle_hash=m_hash
                    ))

                    # Update Bloom Sieve for O(1) lookups
                    with self._lock:
                        self._staged_paths_bloom.add(path_key)

                except Exception as e:
                    self.logger.warn(f"Chronos Vault: Backup of '{abs_path.name}' failed: {e}")

    def record_edict(self, command: str, undo_command: Optional[str] = None):
        """[ASCENSION 4]: KINETIC WILL REGISTRATION."""
        vessel = self.get_active_transaction()
        if not vessel: return

        with vessel._lock:
            vessel.ops.append(FileOp(
                type='edict',
                path=Path("KINETIC_WILL"),
                edict_command=command,
                backup_path=Path(undo_command) if undo_command else None
            ))

    def get_staging_path(self, logical_path: Path) -> Path:
        """[ASCENSION 2]: Returns the temporal backup path for a given file."""
        vessel = self.get_active_transaction()
        if not vessel: return logical_path

        abs_path = logical_path.resolve()
        path_key = str(abs_path).replace('\\', '/')

        # [ASCENSION 12]: Bloom Fast-Path
        if path_key not in self._staged_paths_bloom:
            return logical_path

        with vessel._lock:
            for op in vessel.ops:
                if op.path == abs_path and op.backup_path:
                    return op.backup_path

        return logical_path

    def is_file_in_staging(self, rel_path: Path) -> bool:
        """Used by the Sentinel to perceive future matter."""
        vessel = self.get_active_transaction()
        if not vessel: return False

        # Heuristic: verify against Bloom filter
        # (This assumes relative paths are normalized against project root)
        search_key = str(rel_path).lower().replace('\\', '/')
        for path in self._staged_paths_bloom:
            if path.lower().endswith(search_key):
                return True
        return False

    # =========================================================================
    # == STRATUM III: KINETIC TERMINALS (COMMIT / ROLLBACK)                  ==
    # =========================================================================

    def _commit(self, vessel: TransactionVessel):
        """[THE RITE OF CONSECRATION] Seals the new reality."""
        with vessel._lock:
            # [ASCENSION 3]: Generate Merkle Anchor
            hasher = hashlib.sha256()
            for op in sorted(vessel.ops, key=lambda x: str(x.path)):
                hasher.update(op.merkle_hash.encode())

            final_seal = hasher.hexdigest()[:16].upper()
            vessel.metadata["merkle_seal"] = f"0x{final_seal}"

            self.logger.success(f"Transaction '{vessel.tx_id}' consecrated. Seal: 0x{final_seal}")
            self._radiate_hud_pulse(vessel.tx_id, "TX_COMMIT", "#64ffda", vessel.trace_id)

            # Annihilate the shadows
            for op in vessel.ops:
                if op.backup_path and op.backup_path.exists():
                    try:
                        if op.backup_path.is_dir() and not op.backup_path.is_symlink():
                            shutil.rmtree(op.backup_path, ignore_errors=True)
                        else:
                            op.backup_path.unlink(missing_ok=True)
                    except:
                        pass

        self._sweep_orphans()

    def _rollback(self, vessel: TransactionVessel):
        """[THE RITE OF REVERSAL] Temporal Inversion."""
        with vessel._lock:
            # [ASCENSION 3]: Reverse order for topological safety
            for op in reversed(vessel.ops):
                try:
                    # 1. UNDO WILL (EDICTS)
                    if op.type == 'edict' and op.backup_path:
                        undo_cmd = str(op.backup_path)
                        self.logger.warn(f"   <- [REVERSING WILL]: {undo_cmd}")
                        os.system(undo_cmd)

                    # 2. UNDO MATTER GENESIS (CREATION)
                    elif op.type == 'create':
                        if op.path.exists():
                            if op.path.is_dir() and not op.path.is_symlink():
                                shutil.rmtree(op.path, ignore_errors=True)
                            else:
                                op.path.unlink(missing_ok=True)

                    # 3. UNDO TRANSMUTATION (MODIFY/DELETE)
                    elif op.type in ('modify', 'delete') and op.backup_path:
                        if op.backup_path.exists():
                            op.path.parent.mkdir(parents=True, exist_ok=True)
                            if op.is_dir and not op.backup_path.is_symlink():
                                if op.path.exists(): shutil.rmtree(op.path, ignore_errors=True)
                                shutil.copytree(op.backup_path, op.path)
                            else:
                                shutil.copy2(op.backup_path, op.path)

                except Exception as e:
                    self.logger.error(f"   -> [ROLLBACK_FRACTURE] '{op.path.name}': {e}")

        self._radiate_hud_pulse(vessel.tx_id, "TX_ROLLBACK", "#ef4444", vessel.trace_id)
        # Force a clean commit state after rollback
        self._commit(vessel)

    # =========================================================================
    # == INTERNAL ORGANS (PHYSICS & TELEMETRY)                               ==
    # =========================================================================

    def _pierce_the_void(self):
        """[ASCENSION 1]: Vault materialization."""
        try:
            self.STAGING_DIR.mkdir(parents=True, exist_ok=True)
            if self._is_windows:
                # Set hidden attribute on Windows
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(str(self.STAGING_DIR), 2)
        except:
            pass

    def _calculate_merkle_sample(self, path: Path) -> str:
        """Quick Merkle fragment for state comparison."""
        try:
            if path.is_dir(): return "0xDIR"
            with open(path, 'rb') as f:
                return hashlib.md5(f.read(4096)).hexdigest()
        except:
            return "0xVOID"

    def _sweep_orphans(self):
        """[ASCENSION 7]: Lazarus Reaper."""
        if self._is_wasm or not self.STAGING_DIR.exists(): return
        now = time.time()
        try:
            for item in self.STAGING_DIR.iterdir():
                if (now - item.stat().st_mtime) > 86400:  # 24hr TTL
                    if item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                    else:
                        item.unlink(missing_ok=True)
            if not any(self.STAGING_DIR.iterdir()): self.STAGING_DIR.rmdir()
        except:
            pass

    def _radiate_hud_pulse(self, tx_id: str, type_label: str, color: str, trace: str):
        """[ASCENSION 21]: OCULAR HUD MULTICAST."""
        try:
            import sys
            main_mod = sys.modules.get('__main__')
            engine = getattr(main_mod, 'engine', None)
            if engine and hasattr(engine, 'akashic') and engine.akashic:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "TRANSACTION_EVENT",
                        "label": f"{type_label}: {tx_id[:12]}",
                        "color": color,
                        "trace": trace
                    }
                })
        except:
            pass

    def __repr__(self) -> str:
        return f"<Ω_CHRONOS_VAULT active_tx={len(self._active_transactions)} status=RESONANT>"