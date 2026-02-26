# Path: src/velm/core/kernel/transaction/facade.py
# ------------------------------------------------

from __future__ import annotations

import gc
import os
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

# --- THE DIVINE UPLINKS ---
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

Logger = Scribe("GnosticTransaction")


class TransactionState(Enum):
    """
    =============================================================================
    == THE QUANTUM STATE AUTOMATON (V-Ω-LIFECYCLE-STATES)                      ==
    =============================================================================
    Defines the absolute, unbreakable stages of the transaction's existence.
    """
    VOID = auto()  # Unmanifest
    INCEPTED = auto()  # Lock acquired, ready to stage
    STAGING = auto()  # Accumulating matter in the ephemeral realm
    LUSTRATING = auto()  # Flushing to the Shadow Volume
    RESONANT = auto()  # Matter is fully prepared for the flip
    FLIPPING = auto()  # The critical microsecond of reality swapping
    SEALED = auto()  # Triumph. Chronicle written.
    LIMINAL = auto()  # Suspended state attempting auto-recovery
    FRACTURED = auto()  # Rolled back.


class GnosticTransaction:
    """
    =================================================================================
    == THE QUANTUM CRUCIBLE: OMEGA POINT (V-Ω-TOTALITY-V3000-RE-OPENING-RITE)      ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_STABILIZER | RANK: OMEGA_SINGULARITY

    The sovereign engine of Spacetime and Causality. It provides true Database-Grade
    ACID compliance for the filesystem, incorporating Event-Sourced Ledgering,
    Predictive Liminal Healing, and Dynamic Barycentric Re-Anchoring.

    [ASCENSION CURE]: Implements the "Re-Opening Rite". If late-stage matter (like
    the finalized scaffold.scaffold blueprint) arrives after the primary Lustration,
    the Crucible seamlessly unseals from RESONANT back to STAGING, enabling infinite
    multi-pass materialization.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    MAX_LUSTRATION_PASSES: Final[int] = 5
    IO_THROTTLE_THRESHOLD_MS: Final[float] = 100.0
    LIMINAL_HEALING_RETRIES: Final[int] = 2

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
        =============================================================================
        == THE RITE OF INCEPTION: OMEGA (V-Ω-TOTALITY-V2000-SUTURED-FINALIS)       ==
        =============================================================================
        LIF: ∞ | ROLE: TRANSACTION_CONSTRUCTOR | RANK: OMEGA_SUPREME
        AUTH: Ω_INIT_TX_V2000_ORGAN_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme constructor of the Quantum Crucible. It has been ascended to
        annihilate the 'StagingManager TypeError' by righteously scrying for the
        Engine soul and bestowing it upon the metabolic organs at birth.
        =============================================================================
        """
        self.logger = Logger

        self._state = TransactionState.VOID
        self._state_lock = threading.RLock()

        self._flip_conducted = False
        self._manifest_count = 0
        self._committed_paths: Set[Path] = set()
        self._dossier_enriched = False

        # --- I. THE GEOMETRIC ANCHORS ---
        self.base_path = project_root.resolve()
        self.project_root = self.base_path

        self.rite_name = rite_name
        self.blueprint_path = blueprint_path or Path(f"manual/{rite_name.replace(' ', '_')}")

        # --- II. IDENTITY & CAUSALITY ---
        self.tx_id = uuid.uuid4().hex
        self.trace_id = (
                kwargs.get('trace_id') or
                os.environ.get("SCAFFOLD_TRACE_ID") or
                f"tr-{self.tx_id[:8].upper()}"
        )
        self.use_lock = use_lock
        self.simulate = simulate
        self._boot_ns = time.perf_counter_ns()

        # =========================================================================
        # == [THE CURE]: SOVEREIGN ENGINE DISCOVERY                              ==
        # =========================================================================
        # We scry the incoming kwargs for the Engine, or fallback to the global
        # main module to ensure the StagingManager receives its required soul.
        self.engine = kwargs.get('engine')
        if not self.engine:
            import sys
            main_mod = sys.modules.get('__main__')
            self.engine = getattr(main_mod, 'engine', None)
        # =========================================================================

        self._merkle_accumulator = hashlib.sha256(self.tx_id.encode())
        self._event_stream: deque = deque()

        # --- III. GNOSTIC MEMORY LATTICE ---
        from ...runtime.vessels import GnosticSovereignDict
        self.write_dossier: Dict[Path, GnosticWriteResult] = {}
        self.edicts_executed: List[str] = []
        self.heresies_perceived: List[Heresy] = []
        self.context = GnosticSovereignDict(kwargs.get('context', {}))

        # --- IV. ORGAN MATERIALIZATION (THE TITANIUM SUTURE) ---
        # [ASCENSION 1]: Birth the StagingManager with its required dependencies.
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
            # Link the Registers to the Engine's Akashic link for HUD radiation
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

        self._finalizer = weakref.finalize(
            self, self._emergency_cleanup, self.staging_manager,
            self.volume_shifter, self.use_lock, self.lock
        )

        self.logger.debug(f"Crucible [soul]{self.tx_id[:8]}[/] manifest for [cyan]{self.rite_name}[/].")

    @property
    def chronicle_bridge(self) -> ChronicleBridge:
        if self._bridge is None:
            self._bridge = ChronicleBridge(self)
        return self._bridge

    @property
    def active(self) -> bool:
        return self._state.value >= TransactionState.INCEPTED.value and self._state.value < TransactionState.SEALED.value

    def is_file_in_staging(self, logical_path: Union[str, Path]) -> bool:
        p_obj = Path(logical_path)
        if p_obj in self.write_dossier:
            return True
        staging_path = self.get_staging_path(p_obj)
        return staging_path.exists() and staging_path.is_file()

    @staticmethod
    def _emergency_cleanup(staging: StagingManager, shifter: Any, use_lock: bool, lock: GnosticLock):
        try:
            staging.cleanup()
            if hasattr(shifter, 'cleanup'):
                shifter.cleanup()
            if use_lock and lock:
                lock.release()
        except Exception:
            pass

    def re_anchor(self, new_root: Path):
        with self._state_lock:
            if self._state.value > TransactionState.STAGING.value and self._state != TransactionState.RESONANT:
                self.logger.warn("Re-anchoring stayed: Lustration actively manifest. Spatial drift warded.")
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

            self.logger.verbose(f"Transaction re-anchored to Axis Mundi: [cyan]{self.project_root}[/cyan]")

    def __enter__(self) -> GnosticTransaction:
        _inception_start = time.perf_counter_ns()

        if self.use_lock:
            try:
                self.lock.acquire()
            except Exception as lock_paradox:
                self.logger.critical(f"Lattice Lock Fracture: {lock_paradox}")
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
                                "color": "#a855f7",
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
                    "status": "RESONANT",
                    "trace_id": self.trace_id
                })

            _duration_ms = (time.perf_counter_ns() - _inception_start) / 1_000_000
            self.logger.verbose(
                f"Transaction '{self.rite_name}' (ID: {self.tx_id[:8]}) "
                f"initialized in {_duration_ms:.2f}ms. Resonance: TITANIUM."
            )

            return self

        except Exception as catastrophic_paradox:
            self._transition_to_fractured(catastrophic_paradox)
            raise catastrophic_paradox

    # =========================================================================
    # == MOVEMENT III: THE LEDGER OF WILL (RECORDING)                        ==
    # =========================================================================

    def record(self, result: GnosticWriteResult):
        """
        =============================================================================
        == THE RITE OF INSCRIPTION (RECORD)                                        ==
        =============================================================================
        """
        with self._state_lock:
            # =========================================================================
            # == [THE CURE]: THE RE-OPENING RITE                                     ==
            # =========================================================================
            # If the Crucible is RESONANT, it means an earlier lustration pass finished.
            # But late-stage matter (like scaffold.scaffold) needs to be added.
            # We automatically unseal the Crucible and return to STAGING.
            if self._state == TransactionState.RESONANT:
                self._state = TransactionState.STAGING
                self.logger.verbose(f"Crucible unsealed. Re-entering STAGING for late inscription: {result.path.name}")

            # [ASCENSION 20]: SEALED CRUCIBLE GUARD
            if self._state.value >= TransactionState.FLIPPING.value:
                raise RuntimeError(
                    f"Heresy: Attempted to record '{result.path.name}' to a sealed Crucible (State: {self._state.name})."
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
    # == MOVEMENT IV: THE KINETIC PHASES (MATERIALIZE & FLIP)                ==
    # =========================================================================

    def materialize(self):
        """
        =============================================================================
        == THE RITE OF KINETIC LUSTRATION (V-Ω-TOTALITY-V2000-LAZY-SHADOW)         ==
        =============================================================================
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

        # --- MOVEMENT I: THE LAZY SHADOW FORGE (THE CURE) ---
        if hasattr(self, 'volume_shifter') and self.volume_shifter.state.name == "VOID":
            strategy = self.context.get("flip_strategy") or (
                "SYMLINK" if os.environ.get("SCAFFOLD_ENV") == "DOCKER" else "RENAME"
            )
            try:
                self.logger.verbose(f"Forging Shadow Volume [Green] via strategy: {strategy}")
                self.volume_shifter.prepare(strategy=strategy)

                if hasattr(self.volume_shifter, 'merkle_root'):
                    self.context["_initial_merkle_root"] = self.volume_shifter.merkle_root

            except Exception as shadow_fracture:
                self.logger.warn(f"Shadow Volume Forge fractured: {shadow_fracture}. Falling back to standard staging.")
                self.volume_shifter.state = VolumeState.FRACTURED

        # --- MOVEMENT II: THE DELTA GAZE ---
        current_shards = set(self.write_dossier.keys())
        new_shards = current_shards - self._committed_paths

        if not new_shards and self._manifest_count > 0:
            with self._state_lock:
                self._state = TransactionState.RESONANT
            return

        if self._manifest_count >= self.MAX_LUSTRATION_PASSES:
            self.logger.warn(
                f"Metabolic Limit: Lustration capped at {self.MAX_LUSTRATION_PASSES} passes. Ignoring further drift.")
            with self._state_lock:
                self._state = TransactionState.RESONANT
            return

        self.logger.info(f"Lustration Movement #{self._manifest_count + 1}: Committing structural bonds...")

        self._enrich_if_needed()

        try:
            self.committer.commit()

            self._committed_paths.update(new_shards)
            self._manifest_count += 1
            self._event_stream.append({
                "event": "MATERIALIZE_PASS",
                "count": self._manifest_count,
                "shards": len(new_shards),
                "ts": time.time_ns(),
                "trace_id": self.trace_id
            })

            self._project_hud_pulse("LUSTRATION_SUCCESS", "#64ffda")

            with self._state_lock:
                self._state = TransactionState.RESONANT

        except Exception as lustration_paradox:
            if not self._liminal_healing_rite(lustration_paradox, "materialize"):
                self.logger.error(f"Lustration fractured: {lustration_paradox}")
                raise lustration_paradox
            else:
                self.materialize()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        =============================================================================
        == THE OMEGA EXIT RITE: TOTALITY (V-Ω-TOTALITY-V2100-UNBREAKABLE-FINALIS)  ==
        =============================================================================
        """
        death_ts_ns = time.perf_counter_ns()
        self.active_death_ns = death_ts_ns

        self.logger.verbose(f"[{self.tx_id[:8]}] Concluding Rite: {self.rite_name}")

        was_healed = False
        final_exception = exc_val

        try:
            if exc_type or self._state == TransactionState.FRACTURED:
                # --- BRANCH A: THE PATH OF PARADOX (ROLLBACK) ---
                with self._state_lock:
                    self._state = TransactionState.FRACTURED

                self.logger.warn(f"Transaction '{self.rite_name}' aborted by paradox: {exc_val or 'Internal Fracture'}")
                self._project_hud_pulse("TX_FRACTURE", "#ef4444")

                if exc_type:
                    try:
                        if self._liminal_healing_rite(exc_val, "exit"):
                            was_healed = True
                            self.logger.success("Liminal Healing Resonated. Reality Stabilized.")
                    except Exception as secondary_heresy:
                        self.logger.error(f"Liminal Healing itself fractured: {secondary_heresy}")

                if not was_healed:
                    self._event_stream.append({
                        "event": "ROLLBACK_INITIATED",
                        "reason": str(exc_val),
                        "ts": time.time_ns(),
                        "trace_id": self.trace_id
                    })
                    try:
                        self.chronomancer.perform_emergency_rollback()
                    except Exception as rollback_fracture:
                        self.logger.critical(f"CHRONOMANTIC REVERSAL FAILED: {rollback_fracture}")

                    self._archive_failed_rite(exc_type, exc_val, exc_tb)

            # If no exception, or if it was healed, we proceed to commit.
            if not exc_type or was_healed:
                # --- BRANCH B: THE PATH OF APOTHEOSIS (COMMIT) ---

                # 1. FINAL LUSTRATION (Seal all secondary matter)
                self.materialize()

                # 2. THE ACHRONAL FLIP
                if not self.simulate:
                    with self._state_lock:
                        self._state = TransactionState.FLIPPING

                    try:
                        shifter_state = getattr(self.volume_shifter, 'state', None)
                        if not shifter_state or (shifter_state.name != "RESONANT" and shifter_state.name != "ACTIVE"):
                            raise ArtisanHeresy("Volumetric Schism: Shadow Volume is not resonant for Flip.")

                        # [STRIKE]: The absolute pointer swap
                        self.volume_shifter.flip(target_dir=self.project_root)
                        self._flip_conducted = True

                        self._event_stream.append(
                            {"event": "ACHRONAL_FLIP_COMPLETE", "ts": time.time_ns(), "trace_id": self.trace_id})
                        self._project_hud_pulse("ACHRONAL_FLIP_SUCCESS", "#64ffda")

                    except Exception as flip_paradox:
                        self.logger.critical(f"Achronal Flip Paradox: {flip_paradox}")
                        with self._state_lock:
                            self._state = TransactionState.FRACTURED
                        final_exception = flip_paradox
                        raise flip_paradox

                # 3. SEAL THE CHRONICLE
                if not self.simulate and self._state != TransactionState.FRACTURED:
                    if self.write_dossier or self.edicts_executed:
                        try:
                            self.logger.verbose("Sealing the Gnostic Chronicle...")
                            self.chronicle_bridge.seal_chronicle()
                            self._project_hud_pulse("TX_SEALED", "#a855f7")
                        except Exception as bridge_fracture:
                            self.logger.warn(
                                f"Chronicle Bridge fractured: {bridge_fracture}. Reality preserved, metadata delayed.")

                with self._state_lock:
                    self._state = TransactionState.SEALED
                    self._event_stream.append({"event": "SEALED", "ts": time.time_ns(), "trace_id": self.trace_id})

        except Exception as final_heresy:
            final_exception = final_heresy
            self.logger.error(f"Catastrophic paradox during Seal: {final_heresy}", exc_info=True)

        # =========================================================================
        # == MOVEMENT II: THE UNBREAKABLE PURIFICATION (CLEANUP PHALANX)        ==
        # =========================================================================

        # 1. STAGING PURIFICATION
        try:
            self.logger.verbose(f"[{self.tx_id[:8]}] Purging Ephemeral Sanctums...")
            self.staging_manager.cleanup()
        except Exception as e:
            self.logger.debug(f"Staging cleanup deferred: {e}")

        # 2. VOLUME OBLIVION
        if self._flip_conducted or final_exception or self._state == TransactionState.FRACTURED:
            try:
                self.volume_shifter.cleanup()
            except Exception as e:
                self.logger.debug(f"Volume cleanup deferred: {e}")

        # 3. ADRENALINE LUSTRATION
        if os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            try:
                os.environ.pop("SCAFFOLD_ADRENALINE", None)
                import gc
                gc.enable()
                gc.collect(1)
            except Exception:
                pass

        # 4. APEIRON LOCK RELEASE
        if self.use_lock:
            try:
                self.lock.release()
            except Exception as e:
                self.logger.error(f"Lock release fractured: {e}")

        # 5. METABOLIC FINALITY LOG
        latency_ms = (time.perf_counter_ns() - self._boot_ns) / 1_000_000
        self.logger.verbose(
            f"Transaction '{self.rite_name}' concluded in {latency_ms:.2f}ms. "
            f"Final State: [bold cyan]{self._state.name}[/bold cyan]"
        )

        # --- THE FINAL ADJUDICATION ---
        if was_healed and not final_exception:
            return True

        return False

    def _liminal_healing_rite(self, exception: Exception, phase: str) -> bool:
        with self._state_lock:
            original_state = self._state
            self._state = TransactionState.LIMINAL

        self.logger.warn(
            f"[{self.tx_id[:8]}] Entering LIMINAL STATE to attempt auto-healing of: {type(exception).__name__}")

        healed = False
        error_str = str(exception).lower()

        if isinstance(exception,
                      PermissionError) or "access is denied" in error_str or "being used by another process" in error_str:
            self.logger.verbose("Liminal Diagnosis: Transient OS File Lock suspected.")
            for attempt in range(self.LIMINAL_HEALING_RETRIES):
                time.sleep(0.5 * (attempt + 1))
                self.logger.verbose(f"Liminal Probe {attempt + 1}: Re-attempting physical access...")
                pass

        elif isinstance(exception, MemoryError):
            self.logger.verbose("Liminal Diagnosis: Heap Saturation. Invoking tiered lustration.")
            gc.collect(2)

        with self._state_lock:
            self._state = original_state if healed else TransactionState.FRACTURED
        return healed

    def _transition_to_fractured(self, reason: Exception):
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
        with self._state_lock:
            if self._state == TransactionState.VOID or self._state == TransactionState.FRACTURED:
                return
            self.logger.warn(f"Rite '{self.rite_name}' was explicitly cancelled.")
            self._transition_to_fractured(Exception("Architect Explicit Cancel"))

    def _project_hud_pulse(self, type_label: str, color: str):
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

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_TRANSACTION state={self._state.name} id={self.tx_id[:8]}>"

    def get_staging_path(self, logical_path: Union[str, Path]) -> Path:
        return self.staging_manager.get_staging_path(logical_path)
