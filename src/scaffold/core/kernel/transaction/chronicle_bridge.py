# Path: scaffold/core/kernel/transaction/chronicle_bridge.py
# ----------------------------------------------------------
import json
import time
from pathlib import Path
from typing import TYPE_CHECKING, List, Dict, Any, Set

# --- THE DIVINE SUMMONS OF PERCEPTION ---
from ....inquisitor import get_treesitter_gnosis
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....logger import Scribe

if TYPE_CHECKING:
    from ..transaction.facade import GnosticTransaction

Logger = Scribe("ChronicleBridge")


class ChronicleBridge:
    """
    =================================================================================
    == THE SCRIBE'S EMISSARY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                     ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000 (THE KEEPER OF THE ETERNAL SCROLL)

    This divine artisan is the one true, sentient conduit between an active
    Transaction and the eternal Gnostic Chronicle (`scaffold.lock`). It is a
    Forensic Inquisitor that enriches the raw data of a rite with deep, structural
    Gnosis before commanding the High Scribe to seal it into history.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Structural Enshrinement (THE FIX):** It now surgically extracts the
        souls of Functions and Classes from the ephemeral AST dossier and embeds
        them into the persistent `metrics` vessel. This ensures the `GnosticDatabase`
        can resurrect the full symbol map even from a cold, dead lockfile.
    2.  **The Gnostic Linker:** Performs a deep, two-pass Gaze to resolve raw
        imported symbols into fully-resolved file paths, forging the unbreakable
        bonds of the dependency graph.
    3.  **The Unbreakable Ward of Gnosis:** It wraps the AST extraction in a
        shielded block, ensuring that a parsing paradox does not halt the sealing
        of the chronicle.
    4.  **The Lazy Staging Gaze:** It reads content directly from the Staging Area,
        ensuring it perceives the *intended* reality before it is even committed
        to the mortal realm.
    5.  **The Module Path Alchemist:** It correctly calculates the Pythonic dotted
        path for every file, handling `__init__.py` logic with divine precision.
    6.  **The Symbol Map Forge:** It constructs a temporary, high-speed map of
        `Symbol -> FilePath` to resolve dependencies with O(1) lookups.
    7.  **The Dependency Weaver:** It updates the `result.dependencies` list with
        the resolved paths, creating a causal link between scriptures.
    8.  **The Filter of Relevance:** It only gazes upon scriptures that were
        Created, Transfigured, or Adopted, ignoring those untouched by the rite.
    9.  **The Metadata Injector:** It enriches the `GnosticWriteResult` with
        cyclomatic complexity metrics and other deep insights.
    10. **The Encoding Healer:** It reads file content with `errors='ignore'`,
        forgiving minor encoding heresies to preserve the greater truth.
    11. **The Luminous Voice:** It proclaims its progress to the log, revealing
        the depth of its perception.
    12. **The Sovereign Bridge:** It acts as the final preparation stage before
        the `ManifestFederator` merges the new truth into the eternal timeline.
    =================================================================================
    """

    def __init__(self, transaction: "GnosticTransaction"):
        self.tx = transaction

    def seal_chronicle(self):
        """The Grand Rite of Sealing. Gathers all Gnosis and summons the High Scribe."""
        if not self.tx.write_dossier and not self.tx.edicts_executed:
            Logger.verbose("Hollow rite perceived. The Chronicle remains untouched.")
            return

        Logger.info(f"The Chronicle Bridge awakens. Sealing the history of '{self.tx.rite_name}'...")
        start_time = time.monotonic()

        old_lock_data = {}
        main_lock_path = self.tx.project_root / "scaffold.lock"
        if main_lock_path.exists():
            try:
                old_lock_data = json.loads(main_lock_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError):
                Logger.warn(
                    "Could not read previous chronicle for federation; it may be profane. Forging a new history.")

        # ★★★ THE DIVINE HEALING ★★★
        # The Rite of Gnostic Enrichment is the final word before sealing.
        # We ensure the write dossier currently held in memory is fully enriched.
        # Note: The Transaction calls _enrich_if_needed() before commit, which calls this class's _enrich_dossier().
        # However, to be absolutely safe, we reference the values which are updated in-place.
        enriched_dossier = list(self.tx.write_dossier.values())
        # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

        from ..chronicle import update_chronicle

        update_chronicle(
            project_root=self.tx.project_root,
            blueprint_path=self.tx.blueprint_path,
            rite_dossier={},
            old_lock_data=old_lock_data,
            write_dossier=enriched_dossier,
            final_vars=self.tx.context,
            rite_name=self.tx.rite_name,
            edicts_executed=self.tx.edicts_executed,
            heresies_perceived=self.tx.heresies_perceived
        )

        duration = (time.monotonic() - start_time) * 1000
        Logger.success(f"Chronicle sealed in {duration:.2f}ms.")

    def _enrich_dossier(self) -> List[GnosticWriteResult]:
        """
        [THE TRUE GNOSTIC LINKER - V-Ω-APOTHEOSIS]
        Performs a deep, two-pass Gaze to resolve symbols to file paths and
        embed structural souls into the persistent metrics.
        """
        items_to_scan = [
            res for res in self.tx.write_dossier.values()
            if res.success and res.action_taken in (InscriptionAction.CREATED, InscriptionAction.TRANSFIGURED,
                                                    InscriptionAction.SYMBIOTIC_MERGE, InscriptionAction.ADOPTED)
        ]

        if not items_to_scan:
            return list(self.tx.write_dossier.values())

        Logger.verbose(f"The Soul-Reader awakens its Two-Pass Gaze upon {len(items_to_scan)} scripture(s)...")

        raw_gnosis_map: Dict[Path, Dict] = {}
        symbol_map: Dict[str, str] = {}

        # --- PASS 1: GNOSTIC CENSUS & STRUCTURAL ENSHRINEMENT ---
        for result in items_to_scan:
            try:
                staged_path = self.tx.get_staging_path(result.path)
                if not staged_path.is_file(): continue

                content = staged_path.read_bytes().decode('utf-8', errors='ignore')

                # The Inquisitor perceives the AST
                gnosis = get_treesitter_gnosis(staged_path, content)
                raw_gnosis_map[result.path] = gnosis

                if gnosis and "error" not in gnosis:
                    # [THE FIX: STRUCTURAL EMBEDDING]
                    # We surgically extract the structural soul (functions/classes) and
                    # embed it into the 'metrics' payload. This payload is what gets
                    # written to scaffold.lock, ensuring the database can hydrate correctly.

                    metrics = gnosis.get("metrics", {})

                    # 1. Embed Functions
                    metrics["functions"] = [
                        {
                            "name": f.get("name", "unknown"),
                            "lineno": f.get("start_point", [0, 0])[0] + 1
                        }
                        for f in gnosis.get("functions", [])
                    ]

                    # 2. Embed Classes
                    metrics["classes"] = [
                        {
                            "name": c.get("name", "unknown"),
                            "lineno": c.get("start_point", [0, 0])[0] + 1
                        }
                        for c in gnosis.get("classes", [])
                    ]

                    # Persist the enriched metrics back to the result object
                    result.metrics = metrics

                    # --- Symbol Mapping for Dependency Resolution ---
                    # Use the result's logical path for the module base
                    module_base_path = result.path.with_suffix('')
                    module_base = str(module_base_path).replace('/', '.').replace('\\', '.')
                    if module_base.endswith('.__init__'):
                        module_base = module_base[:-9]

                    path_posix = result.path.as_posix()

                    # Map defined symbols to this file's path string
                    for func in gnosis.get("functions", []):
                        symbol_map[func['name']] = path_posix
                        symbol_map[f"{module_base}.{func['name']}"] = path_posix
                    for cls in gnosis.get("classes", []):
                        symbol_map[cls['name']] = path_posix
                        symbol_map[f"{module_base}.{cls['name']}"] = path_posix

            except Exception as e:
                Logger.warn(f"Soul-Reader's Gaze was clouded for '{result.path.name}' during census: {e}")

        # --- PASS 2: BOND FORGING (DEPENDENCY RESOLUTION) ---
        for result in items_to_scan:
            gnosis = raw_gnosis_map.get(result.path)
            if not gnosis or "error" in gnosis:
                continue

            # The Inquisitor gives us symbol dependencies from the `imported_symbols` key
            symbol_dependencies = gnosis.get("dependencies", {}).get("imported_symbols", [])
            resolved_deps = set()

            for dep_symbol in symbol_dependencies:
                # We strip to the leaf symbol name for matching against our flat map
                cleaned_dep = dep_symbol.split('.')[-1]

                if target_path_str := symbol_map.get(cleaned_dep):
                    # Prevent self-reference
                    if target_path_str != result.path.as_posix():
                        resolved_deps.add(target_path_str)
                else:
                    # Could be stdlib or third-party lib.
                    # Future ascension: deeper resolution for external packages.
                    pass

            result.dependencies = sorted(list(resolved_deps))

        return list(self.tx.write_dossier.values())