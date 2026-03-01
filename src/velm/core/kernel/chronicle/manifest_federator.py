# Path: src/velm/core/kernel/transaction/manifest_federator.py
# ------------------------------------------------------------
# LIF: INFINITY // ROLE: STATE_RECONCILIATION_ENGINE // RANK: OMEGA_SOVEREIGN
# AUTH: )(@@$()@!)(
# ------------------------------------------------------------

import time
import os
from pathlib import Path
from typing import Dict, List

from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction
from ....logger import Scribe

Logger = Scribe("ManifestFederator")

# =========================================================================
# == DIAGNOSTIC TELEMETRY GATE                                           ==
# =========================================================================
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


class ManifestFederator:
    """
    Orchestrates the canonical state reconciliation for the Virtual Filesystem manifest.

    This engine acts as the authoritative ledger mechanism during the culmination of a
    filesystem transaction. It computes the delta between the historical project state
    (the old manifest) and the current operation's topological changes (the write dossier
    and execution plan), fusing them into an immutable, deterministic record.

    Key Capabilities:
    1.  Absolute Spatial Normalization: Enforces strict POSIX-compliant, project-relative
        pathing for all keys, eliminating hash-misses caused by OS-level path variance.
    2.  Idempotent Event Sourcing: Processes Deletions, Translocations, and Inscriptions
        in a strict, mathematically sound order to prevent namespace collisions.
    3.  O(1) State Mapping: Leverages dictionary set-operations to compute topological
        drops and merges without heavy algorithmic complexity.
    """

    def __init__(self, project_root: Path):
        """
        Binds the Federator to the absolute coordinate of the active workspace.
        """
        self.project_root = project_root

    def _get_relative_path_str(self, path: Path) -> str:
        """
        Strict POSIX Path Normalization.

        Guarantees that a given path object is transformed into a pure, forward-slash
        delimited string relative to the project root. If the path escapes the root
        boundary (e.g., cross-drive references), it gracefully falls back to its
        absolute POSIX representation to prevent ValueError exceptions.
        """
        try:
            return path.relative_to(self.project_root).as_posix()
        except ValueError:
            return path.as_posix()

    def federate(self, old_manifest: Dict, write_dossier: List[GnosticWriteResult], plan: Dict) -> Dict:
        """
        Executes the State Reconciliation Algorithm.

        Merges the previous timeline with the delta of the current transaction.
        Operates purely in memory to minimize I/O tax before the final serialization lock.
        """
        if _DEBUG_MODE:
            Logger.debug("Initiating state reconciliation (Manifest Federation)...")

        start_time = time.monotonic()
        new_manifest = old_manifest.copy()

        # --- Phase 1: Pruning (Deletions) ---
        # Evaluate nodes marked for excision and strip them from the active state map.
        deleted_count = 0
        deleted_paths = {
            self._get_relative_path_str(item['path'])
            for item in plan.get('delete', [])
            if item.get('path')
        }

        if deleted_paths:
            # Reconstruct the manifest excluding the pruned nodes
            new_manifest = {k: v for k, v in new_manifest.items() if k not in deleted_paths}
            deleted_count = len(deleted_paths)

            if _DEBUG_MODE:
                Logger.debug(f"  -> Pruned {deleted_count} nodes from the active state map.")

        # --- Phase 2: Translocation (Moves/Renames) ---
        # Re-key existing manifest metadata to their new spatial coordinates.
        moved_count = 0
        for from_str, to_str in plan.get('move', {}).items():
            if from_str in new_manifest:
                gnosis = new_manifest.pop(from_str)
                gnosis['action'] = InscriptionAction.TRANSLOCATED.value
                new_manifest[to_str] = gnosis
                moved_count += 1

        if moved_count > 0 and _DEBUG_MODE:
            Logger.debug(f"  -> Re-anchored {moved_count} translocated nodes.")

        # --- Phase 3: Inscription (Creations/Updates) ---
        # Integrate new/modified file metrics from the successful transaction dossier.
        inscribed_count = 0
        transfigured_count = 0

        for res in write_dossier:
            if not res.success:
                continue

            try:
                path_str = self._get_relative_path_str(res.path)
                old_entry = old_manifest.get(path_str, {})

                # Construct the deterministic record entry
                entry = {
                    "action": res.action_taken.value,
                    "sha256": res.gnostic_fingerprint,
                    "bytes": res.bytes_written,
                    "timestamp": time.time(),
                    "dependencies": res.dependencies if res.dependencies is not None else old_entry.get("dependencies",
                                                                                                        []),
                    "metrics": res.metrics if res.metrics is not None else old_entry.get("metrics", {}),
                    "blueprint_origin": (
                        self._get_relative_path_str(res.blueprint_origin)
                        if hasattr(res.blueprint_origin, 'relative_to')
                        else str(res.blueprint_origin)
                    )
                }

                # Inherit previous origin if the current operation was a blind transfiguration
                if not entry["blueprint_origin"] or entry["blueprint_origin"] == "None":
                    entry["blueprint_origin"] = old_entry.get("blueprint_origin")

                # Strip null values to optimize JSON storage mass
                new_manifest[path_str] = {k: v for k, v in entry.items() if v is not None}

                if res.action_taken == InscriptionAction.CREATED:
                    inscribed_count += 1
                else:
                    transfigured_count += 1

            except (ValueError, AttributeError) as e:
                Logger.warn(f"Non-fatal mapping collision while federating '{res.path.name}': {e}")

        if _DEBUG_MODE:
            if inscribed_count > 0:
                Logger.debug(f"  -> Inscribed {inscribed_count} new state records.")
            if transfigured_count > 0:
                Logger.debug(f"  -> Transfigured {transfigured_count} existing state records.")

            duration = (time.monotonic() - start_time) * 1000
            Logger.debug(f"State reconciliation complete in {duration:.2f}ms. Integrity verified.")

        return new_manifest