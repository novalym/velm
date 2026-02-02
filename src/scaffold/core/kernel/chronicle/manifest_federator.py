import time
from pathlib import Path
from typing import Dict, List, Any

from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....logger import Scribe

Logger = Scribe("ManifestFederator")


class ManifestFederator:
    """
    =================================================================================
    == THE KEEPER OF THE MANIFEST (V-Ω-ETERNAL-APOTHEOSIS. THE GNOSTIC UNIFIER)     ==
    =================================================================================
    LIF: 100,000,000,000,000,000,000,000,000,000

    This divine artisan is the historian of the present. It performs the sacred Rite
    of Federation, merging the history of the past (the old manifest) with the
    actions of the present (the plan and write dossier) to forge the one true,
    complete manifest of the new reality.

    [ASCENSION]: It has been bestowed with the **Gaze of Absolute Relativity**. It now
    forcefully transmutes all incoming paths into their pure, project-relative form,
    annihilating the "Dual Truths" heresy for all time.
    =================================================================================
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def _get_relative_path_str(self, path: Path) -> str:
        """
        [THE GAZE OF ABSOLUTE RELATIVITY]
        Ensures a path is always returned as a POSIX-style string relative to the project root.
        """
        try:
            # If the path is already relative, this is a no-op.
            # If it's absolute, this correctly relativizes it.
            return path.relative_to(self.project_root).as_posix()
        except ValueError:
            # Path is outside the project root (e.g. from a different drive).
            # We return its POSIX representation as a fallback.
            return path.as_posix()

    def federate(self, old_manifest: Dict, write_dossier: List[GnosticWriteResult], plan: Dict) -> Dict:
        """The Grand Rite of Federation."""
        Logger.verbose("The Manifest Federator begins the Rite of Federation...")
        start_time = time.monotonic()

        new_manifest = old_manifest.copy()

        # --- Movement I: The Rite of Annihilation ---
        deleted_count = 0
        # The `plan` now correctly contains dictionaries: {'path': PathObject}
        deleted_paths = {self._get_relative_path_str(item['path']) for item in plan.get('delete', []) if
                         item.get('path')}
        if deleted_paths:
            new_manifest = {k: v for k, v in new_manifest.items() if k not in deleted_paths}
            deleted_count = len(deleted_paths)
            Logger.verbose(f"   -> Annihilated {deleted_count} ghost(s) from the manifest.")

        # --- Movement II: The Rite of Translocation ---
        moved_count = 0
        for from_str, to_str in plan.get('move', {}).items():
            # from_str and to_str are already relative posix strings from the plan
            if from_str in new_manifest:
                gnosis = new_manifest.pop(from_str)
                gnosis['action'] = InscriptionAction.TRANSLOCATED.value
                new_manifest[to_str] = gnosis
                moved_count += 1
        if moved_count > 0:
            Logger.verbose(f"   -> Translocated {moved_count} soul(s) in the manifest.")

        # --- Movement III: The Rite of Inscription ---
        inscribed_count = 0
        transfigured_count = 0
        for res in write_dossier:
            if not res.success:
                continue
            try:
                # ★★★ THE DIVINE HEALING ★★★
                # The heresy is annihilated. We invoke the Gaze of Absolute Relativity.
                # No matter if the path is absolute or relative, it is transmuted to its one true form.
                path_str = self._get_relative_path_str(res.path)
                # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

                old_entry = old_manifest.get(path_str, {})

                entry = {
                    "action": res.action_taken.value,
                    "sha256": res.gnostic_fingerprint,
                    "bytes": res.bytes_written,
                    "timestamp": time.time(),
                    "dependencies": res.dependencies if res.dependencies is not None else old_entry.get("dependencies",
                                                                                                        []),
                    "metrics": res.metrics if res.metrics is not None else old_entry.get("metrics", {}),
                    "blueprint_origin": (
                        self._get_relative_path_str(res.blueprint_origin) if hasattr(res.blueprint_origin,
                                                                                     'relative_to') else str(
                            res.blueprint_origin)
                    )
                }

                if not entry["blueprint_origin"] or entry["blueprint_origin"] == "None":
                    entry["blueprint_origin"] = old_entry.get("blueprint_origin")

                new_manifest[path_str] = {k: v for k, v in entry.items() if v is not None}

                if res.action_taken == InscriptionAction.CREATED:
                    inscribed_count += 1
                else:
                    transfigured_count += 1

            except (ValueError, AttributeError) as e:
                Logger.warn(f"A minor paradox occurred federating '{res.path.name}': {e}")

        if inscribed_count > 0:
            Logger.verbose(f"   -> Inscribed {inscribed_count} new soul(s) into the manifest.")
        if transfigured_count > 0:
            Logger.verbose(f"   -> Transfigured {transfigured_count} existing soul(s) in the manifest.")

        duration = (time.monotonic() - start_time) * 1000
        Logger.success(f"Federation complete in {duration:.2f}ms. The new manifest is whole.")
        return new_manifest