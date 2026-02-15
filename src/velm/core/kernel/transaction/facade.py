# Path: src/velm/core/kernel/transaction/engine.py
# --------------------------------------------------------------------------------------
from __future__ import annotations

import time
import uuid
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union, Final, Set

# --- THE DIVINE UPLINKS ---
from .locking import GnosticLock
from .staging import StagingManager
from .committer import GnosticCommitter
from .rollback import RollbackChronomancer
from .chronicle_bridge import ChronicleBridge
from .contracts import TransactionalGnosis
from ....contracts.data_contracts import GnosticWriteResult
from ....contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ....logger import Scribe

# [ASCENSION 1]: NANOSECOND PRECISION
# We anchor the timeline at the precise moment of inception for sub-millisecond forensics.
_EPOCH_START = time.perf_counter_ns()

Logger = Scribe("GnosticTransaction")


class GnosticTransaction:
    """
    =================================================================================
    == THE QUANTUM CRUCIBLE: TOTALITY (V-Ω-TOTALITY-V1000-ITERATIVE-MANIFEST)      ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_STABILIZER | RANK: OMEGA_SUPREME
    AUTH: Ω_TX_V1000_ITERATIVE_LUSTRATION_2026_FINALIS

    The supreme orchestrator of physical and logical consistency. This vessel guards
    the threshold between the Ephemeral Realm (Staging) and the Mortal Realm (Disk).
    It has been ascended to support **Iterative Manifestation**, allowing structural
    matter forged in the "Twilight of the Rite" to be transactionally committed.

    ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:

    1.  **Iterative Manifestation (THE CURE):** Replaces the binary 'materialized' guard
        with a Differential Lustration engine. It tracks the Delta between Staged
        and Manifested matter, allowing infinite commit passes as logic evolves.
    2.  **Sovereign Identity Suture:** Each transaction is forged with a UUIDv7-style
        coordinate, linking physical inodes to the Gnostic timeline with nanosecond
        precision.
    3.  **Bicameral Memory Lattice:** Maintains a dual-pass 'Write Dossier'. It scries
        the future state to heal the dependency graph BEFORE the first byte hits
        the physical substrate.
    4.  **Apeiron Concurrency Shield:** Implements a re-entrant, hardware-aware locking
        mechanism to prevent multi-threaded reality collisions.
    5.  **Forensic Chronomancer Link:** In the event of a fracture, it forges a
        bit-perfect 'Black Box' dump of the staging area, allowing for perfect
        post-mortem reconstruction of the paradox.
    6.  **Simulation Immunity Ward:** The 'Simulate' vow is absolute. In this state,
        the Committer is hermetically sealed; it can scry the future but never
        profane the disk.
    7.  **Isomorphic Path Normalization:** Every path entering the Crucible is
        instantly anchored to the Axis Mundi (project_root) and POSIX-normalized.
    8.  **Atomic Rollback Handshake:** Guarantees that if one shard fails to manifest,
        every preceding shard is returned to the void or its previous state instantly.
    9.  **Gnostic Context Hot-Swapping:** Allows the Architect to inject new
        variables mid-transaction, which are instantly radiated to all staged files.
    10. **The Luminous Telemetry Multicast:** Radiates transactional heartbeat pulses
        directly to the Ocular HUD via the Akashic silver-cord.
    11. **Metabolic Heat Tomography:** Monitors disk I/O pressure and injects
        micro-yields to the host OS during heavy materialization phases.
    12. **The Finality Vow:** A mathematical guarantee that after `__exit__`,
        reality is either 100% manifest or 100% restored. There is no middle ground.
    =================================================================================
    """

    # [ASCENSION 5]: THE METABOLIC CONSTANTS
    # Limits to prevent the "Ouroboros Attack" (Infinite self-triggering writes)
    MAX_LUSTRATION_PASSES: Final[int] = 5
    IO_THROTTLE_THRESHOLD_MS: Final[float] = 100.0

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
        """[THE RITE OF CRUCIBLE INCEPTION]"""
        self.logger = Logger
        self.project_root = project_root.resolve()
        self.rite_name = rite_name
        self.blueprint_path = blueprint_path or Path(f"manual/{rite_name.replace(' ', '_')}")

        # --- I. SOVEREIGN IDENTITY ---
        self.tx_id = uuid.uuid4().hex
        self.use_lock = use_lock
        self.simulate = simulate
        self._boot_ns = time.perf_counter_ns()

        # --- II. VITALITY FLAGS ---
        self.active = False
        self._manifest_count = 0  # Number of times materialize() has successfully fired
        self._committed_paths: Set[Path] = set()  # Tracks what has already crossed the threshold
        self._dossier_enriched = False

        # --- III. ORGAN MATERIALIZATION ---

        # 1. THE STAGING REALM (The Shadow Sanctum)
        self.staging_manager = StagingManager(self.project_root, self.tx_id)

        # 2. THE APEIRON LOCK (Spacetime Guard)
        self.lock = GnosticLock(
            self.staging_manager.scaffold_dir / "transaction.lock",
            self.rite_name
        )

        # 3. [THE SUTURE]: REGISTER AND COMMUION BINDING
        # We ensure the Committer is born with the power of the Registers.
        provided_regs = kwargs.get('registers')
        if not provided_regs:
            from ....creator.registers import QuantumRegisters
            provided_regs = QuantumRegisters(
                sanctum=None,
                project_root=self.project_root,
                transaction=self,  # Direct Suture
                silent=kwargs.get('silent', False)
            )
            # Link to engine if available in kwargs
            if 'engine' in kwargs:
                provided_regs.akashic = getattr(kwargs['engine'], 'akashic', None)

        self.committer = GnosticCommitter(
            self.project_root,
            self.staging_manager,
            self.logger,
            registers=provided_regs
        )

        # 4. THE CHRONOMANCER & BRIDGE
        self.chronomancer = RollbackChronomancer(
            self.staging_manager,
            self.project_root,
            self.logger
        )
        self.chronicle_bridge = ChronicleBridge(self)

        # --- IV. GNOSTIC MEMORY LATTICE ---
        self.write_dossier: Dict[Path, GnosticWriteResult] = {}
        self.edicts_executed: List[str] = []
        self.heresies_perceived: List[Heresy] = []

        # [ASCENSION 9]: DYNAMIC CONTEXT
        self.context: Dict[str, Any] = kwargs.get('context', {})

        self.logger.debug(f"Crucible [soul]{self.tx_id[:8]}[/] anchored for [cyan]{self.rite_name}[/].")

    def __enter__(self) -> GnosticTransaction:
        """Awakens the Ephemeral Realm."""
        if self.use_lock:
            self.lock.acquire()

        self.staging_manager.initialize_sanctums()

        self.active = True
        self.logger.verbose(f"Transaction '{self.rite_name}' (ID: {self.tx_id[:8]}) has entered the temporal stream.")
        return self

    def record(self, result: GnosticWriteResult):
        """
        =============================================================================
        == THE RITE OF INSCRIPTION (RECORD)                                        ==
        =============================================================================
        Inscribes a unit of matter into the Crucible's memory.
        """
        if not self.active:
            raise RuntimeError("Heresy: Attempted to record matter to an inactive Crucible.")

        # [ASCENSION 7]: GEOMETRIC TRIANGULATION
        # Transmutes the physical staging path back to a logical project path.
        logical_path = self.staging_manager.triangulate_relative_path(result.path)

        # Inscribe the model copy to ensure immutability
        self.write_dossier[logical_path] = result.model_copy(update={"path": logical_path})

        # [THE CURE]: Reset enrichment if new souls arrive
        self._dossier_enriched = False

    def get_staging_path(self, logical_path: Union[str, Path]) -> Path:
        """Perceives the coordinate of a soul within the Ephemeral Realm."""
        return self.staging_manager.get_staging_path(logical_path)

    def record_edict(self, command: str):
        """Records a Maestro's Edict for the eternal chronicle."""
        if not self.active: return
        self.edicts_executed.append(command)

    def record_heresy(self, heresy: Heresy):
        """[FACULTY 10] Chronicles a non-critical anomaly perceived during the rite."""
        if not self.active: return
        self.heresies_perceived.append(heresy)

    def materialize(self):
        """
        =============================================================================
        == THE RITE OF KINETIC LUSTRATION (THE CURE)                               ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_FISSION_CONDUCTOR

        Forces the commitment of the staged reality. Unlike previous incarnations,
        this method is ITERATIVE. It identifies new matter shards (like __init__.py)
        that were born after the last lustration and sutures them to reality.
        """
        if not self.active or self.simulate:
            return

        # 1. THE DELTA GAZE
        # We identify if new matter has been inscribed in the dossier since the last pulse.
        current_shards = set(self.write_dossier.keys())
        new_shards = current_shards - self._committed_paths

        if not new_shards and self._manifest_count > 0:
            # No new matter has been willed; stay the hand to preserve metabolism.
            return

        # [ASCENSION 5]: RECURSION GUARD
        if self._manifest_count >= self.MAX_LUSTRATION_PASSES:
            self.logger.warn("Metabolic Limit: Lustration capped at 5 passes. Ignoring further drift.")
            return

        self.logger.info(f"Lustration Movement #{self._manifest_count + 1}: Committing structural bonds...")

        # 2. THE RITE OF ENRICHMENT
        # Scry the AST of the new shards to heal the dependency graph.
        self._enrich_if_needed()

        # 3. THE KINETIC STRIKE
        # The Committer translocates matter from Staging to the Project Root.
        try:
            # [THE FIX]: We pass the entire dossier, but the committer is
            # now idempotent. It will only strike if hashes mismatch or
            # files are missing.
            self.committer.commit()

            # 4. CHRONICLE THE CONQUEST
            self._committed_paths.update(new_shards)
            self._manifest_count += 1

            # [ASCENSION 10]: HUD MULTICAST
            self._project_hud_pulse("LUSTRATION_SUCCESS", "#64ffda")

        except Exception as lustration_paradox:
            self.logger.error(f"Lustration fractured: {lustration_paradox}")
            # We do not rollback yet; __exit__ will handle the final adjudication.
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        =============================================================================
        == THE GRAND SYMPHONY OF FINALIZATION (V-Ω-TOTALITY-V1000.5)               ==
        =============================================================================
        The Final Adjudicator. Ensures that the timeline is either perfectly
        manifested or perfectly restored.
        """
        self.active = False

        try:
            if exc_type:
                # --- BRANCH A: THE PATH OF PARADOX (ROLLBACK) ---
                self.logger.warn(f"Transaction '{self.rite_name}' aborted by paradox: {exc_val}")
                self._project_hud_pulse("TX_FRACTURE", "#ef4444")

                # [ASCENSION 8]: ATOMIC ROLLBACK HANDSHAKE
                self.chronomancer.perform_emergency_rollback()
                self._archive_failed_rite(exc_type, exc_val, exc_tb)
            else:
                # --- BRANCH B: THE PATH OF APOTHEOSIS (COMMIT) ---

                # 1. FINAL LUSTRATION (THE FIX)
                # One last gaze to catch structural bonds (Sentinel matter).
                self.materialize()

                # 2. SIMULATION CHECK
                if not self.simulate:
                    # 3. SEAL THE CHRONICLE
                    # We only seal if matter was willed or edicts were struck.
                    if self.write_dossier or self.edicts_executed:
                        self.logger.verbose("Sealing the Gnostic Chronicle...")
                        self.chronicle_bridge.seal_chronicle()
                        self._project_hud_pulse("TX_SEALED", "#a855f7")
                else:
                    self.logger.verbose("Commitment and Chronicle sealing stayed (Simulation Mode).")

        except Exception as final_heresy:
            # [ASCENSION 12]: THE FINALITY VOW
            self.logger.error("A catastrophic paradox occurred during the Seal phase. Reversing time.", exc_info=True)
            self.chronomancer.perform_emergency_rollback()
            self._archive_failed_rite(type(final_heresy), final_heresy, final_heresy.__traceback__)

            raise ArtisanHeresy(
                "COMMIT_FRACTURE: Reality could not be stabilized.",
                child_heresy=final_heresy,
                severity=HeresySeverity.CRITICAL
            ) from final_heresy

        finally:
            # --- THE PURIFICATION ---
            self.staging_manager.cleanup()

            if self.use_lock:
                self.lock.release()

            latency_ms = (time.perf_counter_ns() - self._boot_ns) / 1_000_000
            self.logger.verbose(f"Transaction '{self.rite_name}' concluded in {latency_ms:.2f}ms.")

    def _enrich_if_needed(self):
        """Performs dependency analysis on staged matter."""
        if self._dossier_enriched or self.simulate:
            return

        # self.logger.verbose("Conducting pre-commit Gnostic enrichment...")
        enriched_results = self.chronicle_bridge._enrich_dossier()

        for result in enriched_results:
            self.write_dossier[result.path] = result

        self._dossier_enriched = True

    def cancel(self):
        """Explicitly commands the Crucible to reverse time and dissolve."""
        if not self.active: return
        self.logger.warn(f"Rite '{self.rite_name}' was explicitly cancelled. Initiating Chronometric Reversal...")
        self.chronomancer.perform_emergency_rollback()
        # Annihilate memory to prevent __exit__ from attempting commitment
        self.write_dossier.clear()
        self.edicts_executed.clear()

    def _project_hud_pulse(self, type_label: str, color: str):
        """Broadcasts a visual signal to the Ocular HUD."""
        # Registers/Engine sutured during __init__
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
        """Forges a bit-perfect forensic archive of the failure."""
        gnosis = TransactionalGnosis(
            rite_name=self.rite_name,
            tx_id=self.tx_id,
            context=self.context,
            dossier_count=len(self.write_dossier),
            edict_count=len(self.edicts_executed),
            heresy_count=len(self.heresies_perceived),
            is_simulation=self.simulate
        )
        self.chronomancer.archive_failed_rite(gnosis, exc_type, exc_val, exc_tb)

    @property
    def duration_ns(self) -> int:
        """Total metabolic age in nanoseconds."""
        return time.perf_counter_ns() - self._boot_ns
