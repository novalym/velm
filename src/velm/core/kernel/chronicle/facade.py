# Path: src/velm/core/kernel/chronicle/facade.py
# ----------------------------------------------


import json
import time
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

from .manifest_federator import ManifestFederator
from .integrity_alchemist import IntegrityAlchemist
from .provenance_scribe import ProvenanceScribe
from .archivist import GnosticArchivist
from ....contracts.data_contracts import GnosticWriteResult
from ....contracts.heresy_contracts import Heresy
from ....logger import Scribe
from ....utils import atomic_write

# --- THE DIVINE SUMMONS OF THE CRYSTAL MIND ---
# We check for the Gnostic Database's presence.
# In WASM/Pyodide, this import may succeed but yield None if __init__.py masks it.
try:
    from ...state.gnostic_db import GnosticDatabase
except ImportError:
    GnosticDatabase = None

Logger = Scribe("ChronicleScribe")


def update_chronicle(
        project_root: Path,
        blueprint_path: Path,
        rite_dossier: Dict,
        old_lock_data: Dict,
        write_dossier: List[GnosticWriteResult],
        final_vars: Dict,
        rite_name: str = "Unknown Rite",
        edicts_executed: Optional[List[str]] = None,
        heresies_perceived: Optional[List[Heresy]] = None
) -> None:
    """
    The one true gateway. It summons the Scribe and commands it to work.
    """
    scribe = _ChronicleScribe(
        project_root=project_root,
        blueprint_path=blueprint_path,
        plan=rite_dossier,
        old_lock_data=old_lock_data,
        write_dossier=write_dossier,
        gnosis_map=final_vars,
        rite_name=rite_name,
        edicts_executed=edicts_executed or [],
        heresies_perceived=heresies_perceived or []
    )
    scribe.forge()


class _ChronicleScribe:
    """
    =================================================================================
    == THE HIGH CONDUCTOR OF HISTORY (V-Ω-HYBRID-PERSISTENCE-ULTIMA)               ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    This is the divine artisan that bridges the gap between the Ephemeral (Memory),
    the Persistent (JSON), and the Queryable (SQLite).

    [ASCENSION 13]: WASM-PROOF NULL GUARD
    It now checks if the GnosticDatabase class is actually manifest (not None)
    before attempting to summon it, preventing the 'NoneType' heresy in the browser.
    """

    def __init__(self, **kwargs: Any):
        # The Unbreakable Contract remains, accepting all Gnosis.
        self.project_root: Path = kwargs["project_root"]
        self.plan: Dict[str, List] = kwargs["plan"]
        self.old_lock_data: Dict = kwargs["old_lock_data"]
        self.write_dossier: List[GnosticWriteResult] = kwargs["write_dossier"]
        self.gnosis_map: Dict[str, Any] = kwargs["gnosis_map"]
        self.edicts_executed: List[str] = kwargs["edicts_executed"]
        self.heresies_perceived: List[Heresy] = kwargs["heresies_perceived"]

        self.lock_path = self.project_root / "scaffold.lock"

        # --- The Forging of the Pantheon ---
        self.archivist = GnosticArchivist(self.lock_path, self.project_root)
        self.provenance_scribe = ProvenanceScribe(
            rite_name=kwargs["rite_name"],
            blueprint_path=kwargs["blueprint_path"],
            project_root=self.project_root
        )
        self.manifest_federator = ManifestFederator(self.project_root)
        self.integrity_alchemist = IntegrityAlchemist()

    def forge(self) -> None:
        """The Grand Symphony of Chronicle Forging."""
        Logger.info(f"Sealing the Chronicle for '{self.provenance_scribe.rite_name}'...")
        start_time = time.monotonic()

        # --- Movement I: The Gaze of the Past ---
        # We archive the old JSON lockfile to .scaffold/chronicles/
        old_manifest = self.archivist.archive_previous_chronicle(self.old_lock_data)

        # --- Movement II: The Forging of the Present ---
        # We merge the old manifest with the new write results
        new_manifest = self.manifest_federator.federate(
            old_manifest=old_manifest,
            write_dossier=self.write_dossier,
            plan=self.plan
        )

        # --- Movement III: The Forging of Provenance ---
        # We calculate metadata (Git commit, timestamp, architect)
        provenance, gnosis_delta = self.provenance_scribe.forge_dossier(
            rite_stats={k: len(v) for k, v in self.plan.items()},
            gnosis_map=self.gnosis_map,
            old_gnosis=self.old_lock_data.get("gnosis", {})
        )

        # --- Movement IV: The Forging of the Final Scripture (JSON Model) ---
        lock_data = {
            "chronicle_version": "9.0-crystal",  # Ascended Schema
            "provenance": provenance,
            "gnosis_delta": gnosis_delta,
            "edicts": {
                "executed": self.edicts_executed,
                "fingerprint": self.integrity_alchemist.hash_data(self.edicts_executed)
            },
            "heresies": [h.model_dump() for h in self.heresies_perceived],
            "integrity": {},  # To be filled by the Alchemist
            "manifest": new_manifest
        }

        # --- Movement V: The Cryptographic Sealing ---
        integrity_seals = self.integrity_alchemist.forge_seals(
            lock_data_for_hash=lock_data,
            new_manifest=new_manifest,
            old_manifest=old_manifest
        )
        lock_data["integrity"] = integrity_seals

        # --- Movement VI: The Proclamation to the Scroll (JSON Write) ---
        # This is the primary persistence layer (Git-compatible)
        # We use verbose=False to keep the CLI clean during automated rites.
        json_start = time.monotonic()
        atomic_write(self.lock_path, json.dumps(lock_data, indent=2), Logger, self.project_root, verbose=False)
        json_duration = (time.monotonic() - json_start) * 1000

        # --- Movement VII: The Engraving of the Crystal (SQLite Write) ---
        # This is the secondary persistence layer (Query-optimized).
        # [THE CURE]: We explicitly check if GnosticDatabase is a Class, not None.
        db_duration = 0.0

        if GnosticDatabase is not None:
            db_start = time.monotonic()
            try:
                db = GnosticDatabase(self.project_root)

                # We forge the Rite Data specifically for the DB
                rite_data = {
                    **provenance,
                    "gnosis": gnosis_delta,
                    "id": provenance.get("rite_id", str(uuid.uuid4())),
                    "command": f"scaffold {provenance.get('rite_name', 'unknown')}",
                }

                db.sync_manifest(new_manifest, rite_data)
                Logger.verbose("Crystal Mind synchronized successfully.")
            except Exception as e:
                # [FACULTY 10] The Resilience Fallback
                # If the DB fails (e.g. WASM file lock issues), we do NOT crash.
                # The JSON scroll (scaffold.lock) is the ultimate source of truth.
                Logger.warn(f"Crystal Mind update faltered: {e}. The Textual Scroll remains the source of truth.")

            db_duration = (time.monotonic() - db_start) * 1000
        else:
            Logger.verbose("Crystal Mind unavailable in this substrate. Skipping SQL inscription.")

        total_duration = (time.monotonic() - start_time) * 1000

        # [FACULTY 11] Telemetric Split
        Logger.success(
            f"Transaction Sealed. JSON: {json_duration:.1f}ms | SQL: {db_duration:.1f}ms | Total: {total_duration:.1f}ms")