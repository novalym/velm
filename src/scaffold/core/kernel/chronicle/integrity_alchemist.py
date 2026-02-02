# Path: scaffold/core/kernel/chronicle/integrity_alchemist.py
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Any

from ....logger import Scribe

Logger = Scribe("IntegrityAlchemist")


class IntegrityAlchemist:
    """
    =================================================================================
    == THE CRYPTOGRAPHIC SEALER (V-Ω-ETERNAL-APOTHEOSIS)                           ==
    =================================================================================
    This divine artisan is the master of cryptographic integrity. It forges the
    unbreakable seals—the Merkle Root, the Diff Hash, and the Chronicle Hash—that
    guarantee the Gnostic Chronicle's purity and guard it against profane alteration.
    =================================================================================
    """

    def hash_data(self, data: Any) -> str:
        """Ascension X: The Universal Data Hasher."""
        try:
            # We use json.dumps with sort_keys for a canonical representation.
            canonical_string = json.dumps(data, sort_keys=True)
            return hashlib.sha256(canonical_string.encode('utf-8')).hexdigest()
        except TypeError:
            # Fallback for non-serializable data
            return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

    def _forge_merkle_root(self, manifest: Dict) -> str:
        """Ascension II & VIII: The Merkle Tree Alchemist."""
        if not manifest:
            return self.hash_data({})

        sanctum_map: Dict[str, List[str]] = {}
        for path_str in manifest.keys():
            parent = str(Path(path_str).parent)
            parent = "root" if parent == '.' else parent
            if parent not in sanctum_map:
                sanctum_map[parent] = []
            sanctum_map[parent].append(path_str)

        sanctum_hashes = {
            s_name: self.hash_data([manifest[f].get("sha256", "") for f in sorted(files)])
            for s_name, files in sanctum_map.items()
        }

        return self.hash_data(dict(sorted(sanctum_hashes.items())))

    def forge_seals(self, lock_data_for_hash: Dict, new_manifest: Dict, old_manifest: Dict) -> Dict:
        """Ascension IX: The Pure Gnostic Contract."""
        Logger.verbose("The Integrity Alchemist begins the Rite of Sealing...")

        # --- The Merkle Tree Rite ---
        project_merkle_root = self._forge_merkle_root(new_manifest)
        Logger.verbose(f"   -> Merkle Root Forged: {project_merkle_root[:12]}...")

        # --- The Gnostic Differentiator Rite ---
        old_manifest_hash = self.hash_data(old_manifest)
        new_manifest_hash = self.hash_data(new_manifest)
        manifest_diff_hash = self.hash_data(old_manifest_hash + new_manifest_hash)
        Logger.verbose(f"   -> Manifest Diff Hash Forged: {manifest_diff_hash[:12]}...")

        # --- The Final Sealing Rite ---
        # We must exclude the integrity block itself from the hash to avoid paradox.
        data_to_seal = {k: v for k, v in lock_data_for_hash.items() if k != 'integrity'}
        chronicle_hash = self.hash_data(data_to_seal)
        Logger.verbose(f"   -> Final Chronicle Seal Forged: {chronicle_hash[:12]}...")

        return {
            "project_merkle_root": project_merkle_root,
            "manifest_diff_hash": manifest_diff_hash,
            "chronicle_hash": chronicle_hash,
        }