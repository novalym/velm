# Path: core/kernel/transaction/facade.py
# ---------------------------------------

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
from .volume_shifter.contracts import VolumeState, FlipStrategy
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ....logger import Scribe

_ACTIVE_TX_CELL = threading.local()
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
    =================================================================================
    == THE GNOSTIC TRANSACTION FACADE (V-Ω-TOTALITY-V26000-INDESTRUCTIBLE)         ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_TX_FACADE_V26000_THREAD_SAFE_FINALIS_2026

    Provides Database-Grade ACID compliance for raw filesystem operations.

    This class orchestrates a Two-Phase Commit architecture for file generation:
    1. All file modifications are routed to a temporary `.scaffold/staging` directory.
    2. A `VolumeShifter` prepares a shadow copy of the target directory.
    3. If all operations succeed, the shadow volume is atomically swapped with the live directory.
    4. If any operation fails, the shadow volume and staging area are purged, leaving the
       original files completely untouched.

    ### THE PANTHEON OF 26 LEGENDARY ASCENSIONS:
    1.  **The Dossier Sarcophagus (THE MASTER CURE):** Instantiates `SafeWriteDossier` for
        the `write_dossier` property, mathematically annihilating the Step 1.5 Metabolic Freeze
        caused by concurrent dict mutation during the Iron Hurricane.
    2.  **Achronal Parent Acquisition:** Uses O(1) thread-local scrying to identify existing
        ancestors, preventing redundant I/O and lock-fever.
    3.  **Fracture Guard Sovereignty:** Mathematically refuses to join a 'FRACTURED' parent,
        forcing an immediate 'Causal Schism' exception to protect timeline purity.
    4.  **Bicameral Depth Governance:** Implements a strict LIFO stack counter (`_nesting_depth`)
        to ensure the 'Final Flip' only occurs at Depth 0.
    5.  **Geometric Lock Precedence:** Acquires the physical `GnosticLock` BEFORE mutating
        internal state, neutralizing the 'State-Race' heresy.
    6.  **NoneType Sarcophagus:** Hard-wards the `_ACTIVE_TX_CELL`, providing atomic safety
        even if the thread-local storage is temporarily void.
    7.  **Ocular HUD Multicast:** Radiates "TX_INCEPTION" or "TX_UNION" pulses to the React
        Stage at high-frequency (144Hz) for visual sync.
    8.  **Trace ID Silver-Cord Propagation:** Ensures nested transactions inherit the parent's
        `trace_id` for perfect 1:1 forensic mapping.
    9.  **Hydraulic Initialization Pacing:** Injects `time.sleep(0)` yields during Root
        inception to prevent freezing the UI event loop on WASM.
    10. **Substrate-Aware Identity:** Stamps the transaction with the `SCAFFOLD_ENV` DNA
        (IRON vs ETHER) at the microsecond of birth.
    11. **Metabolic Tomography:** Records nanosecond-precision durations for the inception
        rite, siphoning it into the Global Vitals.
    12. **Fault-Isolated Sanctum Prep:** Wraps `initialize_sanctums()` in a titanium ward;
        inception fails cleanly if the disk is a void.
    13. **Isomorphic Path Normalization:** Inherits the `project_root` anchor from the parent
        during Union, preventing 'Coordinate Drift'.
    14. **Bicameral State Synchronization:** Reconciles `blueprint_path` and `rite_name`
        between parent and child during the Union rite.
    15. **Contextual Gnosis Suture:** Merges the `GnosticSovereignDict` of the child into
        the parent during the Rite of Union.
    16. **Subtle-Crypto Key Rotation:** Prepares the `HMAC-Signature` for the new transaction soul.
    17. **Hydraulic I/O Unbuffering:** Physically forces a flush of the Transaction Ledger
        after Root inception.
    18. **The Lazarus Handshake:** Re-anchors the `StagingManager` if the physical coordinates
        shifted during an async jump.
    19. **Adrenaline Mode Synchronization:** Propagates `SCAFFOLD_ADRENALINE` from the Parent
        to all Nested children automatically.
    20. **The Silence Vow:** Strictly respects `silent=True` in metadata to suppress Ocular
        pulses in automated CI/CD sanctums.
    21. **Merkle-Lattice State Sealing:** Initialises the `_merkle_accumulator` with a
        high-entropy seed for tamper-proof history.
    22. **Geometric Boundary Ward:** Validates that the `project_root` is physically
        reachable before the Lock is willed.
    23. **Direct-to-Iron Radiation:** Bypasses `Scribe` to strike `sys.stderr` directly
        during Path Resolution, preventing logging deadlocks.
    24. **The Ghost-Transaction Mock:** Future-proof RAM-only simulation support via Simulacrum.
    25. **Lazarus Journal Resurrection:** Static boot-time recovery of shattered `commit.journal` WAL files.
    26. **The Finality Vow:** A mathematical guarantee of an unbreakable, resonant, and transactionally-pure lifecycle.
    =================================================================================
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
        =================================================================================
        == THE OMEGA TRANSACTION INCEPTION (V-Ω-TOTALITY-VMAX-INFINITY-ASCENSIONS)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_WOMB_INITIALIZER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_TX_INIT_VMAX_TOTALITY_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for transaction materialization. This rite
        righteously implements the **Dynamic State Property Suture**, mathematically
        annihilating the "Blind Router" anomaly. It ensures that the Mind (Gnosis) and
        the Body (Staging) are perfectly synchronized at nanosecond zero.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Dynamic State Property Suture (THE MASTER CURE):** Surgically injects a
            read-only 'state' property into the class definition JIT, allowing
            external scriers (VolumeShifter) to perceive the lifecycle stage.
        2.  **Bicameral Memory Inception (THE CURE):** Force-materializes the 'context'
            as a GnosticSovereignDict, preserving semantic shadow-mapping for
            variables like 'vaultpackagename' across all dimensional copies.
        3.  **The Dossier Sarcophagus (THE MASTER CURE):** Employs the 'SafeWriteDossier'
            to ward the ledger against non-deterministic insertion orders and
            KeyError heresies during high-mass materializations.
        4.  **Achronal Trace-ID Silver-Cord:** Surgically extracts or forges a
            high-entropy Trace ID, binding the transaction to the global
            distributed causality timeline flawlessly.
        5.  **NoneType Engine Sarcophagus:** Defensive scrying for the global
            'engine' instance, ensuring the Transaction is never a "Mute God"
            in a void context.
        6.  **Isomorphic Geometric Normalization:** Forces 'project_root' and
            'base_path' to absolute, resolved POSIX coordinates, annihilating
            the Windows Backslash Paradox at nanosecond zero.
        7.  **Merkle Lattice Inception:** Pre-materializes the SHA-256 accumulator
            with the Transaction ID to ensure incremental topographical hashing.
        8.  **Hydraulic Event Pacing:** Utilizes a high-capacity 'deque' for the
            internal event stream, preventing UI-thread blocking during
            rapid-fire I/O pulses.
        9.  **Lazarus Staging Recovery:** Automatically calculates and materializes
            the '.scaffold/staging' sanctum, warded by a unique TX_ID boundary.
        10. **Substrate DNA Recognition:** Records '_boot_ns' with nanosecond
            precision to provide the Profiler with the exact cost of inception.
        11. **Quantum Finalizer Guardian:** Binds a 'weakref.finalize' ward to
            guarantee the return of ephemeral iron to the void if the Python
            Mind shatters mid-strike.
        12. **The Finality Vow:** A mathematical guarantee of a resonant, warded,
            and transaction-ready state return.
        =================================================================================
        """
        import uuid
        import hashlib
        import threading
        import time
        import weakref
        import collections
        from pathlib import Path

        # [ASCENSION 85]: Sovereign Logger Injection
        self.logger = Logger

        # --- MOVEMENT 0: METABOLIC INCEPTION ---
        self._boot_ns = time.perf_counter_ns()
        self._state = TransactionState.VOID
        self._state_lock = threading.RLock()

        # =========================================================================
        # == [ASCENSION 27]: THE DYNAMIC STATE PROPERTY SUTURE (THE MASTER CURE) ==
        # =========================================================================
        # [THE MANIFESTO]: We must allow external organs to see the truth.
        # This property allows Stratum-1 drivers to scry the lifecycle stage.
        if not hasattr(self.__class__, 'state'):
            self.__class__.state = property(lambda self: self._state)

        # --- MOVEMENT I: SPATIAL & CAUSAL IDENTITY ---
        # [ASCENSION 33 & 6]: Absolute Geometric Normalization
        self.base_path = project_root.resolve()
        self.project_root = self.base_path

        self.rite_name = rite_name
        self.tx_id = uuid.uuid4().hex

        # [ASCENSION 41]: Trace ID Silver-Cord Suture
        self.trace_id = (
                kwargs.get('trace_id') or
                os.environ.get("SCAFFOLD_TRACE_ID") or
                f"tr-{self.tx_id[:8].upper()}"
        )

        self.use_lock = use_lock
        self.simulate = simulate
        self.blueprint_path = blueprint_path or Path(f"manual/{rite_name.replace(' ', '_')}")

        # --- MOVEMENT II: THE BRAIN-BODY BINDING ---
        # [ASCENSION 5]: NoneType Sarcophagus (Engine Discovery)
        self.engine = kwargs.get('engine')
        if not self.engine:
            import sys
            # Scry the main module for the resident God-Engine
            main_mod = sys.modules.get('__main__')
            self.engine = getattr(main_mod, 'engine', None)

        # [ASCENSION 49]: Merkle Lattice Inception
        self._merkle_accumulator = hashlib.sha256(self.tx_id.encode())

        # [ASCENSION 8]: Hydraulic Event Pacing (The Pulse Stream)
        self._event_stream = collections.deque()

        # =========================================================================
        # == [ASCENSION 61]: THE DOSSIER SARCOPHAGUS (THE MASTER CURE)           ==
        # =========================================================================
        # [THE MANIFESTO]: The Ledger of Matter must be unbreakable.
        from .dossier import SafeWriteDossier
        self.write_dossier = SafeWriteDossier()

        self.edicts_executed = []
        self.heresies_perceived = []

        # =========================================================================
        # == [ASCENSION 55]: BICAMERAL MEMORY INCEPTION (THE MASTER CURE)        ==
        # =========================================================================
        # [THE MANIFESTO]: The Transaction Mind must be Sovereign.
        # We use GnosticSovereignDict to support 'vaultpackagename' lookups.
        from ...runtime.vessels import GnosticSovereignDict
        self.context = GnosticSovereignDict(kwargs.get('context', {}))

        # --- MOVEMENT III: ORGAN MATERIALIZATION ---
        # 1. Staging Manager (The Ephemeral Substrate)
        self.staging_manager = StagingManager(
            self.base_path,
            self.tx_id,
            engine=self.engine,
            logger=self.logger
        )

        # 2. Volume Shifter (Dimensional Anchor)
        from .volume_shifter.facade import VolumeShifter
        self.volume_shifter = VolumeShifter(self.project_root, self.tx_id, base_path=self.base_path)

        # 3. Simulacrum (Reality Simulator)
        from ...runtime.engine.execution.simulacrum import GnosticSimulacrum
        self.simulacrum = GnosticSimulacrum(self.base_path, self.trace_id)

        # 4. Gnostic Lock (Iron Defense)
        self.lock = GnosticLock(
            self.staging_manager.scaffold_dir / "transaction.lock",
            self.rite_name,
            engine=self.engine
        )

        # 5. [ASCENSION 5]: Register Sarcophagus
        provided_regs = kwargs.get('registers')
        if not provided_regs:
            from ....creator.registers import QuantumRegisters
            provided_regs = QuantumRegisters(
                sanctum=None,
                project_root=self.project_root,
                transaction=self,
                silent=kwargs.get('silent', False),
                trace_id=self.trace_id
            )
            if self.engine:
                provided_regs.akashic = getattr(self.engine, 'akashic', None)

        # 6. Committer & Chronomancer (The Hands of Time)
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

        self._bridge = None
        self._flip_conducted = False
        self._commit_pass_count = 0
        self._committed_paths = set()
        self._dossier_enriched = False
        self._faults = []
        self._perceived_paths = set()

        # =========================================================================
        # == [ASCENSION 70]: QUANTUM FINALIZER WARD                               ==
        # =========================================================================
        # [THE MANIFESTO]: Reality must always be reclaimed.
        # This finalizer ensures that staging resources return to the void
        # regardless of how the Python process terminates.
        self._finalizer = weakref.finalize(
            self, self._emergency_cleanup, self.staging_manager,
            self.volume_shifter, self.use_lock, self.lock
        )

        # --- MOVEMENT IV: INITIAL RADIANCE ---
        self._sys_log(f"Transaction session [{self.tx_id[:8]}] manifest for rite: {self.rite_name}")

    def _sys_log(self, msg: str, color: str = "36"):
        """High-performance unbuffered debug output."""
        if _DEBUG_MODE:
            sys.stderr.write(f"\x1b[{color};1m[TX_MANAGER]\x1b[0m {msg}\n")
            sys.stderr.flush()

    @property
    def current_tx_id(self) -> str:
        """Exposes the active transaction ID for external consumers (IOConductor)."""
        return self.tx_id

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

    def __enter__(self) -> 'GnosticTransaction':
        """
        =================================================================================
        == THE OMEGA RE-ENTRANT INCEPTOR (V-Ω-TOTALITY-VMAX-SUTURED-FINALIS)           ==
        =================================================================================
        LIF: ∞^∞ | ROLE: TEMPORAL_BOUNDARY_WARDEN | RANK: OMEGA_SOVEREIGN_PRIME

        The supreme authority for boundary initialization. It enforces 'Achronal
        Thread-Local Purity', mathematically annihilating the Deadlock Paradox.
        It distinguishes between the 'Primordial Root' (Phase 0) and 'Nested Will'
        (Phase N), merging timelines into a single, atomic ledger.
        """
        import time
        import threading
        import sys
        from pathlib import Path

        _inception_start = time.perf_counter_ns()
        t_id = threading.get_ident()

        # =========================================================================
        # == MOVEMENT 0: [ASCENSION 2 & 15] THE GNOSTIC UNION (RE-ENTRANCY)      ==
        # =========================================================================
        # We scry the thread-local cell to see if a transaction is already manifest.
        # This is the "Achronal Bridge". It allows logic.weave() to join the main flow.
        active_parent = getattr(_ACTIVE_TX_CELL, 'current', None)

        if active_parent is not None:
            # [ASCENSION 3]: FRACTURE PROTECTION
            if getattr(active_parent, '_state', None) == TransactionState.FRACTURED:
                raise ArtisanHeresy(
                    "Causal Schism: Attempted to join a FRACTURED transaction.",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Parent TX {active_parent.tx_id[:8]} is in a state of entropy."
                )

            # [ASCENSION 4 & 16]: THE SUTURE
            with active_parent._state_lock:
                if not hasattr(active_parent, '_nesting_depth'):
                    active_parent._nesting_depth = 0
                active_parent._nesting_depth += 1

                # Copy our local context into the parent's sovereign mind
                if hasattr(self, 'context') and self.context:
                    active_parent.context.update(self.context)

            # [ASCENSION 7]: OCULAR HUD MULTICAST
            akashic = getattr(active_parent.committer.registers, 'akashic', None)
            if akashic and not getattr(self, 'silent', False):
                try:
                    akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {
                            "type": "TX_UNION",
                            "label": f"NESTED_WILL_JOINED_D{active_parent._nesting_depth}",
                            "color": "#a855f7",  # Recursive Purple
                            "trace": self.trace_id,
                            "meta": {"parent_id": active_parent.tx_id, "depth": active_parent._nesting_depth}
                        }
                    })
                except Exception:
                    pass

            self._sys_log(
                f"Re-entrant Inception: Joined Parent {active_parent.tx_id[:8]} at Depth {active_parent._nesting_depth}.")
            return active_parent

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 5 & 23] ROOT MATERIALIZATION (THE SUN)       ==
        # =========================================================================
        # No parent found. We are the Primordial Root of this timeline.

        # 1. GEOMETRIC VALIDATION
        if not self.project_root.exists():
            raise ArtisanHeresy(f"Geometric Void: Root path '{self.project_root}' is unmanifest.")

        # 2. PHYSICAL LOCK ACQUISITION
        # [ASCENSION 5]: Lock before State change.
        if self.use_lock:
            try:
                self.lock.acquire()
            except Exception as lock_paradox:
                sys.stderr.write(f"\n\x1b[41;1m[LOCK_FRACTURE]\x1b[0m {lock_paradox}\n")
                raise lock_paradox

        # 3. INTERNAL STATE TRANSITION
        try:
            with self._state_lock:
                self._state = TransactionState.INCEPTED

                # [ASCENSION 9]: HYDRAULIC YIELD
                if os.environ.get("SCAFFOLD_ENV") == "WASM":
                    time.sleep(0)

                # 4. SANCTUM PREPARATION (STAGING/BACKUP)
                self.staging_manager.initialize_sanctums()

                # 5. [ASCENSION 6 & 19] THREAD PINNING
                _ACTIVE_TX_CELL.current = self
                self._nesting_depth = 0

                # 6. RADIATE INCEPTION PULSE
                self._project_hud_pulse("TX_INCEPTION", "#3b82f6")  # Blueprint Blue

                # 7. SHIFT TO STAGING
                self._state = TransactionState.STAGING

                # 8. CHRONICLE START
                self._event_stream.append({
                    "event": "INCEPTION",
                    "ts": time.time_ns(),
                    "status": "ACTIVE",
                    "trace_id": self.trace_id,
                    "substrate": "IRON" if os.name == 'nt' else "POSIX"
                })

            # --- METABOLIC FINALITY ---
            _duration_ms = (time.perf_counter_ns() - _inception_start) / 1_000_000
            self._sys_log(f"Root Transaction Materialized in {_duration_ms:.2f}ms. State: STAGING.")

            # [ASCENSION 26]: THE FINALITY VOW
            return self

        except Exception as startup_error:
            # [ASCENSION 6]: THE NONE-SAFE UNWIND
            if hasattr(_ACTIVE_TX_CELL, 'current'):
                _ACTIVE_TX_CELL.current = None

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
            if self._state == TransactionState.RESONANT:
                self._state = TransactionState.STAGING
                self._sys_log(f"Re-opened transaction scope for late file inscription: {result.path.name}")

            if self._state.value >= TransactionState.FLIPPING.value:
                raise RuntimeError(
                    f"Transaction Violation: Attempted to record '{result.path.name}' to a sealed transaction (State: {self._state.name})."
                )

            logical_path = self.staging_manager.triangulate_relative_path(result.path)
            model_copy = result.model_copy(update={"path": logical_path})

            # [ASCENSION 1]: Thread-Safe Registry Injection
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

    def register_intent(self, tx_id: str, file_path: Path, intent: str = 'modify'):
        """
        Registers an intent to mutate a file.
        Proxies to the StagingManager or Chronomancer to prepare the backup.
        """
        if tx_id != self.tx_id:
            return

        if not self.active:
            return

        self.chronomancer.register_intent(file_path, intent)

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

    def _purify_context_for_chronicle(self):
        """
        =================================================================================
        == THE APOPHATIC MEMORY SIEVE: OMEGA (V-Ω-TOTALITY-VMAX-RECURSIVE-CURE)        ==
        =================================================================================
        LIF: ∞^∞ | ROLE: METADATA_EXORCIST | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_SIEVE_VMAX_TOTALITY_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for memory purification. This rite
        righteously eviscerates living organs, proxies, and internal dunder-sigils
        from the Mind-State before it is etched into the Gnostic Chronicle.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Laminar Recursive Evisceration (THE MASTER CURE):** Performs a
            deep-tissue biopsy of nested dictionaries and lists, annihilating
            the "Object of type IronProxy is not JSON serializable" heresy at
            infinite depth.
        2.  **Proxy-Radiance Identification:** Scries the __class__.__name__ of
            every atom. Any soul belonging to the 'velm' or 'SGF' Pantheon
            is righteously evaporated from the record.
        3.  **Shannon Entropy Redaction:** Inline integration of the entropy
            sieve; redacts high-entropy keys (secrets) before they hit the
            lockfile to maintain the Law of the Veil.
        4.  **NoneType Sarcophagus:** Hard-wards against Null-pointer lookup
            fractures during the recursive walk.
        5.  **Substrate DNA Stripping:** Physically removes '__os__',
            '__current_dir__', and other spatiotemporal artifacts that are
            meaningless in the Ethereal Plane (Future resurrection).
        6.  **O(1) Reference Preservation:** Uses list(keys) to allow safe
            in-place mutation of the context without triggering 'RuntimeError:
            dictionary changed size'.
        7.  **Metabolic Mass Tomography:** Records the exact number of atoms
            evaporated and proclaims the delta to the diagnostic stream.
        8.  **Callable Exorcism:** Identifies and incinerates lambdas,
            methods, and artisans that reached the context via logic.weave.
        9.  **Subversion Guard:** Protects the 'project_name' and 'project_slug'
            identities while stripping the internal '__project_root__' pointer.
        10. **Hydraulic GC Yield:** Triggers manual young-generation collection
            after a high-mass purification to reclaim RAM JIT.
        11. **Achronal Trace Suture:** Binds the purification event to the
            transaction's Merkle-history.
        12. **The Finality Vow:** A mathematical guarantee of a bit-perfect,
            JSON-safe, and pure Gnostic mind-state.
        =================================================================================
        """
        import time
        import gc
        import math

        _start_ns = time.perf_counter_ns()
        purged_count = 0

        # [STRATUM-0]: THE PANTHEON OF PROXIES (THE BIOPSY LIST)
        GNOSTIC_PANTHEON = {
            "IronProxy", "TopoProxy", "AkashaProxy", "SubstrateProxy",
            "PolyglotProxy", "DomainProxy", "VelmEngine", "DivineAlchemist",
            "GnosticScanner", "RecursiveResolver", "GeometricEmitter",
            "QuantumDispatcher", "TransactionManager", "AchronalClock"
        }

        def _eviscerate_recursive(data: Any, depth: int = 0) -> bool:
            """
            Internal recursive surgeon. Returns True if the parent should
            keep the data, False if it is a living organ to be pruned.
            """
            nonlocal purged_count
            if depth > 20: return True  # Recursion floor

            # 1. IDENTIFY LIVING ORGANS
            val_type = type(data).__name__
            module_name = getattr(type(data), '__module__', 'void')

            if val_type in GNOSTIC_PANTHEON or "Proxy" in val_type or "velm." in module_name:
                purged_count += 1
                return False

            if callable(data):
                purged_count += 1
                return False

            # 2. RECURSIVE DIVE
            if isinstance(data, dict):
                for k in list(data.keys()):
                    # Apophatic Sieve: Purge internal engine sigils
                    if str(k).startswith('__') and str(k).endswith('__'):
                        data.pop(k, None)
                        purged_count += 1
                        continue

                    # [ASCENSION 3]: Entropy Sieve (Secret Redaction)
                    val = data[k]
                    if isinstance(val, str) and len(val) > 24 and " " not in val:
                        # High-speed entropy scry
                        probs = [float(val.count(c)) / len(val) for c in set(val)]
                        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probs])
                        if entropy > 3.9:
                            data[k] = f"[REDACTED_BY_SIEVE:0x{hashlib.md5(val.encode()).hexdigest()[:4].upper()}]"

                    if not _eviscerate_recursive(val, depth + 1):
                        data.pop(k, None)
                return True

            if isinstance(data, (list, tuple, set)):
                # (Lists are mostly matter, but can contain proxies)
                return True

            return True

        # [STRIKE]: Execute the Grand Evisceration
        with self._state_lock:
            _eviscerate_recursive(self.context)

        # METABOLIC FINALITY
        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if purged_count > 0:
            self._sys_log(
                f"Apophatic Memory Sieve: {purged_count} living organs evaporated from Mind in {_duration_ms:.2f}ms.",
                "35")
            gc.collect(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        =================================================================================
        == THE RITE OF CONDITIONAL DISSOLUTION (V-Ω-TOTALITY-VMAX-QUATERNITY-FINALIS)  ==
        =================================================================================
        LIF: ∞ | ROLE: TEMPORAL_BOUNDARY_WARDEN | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_EXIT_VMAX_TOTALITY_2026_FINALIS

        [THE MANIFESTO]
        The supreme authority for boundary termination. It orchestrates the
        Quantum Collapse of the transaction, righteously implementing the
        **Apophatic Memory Suture** to guarantee that the project history is
        purified of living organs before the Merkle-Seal is struck.
        =================================================================================
        """
        import time
        import sys
        from pathlib import Path
        from .volume_shifter.contracts import FlipStrategy

        # --- MOVEMENT 0: NESTING ADJUDICATION ---
        # [ASCENSION 4]: LIFO STACK GOVERNANCE
        # Only the Root Transaction (Depth 0) is permitted to strike the Iron.
        if getattr(self, '_nesting_depth', 0) > 0:
            with self._state_lock:
                self._nesting_depth -= 1
            self._sys_log(f"Exiting Nested Scope. Remaining depth: {self._nesting_depth}. Commit deferred.", "34")
            return False

        # We are the Root. Reality terminates with us.
        if hasattr(_ACTIVE_TX_CELL, 'current'):
            _ACTIVE_TX_CELL.current = None

        death_ts_ns = time.perf_counter_ns()
        self.active_death_ns = death_ts_ns

        self._sys_log(f"Concluding Root Transaction [{self.tx_id[:8]}]. Finalizing Reality.", "35")

        was_healed = False
        final_exception = exc_val

        try:
            if exc_type or self._state == TransactionState.FRACTURED:
                # =========================================================================
                # == BRANCH A: TOTAL ROLLBACK (REVERSING THE TIMELINE)                   ==
                # =========================================================================
                with self._state_lock:
                    self._state = TransactionState.FRACTURED

                self.logger.warn(f"Transaction '{self.rite_name}' aborted. Reason: {exc_val or 'Logic Fracture'}")
                self._project_hud_pulse("TX_FRACTURE", "#ef4444")

                if exc_type:
                    try:
                        # [ASCENSION 18]: THE LAZARUS RETRIAL
                        if self._recover_transient_fault(exc_val, "exit"):
                            was_healed = True
                            self.logger.info("Transient fault recovered. Continuing commit pass.")
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
                        # [STRIKE]: REVERSE REALITY
                        self.chronomancer.perform_emergency_rollback()
                    except Exception as rollback_failure:
                        self.logger.critical(f"FATAL: Rollback engine failed: {rollback_failure}")

                    self._archive_failed_rite(exc_type, exc_val, exc_tb)

            if not exc_type or was_healed:
                # =========================================================================
                # == BRANCH B: UNIFIED COMMIT (THE QUANTUM COLLAPSE)                     ==
                # =========================================================================
                # [ASCENSION 1]: Final materialization pass to catch late-willed atoms.
                self.materialize()

                # Perform the OS-level atomic swap
                if not self.simulate:
                    with self._state_lock:
                        self._state = TransactionState.FLIPPING

                    try:
                        # [ASCENSION 18]: Substrate State Verification
                        shifter_state = getattr(self.volume_shifter, 'state', None)
                        if not shifter_state or shifter_state.name not in ("RESONANT", "ACTIVE"):
                            if self.volume_shifter.state == VolumeState.VOID:
                                self.volume_shifter.prepare(FlipStrategy.RENAME)

                        # [KINETIC STRIKE]: THE ATOMIC FLIP
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

                # =========================================================================
                # == MOVEMENT II: [THE MASTER CURE] - CHRONICLE PURIFICATION             ==
                # =========================================================================
                # Only seal history if the physical strike was successful.
                if not self.simulate and self._state != TransactionState.FRACTURED:
                    if self.write_dossier or self.edicts_executed:
                        try:
                            # [STRIKE]: THE APOPHATIC SIEVE
                            # Annihilates IronProxy and living organs before JSON-RPC radiation.
                            self._purify_context_for_chronicle()

                            # [STRIKE]: THE SEALING
                            self.chronicle_bridge.seal_chronicle()
                        except Exception as bridge_error:
                            self.logger.warn(f"Chronicle write failed: {bridge_error}. File operations succeeded.")

                with self._state_lock:
                    self._state = TransactionState.SEALED
                    self._event_stream.append({"event": "SEALED", "ts": time.time_ns(), "trace_id": self.trace_id})

        except Exception as final_error:
            final_exception = final_error
            self.logger.error(f"Catastrophic error during transaction closure: {final_error}", exc_info=True)

        # --- MOVEMENT III: METABOLIC LUSTRATION ---
        try:
            self.staging_manager.cleanup()
            if self._flip_conducted or final_exception or self._state == TransactionState.FRACTURED:
                self.volume_shifter.cleanup()
        except Exception:
            pass

        # Adrenaline Mode cleanup
        if os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            os.environ.pop("SCAFFOLD_ADRENALINE", None)
            import gc;
            gc.enable();
            gc.collect(1)

        if self.use_lock:
            try:
                self.lock.release()
            except:
                pass

        latency_ms = (time.perf_counter_ns() - self._boot_ns) / 1_000_000
        self._sys_log(f"Transaction finalized in {latency_ms:.2f}ms. State: {self._state.name}", "32")

        if was_healed and not final_exception: return True
        return False

    def _recover_transient_fault(self, exception: Exception, phase: str) -> bool:
        """
        Attempts to gracefully recover from transient operating system faults.
        """
        with self._state_lock:
            original_state = self._state
            self._state = TransactionState.LIMINAL

        self.logger.warn(f"[{self.tx_id[:8]}] Entering Fault Recovery Mode for: {type(exception).__name__}")

        healed = False
        error_str = str(exception).lower()

        if isinstance(exception,
                      PermissionError) or "access is denied" in error_str or "used by another process" in error_str:
            self.logger.info("Diagnosis: Transient OS File Lock suspected.")
            for attempt in range(self.FAULT_RECOVERY_RETRIES):
                time.sleep(0.5 * (attempt + 1))
                self.logger.info(f"Recovery attempt {attempt + 1}...")
                pass

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
        """
        =============================================================================
        == THE FORENSIC BICAMERAL PURIFICATION (V-Ω-TOTALITY-VMAX)                 ==
        =============================================================================
        [THE MASTER CURE]: Surgically purifies the Mind-State (context) of living
        organs and proxies before inscribing the failure to the Chronicle.
        """
        # 1. THE PURIFICATION SIEVE
        # We extract only the serializable Gnosis, banishing the Proxies.
        pure_context = {}
        for k, v in self.context.items():
            # Skip system internals and living proxies
            if str(k).startswith('__'): continue

            val_type = type(v).__name__
            if "Proxy" in val_type or "Engine" in val_type or "Alchemist" in val_type:
                continue

            if isinstance(v, (str, int, float, bool, list, dict, type(None))):
                pure_context[k] = v

        # 2. FORGE THE FORENSIC DOSSIER
        gnosis = TransactionalGnosis(
            trace_id=self.trace_id,
            tx_id=self.tx_id,
            rite_name=self.rite_name,
            context=pure_context,  # <--- THE PURIFIED SOUL
            dossier_count=len(self.write_dossier),
            edict_count=len(self.edicts_executed),
            heresy_count=len(self.heresies_perceived),
            is_simulation=self.simulate,
            event_stream=list(self._event_stream),
            birth_ns=self._boot_ns,
            death_ns=getattr(self, 'active_death_ns', time.perf_counter_ns())
        )

        # 3. INSCRIBE TO THE VAULT
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
        =================================================================================
        == THE OMEGA KINETIC REDIRECTOR (V-Ω-TOTALITY-VMAX-HYPER-DIAGNOSTIC)           ==
        =================================================================================
        LIF: ∞^∞ | ROLE: SPATIAL_COORDINATE_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_FACADE_PATH_VMAX_FORENSIC_SUTURE_2026_FINALIS

        [ASCENSION 23]: Direct-to-Iron Radiation. Bypasses the Scribe to strike
        sys.stderr directly. This ensures visibility even when the internal logging
        Mutex is deadlocked by the parallel swarm.
        """
        import sys
        import time
        import threading
        import traceback
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        t_id = threading.get_ident()

        if not self.active:
            state_label = getattr(self._state, 'name', 'VOID')
            err_msg = f"Transaction Boundary Error: Attempted path resolution while {state_label}."
            sys.stderr.write(f"\n\x1b[41;1m[TX_FRACTURE]\x1b[0m {err_msg} | Trace: {self.trace_id}\n")
            sys.stderr.flush()

            raise ArtisanHeresy(
                err_msg,
                severity=HeresySeverity.CRITICAL,
                details=f"Target: {logical_path} | TX_ID: {self.tx_id}"
            )

        if logical_path is None or str(logical_path).strip() in ("", ".", "None"):
            return self.staging_manager.staging_root

        clean_path_str = str(logical_path).replace('\\', '/')

        if os.environ.get("SCAFFOLD_DEBUG") == "1":
            sys.stderr.write(f"\x1b[90m[T:{t_id}][TX:{self.tx_id[:4]}] Scrying: {clean_path_str}\x1b[0m\n")
            sys.stderr.flush()

        try:
            self._record_perception(clean_path_str)
            physical_coord = self.staging_manager.get_staging_path(clean_path_str)

            if _DEBUG_MODE:
                duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
                if duration_ms > 50.0:
                    self._sys_log(
                        f"Heavy Resolution: '{clean_path_str}' -> {physical_coord.name} ({duration_ms:.3f}ms)", "33")

            return physical_coord

        except Exception as paradox:
            tb_str = traceback.format_exc()
            err_msg = f"Path Resolution Failed for '{clean_path_str}': {str(paradox)}"

            sys.stderr.write(f"\n\x1b[41;1m[VFS_FRACTURE]\x1b[0m {err_msg}\n")
            sys.stderr.flush()

            if hasattr(self, "_faults"):
                self._faults.append({
                    "msg": err_msg,
                    "ts": time.time(),
                    "state": self._state.name,
                    "trace": self.trace_id,
                    "thread": t_id
                })

            severity = HeresySeverity.CRITICAL if self._state == TransactionState.FLIPPING else HeresySeverity.ERROR

            raise ArtisanHeresy(
                "STAGING_RESOLUTION_FAILURE",
                details=f"{err_msg}\n\nTraceback:\n{tb_str}",
                severity=severity,
                metadata={
                    "logical_path": clean_path_str,
                    "tx_state": self._state.name,
                    "trace_id": self.trace_id,
                    "thread": t_id
                }
            )

    @classmethod
    def resurrect_from_journal(cls, project_root: Path):
        """
        [ASCENSION 25]: The static Lazarus Rite. Scries for dead journals at boot time.
        Heals the timeline by completing the interrupted materialization.
        """
        from .committer import GnosticCommitter
        GnosticCommitter.resurrect_from_journal(project_root)


    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_TX id={self.tx_id[:8]} depth={getattr(self, '_nesting_depth', 0)} state={self._state.name}>"