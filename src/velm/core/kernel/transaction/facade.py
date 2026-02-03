from __future__ import annotations
import uuid
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union

from .locking import GnosticLock
from .staging import StagingManager
from .committer import GnosticCommitter
from .rollback import RollbackChronomancer
from .chronicle_bridge import ChronicleBridge
from .contracts import TransactionalGnosis
from ....contracts.data_contracts import GnosticWriteResult
from ....contracts.heresy_contracts import Heresy, ArtisanHeresy
from ....logger import Scribe

Logger = Scribe("GnosticTransaction")


class GnosticTransaction:
    """
    =================================================================================
    == THE GOD-ENGINE OF CONSISTENCY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)             ==
    =================================================================================
    LIF: 10,000,000

    This is the High Conductor of Consistency in its final, eternal form. It has
    been ascended to become a sentient, self-aware guardian of causality, ensuring
    every rite that alters reality is atomic, reversible, and forensically chronicled.

    ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:

    1.  **The Gnostic Soul (Immutable ID):** Each transaction is born with a unique,
        immutable `tx_id`, its one true name in the cosmos, linking all its actions.
    2.  **The Chronicle Linkage:** Every file forged or transfigured under its watch
        is eternally bound to its `tx_id` in the Crystal Mind (`gnosis.db`), creating
        an unbreakable chain of provenance.
    3.  **The Gaze of Pre-Commit Gnosis (THE HEALING):** Before any reality is made
        manifest, it commands the `ChronicleBridge` to perform a deep Gnostic Gaze,
        transmuting raw imported symbols into fully resolved file paths. This
        annihilates the "Disconnected Graph" heresy.
    4.  **The Simulation Ward:** It possesses an unbreakable vow. In simulation mode
        (`simulate=True`), its `commit` and `seal_chronicle` rites are stayed,
        preventing any profane touch upon the mortal realm or its history.
    5.  **The Forensic Archivist:** If a paradox shatters the symphony, it commands the
        `RollbackChronomancer` to forge a complete forensic dossier of the failed
        rite for post-mortem inquest.
    6.  **The Architect of Reversibility:** It is the master scribe of the `Ledger`,
        meticulously chronicling the Gnostic Inverse of every action, making universal
        undo a reality.
    7.  **The Maestro's Baton (`materialize`):** It provides a sacred rite to force the
        commitment of the ephemeral reality mid-symphony, allowing the Maestro to
        conduct edicts upon a newly forged world.
    8.  **The Unbreakable Vow (Context Manager):** Its very form is a sacred vow. The
        `__enter__` and `__exit__` rites guarantee that reality is either purely
        transfigured or perfectly restored. There is no middle state.
    9.  **The Polyglot Path Normalizer (`triangulate_relative_path`):** Wields a divine
        artisan to perceive a path's true, relative soul, whether it comes from the
        Mortal Realm or the Ephemeral Staging Realm.
    10. **The Heresy Vessel:** It is the sacred chalice for all non-critical heresies
        perceived during a rite, ensuring they are chronicled without halting the
        Great Work.
    11. **The Gnostic Context Bridge:** It serves as the one true vessel for the living
        Gnosis (variables) of a rite, making them available to all subordinate artisans.
    12. **The Luminous Voice:** Its every major transition—begin, commit, rollback,
        seal—is proclaimed to the Gnostic log, providing a perfect audit trail.
    """

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
        self.logger = Logger
        self.project_root = project_root.resolve()
        self.rite_name = rite_name
        self.blueprint_path = blueprint_path or Path(f"manual/{rite_name.replace(' ', '_')}")
        self.tx_id = uuid.uuid4().hex
        self.use_lock = use_lock
        self.simulate = simulate
        self.start_time = time.monotonic()

        self.active = False
        self.materialized = False
        self._dossier_enriched = False

        # --- The Forging of the Pantheon ---
        self.staging_manager = StagingManager(self.project_root, self.tx_id)
        self.lock = GnosticLock(self.staging_manager.scaffold_dir / "transaction.lock", self.rite_name)
        self.committer = GnosticCommitter(self.project_root, self.staging_manager, self.logger)
        self.chronomancer = RollbackChronomancer(self.staging_manager, self.project_root, self.logger)
        self.chronicle_bridge = ChronicleBridge(self)

        # --- Gnostic Memory ---
        self.write_dossier: Dict[Path, GnosticWriteResult] = {}
        self.edicts_executed: List[str] = []
        self.heresies_perceived: List[Heresy] = []
        self.context: Dict[str, Any] = {}

    def __enter__(self) -> GnosticTransaction:
        if self.use_lock:
            self.lock.acquire()

        self.staging_manager.initialize_sanctums()

        self.active = True
        Logger.verbose(f"Transaction '{self.rite_name}' (ID: {self.tx_id[:8]}) has begun.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """The Grand Symphony of Finalization."""
        self.active = False
        try:
            if exc_type:
                Logger.warn(f"Transaction '{self.rite_name}' aborted by paradox: {exc_val}")
                self.chronomancer.perform_emergency_rollback()
                self._archive_failed_rite(exc_type, exc_val, exc_tb)
            else:
                # [FACULTY 3] THE GAZE OF PRE-COMMIT GNOSIS
                # The final, sacred Gaze that heals the dependency graph.
                self._enrich_if_needed()

                # [FACULTY 4] THE SIMULATION WARD
                if not self.simulate:
                    if self.write_dossier and not self.materialized:
                        self.committer.commit()
                        self.materialized = True

                    if self.write_dossier or self.edicts_executed:
                        self.chronicle_bridge.seal_chronicle()
                else:
                    Logger.verbose("Commitment and Chronicle sealing stayed (Simulation Mode).")

        except Exception as commit_heresy:
            Logger.error("A catastrophic paradox occurred during the commit phase. Initiating rollback.", exc_info=True)
            self.chronomancer.perform_emergency_rollback()
            self._archive_failed_rite(type(commit_heresy), commit_heresy, commit_heresy.__traceback__)
            raise ArtisanHeresy("COMMIT_HERESY: Final materialization failed. Reality restored.",
                                child_heresy=commit_heresy) from commit_heresy
        finally:
            self.staging_manager.cleanup()
            if self.use_lock:
                self.lock.release()
            Logger.verbose(f"Transaction '{self.rite_name}' concluded.")

    def _enrich_if_needed(self):
        """Performs dependency analysis on staged files before they are moved."""
        if self._dossier_enriched or self.simulate:
            return

        Logger.verbose("Performing pre-commit Gnostic enrichment of write dossier...")
        enriched_dossier_list = self.chronicle_bridge._enrich_dossier()
        for result in enriched_dossier_list:
            self.write_dossier[result.path] = result
        self._dossier_enriched = True
        Logger.verbose("Enrichment complete.")

    def get_staging_path(self, logical_path: Union[str, Path]) -> Path:
        """Delegates the sacred duty of path resolution to the Staging Manager."""
        return self.staging_manager.get_staging_path(logical_path)

    def record(self, result: GnosticWriteResult):
        """Records the outcome of a write operation."""
        if not self.active: raise RuntimeError("Cannot record to an inactive transaction.")
        logical_path = self.staging_manager.triangulate_relative_path(result.path)
        self.write_dossier[logical_path] = result.model_copy(update={"path": logical_path})

    def record_edict(self, command: str):
        """Records a Maestro's Edict for the chronicle."""
        if not self.active: raise RuntimeError("Cannot record to an inactive transaction.")
        self.edicts_executed.append(command)

    def record_heresy(self, heresy: Heresy):
        """[FACULTY 10] Chronicles a non-critical heresy perceived during the rite."""
        if not self.active: return
        self.heresies_perceived.append(heresy)

    def materialize(self):
        """[FACULTY 7] Forces an early commit of the staged reality for the Maestro's Gaze."""
        if self.materialized or self.simulate: return
        Logger.info("Materializing Staged Reality for Maestro's access...")
        self._enrich_if_needed()
        self.committer.commit()
        self.materialized = True

    def cancel(self):
        """A sacred rite to explicitly command a rollback from within an artisan."""
        if not self.active: return
        Logger.warn(f"Rite '{self.rite_name}' was explicitly cancelled. Reversing time...")
        self.chronomancer.perform_emergency_rollback()
        # We must prevent the __exit__ block from trying to commit
        self.write_dossier.clear()
        self.edicts_executed.clear()

    @property
    def duration(self) -> float:
        """Returns the elapsed time since the transaction began."""
        return time.monotonic() - self.start_time

    def get_gnostic_context_view(self) -> Dict[str, Any]:
        """[FACULTY 11] Returns a safe, read-only copy of the Gnostic context."""
        return self.context.copy()

    def _archive_failed_rite(self, exc_type, exc_val, exc_tb):
        """[FACULTY 5] Delegates the Rite of Forensic Archival to the Rollback Chronomancer."""
        gnosis = TransactionalGnosis(
            rite_name=self.rite_name, tx_id=self.tx_id, context=self.context,
            dossier_count=len(self.write_dossier), edict_count=len(self.edicts_executed),
            heresy_count=len(self.heresies_perceived), is_simulation=self.simulate
        )
        self.chronomancer.archive_failed_rite(gnosis, exc_type, exc_val, exc_tb)