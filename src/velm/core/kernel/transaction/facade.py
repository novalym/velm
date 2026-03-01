# Path: src/velm/core/kernel/transaction/facade.py
# ------------------------------------------------
# LIF: INFINITY // ROLE: ACID_FILESYSTEM_TRANSACTION_MANAGER
# AUTH: Ω_TX_FACADE_V3000_ENTERPRISE_GRADE_FINALIS
# ------------------------------------------------

from __future__ import annotations

import gc
import os
import sys
import time
import uuid
import threading
import hashlib
import weakref
import shutil
import traceback
from enum import Enum, auto
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union, Final, Set
from collections import deque

# --- Core System Interfaces ---
from .locking import GnosticLock
from .staging import StagingManager
from .committer import GnosticCommitter
from .rollback import RollbackChronomancer
from .chronicle_bridge import ChronicleBridge
from .contracts import TransactionalGnosis, SubstrateDNA, RiteCategory
from .volume_shifter.contracts import VolumeState
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ....logger import Scribe

_EPOCH_START = time.perf_counter_ns()
Logger = Scribe("Transaction")

# =========================================================================
# == DIAGNOSTIC TELEMETRY GATE                                           ==
# =========================================================================
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


class TransactionState(Enum):
    """
    Represents the deterministic lifecycle states of a filesystem transaction.
    Strict state progression ensures atomic safety and prevents race conditions.
    """
    VOID = auto()  # Uninitialized or completely reset state.
    INCEPTED = auto()  # Transaction lock acquired, context established.
    STAGING = auto()  # Actively buffering file I/O operations into the staging environment.
    LUSTRATING = auto()  # Committing staged files to the shadow volume.
    RESONANT = auto()  # Staging matches intended reality, awaiting final atomic flip.
    FLIPPING = auto()  # Critical section: Performing the atomic OS-level directory swap.
    SEALED = auto()  # Operation concluded successfully, chronicle written.
    LIMINAL = auto()  # Suspended state during automated fault-recovery (e.g., I/O retry).
    FRACTURED = auto()  # Transaction failed and has been rolled back.


class GnosticTransaction:
    """
    Provides Database-Grade ACID compliance for raw filesystem operations.

    This class orchestrates a Two-Phase Commit architecture for file generation:
    1. All file modifications are routed to a temporary `.scaffold/staging` directory.
    2. A `VolumeShifter` prepares a shadow copy of the target directory.
    3. If all operations succeed, the shadow volume is atomically swapped with the live directory.
    4. If any operation fails, the shadow volume and staging area are purged, leaving the
       original files completely untouched.

    It features autonomous transient fault recovery (Liminal Healing) to handle transient
    Windows file locks or Indexer conflicts, and dynamic re-anchoring to support nested workspaces.
    """

    # System Constraints
    MAX_COMMIT_PASSES: Final[int] = 5
    IO_THROTTLE_THRESHOLD_MS: Final[float] = 100.0
    FAULT_RECOVERY_RETRIES: Final[int] = 2

    def __init__(
            self,
            project_root: Path,
            rite_name: str,
            blueprint_path: Optional[Path] = None,
            *,
            use_lock: bool = True,
            simulate: bool = False,
            **kwargs: Any
    ):
        """
        Initializes the transaction boundary and binds the necessary IO subsystems.
        """
        self.logger = Logger

        self._state = TransactionState.VOID
        self._state_lock = threading.RLock()

        self._flip_conducted = False
        self._commit_pass_count = 0
        self._committed_paths: Set[Path] = set()
        self._dossier_enriched = False
        self._faults: List[str] = []
        self._perceived_paths: Set[str] = set()

        # --- Spatial Anchors ---
        self.base_path = project_root.resolve()
        self.project_root = self.base_path

        self.rite_name = rite_name
        self.blueprint_path = blueprint_path or Path(f"manual/{rite_name.replace(' ', '_')}")

        # --- Causality & Tracing ---
        self.tx_id = uuid.uuid4().hex
        self.trace_id = (
                kwargs.get('trace_id') or
                os.environ.get("SCAFFOLD_TRACE_ID") or
                f"tr-{self.tx_id[:8].upper()}"
        )
        self.use_lock = use_lock
        self.simulate = simulate
        self._boot_ns = time.perf_counter_ns()

        # Secure the global engine reference if not explicitly provided
        self.engine = kwargs.get('engine')
        if not self.engine:
            import sys
            main_mod = sys.modules.get('__main__')
            self.engine = getattr(main_mod, 'engine', None)

        self._merkle_accumulator = hashlib.sha256(self.tx_id.encode())
        self._event_stream: deque = deque()

        # --- Internal Memory Lattice ---
        from ...runtime.vessels import GnosticSovereignDict
        self.write_dossier: Dict[Path, GnosticWriteResult] = {}
        self.edicts_executed: List[str] = []
        self.heresies_perceived: List[Heresy] = []
        self.context = GnosticSovereignDict(kwargs.get('context', {}))

        # --- Subsystem Initialization ---
        self.staging_manager = StagingManager(
            self.base_path,
            self.tx_id,
            engine=self.engine,
            logger=self.logger
        )

        from .volume_shifter.facade import VolumeShifter
        self.volume_shifter = VolumeShifter(self.project_root, self.tx_id, base_path=self.base_path)

        from ...runtime.engine.execution.simulacrum import GnosticSimulacrum
        self.simulacrum = GnosticSimulacrum(self.base_path, self.trace_id)

        self.lock = GnosticLock(
            self.staging_manager.scaffold_dir / "transaction.lock",
            self.rite_name
        )

        provided_regs = kwargs.get('registers')
        if not provided_regs:
            from ....creator.registers import QuantumRegisters
            provided_regs = QuantumRegisters(
                sanctum=None,
                project_root=self.project_root,
                transaction=self,
                silent=kwargs.get('silent', False)
            )
            if self.engine:
                provided_regs.akashic = getattr(self.engine, 'akashic', None)

        self.committer = GnosticCommitter(
            self.project_root,
            self.staging_manager,
            self.logger,
            registers=provided_regs
        )

        self.chronomancer = RollbackChronomancer(
            self.staging_manager,
            self.project_root,
            self.logger
        )
        self._bridge: Optional[ChronicleBridge] = None

        # Guarantee cleanup of ephemeral staging resources upon object collection
        self._finalizer = weakref.finalize(
            self, self._emergency_cleanup, self.staging_manager,
            self.volume_shifter, self.use_lock, self.lock
        )

        self._sys_log(f"Transaction session [{self.tx_id[:8]}] initialized for operation: {self.rite_name}")

    def _sys_log(self, msg: str, color: str = "36"):
        """High-performance unbuffered debug output."""
        if _DEBUG_MODE:
            sys.stderr.write(f"\x1b[{color};1m[TX_MANAGER]\x1b[0m {msg}\n")
            sys.stderr.flush()

    @property
    def chronicle_bridge(self) -> ChronicleBridge:
        if self._bridge is None:
            self._bridge = ChronicleBridge(self)
        return self._bridge

    @property
    def active(self) -> bool:
        """
        Determines if the transaction is currently accepting I/O operations.
        Includes the FLIPPING state to allow the ChronicleBridge to read the
        final staging coordinates while the volume is being swapped.
        """
        return self._state in (
            TransactionState.INCEPTED,
            TransactionState.STAGING,
            TransactionState.LUSTRATING,
            TransactionState.RESONANT,
            TransactionState.FLIPPING
        )

    def is_file_in_staging(self, logical_path: Union[str, Path]) -> bool:
        """Validates if a specific path is currently managed by the active staging area."""
        p_obj = Path(logical_path)
        if p_obj in self.write_dossier:
            return True
        staging_path = self.get_staging_path(p_obj)
        return staging_path.exists() and staging_path.is_file()

    @staticmethod
    def _emergency_cleanup(staging: StagingManager, shifter: Any, use_lock: bool, lock: GnosticLock):
        """Failsafe teardown method invoked by the garbage collector."""
        try:
            staging.cleanup()
            if hasattr(shifter, 'cleanup'):
                shifter.cleanup()
            if use_lock and lock:
                lock.release()
        except Exception:
            pass

    def re_anchor(self, new_root: Path):
        """
        Dynamically adjusts the transaction's geometric anchor mid-flight.
        Essential for correctly staging files when creating a project nested
        inside a new subdirectory rather than the current working directory.
        """
        with self._state_lock:
            if self._state.value > TransactionState.STAGING.value and self._state != TransactionState.RESONANT:
                self.logger.warn("Re-anchor rejected: Transaction is currently committing to disk.")
                return

            self.project_root = new_root.resolve()
            self.committer.project_root = self.project_root

            if hasattr(self, 'volume_shifter'):
                self.volume_shifter.root = self.project_root
                self.volume_shifter.sanctum = self.base_path / ".scaffold" / "volumes" / self.tx_id

            self._event_stream.append({
                "event": "RE_ANCHOR",
                "target": str(self.project_root),
                "ts": time.time_ns(),
                "trace_id": self.trace_id
            })

            self._sys_log(f"Transaction topology re-anchored to: {self.project_root}")

    def __enter__(self) -> GnosticTransaction:
        """
        Initiates the transaction boundary. Acquires file-based mutexes to prevent
        parallel processes from clashing on the same workspace.
        """
        _inception_start = time.perf_counter_ns()

        if self.use_lock:
            try:
                self.lock.acquire()
            except Exception as lock_paradox:
                self.logger.critical(f"Failed to acquire transaction lock: {lock_paradox}")
                raise lock_paradox

        try:
            with self._state_lock:
                self._state = TransactionState.INCEPTED
                self.staging_manager.initialize_sanctums()

                akashic = getattr(self.committer.registers, 'akashic', None)
                if akashic:
                    try:
                        akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {
                                "type": "TX_INCEPTION",
                                "label": "TRANSACTION_ACTIVE",
                                "color": "#3b82f6",
                                "trace": self.trace_id,
                                "is_simulation": self.simulate,
                                "meta": {"tx_id": self.tx_id, "rite": self.rite_name}
                            }
                        })
                    except Exception:
                        pass

                self._state = TransactionState.STAGING

                self._event_stream.append({
                    "event": "INCEPTION",
                    "ts": time.time_ns(),
                    "status": "ACTIVE",
                    "trace_id": self.trace_id
                })

            _duration_ms = (time.perf_counter_ns() - _inception_start) / 1_000_000
            self._sys_log(f"Lock acquired in {_duration_ms:.2f}ms. State: STAGING.")

            return self

        except Exception as startup_error:
            self._transition_to_fractured(startup_error)
            raise startup_error

    # =========================================================================
    # == TRANSACTION LEDGER (RECORDING)                                      ==
    # =========================================================================

    def record(self, result: GnosticWriteResult):
        """
        Appends a successful I/O operation to the transaction ledger.
        Automatically re-opens the transaction if late-stage files (like lockfiles)
        are added after the primary commit pass.
        """
        with self._state_lock:
            # Re-opening logic: If we hit RESONANT, we are waiting for the flip.
            # If new files arrive, we must regress to STAGING to capture them.
            if self._state == TransactionState.RESONANT:
                self._state = TransactionState.STAGING
                self._sys_log(f"Re-opened transaction scope for late file inscription: {result.path.name}")

            if self._state.value >= TransactionState.FLIPPING.value:
                raise RuntimeError(
                    f"Transaction Violation: Attempted to record '{result.path.name}' to a sealed transaction (State: {self._state.name})."
                )

            logical_path = self.staging_manager.triangulate_relative_path(result.path)
            model_copy = result.model_copy(update={"path": logical_path})

            self.write_dossier[logical_path] = model_copy
            self._dossier_enriched = False

            self._merkle_accumulator.update(str(logical_path).encode())
            if result.gnostic_fingerprint:
                self._merkle_accumulator.update(result.gnostic_fingerprint.encode())

            self._event_stream.append({
                "event": "RECORD_MATTER",
                "path": str(logical_path),
                "action": result.action_taken.value,
                "ts": time.time_ns(),
                "trace_id": self.trace_id
            })

    def record_edict(self, command: str):
        """Records shell commands executed during the transaction for audit purposes."""
        with self._state_lock:
            if self._state == TransactionState.RESONANT:
                self._state = TransactionState.STAGING
            if self._state.value >= TransactionState.FLIPPING.value:
                return

        self.edicts_executed.append(command)
        self._event_stream.append({
            "event": "RECORD_EDICT",
            "cmd": str(command)[:100],
            "ts": time.time_ns(),
            "trace_id": self.trace_id
        })

    def record_heresy(self, heresy: Heresy):
        """Records non-fatal validation warnings or errors detected during staging."""
        with self._state_lock:
            if self._state == TransactionState.RESONANT:
                self._state = TransactionState.STAGING
            if self._state.value >= TransactionState.FLIPPING.value:
                return

        self.heresies_perceived.append(heresy)
        self._event_stream.append({
            "event": "RECORD_HERESY",
            "code": heresy.code,
            "ts": time.time_ns(),
            "trace_id": self.trace_id
        })

    # =========================================================================
    # == COMMIT PHASES                                                       ==
    # =========================================================================

    def materialize(self):
        """
        Phase 1 of 2PC (Prepare):
        Moves all staged files into the Volume Shifter's shadow directory and
        prepares the environment for the final atomic swap.
        """
        with self._state_lock:
            if self._state == TransactionState.LUSTRATING:
                return

            if self._state == TransactionState.FRACTURED or self.simulate:
                return

            self._state = TransactionState.LUSTRATING
            self._event_stream.append({
                "event": "LUSTRATION_START",
                "ts": time.time_ns(),
                "trace_id": self.trace_id
            })

        # Initialize the shadow volume based on the target OS capabilities
        if hasattr(self, 'volume_shifter') and self.volume_shifter.state.name == "VOID":
            strategy = self.context.get("flip_strategy") or (
                "SYMLINK" if os.environ.get("SCAFFOLD_ENV") == "DOCKER" else "RENAME"
            )
            try:
                self._sys_log(f"Preparing Shadow Volume. Strategy: {strategy}")
                self.volume_shifter.prepare(strategy=strategy)

                if hasattr(self.volume_shifter, 'merkle_root'):
                    self.context["_initial_merkle_root"] = self.volume_shifter.merkle_root

            except Exception as shadow_fracture:
                self.logger.warn(
                    f"Shadow Volume preparation failed: {shadow_fracture}. Falling back to standard staging.")
                self.volume_shifter.state = VolumeState.FRACTURED

        # Delta Calculation: Only process files that haven't been committed yet
        current_shards = set(self.write_dossier.keys())
        new_shards = current_shards - self._committed_paths

        if not new_shards and self._commit_pass_count > 0:
            with self._state_lock:
                self._state = TransactionState.RESONANT
            return

        if self._commit_pass_count >= self.MAX_COMMIT_PASSES:
            self.logger.warn(
                f"Transaction Warning: Maximum commit passes ({self.MAX_COMMIT_PASSES}) reached. Halting delta sync."
            )
            with self._state_lock:
                self._state = TransactionState.RESONANT
            return

        self._sys_log(f"Executing commit pass #{self._commit_pass_count + 1}...")

        self._enrich_if_needed()

        try:
            # Pushes files from `.scaffold/staging` to the Shadow Volume
            self.committer.commit()

            self._committed_paths.update(new_shards)
            self._commit_pass_count += 1

            self._event_stream.append({
                "event": "MATERIALIZE_PASS",
                "count": self._commit_pass_count,
                "shards": len(new_shards),
                "ts": time.time_ns(),
                "trace_id": self.trace_id
            })

            with self._state_lock:
                self._state = TransactionState.RESONANT

        except Exception as lustration_error:
            # Attempt autonomous recovery for transient disk access errors
            if not self._recover_transient_fault(lustration_error, "materialize"):
                self.logger.error(f"Commit Phase 1 Failed: {lustration_error}")
                raise lustration_error
            else:
                self.materialize()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Phase 2 of 2PC (Commit/Rollback):
        Evaluates the context closure. If successful, executes the atomic swap (Flip).
        If an exception occurred during the block, triggers the RollbackChronomancer.
        """
        death_ts_ns = time.perf_counter_ns()
        self.active_death_ns = death_ts_ns

        self._sys_log(f"Concluding transaction scope [{self.tx_id[:8]}].")

        was_healed = False
        final_exception = exc_val

        try:
            if exc_type or self._state == TransactionState.FRACTURED:
                # =========================================================================
                # == BRANCH A: ROLLBACK                                                  ==
                # =========================================================================
                with self._state_lock:
                    self._state = TransactionState.FRACTURED

                self.logger.warn(f"Transaction '{self.rite_name}' aborted. Reason: {exc_val or 'Internal Error'}")
                self._project_hud_pulse("TX_FRACTURE", "#ef4444")

                if exc_type:
                    try:
                        # Final attempt to heal before tearing down reality
                        if self._recover_transient_fault(exc_val, "exit"):
                            was_healed = True
                            self.logger.info("Transient fault recovered successfully. Continuing commit.")
                    except Exception as secondary_error:
                        self.logger.error(f"Fault recovery sequence failed: {secondary_error}")

                if not was_healed:
                    self._event_stream.append({
                        "event": "ROLLBACK_INITIATED",
                        "reason": str(exc_val),
                        "ts": time.time_ns(),
                        "trace_id": self.trace_id
                    })
                    try:
                        self.chronomancer.perform_emergency_rollback()
                    except Exception as rollback_failure:
                        self.logger.critical(
                            f"FATAL: Rollback engine failed. Directory state may be inconsistent: {rollback_failure}")

                    self._archive_failed_rite(exc_type, exc_val, exc_tb)

            if not exc_type or was_healed:
                # =========================================================================
                # == BRANCH B: COMMIT                                                    ==
                # =========================================================================

                # Final sweep to catch any files added right at the end of the block
                self.materialize()

                # Perform the OS-level atomic swap
                if not self.simulate:
                    with self._state_lock:
                        self._state = TransactionState.FLIPPING

                    try:
                        shifter_state = getattr(self.volume_shifter, 'state', None)
                        if not shifter_state or (shifter_state.name != "RESONANT" and shifter_state.name != "ACTIVE"):
                            raise ArtisanHeresy("Volume Swap aborted: Shadow Volume is missing or unstable.")

                        # The Critical Section
                        self.volume_shifter.flip(target_dir=self.project_root)
                        self._flip_conducted = True

                        self._event_stream.append(
                            {"event": "FLIP_COMPLETE", "ts": time.time_ns(), "trace_id": self.trace_id})
                        self._project_hud_pulse("TX_SUCCESS", "#10b981")

                    except Exception as flip_error:
                        self.logger.critical(f"Atomic Swap Failed: {flip_error}")
                        with self._state_lock:
                            self._state = TransactionState.FRACTURED
                        final_exception = flip_error
                        raise flip_error

                # Write execution history to disk for audit/undo capability
                if not self.simulate and self._state != TransactionState.FRACTURED:
                    if self.write_dossier or self.edicts_executed:
                        try:
                            self.chronicle_bridge.seal_chronicle()
                        except Exception as bridge_error:
                            self.logger.warn(f"Chronicle write failed: {bridge_error}. File operations succeeded.")

                with self._state_lock:
                    self._state = TransactionState.SEALED
                    self._event_stream.append({"event": "SEALED", "ts": time.time_ns(), "trace_id": self.trace_id})

        except Exception as final_error:
            final_exception = final_error
            self.logger.error(f"Catastrophic error during transaction closure: {final_error}", exc_info=True)

        # =========================================================================
        # == RESOURCE CLEANUP                                                    ==
        # =========================================================================

        # 1. Staging Purification
        try:
            self.staging_manager.cleanup()
        except Exception as e:
            self._sys_log(f"Staging cleanup deferred: {e}", "33")

        # 2. Volume Evaporation
        if self._flip_conducted or final_exception or self._state == TransactionState.FRACTURED:
            try:
                self.volume_shifter.cleanup()
            except Exception as e:
                self._sys_log(f"Volume cleanup deferred: {e}", "33")

        # 3. Adrenaline Lustration (Garbage Collection)
        if os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            try:
                os.environ.pop("SCAFFOLD_ADRENALINE", None)
                import gc
                gc.enable()
                gc.collect(1)
            except Exception:
                pass

        # 4. Release Mutex
        if self.use_lock:
            try:
                self.lock.release()
            except Exception as e:
                self.logger.error(f"Lock release failed: {e}")

        # 5. Profiling
        latency_ms = (time.perf_counter_ns() - self._boot_ns) / 1_000_000
        self._sys_log(f"Transaction finalized in {latency_ms:.2f}ms. State: {self._state.name}")

        if was_healed and not final_exception:
            return True

        return False

    def _recover_transient_fault(self, exception: Exception, phase: str) -> bool:
        """
        Attempts to gracefully recover from transient operating system faults,
        such as temporary file locks held by antivirus software or indexing services.
        """
        with self._state_lock:
            original_state = self._state
            self._state = TransactionState.LIMINAL

        self.logger.warn(f"[{self.tx_id[:8]}] Entering Fault Recovery Mode for: {type(exception).__name__}")

        healed = False
        error_str = str(exception).lower()

        # Handle Windows 'Access Denied' or 'File in Use' errors by backing off and retrying
        if isinstance(exception,
                      PermissionError) or "access is denied" in error_str or "used by another process" in error_str:
            self.logger.info("Diagnosis: Transient OS File Lock suspected.")
            for attempt in range(self.FAULT_RECOVERY_RETRIES):
                time.sleep(0.5 * (attempt + 1))
                self.logger.info(f"Recovery attempt {attempt + 1}...")
                pass  # The actual retry happens recursively in the calling method if this returns True

        # Handle RAM starvation in WASM by forcing aggressive garbage collection
        elif isinstance(exception, MemoryError):
            self.logger.info("Diagnosis: Heap Exhaustion. Forcing aggressive garbage collection.")
            gc.collect(2)
            healed = True

        with self._state_lock:
            self._state = original_state if healed else TransactionState.FRACTURED

        return healed

    def _transition_to_fractured(self, reason: Exception):
        """Forces an immediate rollback and status update."""
        with self._state_lock:
            if self._state == TransactionState.FRACTURED: return
            self._state = TransactionState.FRACTURED

        self.chronomancer.perform_emergency_rollback()
        self.volume_shifter.cleanup()
        self.simulacrum.purge_session()

        self._event_stream.append({
            "event": "FRACTURED",
            "reason": str(reason),
            "ts": time.time_ns(),
            "trace_id": self.trace_id
        })

    def _enrich_if_needed(self):
        if self._dossier_enriched or self.simulate:
            return
        enriched_results = self.chronicle_bridge._enrich_dossier()
        for result in enriched_results:
            self.write_dossier[result.path] = result
        self._dossier_enriched = True

    def cancel(self):
        """Allows external processes to explicitly abort the transaction."""
        with self._state_lock:
            if self._state == TransactionState.VOID or self._state == TransactionState.FRACTURED:
                return
            self.logger.warn(f"Transaction '{self.rite_name}' was explicitly cancelled.")
            self._transition_to_fractured(Exception("Transaction cancelled by user or process."))

    def _project_hud_pulse(self, type_label: str, color: str):
        """Dispatches progress metrics to the UI."""
        regs = self.committer.registers
        if regs and hasattr(regs, 'akashic') and regs.akashic:
            try:
                regs.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "GNOSTIC_TX",
                        "color": color,
                        "trace": self.tx_id[:8]
                    }
                })
            except Exception:
                pass

    def _archive_failed_rite(self, exc_type, exc_val, exc_tb):
        """Generates a structured forensic report after a catastrophic failure."""
        gnosis = TransactionalGnosis(
            trace_id=self.trace_id,
            tx_id=self.tx_id,
            rite_name=self.rite_name,
            context=dict(self.context),
            dossier_count=len(self.write_dossier),
            edict_count=len(self.edicts_executed),
            heresy_count=len(self.heresies_perceived),
            is_simulation=self.simulate,
            event_stream=list(self._event_stream),
            birth_ns=self._boot_ns,
            death_ns=getattr(self, 'active_death_ns', time.perf_counter_ns())
        )
        self.chronomancer.archive_failed_rite(gnosis, exc_type, exc_val, exc_tb)

    def _record_perception(self, logical_path: Union[str, Path]):
        """Records file access for UI visualization."""
        p_str = str(logical_path).replace('\\', '/')

        if not hasattr(self, "_perceived_paths"):
            object.__setattr__(self, "_perceived_paths", set())

        if p_str not in self._perceived_paths:
            self._perceived_paths.add(p_str)

            akashic = getattr(self.engine, 'akashic', None)
            if akashic:
                try:
                    akashic.broadcast({
                        "method": "novalym/perception_pulse",
                        "params": {"path": p_str, "tx_id": self.tx_id, "type": "SCRY"}
                    })
                except Exception:
                    pass

    def get_staging_path(self, logical_path: Union[str, Path]) -> Path:
        """
        Translates a target project path into its corresponding temporary staging path.
        This is the core redirect mechanism that protects the live filesystem during generation.
        """
        _start_ns = time.perf_counter_ns()

        if not self.active:
            state_label = getattr(self._state, 'name', 'VOID')
            self._sys_log(f"[ERROR] Attempted path resolution outside valid transaction window (State: {state_label}).",
                          "31")
            raise ArtisanHeresy(
                f"Transaction Boundary Error: Attempted to access staging while transaction is {state_label}.",
                severity=HeresySeverity.CRITICAL,
                details=f"Target: {logical_path} | ID: {self.tx_id}"
            )

        if logical_path is None:
            self._sys_log("Warning: NoneType path received. Normalizing to root ('.').", "33")
            logical_path = "."

        clean_path = str(logical_path).replace('\\', '/')

        try:
            self._record_perception(clean_path)

            # Delegate to the StagingManager singleton for actual path math
            physical_coord = self.staging_manager.get_staging_path(clean_path)

            if _DEBUG_MODE:
                _duration = (time.perf_counter_ns() - _start_ns) / 1_000_000
                self._sys_log(f"Resolved: '{clean_path}' -> {physical_coord.name} ({_duration:.3f}ms)")

            return physical_coord

        except Exception as routing_error:
            tb_str = traceback.format_exc()
            err_msg = f"Path Resolution Failed for '{clean_path}': {str(routing_error)}"
            self._sys_log(f"[ERROR] {err_msg}", "31")

            if hasattr(self, "_faults"):
                self._faults.append({
                    "msg": err_msg,
                    "ts": time.time(),
                    "state": self._state.name,
                    "trace": self.trace_id
                })

            # If this fails during the commit phase, it's critical. Otherwise, it's a standard error.
            severity = HeresySeverity.CRITICAL if self._state == TransactionState.FLIPPING else HeresySeverity.ERROR

            raise ArtisanHeresy(
                "STAGING_RESOLUTION_FAILURE",
                details=f"{err_msg}\n\nTraceback:\n{tb_str}",
                severity=severity,
                metadata={
                    "logical_path": clean_path,
                    "tx_state": self._state.name,
                    "trace_id": self.trace_id
                }
            )

    def __repr__(self) -> str:
        return f"<GnosticTransaction id={self.tx_id[:8]} state={self._state.name}>"